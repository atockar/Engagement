### TAKE A SUBSET OF ALL DATA FOR DEVELOPMENT

### Use library h5py to read matlab's 7.3 format
import h5py 
import numpy as np
import pandas as pd
f = h5py.File('C:/Users/Anthony/Documents/MSiA Notes/Engagement Project/HitchcockData.mat','r+')

list_of_names = []

try:
	f.visit(list_of_names.append)
except:
	pass

# Now we can get value for a subject s at time t in region (x,y,z) through something like:
# b = f.get("#refs#/b")
# Need to check with Pieman to ensure consistent format, otherwise need to specify in input

subjects = []
for name in list_of_names[2:]:
	subject = f.get(name)
	subjects.append(subject)

# Create dataset
columns = ['X','Y','Z','T']
for i in range(len(subjects)):
	columns.append('Sub'+str(i+1))
# dims = {'X': subjects[0].shape[3], 'Y': subjects[0].shape[2], 'Z': subjects[0].shape[1], 'T': subjects[0].shape[0]}
dims = {'X': 2, 'Y': 2, 'Z': 2, 'T': 50}
nrow = dims['X']*dims['Y']*dims['Z']*dims['T']

row=0
rawData = np.zeros(shape=(nrow,(4+len(subjects))))
for x in range(dims['X']):
	for y in range(dims['Y']):
		for z in range(dims['Z']):
			for t in range(dims['T']):
				rawData[row,0] = x + 1
				rawData[row,1] = y + 1
				rawData[row,2] = z + 1
				rawData[row,3] = t + 1
				for i, subject in enumerate(subjects):
					rawData[row, 4 + i] = subject[t,z,y,x]
				row += 1
rawData_df=pd.DataFrame(rawData,columns=columns)

# Output as CSV (will be an option in future)
rawData_df.to_csv('1 RawData.csv', index=False)