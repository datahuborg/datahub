package DataHubAnnotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

import DataHubResources.Constants;

@Retention(RetentionPolicy.RUNTIME)
public @interface Database {
	
	AnnotationsConstants.SetupModes setupMode() default AnnotationsConstants.SetupModes.Default;
	String name() default Constants.unassignedDatabaseName;
}
