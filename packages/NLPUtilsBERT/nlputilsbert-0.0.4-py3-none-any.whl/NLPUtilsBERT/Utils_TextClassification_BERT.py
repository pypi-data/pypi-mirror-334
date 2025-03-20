import json
import logging
import os
import pathlib

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import seaborn as sns
import torch
from sklearn.metrics import (accuracy_score, roc_curve, auc, balanced_accuracy_score, f1_score, recall_score,
                             precision_score, confusion_matrix)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from torch.utils.data import Dataset as TorchDataset
from transformers import (AutoTokenizer, AutoConfig, AutoModelForSequenceClassification, TrainingArguments, Trainer,
                          DataCollatorWithPadding, EarlyStoppingCallback)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

# do not change below unless necessary
EDA_PLOT_FOLDER_NAME = "plots"
SAVED_MODEL_FOLDER_NAME = "saved_model"
MODEL_RESULTS_FOLDER_NAME = "Plots"
TOKENIZER_FOLDER_NAME = "saved_tokenizer"
CHECKPOINT_FOLDER_NAME = "checkpoints"
ID2LABEL_JSON_NAME = "id2label.json"
MODEL_CACHE_FOLDER_NAME = "model_cache"


class TextDataset(TorchDataset):
    def __init__(self, text, labels, tokenizer, configuration):
        logger.info("Initializing TextDataset...")
        self.tokenized_texts = tokenizer(text, max_length=configuration.max_length, truncation=True,
                                         padding='max_length', return_tensors='pt')
        self.labels = labels
        # logger.info(f"Tokenized texts: {self.tokenized_texts}")
        logger.info(f"Labels: {self.labels}")

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.tokenized_texts.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item


class TextClassificationModel:
    def __init__(self, pretrained_model_name=None, batch_size=None, learning_rate=None, num_train_epochs=None,
                 weight_decay=None, model_folder="MODEL", early_stopping_patience=None, test_size=0.2, val_size=0.1,
                 random_state=42, resume_from_checkpoints=True):

        logger.info("Initializing TextClassificationModel...")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Device: {self.device}")
        self.model_folder = model_folder
        self.tokenizer = None
        self.config = None
        self.pretrained_model_name = pretrained_model_name
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.num_train_epochs = num_train_epochs
        self.weight_decay = weight_decay
        self.early_stopping_patience = early_stopping_patience
        self.model = None
        self.optimizer = None
        self.scheduler = None
        self.best_val_loss = float('inf')
        self.train_loss = []
        self.eval_loss = []
        self.train_epochs = []
        self.eval_epochs = []
        self.random_state = random_state
        self.test_size = test_size
        self.val_size = val_size
        self.model_path = os.path.join(model_folder, SAVED_MODEL_FOLDER_NAME)
        self.tokenizer_path = os.path.join(model_folder, TOKENIZER_FOLDER_NAME)
        self.id2label_path = os.path.join(model_folder, ID2LABEL_JSON_NAME)
        self.checkpoint_path = os.path.join(model_folder, CHECKPOINT_FOLDER_NAME)
        self.model_results_path = os.path.join(model_folder, MODEL_RESULTS_FOLDER_NAME)
        self.resume_from_checkpoints = resume_from_checkpoints
        self.model_cache_path = os.path.join(model_folder, MODEL_CACHE_FOLDER_NAME)
        self.eval_metrics = {}
        self.create_dirs()

        if pretrained_model_name is not None:
            self.initialize()

    def create_dirs(self):
        paths = [self.model_path, self.tokenizer_path, self.checkpoint_path, self.model_results_path,
                 self.model_cache_path]
        for path in paths:
            os.makedirs(path, exist_ok=True)

    def initialize(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.pretrained_model_name, cache_dir=self.model_cache_path)
        self.config = AutoConfig.from_pretrained(self.pretrained_model_name, cache_dir=self.model_cache_path)

    def initialize_model(self, num_labels=None, id2label=None, label2id=None):
        logger.info("Initializing model...")
        self.model = AutoModelForSequenceClassification.from_pretrained(self.pretrained_model_name,
                                                                        num_labels=num_labels,
                                                                        id2label=id2label,
                                                                        label2id=label2id,
                                                                        cache_dir=self.model_cache_path).to(self.device)
        logger.info(f"Model initialized with num_labels={num_labels}, id2label={id2label}, label2id={label2id}")

    def create_datasets(self, df, target_column):
        y = self.get_y(df, target_column)
        logger.info("Creating datasets...")
        adjusted_test_size = self.test_size + self.val_size
        text_train, text_test, y_train, y_test = train_test_split(df, y, test_size=adjusted_test_size,
                                                                  stratify=y, random_state=self.random_state)
        adjusted_val_size = 1 - (self.val_size / (self.test_size + self.val_size))
        text_val, text_test, y_val, y_test = train_test_split(text_test, y_test, test_size=adjusted_val_size,
                                                              stratify=y_test, random_state=self.random_state)

        # Create TextDataset instances
        ds_train = TextDataset(text_train['text'].to_list(), y_train.to_list(), self.tokenizer, self.config)
        ds_val = TextDataset(text_val['text'].to_list(), y_val.to_list(), self.tokenizer, self.config)
        ds_test = TextDataset(text_test['text'].to_list(), y_test.to_list(), self.tokenizer, self.config)

        logger.info(f"Total dataset: {len(df)} samples")
        logger.info(f"Training dataset: {len(ds_train)} samples: {len(ds_train) / len(df):.2f}")
        logger.info(f"Validation dataset: {len(ds_val)} samples: {len(ds_val) / len(df):.2f}")
        logger.info(f"Test dataset: {len(ds_test)} samples: {len(ds_test) / len(df):.2f}")

        return ds_train, ds_val, ds_test

    @staticmethod
    def compute_metrics(pred):
        # logger.info("Computing metrics...")
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        metrics = {'accuracy': float(accuracy_score(labels, preds)),
                   'balanced_accuracy': float(balanced_accuracy_score(labels, preds)),
                   'f1_score': float(f1_score(labels, preds, average='weighted')),
                   'recall_score': float(recall_score(labels, preds, average='weighted'))}
        # logger.info(f"Computed metrics: {metrics}")
        return metrics

    def train(self, ds_train, ds_val):
        logger.info("Starting training...")
        num_labels = len(set(ds_train.labels))
        id2label = dict(enumerate(sorted(set(ds_train.labels))))
        label2id = {v: k for k, v in id2label.items()}
        logger.info(f"Number of labels: {num_labels}")
        logger.info(f"id2label mapping: {id2label}")
        logger.info(f"label2id mapping: {label2id}")

        self.initialize_model(num_labels=num_labels, id2label=id2label, label2id=label2id)

        training_args = TrainingArguments(output_dir=self.checkpoint_path,
                                          eval_strategy='epoch',
                                          learning_rate=self.learning_rate,
                                          per_device_train_batch_size=self.batch_size,
                                          per_device_eval_batch_size=self.batch_size,
                                          num_train_epochs=self.num_train_epochs,
                                          weight_decay=self.weight_decay,
                                          save_strategy='epoch',
                                          logging_strategy='epoch',  # Log training  and evaluation loss every epoch
                                          load_best_model_at_end=True,
                                          fp16=True)  # Enable mixed-precision training

        logger.info(f"Training arguments: {training_args}")

        # Add early stopping callback
        callbacks = [EarlyStoppingCallback(early_stopping_patience=self.early_stopping_patience)]
        trainer = Trainer(model=self.model,
                          args=training_args,
                          train_dataset=ds_train,
                          eval_dataset=ds_val,
                          processing_class=self.tokenizer,
                          data_collator=DataCollatorWithPadding(tokenizer=self.tokenizer),
                          compute_metrics=self.compute_metrics,
                          callbacks=callbacks)

        checkpoints = list(pathlib.Path(training_args.output_dir).glob("checkpoint-*"))
        if checkpoints and self.resume_from_checkpoints:
            logger.info(f"Resuming from checkpoint {checkpoints}")
            trainer.train(resume_from_checkpoint=True)
        else:
            trainer.train()

        logger.info("Training completed...")
        self.model.save_pretrained(self.model_path)
        torch.save(self.model.state_dict(), os.path.join(self.model_path, 'model.pth'))
        self.tokenizer.save_pretrained(self.tokenizer_path)
        logger.info(f"Model saved to {self.model_path}")
        logger.info(f"Tokenizer saved to {self.tokenizer_path}")

        # Save and plot results
        self.train_loss = [log['loss'] for log in trainer.state.log_history if 'loss' in log]
        self.eval_loss = [log['eval_loss'] for log in trainer.state.log_history if 'eval_loss' in log]
        self.train_epochs = [log['epoch'] for log in trainer.state.log_history if 'loss' in log]
        self.eval_epochs = [log['epoch'] for log in trainer.state.log_history if 'eval_loss' in log]
        self.plot_results()

    def plot_results(self):
        # Increase DPI for better quality and adjust figure size
        plt.figure(figsize=(10, 6), dpi=150)

        # Plot the training and validation loss
        if self.train_loss:
            plt.plot(self.train_epochs, self.train_loss, label='Training Loss', marker='o', color='tab:blue',
                     linewidth=2)
        if self.eval_loss:
            plt.plot(self.eval_epochs, self.eval_loss, label='Validation Loss', linestyle='--', color='tab:orange',
                     linewidth=2)

        # Improve aesthetics with grid and labels
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xlabel('Epoch', fontsize=12)
        plt.ylabel('Loss', fontsize=12)
        plt.title('Training and Validation Loss Over Time', fontsize=14)

        # Enhance legend readability
        plt.legend(fontsize=12)

        # Use tight layout to avoid clipping and save
        plt.tight_layout()
        plt.savefig(f'{self.model_results_path}/results.png', bbox_inches='tight')
        plt.show()
        plt.close()

    def plot_evaluation_metrics(self, labels, preds, fpr=None, tpr=None, roc_auc=None):
        # Confusion Matrix
        cm = confusion_matrix(labels, preds)
        label_indices = sorted(list(set(labels) | set(preds)))
        label_names = [self.id2label[str(int(idx))] for idx in label_indices]

        cm_sum = cm.sum(axis=1, keepdims=True)
        cm_normalized = np.divide(cm, cm_sum, where=cm_sum != 0)
        cm_normalized = np.nan_to_num(cm_normalized)

        plt.figure(figsize=(8, 6), dpi=150)
        sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues', xticklabels=label_names,
                    yticklabels=label_names, cbar_kws={'label': 'Proportion'}, linewidths=1.5, linecolor='black')
        plt.xlabel('Predicted Labels', fontsize=12)
        plt.ylabel('True Labels', fontsize=12)
        plt.title('Normalized Confusion Matrix', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(rotation=45, fontsize=10)
        plt.tight_layout()
        plt.savefig(f'{self.model_results_path}/confusion_matrix_normalized.png', bbox_inches='tight')
        plt.show()
        plt.close()

        # Bar plot for evaluation metrics
        metrics = {'Accuracy': self.eval_metrics['accuracy'],
                   'Precision': self.eval_metrics['precision_score'],
                   'Recall': self.eval_metrics['recall_score'],
                   'F1 Score': self.eval_metrics['f1_score']}

        plt.figure(figsize=(8, 5), dpi=150)
        bars = plt.barh(list(metrics.keys()), [round(v, 2) for v in metrics.values()],
                        color=['#4CAF50', '#FF9800', '#03A9F4', '#9C27B0'], edgecolor='black', linewidth=1.5)

        # Annotating the bar chart
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.01, bar.get_y() + bar.get_height() / 2,
                     f'{width:.2f}', ha='center', va='center', fontsize=12)

        plt.xlabel('Score', fontsize=12)
        plt.title('Evaluation Metrics', fontsize=14)
        plt.grid(True, axis='x', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(f'{self.model_results_path}/evaluation_metrics.png', bbox_inches='tight')
        plt.show()
        plt.close()

        # ROC Curve
        if fpr and tpr and roc_auc:
            plt.figure(figsize=(10, 8), dpi=150)
            for i in range(len(fpr)):
                class_name = self.id2label[str(int(i))]  # Convert class index to actual label
                plt.plot(fpr[i], tpr[i], label=f'{class_name} (AUC = {roc_auc[i]:.2f})', linewidth=2)

            plt.plot([0, 1], [0, 1], 'k--', lw=2)
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
            plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
            plt.grid(True, linestyle='--', alpha=0.6)

            plt.xlabel('False Positive Rate', fontsize=12)
            plt.ylabel('True Positive Rate', fontsize=12)
            plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=14)
            plt.legend(loc='lower right', fontsize=12)

            plt.tight_layout()
            plt.savefig(f'{self.model_results_path}/roc_curve.png', bbox_inches='tight')
            plt.show()
            plt.close()

    def evaluate(self, ds_test):
        logger.info("Evaluating model on test data...")
        self.load_model()
        trainer = Trainer(model=self.model,
                          processing_class=self.tokenizer,
                          data_collator=DataCollatorWithPadding(tokenizer=self.tokenizer))
        eval_result = trainer.evaluate(ds_test)
        logger.info(f"Evaluation result for test data: {eval_result}")

        predictions = trainer.predict(ds_test)
        preds = predictions.predictions.argmax(-1)
        labels = predictions.label_ids

        # Compute metrics
        self.eval_metrics = {'accuracy': accuracy_score(labels, preds),
                             'balanced_accuracy': balanced_accuracy_score(labels, preds),
                             'f1_score': f1_score(labels, preds, average='weighted'),
                             'recall_score': recall_score(labels, preds, average='weighted'),
                             'precision_score': precision_score(labels, preds, average='weighted'), }

        # Binarize labels for ROC curve
        binarized_labels = label_binarize(labels, classes=list(set(labels)))
        binarized_preds = label_binarize(preds, classes=list(set(labels)))

        # Compute ROC curve and AUC for each class
        fpr, tpr, roc_auc = {}, {}, {}
        for i in range(binarized_labels.shape[1]):
            fpr[i], tpr[i], _ = roc_curve(binarized_labels[:, i], binarized_preds[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        self.plot_evaluation_metrics(labels, preds, fpr, tpr, roc_auc)
        return eval_result

    def load_model(self):
        print("Loading model...")
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path).to(self.device)
        self.model.load_state_dict(torch.load(os.path.join(self.model_path, 'model.pth'), weights_only=True))
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
        with open(self.id2label_path, "r") as f:
            self.id2label = json.load(f)
        print(f"Model loaded from {self.model_path}")
        print(f"Tokenizer loaded from {self.tokenizer_path}")
        print(f"id2label loaded from {self.id2label_path}")

    def predict(self, text):
        # print("Making predictions...")
        self.model.eval()
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        inputs = {key: val.to(self.device) for key, val in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=-1).item()
        predicted_label = self.id2label[str(predicted_class)]
        # print(f"Predicted class index: {predicted_class}")
        # print(f"Predicted label: {predicted_label}")
        return predicted_label

    def get_y(self, df, target_col):
        logger.info(f"Generating labels for target column '{target_col}'...")
        os.makedirs(self.model_folder, exist_ok=True)

        y = df.pop(target_col)
        id2label = dict(enumerate(y.unique()))
        with open(self.id2label_path, "w") as f:
            json.dump(id2label, f)
        label2id = {v: k for k, v in id2label.items()}
        y = y.map(label2id)
        logger.info(f"id2label mapping: {id2label}")
        logger.info(f"Label2id mapping: {label2id}")
        return y
