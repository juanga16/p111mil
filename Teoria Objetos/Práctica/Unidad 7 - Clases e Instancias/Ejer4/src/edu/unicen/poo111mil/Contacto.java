package edu.unicen.poo111mil;

public class Contacto {
	private String nombre;
	private String apellido;
	private String numeroTel; //puede tener +54 (249) 33233421
	private String mail;
	private int edad;
	
	public Contacto(String nombre, String apellido, String numeroTel, String mail, int edad) {
		super();
		this.nombre = nombre;
		this.apellido = apellido;
		this.numeroTel = numeroTel;
		this.mail = mail;
		this.edad = edad;
	}

	public boolean repetido(Contacto contacto) {
		return (this.nombre.equals(contacto.nombre) &&
				this.apellido.equals(contacto.apellido) &&
				this.numeroTel.equals(contacto.numeroTel));
	}
	
	public String getNombre() {
		return nombre;
	}

	public void setNombre(String nombre) {
		this.nombre = nombre;
	}

	public String getApellido() {
		return apellido;
	}

	public void setApellido(String apellido) {
		this.apellido = apellido;
	}

	public String getNumeroTel() {
		return numeroTel;
	}

	public void setNumeroTel(String numeroTel) {
		this.numeroTel = numeroTel;
	}

	public String getMail() {
		return mail;
	}

	public void setMail(String mail) {
		this.mail = mail;
	}

	public int getEdad() {
		return edad;
	}

	public void setEdad(int edad) {
		this.edad = edad;
	}

	@Override
	public String toString() {
		return "Contacto [nombre=" + nombre + ", apellido=" + apellido + ", numeroTel=" + numeroTel + "]";
	}
	
	
}
