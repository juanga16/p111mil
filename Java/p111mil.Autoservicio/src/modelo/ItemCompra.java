/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

import java.text.DecimalFormat;

/**
 *
 * @author Invitado
 */
public class ItemCompra {
    private Producto producto;
    private int cantidad;
    private int numeroItem;
    
    public ItemCompra(int numeroItem, Producto producto, int cantidad) {
        this.numeroItem = numeroItem;
        this.producto = producto;
        this.cantidad = cantidad;
    }
    
    @Override
    public String toString() {
        DecimalFormat decimalFormat = new DecimalFormat("$ 0.00");
        
        return "Item: " + this.numeroItem + " Producto: " + this.producto.getNombre() 
                    + " Precio: " + decimalFormat.format(this.producto.getPrecio()) + " Cantidad: " 
                    + this.cantidad + " Precio Total: " + decimalFormat.format(this.producto.calcularPrecioTotal(this.cantidad));                    
    }
    
    public double getPrecioTotal() {
        return this.producto.calcularPrecioTotal(this.cantidad);
    }
}
