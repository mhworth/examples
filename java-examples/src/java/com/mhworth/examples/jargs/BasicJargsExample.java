package com.mhworth.examples.jargs;

import jargs.gnu.CmdLineParser;
import jargs.gnu.CmdLineParser.IllegalOptionValueException;
import jargs.gnu.CmdLineParser.UnknownOptionException;

public class BasicJargsExample {
	
	public static void printHelp() {
		String msg = "";
		msg+="Usage:\n";
		msg+="-v, --verbose: Specify logging verbosity\n";
		msg+="-d, --debug: Toggle debug mode";
	}
	
	public static void main(String[] args) {
		//Instantiate the command line parser
		CmdLineParser parser = new CmdLineParser();
		
		//Create the options
		//These are the possible arguments that can be passed on the command line
		//The options are added to the parser, and a handle is returned that you can use to extract the result after parsing
		CmdLineParser.Option verbosity = parser.addIntegerOption('v', "verbose");
		CmdLineParser.Option debug = parser.addBooleanOption('d', "debug");
		
		//parse the command options
		try {
			parser.parse(args);
		} catch (IllegalOptionValueException e) {
			//do something here if the data types don't match those that were specified by addXOption
			e.printStackTrace();
		} catch (UnknownOptionException e) {
			//do something here if none of the names match
			System.err.println(e.getOptionName() + " is an unrecognized option.  Printing usage:");
			printHelp();
		}
	}

}