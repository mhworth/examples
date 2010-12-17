package com.mhworth.examples.basic;

import java.util.Random;
import java.util.Arrays;
public class MultiDimensionalArrays {
	private static Random rnd = new Random();
	public static long[][] get2DArray(long[] arr,int M,int N) {
		long[][] ret = new long[M][N];
		int index = 0;
		for(int m = 0;m<M;m++) {
			for(int n = 0; n<N;n++) {
				
				ret[m][n] = arr[index++];
				
			}
		}
		
		return ret;
		
	}
	
	public static long[] generateArray(int length) {
		long[] ret = new long[length];
		
		for(int i = 0;i<length;i++) {
			//ret[i] = rnd.nextLong();
			ret[i] = i+1;
		}
		
		return ret;
	}
	
	public static void print2DArray(long[][] arr) {
		for(int m = 0;m<arr.length;m++) {
			System.out.println(Arrays.toString(arr[m]));
		}
	}
	
	public static void main(String[] args) {
		long[] arr = generateArray(16*16);
		
		long[][] newArr =  get2DArray(arr,16,16);
		
		print2DArray(newArr);
	}
}
