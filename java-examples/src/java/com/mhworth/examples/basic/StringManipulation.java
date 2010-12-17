package com.mhworth.examples.basic;

public class StringManipulation {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		//Here's how to find the location of a string in another string
		String searchString = "I: search for things! O:";
		
		//Trim the string first (not necessary, just demonstrating)
		searchString = searchString.trim();
		
		//Print the locations of "I:" and "O:"
		System.out.println("Location of 'I:' in '" + searchString + "': " +searchString.indexOf("I:"));
		System.out.println("Location of 'O:' in '" + searchString + "': " +searchString.indexOf("O:"));

		//Here's how you format strings based on patterns
		String formattedString = String.format("%1$s/%2$s/%3$s", "hi","whats","up");
		System.out.println(formattedString);
		
	}

}
