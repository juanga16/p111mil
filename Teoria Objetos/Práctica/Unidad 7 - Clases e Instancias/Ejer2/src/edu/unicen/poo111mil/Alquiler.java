package edu.unicen.poo111mil;

public class Alquiler {

	private Cliente cliente;
	private int dias;
	private Auto auto;
	
	public Alquiler(Cliente cliente, int dias, Auto auto) {
		this.cliente = cliente;
		this.dias = dias;
		this.auto = auto;
	}

	public double liquidar() {
		return this.auto.getValorPorDia() * this.dias;
	}

	public int getDias() {
		return dias;
	}

	public void setDias(int dias) {
		this.dias = dias;
	}

	public Cliente getCliente() {
		return cliente;
	}

	public Auto getAuto() {
		return auto;
	}
}
