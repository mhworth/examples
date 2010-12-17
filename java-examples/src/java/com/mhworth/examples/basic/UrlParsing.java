package com.mhworth.examples.basic;

import java.net.MalformedURLException;
import java.net.URL;
import java.net.Socket;
import java.io.File;

public class UrlParsing {

	public static void main(String[] args) throws MalformedURLException{
		URL url = null;
		
		String path = "/home/matt";
		
		try {
			url = new URL(path);
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			url = new URL("file://" + path);

		}
		
		System.out.println(url.getPath());
		
	}
}
