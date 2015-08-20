import java.io.*;
import java.util.*;
import java.lang.*;

public class Test_BS {

	public static final int SAMPLES = 1000;
	public static final double ALPHA = 0.05;

	public static void Boot(String value) {
	    String[] tokens = value.split("\t");

	    String voxelTime;

	    voxelTime = tokens[0] + "," + tokens[1] + "," + tokens[2] + "," + tokens[234] + "," + tokens[235];

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
	    	int rand;	int j;	double sum;	double sumSq;
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

	    /*	// Check - calculate cruide confidence intervals
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
	    	System.out.println("voxelTime = " + voxelTime);
			System.out.println("overallMean = " + overallMean);
	    }

		// System.out.println("lowerCI = " + lowerCI);
		// System.out.println("UpperCI = " + upperCI);
		
		/*
		System.out.println("overallSD = " + overallSD);
		System.out.println("lowerCrudeCI = " + lowerCrudeCI);
		System.out.println("upperCrudeCI = " + upperCrudeCI);
		*/
	    }	   
	}

    public static void main(String[] args) {
		String value = "1	1	1					0.39914462			0.12869789				0.474341649	0.375		0.296278414		0.535499138			0.612372436																																																																														0.270443048				0.007424742	-0.187832762		-0.40068571		0.211496415			0.316314917																																		-0.651165542	0.731969252		0.583395226		0.681176729			-0.446595897																																			-0.158113883		-0.389756478		0.096765541			0.387298335			0.799951719		0.8701861			-0.40824829										0.441972613			-0.096764125									-0.335732648								1	5";
		Boot(value);
    }
}