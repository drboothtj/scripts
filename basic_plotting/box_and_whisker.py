'''
generate a box and whisker plot from a 2 column .csv
    argv[1]: path to .csv
    argv[2]: 'names' column
    argv[3]: 'scores' column
'''
import pandas as pd
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
from sys import argv

def get_columns_from_csv(filename: str, names: str, scores: str):
    '''
    gets the required columns from the .csv and returns a dataframe
        arguments:
            filename: path to .csv
            names: the column in the csv with the group information
            score: the column in the csv with the score information
        returns:
            df: the dataframe to plot
    '''
    df = pd.read_csv(filename, usecols=[names, scores])
    return df

def plot_df_box_and_whisker(df: DataFrame, name_col: str, score_col:str):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=name_col, y=score_col, data=df)
    plt.title('Box and Whisker Plot of Scores by Names')
    plt.xlabel('Name')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Score')
    plt.tight_layout()
    plt.savefig('boxplot.png')

def main(in_file: str, name_col: str, score_col: str):
    '''
    main routine
        arguments:
            in_file: path to a two column .csv file
            out_file: path to draw the plot
            name_col: names column to extract from .csv
            score_col: scores column to extract from .csv
        returns:
            None
    ''' 
    df = get_columns_from_csv(in_file, name_col, score_col)
    plot_df_box_and_whisker(df, name_col, score_col)

in_file =argv[1]
names_col = argv[2]
score_col = argv[3]
main(in_file, names_col, score_col)
