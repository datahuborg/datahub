package Annotations;

public @interface AccessControl {
	public enum AccessLevels {Read, ReadWrite}
	
	public AccessLevels AccessLevel() default AccessLevels.ReadWrite;
}
