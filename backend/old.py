import numpy as np
import matplotlib.pyplot as pl
import pandas as pd

sheets = pd.read_excel('Family Predictions 2022.xlsx', sheet_name=None)
questions = sheets.pop('Main')
player_sheets = sheets
player_sheets.keys()
questions['ID'] = questions['ID'].astype(int)
questions.set_index('ID')
questions = questions.drop(['Clarifications', 'Outcome', 'Outcome comments', 'Outcome supporting link', 'ID'], axis=1)
guesses = {k: player_sheets[k]['Probability (0.0 to 1.0)'] for k in player_sheets}
guesses = pd.DataFrame(data=guesses)
people = list(guesses.columns)
X = guesses.values.T
X.shape

# extrema
idx_min = np.argmin(X, axis=0)
idx_max = np.argmax(X, axis=0)
idx_min_lbl = [people[i] for i in idx_min]
idx_max_lbl = [people[i] for i in idx_max]
idx_min_vals = np.amin(X, axis=0)
idx_max_vals = np.amax(X, axis=0)

d = {'min': idx_min_vals, 'min_person': idx_min_lbl, 'prediction': questions['Prediction'], 'max': idx_max_vals, 'max_person': idx_max_lbl}
df = pd.DataFrame(data=d)
df


# confidence
def entropy(x):
    return np.sum(x * np.log2(x), axis=-1)

X_soft = np.copy(X)
X_soft[X==0.0] += 1e-20
X_soft[X==1.0] -= 1e-20
e = entropy(X_soft)

idx = np.argsort(e)
res = list(zip(e[idx], np.array(people)[idx]))
res

# some heuristics for cinfidenc
# average distance from 0.5
d = np.mean(np.abs(0.5 - X), axis=-1)
idx = np.argsort(d)
res = list(zip(d[idx], np.array(people)[idx]))




