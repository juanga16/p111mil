/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

/**
 *
 * @author admin
 */
public abstract class Telefono {
    // Que una clase sea abstracta significa que no se pueden instanciar objetos    
    private int numero;
    private String marca;
    
    private static int cantidadTelefonos = 0;
    protected static String PREFIJO_SUAREZ = "(02926)";

    public static int getCantidadTelefonos() {
        return cantidadTelefonos;
    }

    public int getNumero() {
        return numero;
    }

    public void setNumero(int numero) {
        this.numero = numero;
    }

    public String getMarca() {
        return marca;
    }

    public void setMarca(String marca) {
        this.marca = marca;
    }
 
    public abstract void llamar(int numero);    
    
    public void sonar() {
        System.out.println("Estoy sonando ...");
    }
    
    public Telefono(int numero) {
        this.numero = numero;
        
        // Cada vez que instancio un telefono incremento el contador
        cantidadTelefonos = cantidadTelefonos + 1;
    }    
}
