package DataHubAnnotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
public @interface Column {
	public enum Index{PrimaryKey,None}
	public enum NotNullConstraints{NotNull, None};
	public enum UniquenessConstraints{Unique, None};
	String name();
	Index index() default Index.None;
	NotNullConstraints notNullConstraint() default NotNullConstraints.None;
	UniquenessConstraints uniquenessConstraint() default UniquenessConstraints.None;
	//specify whether it is primary key, foreign key, auto increment, etc.

}
