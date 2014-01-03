package Annotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
public @interface column {

	public enum Index{ForeignKey,PrimaryKey,None}
	public enum AssociationType{
		HasMany, 
		HasOne, 
		BelongsTo,
		HasAndBelongsToMany,
		None;
		AssociationType(){
			
		}
	};
	public enum RemovalOptions{CascadingDelete, None};
	String name();
	Index Index() default Index.None;
	AssociationType AssociationType() default AssociationType.None;
	//specify whether it is primary key, foreign key, auto increment, etc.

}
