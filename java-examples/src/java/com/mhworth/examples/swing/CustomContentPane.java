package com.mhworth.examples.swing;

import javax.swing.*;
import java.awt.*;

public class CustomContentPane {
	public static class MyContentPane extends JPanel {
		public MyContentPane() {
			this.setBackground(Color.BLUE);
			this.setLayout(new GridLayout(8,2));
		}
	}
	public static class MyThingy extends JPanel {
		private JButton indicator;
		private JLabel text;
		
		public MyThingy() {
			indicator = new JButton("Indicator");
			text = new JLabel("Hello");
			this.setLayout(new GridLayout(0,2));
			
			this.add(indicator);
			this.add(text);
		}
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		//Setup the frame
		JFrame frame = new JFrame("Custom content pane");
		frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
		frame.setSize(500,500);
		
		MyContentPane contentPane = new MyContentPane();
		MyThingy[] thingys = new MyThingy[16];
		for(int i = 0; i<thingys.length;i++) {
			thingys[i] = new MyThingy();
			contentPane.add(thingys[i]);
		}
		
		frame.setContentPane(contentPane);
		frame.setVisible(true);

	}
	
	

}
