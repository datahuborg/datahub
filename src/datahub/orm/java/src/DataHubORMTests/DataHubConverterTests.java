package DataHubORMTests;

import static org.junit.Assert.*;

import java.lang.reflect.Field;
import java.util.ArrayList;

import org.junit.Test;

import DataHubORM.DataHubConverter;
import DataHubORM.Database;
import DataHubORM.Model;

public class DataHubConverterTests {

	@Test
	public void testFindModelFields() {
		TestDatabase db = new TestDatabase();
		ArrayList<Field> fields = DataHubConverter.findModels(db);
		System.out.println(fields);
	}
	
	@Test
	public void testextractDataFromClass(){
		TestDatabase db = new TestDatabase();
		System.out.println(DataHubConverter.convertDBToSchema(db));
	}
}
