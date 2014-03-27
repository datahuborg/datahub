package DataHubResources;

import java.util.ArrayList;
import java.util.Arrays;

public class Constants {
	public static final String SERVER_ADDR_ROOT = "datahub-experimental.csail.mit.edu";
	public static final int SERVER_ADDR_PORT = 9000;
	//public static int SERVER_ADDR_PORT = 80;
	
	public static final String unassignedDatabaseName = "[unassigned_database]";
	public static final String unassignedTableName = "[unassigned_table]";
	public static final String unassignedColumnName = "[unassigned_column]";
	
	public static final String unassignedAssociationForeignKeyName ="[unassigned_foreign_key]";
	public static final String unassignedAssociationLinkingTableName ="[unassigned_linking_table]";

	public static final ArrayList<String> sqlSpecialChars = new ArrayList<String>(Arrays.asList(new String[]{"%", "_","*",".","|","+","#","(",")","[","]","{","}"}));
}
