package edu.unicen.poo111mil;

public class Auto {
	
	private String patente;
	private String modelo;
	private String marca;
	private boolean sedan;
	private double valorPorDia;
	private Alquiler alquiler;
	
	
	public Auto(String patente, String modelo, String marca, boolean sedan, double valorPorDia) {
		super();
		this.patente = patente;
		this.modelo = modelo;
		this.marca = marca;
		this.sedan = sedan;
		this.valorPorDia = valorPorDia;
	}

	public boolean alquilar(Cliente cliente, int dias) {
		if (this.alquiler == null) {
			this.alquiler = new Alquiler(cliente, dias, this);
			return true;
		}
		return false;
	}

	public double liquidar() {
		if (this.alquiler != null) {
			return this.alquiler.liquidar();
		}
		return 0;
	}

	public boolean retornar() {
		if (this.alquiler != null) {
			this.alquiler = null;
			return true;
		}
		return false;
	}

	public String getPatente() {
		return patente;
	}

	public void setPatente(String patente) {
		this.patente = patente;
	}

	public String getModelo() {
		return modelo;
	}

	public void setModelo(String modelo) {
		this.modelo = modelo;
	}

	public String getMarca() {
		return marca;
	}

	public void setMarca(String marca) {
		this.marca = marca;
	}

	public boolean isSedan() {
		return sedan;
	}

	public void setSedan(boolean sedan) {
		this.sedan = sedan;
	}

	public double getValorPorDia() {
		return valorPorDia;
	}

	public void setValorPorDia(double valorPorDia) {
		this.valorPorDia = valorPorDia;
	}

	public Alquiler getAlquiler() {
		return alquiler;
	}

}
