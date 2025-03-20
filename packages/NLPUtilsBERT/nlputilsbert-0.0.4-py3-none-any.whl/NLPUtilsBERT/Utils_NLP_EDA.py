import os

import seaborn as sns
import spacy
from matplotlib import pyplot as plt
from wordcloud import WordCloud

# Ensure you have downloaded the spacy model with: python -m spacy download en_core_web_md
try:
    nlp = spacy.load('en_core_web_md')
except OSError:
    print("Downloading language model for the spaCy POS tagger\n(don't worry, this will only happen once)")
    spacy.cli.download('en_core_web_md')
    nlp = spacy.load('en_core_web_md')

nlp.max_length = 2000000
EDA_PLOTS_FOLDER = "plots"


class TextEDA:
    DEFAULT_FIG_SIZE = (12, 8)
    DEFAULT_COLOR_PALETTE = 'viridis'
    MAX_WORDS = 200
    DPI = 300

    def __init__(self, dataframe, text_column, label_column, eda_folder="EDA", show_plots=True, output_format='png'):
        self.df = dataframe
        self.text_column = text_column
        self.label_column = label_column
        self.en_stop_words = nlp.Defaults.stop_words
        self.plots_dir = os.path.join(eda_folder, EDA_PLOTS_FOLDER)
        self.show_plots = show_plots
        self.output_format = output_format
        os.makedirs(self.plots_dir, exist_ok=True)
        print("Initiated EDA plots...")

    def perform_eda(self):
        categories_text_df = self.df.groupby(by=self.label_column).agg({self.text_column: ' '.join}).reset_index()
        self._print_each_category_word_cloud(categories_text_df)
        self._print_categories_count()
        print("Built EDA plots...")

    def _preprocess_text(self, text):
        doc = nlp(text)
        tokens = [token.lemma_.lower()
                  for token in doc
                  if (not token.is_stop and not token.is_punct and
                      not token.is_space and not token.like_url and not token.like_num)]
        return ' '.join(tokens)

    def _plot_word_cloud(self, category_name, category_text):
        processed_text = self._preprocess_text(category_text)
        wc = WordCloud(background_color="white",
                       width=1600, height=800,
                       colormap='viridis',
                       max_words=200).generate(processed_text)

        plt.figure(figsize=(12, 8))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title(f'Word Cloud for {category_name.capitalize()}', fontsize=24, color='darkblue')
        plt.tight_layout(pad=0)
        self._save_and_show_plot(plt, f'wordcloud_{category_name}')

    def _print_each_category_word_cloud(self, categories_text_df):
        for _, row in categories_text_df.iterrows():
            self._plot_word_cloud(row[self.label_column], row[self.text_column])

    def _print_categories_count(self):
        sns.set(style="whitegrid", palette="pastel", font_scale=1.2)
        plt.figure(figsize=(12, 8))
        ax = sns.countplot(y=self.label_column,
                           hue=self.label_column,
                           legend=False,
                           data=self.df,
                           order=self.df[self.label_column].value_counts().index,
                           palette='viridis')
        plt.yticks(fontsize=14, color='darkblue')
        plt.xticks(fontsize=14, color='darkblue')

        total = len(self.df)
        plt.title(f'Distribution of {self.label_column.capitalize()} (Total: {total})', fontsize=20, color='darkblue')
        plt.xlabel('Count', fontsize=16, color='darkblue')
        plt.ylabel(self.label_column.capitalize(), fontsize=16, color='darkblue')

        # Annotate each bar with count and percentage
        for p in ax.patches:
            count = p.get_width()
            percentage = f'{100 * count / total:.1f}%'
            count_percentage = f"{int(count)} ({percentage})"

            x_offset = -40 if count < 50 else p.get_width() + 5  # Adjust offset for smaller counts
            y = p.get_y() + p.get_height() / 2

            ax.annotate(count_percentage, (x_offset, y), ha='left' if count < 50 else 'center',
                        va='center', fontsize=12, color='black', weight='bold')

        self._save_and_show_plot(plt, 'categories')

    def _save_and_show_plot(self, plt, filename: str) -> None:
        """
        Save the current plot and display it if required.

        Args:
            filename (str): The name of the file to save the plot.
        """
        plt.tight_layout()
        plt.savefig(f'{self.plots_dir}/{filename}.{self.output_format}', bbox_inches='tight', dpi=self.DPI)
        if self.show_plots:
            plt.show()
        plt.close()
