package com.mhworth.examples.io;

import java.io.*;
import java.util.Arrays;
public class CountLetter {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		File f = new File("sample-text.txt");
		
		
		//First, read from input stram
		FileInputStream fis = null;
		
		try {
			fis = new FileInputStream(f);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		try {
			int count = 0;
			while (fis.available() > 0) {
				
				char currentChar = Character.toChars(fis.read())[0];
				if(currentChar == 'e') {
					count++;
					System.out.println("Count is " + count);
				}
				
				System.out.format("Count=%1$s, Letter=%2$c%n",count,currentChar);
			}
			
			fis.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//Now read from reader:
		FileReader frdr = null;
		try {
			frdr = new FileReader(f);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		try {
			int count = 0;
			int currentChar = 0;
			currentChar = frdr.read();
			while (currentChar > 0) {
				
				if(currentChar == 'e') {
					count++;
					System.out.println("Count is " + count);
				}
				
				System.out.format("Count=%1$s, Letter=%2$c %n",count,currentChar);
				currentChar = frdr.read();
			}
			
			fis.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		

	}

}
