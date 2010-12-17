package com.mhworth.examples.image;


import javax.swing.JFrame;
import javax.swing.WindowConstants;
import java.awt.Toolkit;
import javax.swing.JLabel;
import java.awt.Image;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;

import javax.swing.SwingUtilities;
public class Screenshot {
	
	public static void main(String[] args) {
		final JFrame frame = new JFrame();
		frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
		
		Toolkit toolkit = Toolkit.getDefaultToolkit();
		frame.setExtendedState(JFrame.MAXIMIZED_BOTH);
		
		try {
			SwingUtilities.invokeAndWait(new Runnable() {
				
				public void run() {
					frame.add(new JLabel("Hi"));
					frame.setVisible(true);
					frame.pack();
					frame.setSize(500,500);
				}
			});
		} catch (InterruptedException e1) {
			e1.printStackTrace();
		} catch (InvocationTargetException e1) {
			e1.printStackTrace();
		}
		
		try {
			SwingUtilities.invokeAndWait(new Runnable() {
				
				public void run() {
					File f = new File("out.png");
					BufferedImage img = frame.getGraphicsConfiguration().createCompatibleImage(frame.getWidth(), frame.getHeight());
					frame.paintComponents(img.getGraphics());
					
					try {
						ImageIO.write(img, "png",f);
					} catch (IOException e) {
						e.printStackTrace();
					}
					
					System.exit(0);
				}
			});
		} catch (InterruptedException e1) {
			e1.printStackTrace();
		} catch (InvocationTargetException e1) {
			e1.printStackTrace();
		}
		
		
		
		
	}

}
