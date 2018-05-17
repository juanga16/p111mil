/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

/**
 *
 * @author Invitado
 */
public class ProductoConDescuento extends Producto {

    public ProductoConDescuento(String nombre, double precio) {
        super(nombre, precio);
    }

    @Override
    public double calcularPrecioTotal(int cantidad) {
        double precioTotal = 0;
        
        switch (cantidad) {
            case 0: precioTotal = 0;
                    break;
            case 1: precioTotal = super.getPrecio();
                    break;
            case 2: precioTotal =  super.getPrecio() * 1.75;
                    break;
            default:precioTotal = super.getPrecio() * (1 + (cantidad - 1) * 0.65);                    
        }            
        
        return precioTotal * super.FACTOR_IVA;
    }
    
}
