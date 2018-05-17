/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

import java.text.DecimalFormat;
import java.util.ArrayList;

/**
 *
 * @author Invitado
 */
public class Factura {
    private int numero;
    private ArrayList<ItemCompra> itemsCompra = new ArrayList<ItemCompra>();
    
    private static int cantidadFacturas = 0;

    public Factura() {
        Factura.cantidadFacturas = Factura.cantidadFacturas + 1;
        this.numero = Factura.cantidadFacturas;
    }
        
    public void agregarItemCompra(Producto producto, int cantidad) {
        int numeroItem = this.itemsCompra.size() + 1;
        ItemCompra itemCompra = new ItemCompra(numeroItem, producto, cantidad);
        
        this.itemsCompra.add(itemCompra);
    }
    
    public void imprimir() {
        System.out.println("Factura Número: " + this.numero);
        
        double totalFactura = 0;
        for(ItemCompra itemCompra : this.itemsCompra) {
            System.out.println(itemCompra);
            totalFactura = totalFactura + itemCompra.getPrecioTotal();
        }
        
        DecimalFormat decimalFormat = new DecimalFormat("$ 0.00");
        System.out.println("Total Factura: " + decimalFormat.format(totalFactura));
    }
}
