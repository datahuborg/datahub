package PerformanceTests;

import static org.junit.Assert.*;

import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.Random;

import org.apache.thrift.TException;
import org.junit.BeforeClass;
import org.junit.Test;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import DataHubORM.DataHubException;
import Examples.TestDatabase;
import datahub.DHException;

public class PerformanceTests {
	public static DataHubAccount test_dha;
	public static PerformanceTestDB db;
	
	@BeforeClass
	public static void setUp() throws DHException, TException, DataHubException{
		test_dha = new DataHubAccount("dggoeh1", new DataHubUser("dggoeh1@mit.edu","dggoeh1"));
		PerformanceTestDB db1 = new PerformanceTestDB();
		db1.setDataHubAccount(test_dha);
		try{
			//System.out.println("connecting!");
			db1.clearAndReCreate();
			//System.out.println("connected!");
			db = db1;
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public static String generateRandomString(){
		SecureRandom random = new SecureRandom();
		return new BigInteger(130, random).toString(32);
	}
	public static int randInt(int min, int max) {
	    Random rand = new Random();
	    int randomNum = rand.nextInt((max - min) + 1) + min;
	    return randomNum;
	}
	public static LightTestModel generateRandomLTM() throws DataHubException{
		Random rand = new Random();
		
		LightTestModel ltm = new LightTestModel();
		ltm.ltm1 = generateRandomString();
		ltm.ltm2 = rand.nextInt();
		ltm.ltm3 = rand.nextDouble();
		ltm.ltm4 = rand.nextFloat();
		ltm.ltm5 = generateRandomString();
		ltm.ltm6 = generateRandomString();
		ltm.ltm7 = rand.nextInt();
		ltm.ltm8 = rand.nextBoolean();
		ltm.ltm9 = rand.nextDouble();
		ltm.ltm10 = rand.nextBoolean();
		ltm.ltm11 = generateRandomString();
		ltm.ltm12 = rand.nextInt();
		ltm.ltm13 = rand.nextDouble();
		ltm.ltm14 = rand.nextFloat();
		ltm.ltm15 = generateRandomString();
		ltm.ltm16 = generateRandomString();
		ltm.ltm17 = rand.nextInt();
		ltm.ltm18 = rand.nextBoolean();
		ltm.ltm19 = rand.nextDouble();
		ltm.ltm20 = rand.nextBoolean();
		return ltm;
		
	}
	public static HeavyTestModel generateRandomHTM(int M) throws DataHubException{
		Random rand = new Random();
		
		HeavyTestModel htm = new HeavyTestModel();
		htm.ltm1 = generateRandomString();
		htm.ltm2 = rand.nextInt();
		htm.ltm3 = rand.nextDouble();
		htm.ltm4 = rand.nextFloat();
		htm.ltm5 = generateRandomString();
		htm.ltm6 = generateRandomString();
		htm.ltm7 = rand.nextInt();
		htm.ltm8 = rand.nextBoolean();
		htm.ltm9 = rand.nextDouble();
		htm.ltm10 = rand.nextBoolean();
		for(int i=0; i<M; i++){
			HTM1 ht1 = new HTM1();
			htm.htm1s.add(ht1);
			HTM2 ht2 = new HTM2();
			htm.htm2s.add(ht2);
			HTM3 ht3 = new HTM3();
			htm.htm3s.add(ht3);
			HTM4 ht4 = new HTM4();
			htm.htm4s.add(ht4);
			HTM5 ht5 = new HTM5();
			htm.htm5s.add(ht5);
			HTM6 ht6 = new HTM6();
			htm.htm6s.add(ht6);
			HTM7 ht7 = new HTM7();
			htm.htm7s.add(ht7);
			HTM8 ht8 = new HTM8();
			htm.htm8s.add(ht8);
			HTM9 ht9 = new HTM9();
			htm.htm9s.add(ht9);
			HTM10 ht10 = new HTM10();
			htm.htm10s.add(ht10);
		}
		return htm;	
	}
	public static HeavyTestModel[] generateManyRandomHTM(int N, int M) throws DataHubException{
		HeavyTestModel[] data = new HeavyTestModel[N];
		for(int i=0; i<N; i++){
			data[i] = generateRandomHTM(M);
		}
		return data;
	}
	//@Test
	public void inserTestOneLTM() throws DataHubException {
		generateRandomLTM().save();
	}
	@Test
	public void insertTestOneHTM() throws DataHubException{
		HeavyTestModel h = generateRandomHTM(2);
		h.save();
	}
	//@Test
	public void inserTestManyLTM() throws DataHubException {
		for(int i=0; i<100;i++){
			generateRandomLTM().save();
		}
	}
	//@Test
	public void insertTestManyHTM() throws DataHubException{
		HeavyTestModel[] data = generateManyRandomHTM(10,10);
		for(HeavyTestModel d: data){
			d.save();
		}
	}

}
