package DataHubAnnotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;


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
	LoadTypes loadType() default LoadTypes.Eager; //default load type is Eager = recursive loading of associated model
	String linkingTable() default "";
	String leftTableForeignKey() default ""; //used for HABTM
	String rightTableForeignKey() default ""; //used for HABTM
	String foreignKey();
	RemovalOptions removalOption() default RemovalOptions.None;
	
}
