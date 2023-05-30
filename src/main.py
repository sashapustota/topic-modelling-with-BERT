import pandas as pd
from bertopic import BERTopic
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

import warnings
warnings.filterwarnings("ignore")

import os
import argparse

def input_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, help='Name of the data file, should be a csv file.', default="abcnews-date-text.csv")
    parser.add_argument('--column', type=str, help='Name of the column in the data file that contains the text entries.', default = "headline_text")
    parser.add_argument('--n_topics', type=int, help='Number of topics to be generated.', default = 10)
    args = parser.parse_args()
    return args

def load_data(data, column_name):
    print("Loading data...")
    # Load data into a dataframe
    df = pd.read_csv(os.path.join(os.getcwd(), "data", data))
    # Making a new column titled "text_clean" which is a copy of the column for processing and making it lowercase. This column will host our cleaned text.
    df['text_clean'] = df[column_name].str.lower()
    # Removing punctuation
    df['text_clean'] = df['text_clean'].str.replace('[^\w\s]','')
    # Removing special characters
    df['text_clean'] = df['text_clean'].str.replace('[^A-Za-z0-9]+', ' ')
    # Remove stopwords
    stop_words = stopwords.words('english')
    df['text_clean'] = df['text_clean'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
    df = df[0:10000] # For testing purposes
    # Return the dataframe
    return df

def topic_modeller(df, nr_topics):
    print("Generating topics...")
    topic_model = BERTopic(embedding_model="all-MiniLM-L6-v2", nr_topics = nr_topics)
    topics, probs = topic_model.fit_transform(df['text_clean'])
    topic_labels = topic_model.generate_topic_labels(nr_words = 3, topic_prefix = False, word_length = 15, separator = " - ")
    topic_model.set_topic_labels(topic_labels)
    print("Here are the topics for your data:")
    print(topic_model.get_topic_info())
    # Save the the print output to a text file
    with open(os.path.join(os.getcwd(), "out", 'topics.txt'), 'w') as f:
        print(topic_model.get_topic_info(), file=f)
    # Add a topic label for the "not assigned" topic
    topic_labels[0] = "not assigned"
    # Create the dataframe first
    df_new = pd.DataFrame({'topic': topics, "text" : df['text_clean']})
    df_new['topic'] = df_new['topic'] + 1
    df_new['topic_label'] = df_new['topic'].apply(lambda x: topic_labels[x])
    df_new.to_csv(os.path.join(os.getcwd(), "out", 'data_with_topics.csv'))

def plot_topics():
    print("Plotting the topic distribution...")
    df = pd.read_csv(os.path.join(os.getcwd(), "out", 'data_with_topics.csv'))
    # Remove the "not assigned" topic
    df = df[df['topic'] != 0]
    # Make a barplot of the topic distribution, colored by topic label
    sns.set_theme(style="darkgrid")
    ax = sns.countplot(x="topic_label", data=df, palette="Set2")
    # Remove x axis labels
    ax.set_xticklabels([])
    plt.title("Topic Distribution")
    plt.xlabel("Topic")
    plt.ylabel("Count")
    # Get unique topic labels and their corresponding colors
    unique_labels = df['topic_label'].unique()
    colors = sns.color_palette("Set2", len(unique_labels))
    # Create a legend with topic labels and colors outside the plot
    patches = [mpatches.Patch(color=colors[i], label=label) for i, label in enumerate(unique_labels)]
    plt.legend(handles=patches, title="Topic Labels", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(os.getcwd(), "out", 'topic_distribution.png'))
    print("Done! Check the 'out' folder for the results.")

def main():
    args = input_parse()
    df = load_data(args.data, args.column)
    topic_modeller(df, args.n_topics)
    plot_topics()

if __name__ == "__main__":
    main()





