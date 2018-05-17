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
public class ProductoSinIva extends Producto {

    public ProductoSinIva(String nombre, double precio) {
        super(nombre, precio);
    }

    @Override
    public double calcularPrecioTotal(int cantidad) {
        return super.getPrecio() * cantidad;
    }
    
}
