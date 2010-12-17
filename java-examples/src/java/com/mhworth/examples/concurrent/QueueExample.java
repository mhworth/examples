package com.mhworth.examples.concurrent;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.Queue;
import java.util.Date;

public class QueueExample {
	
	public static ArrayBlockingQueue q = new ArrayBlockingQueue(10);
	
	public static void main(String[] args) {
		
		
		
		Thread t = new Thread(new Runnable() {
			
			public void run() {
				
				while(true) {
					try {
						System.out.println(q.take());
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
			}
			
		});
		
		
		t.start();
		
		while(true) {
			q.offer(new Date());
			pause(1000);
		}
		
	}
	
	public static void pause(int millis) {
		try {
			Thread.sleep(millis);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
