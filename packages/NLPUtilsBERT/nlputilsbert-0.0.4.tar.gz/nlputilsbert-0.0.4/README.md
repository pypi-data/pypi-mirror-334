# NLPUtilsBERT

Imagine you're a data scientist tasked with building a text classification model. You start by cleaning and exploring
the data, creating visualizations, training models, and evaluating performance. Each step requires writing boilerplate
code, debugging, and fine-tuning.

NLPUtilsBERT eliminates this pain by providing ready-to-use tools for:

- **Text EDA:** Quickly generate insights like word frequency plots and word clouds.
- **Text Classification:** Fine-tune pre-trained models with a few lines of code, saving hours of development.
- **Evaluation:** Automatically generate key metrics like accuracy, F1 score, and confusion matrices.

With NLPUtilsBERT, you focus on the results, not the repetitive code. Whether you're a beginner or an experienced data
scientist, this package accelerates your workflow and ensures high-quality outcomes.

---

## Package Description

**NLPUtilsBERT** is a Python package for **text analysis** and **classification**, combining:

1. **Text Exploratory Data Analysis (EDA):** Tools to explore, visualize, and understand text data, including
   tokenization, word frequency analysis, and visualizations (word clouds, bar charts).
2. **Text Classification:** Simplifies text classification using **PyTorch** and **Hugging Face Transformers**, with
   support for model training, evaluation, and predictions.

---

## Features

- **EDA:** Tokenization, word frequency analysis, word clouds, and visualizations.
- **Classification:** Fine-tune pre-trained models, early stopping, and checkpointing.
- **Evaluation Metrics:** Accuracy, F1 score, confusion matrix, and ROC curve.
- **Visualization:** Training loss, confusion matrix, and evaluation metric plots.

---

## Installation

Install the package via pip:

```bash
pip install NLPUtilsBERT
```

---

## Data Requirements

Prepare a CSV file with two columns:

- **category:** Contains class labels.
- **text:** Contains cleaned text data.

Example:  
| category | text |  
|--------------|------------------------------------|  
| sports | I love playing football. |  
| business | This is my new business venture. |  
| technology | My Chrome browser is not working. |

---

## Directory Structure

```
/EDA
    /plots              # Stores category frequency and word cloud plots
    
/MODELS
    /saved_model        # Model files
    /saved_tokenizer    # Tokenizer files
    /checkpoints        # Training checkpoints
    /plots              # Evaluation result plots
```

---

## Evaluation Metrics

- **Accuracy:** Percentage of correct predictions.
- **F1 Score:** Weighted average of precision and recall.
- **Confusion Matrix:** Prediction accuracy across classes.
- **ROC Curve:** Trade-off between true positive and false positive rates.

---

## Usage

### Text EDA

Perform Exploratory Data Analysis on text data:

```python
import pandas as pd
from NLPUtilsBERT.Utils_NLP_EDA import TextEDA

# Load dataset
dataset_path = "path/to/your/file.csv"
df = pd.read_csv(dataset_path)

# Perform EDA
eda = TextEDA(dataframe=df,
              text_column="text",
              label_column="category",
              eda_folder="EDA",
              show_plots=False)
eda.perform_eda()
```

---

### Text Classification

Train, evaluate, and predict using a text classification model:

```python
import pandas as pd
from NLPUtilsBERT.Utils_TextClassification_BERT import TextClassificationModel

# Configuration
dataset_path = "path/to/your/file.csv"
pretrained_model_name = 'bert-base-uncased'  # Options: 'bert-base-uncased', 'distilbert-base-uncased'
batch_size = 16
learning_rate = 1e-7
num_train_epochs = 50
early_stopping_patience = 5
weight_decay = 0.01
test_size = 0.2
val_size = 0.3
resume_from_checkpoints = True
random_state = 73
MODEL_FOLDER = "MODEL"

# Load dataset
df = pd.read_csv(dataset_path)

# Initialize and train the model
text_classifier = TextClassificationModel(pretrained_model_name=pretrained_model_name,
                                          batch_size=batch_size,
                                          learning_rate=learning_rate,
                                          num_train_epochs=num_train_epochs,
                                          weight_decay=weight_decay,
                                          model_folder=MODEL_FOLDER,
                                          early_stopping_patience=early_stopping_patience,
                                          test_size=test_size,
                                          val_size=val_size,
                                          random_state=random_state,
                                          resume_from_checkpoints=resume_from_checkpoints)

ds_train, ds_val, ds_test = text_classifier.create_datasets(df, target_column="category")
text_classifier.train(ds_train, ds_val)

# Evaluate the model
eval_results = text_classifier.evaluate(ds_test)
print('Evaluation results:', eval_results)

# Make predictions
classifier = TextClassificationModel(model_folder=MODEL_FOLDER)
classifier.load_model()

text = "I love playing football."               ; print(f"\n{text} : {classifier.predict(text)}")
text = "This is my business place."             ; print(f"\n{text} : {classifier.predict(text)}")
text = "My Chrome browser is giving issues."    ; print(f"\n{text} : {classifier.predict(text)}")
```

---

## System Requirements

- **Python Version:** >= 3.11.9
- **Intended Audience:** Data Scientists
- **Operating System:** OS Independent

---

## Development and Contributions

Contributions are welcome!

- **Development Status:** TO BE UPDATED
- **How to Contribute:** Fork the repository, make changes, and submit a pull request.

---

## Version History

- **0.0.2:** Initial commit
- **0.0.3:** added requests==2.27.1 so to avoid issue for downloading huggingface models
- **0.0.4:** Fixed issue of not showing class names in ROC curve

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Future Improvements

- Add support for more pre-trained models.
- Integrate additional visualization options.
- Enhance multi-label classification capabilities.
- Add class for Named Entity Recognition (NER) to extract entities like names, organizations, and locations.

---

## Acknowledgements

- Hugging Face Transformers [BERT]
- spaCy
- scikit-learn

---

## FAQ

**Coming Soon**  
