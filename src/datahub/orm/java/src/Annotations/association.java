package Annotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;


@Retention(RetentionPolicy.RUNTIME)
public @interface association {
	public enum RemovalOptions{CascadingDelete, None};
	public enum AssociationType{
		HasMany, 
		HasOne, 
		BelongsTo,
		HasAndBelongsToMany
	};
	AssociationType associationType();
	String linkingTable() default "";
	String table1ForeignKey();
	String table2ForeignKey() default "";
	RemovalOptions removalOption() default RemovalOptions.None;
	
}
