package Annotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;


@Retention(RetentionPolicy.RUNTIME)
public @interface Association {
	public enum RemovalOptions{CascadingDelete, None};
	public enum AssociationType{
		HasMany, 
		HasOne, 
		BelongsTo,
		HasAndBelongsToMany
	};
	AssociationType associationType();
	String linkingTable() default "";
	String leftTableForeignKey() default ""; //used for HABTM
	String rightTableForeignKey() default ""; //used for HABTM
	String foreignKey();
	RemovalOptions removalOption() default RemovalOptions.None;
	
}
