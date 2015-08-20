import java.io.*;
import java.util.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;

public class Bootstrapping extends Configured implements Tool {

    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, DoubleWritable> {

	private Text voxelTime = new Text();
	public static final int SAMPLES = 1000;
	public static final double ALPHA = 0.05;

	public void configure(JobConf job) {
	}

	public void map(LongWritable key, Text value, OutputCollector<Text, DoubleWritable> output, Reporter reporter) throws IOException {
	    String[] tokens = value.toString().split(",");

	    // Ignore first line
	    if (!tokens[0].equals("x")) {
	    	
	    	// Set key
	    	voxelTime.set(tokens[0] + "\t" + tokens[1] + "\t" + tokens[2] + "\t" + tokens[234] + "\t" + tokens[235]);

	    	// BootStrapping

			// Create ArrayList with up to 231 positions (null values not included)
		    ArrayList<Double> correlations = new ArrayList<Double>();
		    for (int i=3; i < 234; i++) {
		    	if (!tokens[i].equals("")) {
		    		correlations.add(Double.parseDouble(tokens[i]));
		    	}
		    }

		    // If length of list = 0 (i.e. all NULL) then don't output anything
		    if (correlations.size() != 0) {

		    	// Declare variables here to improve efficiency
		    	int rand;	int j;	double sum;	// double sumSq;
		    	double[] mean = new double[SAMPLES];
		    	// double[] stdDev = new double[SAMPLES];

				// Sample "SAMPLES" times
		    	for (int sample=0; sample < SAMPLES; sample++) {
		    		sum = 0;
		    		// sumSq = 0;

		    		// Generate random numbers from 0 to length of list
		    		for (j=0; j < correlations.size(); j++) {
		    			rand = (int) (Math.random()*correlations.size());

		    			sum += correlations.get(rand); // sum (for mean)
		    			// sumSq += correlations.get(rand)*correlations.get(rand); // sum of squares (for SD)
		    		}

		    		// Mean and SD of sample
		    		mean[sample] = sum / correlations.size();
		    		// stdDev[sample] = Math.sqrt((sumSq-correlations.size()*mean[sample]*mean[sample])/(correlations.size()-1));
		    	}

			    // Calculate overall mean
			    double sumMeans = 0;
			    for (int k=0; k < SAMPLES; k++) {
			    	sumMeans += mean[k];
			    }
			    double overallMean = sumMeans / SAMPLES;

			    /*	// Check - calculate crude confidence intervals
			    double overallSSE = 0;
			    for (int k=0; k < SAMPLES; k++) {
			    	overallSSE += (mean[k]-overallMean)*(mean[k]-overallMean);
			    }
			    double overallSD = Math.sqrt(overallSSE/(SAMPLES-1));
			    double lowerCrudeCI = overallMean - 1.96 * overallSD;
			    double upperCrudeCI = overallMean + 1.96 * overallSD;
			    */

			    //  Calculate 95% reflected confidence intervals
			    Arrays.sort(mean);
			    
			    //double lowerAlpha = mean[(int) (SAMPLES*(ALPHA/2)) - 1];
			    //double upperAlpha = mean[(int) (SAMPLES*(1 - ALPHA/2)) - 1];
			    double lowerCI = 2 * overallMean - mean[(int) (SAMPLES*(1 - ALPHA/2)) - 1];
			    double upperCI = 2 * overallMean - mean[(int) (SAMPLES*(ALPHA/2)) - 1];;	// Check with Apley

			    // Only output mean if confidence interval does not include 0
			    if (lowerCI > 0 || upperCI < 0) {
					output.collect(voxelTime,new DoubleWritable(overallMean));
			    }
			}
	    }
	}
    }	// mapper output is ("x y z t1 t2",significant mean correlation)


    public int run(String[] args) throws Exception {
	JobConf conf = new JobConf(getConf(), Bootstrapping.class);
	conf.setJobName("Bootstrapping");

	conf.setOutputKeyClass(Text.class);
	conf.setOutputValueClass(DoubleWritable.class);

	conf.setMapperClass(Map.class);

	conf.setInputFormat(TextInputFormat.class);
	conf.setOutputFormat(TextOutputFormat.class);

	FileInputFormat.setInputPaths(conf, new Path(args[0]));
	FileOutputFormat.setOutputPath(conf, new Path(args[1]));

	JobClient.runJob(conf);
	return 0;
    }

    public static void main(String[] args) throws Exception {
	int res = ToolRunner.run(new Configuration(), new Bootstrapping(), args);
	System.exit(res);
    }
}