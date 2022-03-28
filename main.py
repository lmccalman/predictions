import os.path
import numpy as np
import pandas as pd
import streamlit as st

FNAME= 'Family Predictions 2022.xlsx'

def load_data():

    sheets = pd.read_excel(os.path.join('data/', FNAME), sheet_name=None)
    questions = sheets.pop('Main')
    player_sheets = sheets
    player_sheets.keys()
    questions['ID'] = questions['ID'].astype(int)
    questions.set_index('ID')
    questions = questions.drop(
            ['Clarifications',
             'Outcome',
             'Outcome comments',
             'Outcome supporting link',
             'ID'], axis=1)
    guesses = {k: player_sheets[k]['Probability (0.0 to 1.0)']
               for k in player_sheets}
    guesses = pd.DataFrame(data=guesses)
    people = list(guesses.columns)
    X = guesses.values.T
    return people, questions, X


def main():
    st.title("Family Predictions 2022")
    people, questions, X = load_data()
    st.dataframe(questions)


if __name__ == "__main__":
    main()
