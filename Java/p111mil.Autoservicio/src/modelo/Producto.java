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
public abstract class Producto {
    private String nombre;
    private double precio;
    
    protected final double FACTOR_IVA = 1.21;
    
    public abstract double calcularPrecioTotal(int cantidad);

    public Producto(String nombre, double precio) {
        this.nombre = nombre;
        this.precio = precio;
    }

    public String getNombre() {
        return nombre;
    }

    public double getPrecio() {
        return precio;
    }    
}
