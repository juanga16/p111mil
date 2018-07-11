package practica10.escuela;

public class Alumno {
	private String apellido;
	private String nombre;
	
	public Alumno ()
	{
		this.apellido="Perez";
		this.nombre="Juan";
		
	}

	public String getApellido() {
		return apellido;
	}

	public void setApellido(String apellido) {
		this.apellido = apellido;
	}

	public String getNombre() {
		return nombre;
	}

	public void setNombre(String nombre) {
		this.nombre = nombre;
	}

	public Alumno (String apellido, String nombre)
	{
		this.apellido=apellido;
		this.nombre=nombre;
		
	}
}
