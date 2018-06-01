/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.combobox;

import java.awt.Color;


/**
 *
 * @author admin
 */
public class Jugador {
    private String nombre;
    private String apellido;
    private int numero;
    private Color color;
    
    public Jugador(String nombre, String apellido, int numero, Color color) {
        this.nombre = nombre;
        this.apellido = apellido;
        this.numero = numero;
        this.color = color;
    }

    public Color getColor() {
        return color;
    }
    
    @Override
    public String toString() {
        return "#" + this.numero + " - " + this.nombre + " " + this.apellido;
    }
}
