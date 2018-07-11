package edu.unicen.poo111mil;

public class Factura {
	private Cliente cliente;
	private int monto;
	
	public Factura(Cliente cliente, int monto) {
		super();
		this.cliente = cliente;
		this.monto = monto;
	}

	public Cliente getCliente() {
		return cliente;
	}

	public void setCliente(Cliente cliente) {
		this.cliente = cliente;
	}

	public int getMonto() {
		return monto;
	}

	public void setMonto(int monto) {
		this.monto = monto;
	}

	@Override
	public String toString() {
		return "Factura [cliente=" + cliente + ", monto=" + monto + "]";
	}
	
}
