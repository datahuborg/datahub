package Annotations;

public @interface IntegerField {

	boolean AutoIncrement() default false;

	boolean Serial() default false;

}
