package DataHubAnnotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

import DataHubResources.Constants;

@Retention(RetentionPolicy.RUNTIME)
public @interface Table {

	AnnotationsConstants.SetupModes setupMode() default AnnotationsConstants.SetupModes.Default;
	String name() default Constants.unassignedTableName;

}
