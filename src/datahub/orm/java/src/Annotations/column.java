package Annotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
public @interface column {

	public enum Index{ForeignKey,PrimaryKey, LinkedSet, None}
	String name() default "";
	Index Index() default Index.None;
	//specify whether it is primary key, foreign key, auto increment, etc.

}
