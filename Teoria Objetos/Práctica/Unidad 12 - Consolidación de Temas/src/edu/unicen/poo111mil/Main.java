package edu.unicen.poo111mil;

public class Main {

	public static void main(String[] args) {
		Cliente[] clientes = new Cliente[10];
		for(int i = 0; i<10; i++)
			clientes[i] = new Cliente("Nombre: " + i, "Apellido: " + i, "Calle "+i);
		Empresa e = new Empresa(clientes);
		for(int i = 0; i < 100; i++) {
			Cliente c = clientes[(int)(clientes.length * Math.random())];
			int monto = (int)(1000 * Math.random());
			e.facturar(c, monto);
		}

		for(int i = 0; i<10; i++) {
			Cliente c = new Cliente("Nombre: " + i, "Apellido: " + i, "Calle "+i);
			System.out.println(c + " - " + e.facturadoCliente(c));
		}
		Cliente mejor = e.masFacturo();
		System.out.println("El mejor cliente es "+ mejor);
		System.out.println("Facturado: " + e.facturadoCliente(mejor));
	}

}
