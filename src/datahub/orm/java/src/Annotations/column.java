package Annotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
public @interface column {

	public enum Index{ForeignKey,PrimaryKey,None}
	public enum RelationType{HasMany, HasOne, BelongsTo, ManyToMany, HasAndBelongsToMany, None};
	String name();
	Index Index() default Index.None;
	RelationType RelationType() default RelationType.None;
	//specify whether it is primary key, foreign key, auto increment, etc.

}
