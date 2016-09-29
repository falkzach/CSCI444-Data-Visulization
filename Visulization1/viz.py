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
    # for effect, count in lessSideEffects.items(): # don't sort
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
fig.set_size_inches(20, 32)


# labels
ax.set_title('Top 50 Perscribed Drugs by Net Sales and Their Common Side Effects', fontsize=30, y=1.08)
ax.set_ylabel('Perscribed drugs by net sales (highest netting at top)')
ax.set_xlabel('Common, serious side effects (only side effects shared between 7 or more drugs shown)')


ax.xaxis.set_ticks(np.arange(0.5, len(effectLabels) + 1, 1.0))
ax.set_xticklabels(effectLabels, rotation='45', ha='right')

ax.yaxis.set_ticks(np.arange(0.5, len(drugLabels) + 1, 1.0))
ax.set_yticklabels(drugLabels)

# colorscale
red_blue = plt.get_cmap('RdBu_r')

# generate and save
p = ax.pcolormesh(data, cmap=red_blue)
cb = fig.colorbar(p, label='Prevelance of side affect amongst listed drugs (red present in drug, blue not present in drug)')

fig.savefig('drugEffects.png')
