package edu.unicen.poo111mil;

import java.util.ArrayList;
import java.util.List;

public class Empresa {
	private List<Cliente> clientes; 
	private List<Factura> facturas;
	
	public Empresa() {
		this.clientes = new ArrayList<>();
		this.facturas = new ArrayList<>();
	}
	
	public Empresa(Cliente[] clientes){
		this();
		for(Cliente c: clientes)
			this.clientes.add(c);
	}
	
	public Cliente masFacturo() {
		int[] facturado = new int[clientes.size()];
		for(Factura f: facturas)
			facturado[clientes.indexOf(f.getCliente())] += f.getMonto();
		int max = facturado[0];
		Cliente mejor = clientes.get(0);
		for (int i = 1; i < clientes.size(); i++)
			if(max < facturado[i]) {
				max = facturado[i];
				mejor = clientes.get(i);
			}
		return mejor;
	}
	
	public int facturadoCliente(Cliente c) {
		int total = 0;
		for(Factura f: facturas)
			if (f.getCliente().equals(c))
				total += f.getMonto();
		return total;
	}

	public void facturar(Cliente c, int monto) {
		Factura f = new Factura(c, monto);
		this.facturas.add(f);
	}
}
