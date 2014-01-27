package DataHubAnnotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

import DataHubResources.Constants;


@Retention(RetentionPolicy.RUNTIME)
public @interface Association {
	public enum RemovalOptions{CascadingDelete, None};
	
	public enum AssociationTypes{
		HasMany, 
		HasOne, 
		BelongsTo,
		HasAndBelongsToMany
	};
	
	public enum LoadTypes{Eager, None};
	
	AssociationTypes associationType();
	AnnotationsConstants.SetupModes setupMode() default AnnotationsConstants.SetupModes.Default;
	LoadTypes loadType() default LoadTypes.Eager; //default load type is Eager = recursive loading of associated model
	String linkingTable() default "";//used for HABTM
	String leftTableForeignKey() default ""; //used for HABTM
	String rightTableForeignKey() default ""; //used for HABTM
	String foreignKey() default "";
	RemovalOptions removalOption() default RemovalOptions.None;
	
}
