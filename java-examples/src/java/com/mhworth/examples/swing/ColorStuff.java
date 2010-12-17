package com.mhworth.examples.swing;

import java.awt.Color;

public class ColorStuff {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		System.out.println(toHexString(Color.RED));

	}
	
	private static String toHexString(Color color) {
	    return Integer.toHexString(color.getRGB()).substring(2);
	  }


}
