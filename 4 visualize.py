## Outputs graphs of the correlations over time in various sections of the brain

import numpy as np
import matplotlib.pyplot as plt

#// Read in (will change later)
corrs = []
output = "C:\\Users\\Anthony\\Documents\\MSiA Notes\\Engagement Project\\Bootstrapping\\Bootcorr.txt"
with open(output, "r") as f:
	for line in f:
		corrs.append(line.split("\t"))

# Do some filtering
# For now, replicate this: SELECT t1, AVG(corr) FROM boot GROUP BY t1
# This would be a lot easier with pandas
sumCorr, numCorr = {},{}
for row in corrs:
	t1 = row[3]
	if t1 in sumCorr:
		sumCorr[t1] += float(row[5])
		numCorr[t1] += 1
	else:
		sumCorr[t1] = 0
		numCorr[t1] = 0

avgCorr = []
for t1 in numCorr:
	avgCorr.append(sumCorr[t1]/numCorr[t1])

#### Need to import brain regions
#### Need to import events

# Plot this rhino

#Smoothing
def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

# include, colours, axes, legends, regions and events

avgCorrMA = movingaverage(avgCorr, 20)

plt.plot(avgCorrMA)
plt.show()

# Save plots to pdf
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('multipage.pdf')
pp.savefig()
pp.close()