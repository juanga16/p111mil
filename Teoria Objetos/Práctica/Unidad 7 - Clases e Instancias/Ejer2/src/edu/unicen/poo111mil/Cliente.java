package edu.unicen.poo111mil;

public class Cliente {
	private int nroLicencia;
	private String nombre;
	private String apellido;
	
	public Cliente(int nroLicencia, String nombre, String apellido) {
		super();
		this.nroLicencia = nroLicencia;
		this.nombre = nombre;
		this.apellido = apellido;
	}

	public int getNroLicencia() {
		return nroLicencia;
	}

	public void setNroLicencia(int nroLicencia) {
		this.nroLicencia = nroLicencia;
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
	
}
