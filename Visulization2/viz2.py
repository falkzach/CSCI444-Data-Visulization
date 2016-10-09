#!/usr/local/bin/python3

import csv

import prettyplotlib as ppl
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1)

DATA="requests.csv"
# DATA="small.csv"

reportingOrgs = {}
reportCounts = {}
abusers = {}
xlabels = []
X = []
Y = []
Z = []

split_at = 100
totals = [0,0,0,0]
otherCount = [0,0,0,0]




# read data

# 0 Request ID,
# 1 Date,
# 2 Lumen URL,
# 3 Copyright owner ID,
# 4 Copyright owner name,
# 5 Reporting organization ID,
# 6 Reporting organization name,
# 7 URLs removed,
# 8 URLs for which we took no action,
# 9 URLs pending review,
# 10 From Abuser

# read in file
with open(DATA, encoding='utf8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)#skip headings
    for line in reader:
        reportingOrg = line[5]
        reportingOrgName = line[6]
        URLsRemoved = int(line[7])
        URLsNoAction = int(line[8])
        URLsPendingReview = int(line[9])
        abuser = line[10]
        URLsTotal = URLsRemoved + URLsNoAction + URLsPendingReview
        counts = [URLsTotal, URLsRemoved, URLsNoAction, URLsPendingReview]

        # build list of org names
        if reportingOrg not in reportingOrgs:
            reportingOrgs[reportingOrg] = reportingOrgName

        if reportingOrg not in abusers and abuser == 'true':
            abusers[reportingOrg] = 1
        elif abuser == 'true':
            abusers[reportingOrg] += 1

        if reportingOrg not in reportCounts:
            reportCounts[reportingOrg] = counts
        else:
            reportCounts[reportingOrg] = list(map(sum, zip(reportCounts[reportingOrg], counts)))

top = sorted(reportCounts.items(), key=lambda scores: scores[1][0], reverse=True)


for i in range(0,split_at):
    reportingOrg = top[i][0]
    counts = top[i][1]
    totals = list(map(sum, zip(totals, counts)))

    xlabels.append(reportingOrgs[reportingOrg])
    X.append(counts[1])
    Y.append(counts[2])
    Z.append(counts[3])

    if reportingOrg in abusers:
        print("Abuser: " + reportingOrgs[reportingOrg])



for i in range(split_at,len(top) - 1):
    counts = top[i][1]
    totals = list(map(sum, zip(totals, counts)))
    otherCount = list(map(sum, zip(otherCount, counts)))

xlabels.append('Everyone Else Combined')
X.append(otherCount[1])
Y.append(otherCount[2])
Z.append(otherCount[3])



print('Unique Reporters: ' + str(len(reportingOrgs)))
print('Unique Abusers: ' + str(len(abusers)))
print('Totals: ')
print(totals)
print('Others: ')
print(otherCount)



# for plots
fig.set_size_inches(16, 12)

index = np.arange(len(xlabels))
bar_width = 0.35
opacity = 0.75

rects1 = ppl.bar(index, X, bar_width,
                 alpha=opacity,
                 color='r',
                 label='URLs Removed')

rects2 = ppl.bar(index + bar_width, Y, bar_width,
                 alpha=opacity,
                 color='b',
                 label='URLs No Action')

# hidden since so few
# rects3 = ppl.bar(index + (2 * bar_width), Z, bar_width,
#                  alpha=opacity,
#                  color='g',
#                  label='URLs Pending Review')

legend = ppl.legend(ax, loc='upper right')
# ppl.bar(ax, index, d1)




ax.xaxis.set_ticks(np.arange(0.5, len(xlabels) + 1, 1.0))
ax.set_xticklabels(xlabels, rotation='45', ha='right')

fig.text(.01,.01,"Data Source:\nhttps://www.google.com/transparencyreport/removals/copyright/data/")

ax.set_xlabel('Reporting Organization')
ax.set_ylabel('Number of Takedown Requests')
ax.set_title('Google Search Copy Right Removal Requests')

fig.tight_layout()
fig.savefig('takedown_requests_'+ str(split_at) + '.png')
