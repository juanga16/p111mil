package edu.unicen.poo111mil;

import java.util.ArrayList;
import java.util.List;

public class Empresa2 {
	private List<Cliente> clientes; 
	private List<Factura> facturas;
	private List<Integer> total;
	
	public Empresa2() {
		this.clientes = new ArrayList<>();
		this.facturas = new ArrayList<>();
	}
	
	public Empresa2(Cliente[] clientes){
		this();
		for(Cliente c: clientes)
			this.addCliente(c);
	}
	
	public void addCliente(Cliente c) {
		this.clientes.add(c);
		this.total.add(0);
	}

	public Cliente masFacturo() {
		int max = -1;
		Cliente mejor = null;
		for (Cliente c: clientes) {
			int facturado = this.facturadoCliente(c);
			if(max < facturado) {
				max = facturado;
				mejor = c;
			}
		}
		return mejor;
	}
	
	public int facturadoCliente(Cliente c) {
		return total.get(clientes.indexOf(c));
	}

	public void facturar(Cliente c, int monto) {
		Factura f = new Factura(c, monto);
		this.facturas.add(f);
		int index = clientes.indexOf(c);
		this.total.set(index, this.total.get(index)+monto);
	}
}
