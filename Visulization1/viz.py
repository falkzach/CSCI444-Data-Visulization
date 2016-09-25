#!/usr/local/bin/python3

import csv
import ast
import collections

import prettyplotlib as ppl
import matplotlib.pyplot as plt
import numpy as np

DATA = "50_most_common_drugs_and_major_side_effects.csv"

drugs = collections.OrderedDict()
allSideEffects = {}
drugsPlotData = []

# read in file
with open(DATA) as csvfile:
    reader = csv.reader(csvfile)
    next(reader)#skip headings
    for line in reader:
        name = line[2]
        sideEffects = ast.literal_eval(line[4])
        sideEffects.sort()
        drugs[name] = sideEffects

# count how many times each side affect occurs
for drug, sideEffects in drugs.items():
    for sideAffect in sideEffects:
        if sideAffect not in allSideEffects:
            allSideEffects[sideAffect] = 1
        else:
            allSideEffects[sideAffect] += 1

lessSideEffects = {key: value for key, value in allSideEffects.items() if value >= 7} # 7 is good
effectLabels = []
drugLabels = []


# organize data for plotting
for drug, effects in drugs.items():
    row = []
    drugLabels.append(drug)
    for effect, count in sorted(lessSideEffects.items(), key=lambda x: x[1]):
        effectLabels.append(effect)
        if effect in effects:
            row.append(count)
        else:
            # row.append(0)
            row.append(-1 * count)
    drugsPlotData.append(row)

drugsPlotData.reverse()
drugLabels.reverse()
data = np.asarray(drugsPlotData)

# create the plot
fig, ax = plt.subplots(1)

# increase figure resolution
fig.set_size_inches(21, 25)

# labels
ax.set_title('Top 50 Prescribed Drugs and Their Major Side Effects', fontsize=30)

ax.tick_params(axis='both', direction='out')

ax.xaxis.set_ticks(np.arange(0.5, len(effectLabels) + 1, 1.0))
ax.set_xticklabels(effectLabels, rotation='vertical')

ax.yaxis.set_ticks(np.arange(0.5, len(drugLabels) + 1, 1.0))
ax.set_yticklabels(drugLabels)

# generate and save
ppl.pcolormesh(fig, ax, data)
fig.savefig('drugEffects.png')
