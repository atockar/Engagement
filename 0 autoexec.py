## 0 autoexec.py - central file that runs each module of fMRI correlation analysis

import sys, getopt, os

def usage():
	print('"0 autoexec.py" -m <matlabfile> -o <outputfile> (-r <files to run>) (-v <old/new>) (--raw) (--hist)')

def main(argv):
	inputfile = ''
	runFiles = 'all'
	version = 'new'
	printRaw = False
	printHist = False
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hm:o:r:v:",["input=","output=","run=","version=","raw","hist"])
		print(opts)
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit(0)
		elif opt in ('-v','--version'):
			version = arg
		elif opt in ("-i", "--input"):
			inputfile = arg
		elif opt == '-r':
			runFiles = arg
		elif opt == '--raw':	# Export raw data to CSV
			printRaw = True
		elif opt == '--hist':	# Output histograms
			printHist = True
		elif opt in ("-o", "--output"):
			outputfile = arg

	if inputFile == '' or outputFile == '':
		usage()
		sys.exit(2)

	if runFiles == 'all':
		os.system('python "1 read_mat_file_py3_draft_subset.py"')
		if printHist:
			os.system('python "1a histograms.py"')
		os.system('python "2 pairwise_correlations.py"')
	else:
		for script in runFiles:
			os.system('python ' + script)


if __name__ == "__main__":
	main(sys.argv[1:])