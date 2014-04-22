package PerformanceTests;

import static org.junit.Assert.*;

import java.lang.reflect.Field;
import java.lang.reflect.ParameterizedType;
import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.Date;
import java.util.Random;

import org.apache.thrift.TException;
import org.junit.BeforeClass;
import org.junit.Test;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import DataHubORM.DataHubArrayList;
import DataHubORM.DataHubConverter;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;
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
	public static HeavyTestModel generateRandomHTM(int N, int M){
		Random rand = new Random();
		HeavyTestModel htm = null;
		try{
			htm = new HeavyTestModel();
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
			int count = 0;
			for(Field f:HeavyTestModel.class.getFields()){
				if(DataHubConverter.isDataHubArrayListSubclass(f.getType())){
					DataHubArrayList d = (DataHubArrayList) f.get(htm);
					for(int i=0; i<M; i++){
						DataHubModel m = (DataHubModel) ((Class)((ParameterizedType)d.getClass().getGenericSuperclass()).getActualTypeArguments()[0]).newInstance();
						d.add(m);
					}
					if(count>=N){
						break;
					}
					count++;
				}
			}
		}catch(Exception e){
			e.printStackTrace();
		}
		return htm;	
	}
	public static HeavyTestModel[] generateManyRandomHTM(int k, int N, int M){
		HeavyTestModel[] data = new HeavyTestModel[k];
		for(int i=0; i<k; i++){
			data[i] = generateRandomHTM(N,M);
		}
		return data;
	}
	//@Test
	public void inserTestOneLTM() throws DataHubException {
		generateRandomLTM().save();
	}
	//@Test
	public void insertTestOneLTMCompare() throws DataHubException{
		for(int i=0; i<10; i++){
			generateRandomLTM().save();
		}
	}
	//@Test
	public void insertTestOneHTMCompare() throws DataHubException{
		HeavyTestModel h = generateRandomHTM(10,1);
		h.save();
	}
	//@Test
	public void inserTestManyLTM() throws DataHubException {
		for(int i=0; i<1000;i++){
			generateRandomLTM().save();
		}
		Date t = new Date();
		long now = t.getTime();
		db.LightTestModel.all();
		Date t1 = new Date();
		long now1 = t1.getTime();
		System.out.println(new Date(now1-now).getTime());
	}
	@Test
	public void insertTestManyHTM() throws DataHubException{
		HeavyTestModel[] data = generateManyRandomHTM(100,5,1);
		/*for(HeavyTestModel m: data){
			m.save();
		}*/
		DataHubModel.batchSaveOrInsert(data);
		Date t = new Date();
		long now = t.getTime();
		System.out.println(db.HeavyTestModel.all().size());
		Date t1 = new Date();
		long now1 = t1.getTime();
		System.out.println(new Date(now1-now).getTime());
	}
	
	//@Test
	public void HTMStressTest() throws DataHubException{
		int[] Ns = {1,5,10};
		int[] Ms = {1,5,10};
		for(int N:Ns){
			for(int M:Ms){
				db.clearAndReCreate();
				System.out.println("N="+N+",M="+M);
				HeavyTestModel htm = generateRandomHTM(N,M);
				Date t = new Date();
				long now = t.getTime();
				htm.save();
				Date t1 = new Date();
				long now1 = t1.getTime();
				System.out.println("Insert Time"+new Date(now1-now).getTime());
				Date t2 = new Date();
				long now2 = t2.getTime();
				htm.save();
				Date t3 = new Date();
				long now3 = t3.getTime();
				System.out.println("Query Time"+new Date(now3-now2).getTime());
			}
		}
	}
	

}
