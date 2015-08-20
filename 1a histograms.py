# Create a histogram for each subject from the data

import matplotlib.pyplot as plt
import pandas as pd

# Read in raw data
rawData = pd.read_csv('1 RawData.csv')

fig, ax = plt.subplots(ncols=(rawData.shape[1]-4), figsize=(8, 4))

for i, column in enumerate(rawData.columns[4:]):
	ax[i].hist(rawData[column], 20, normed=1, histtype='stepfilled', facecolor='g', alpha=0.75)
	ax[i].set_title(column)

plt.tight_layout()
plt.show()