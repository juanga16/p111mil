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
public class Alumno extends Persona {
    private int legajo;

    public int getLegajo() {
        return legajo;
    }

    public void setLegajo(int legajo) {
        this.legajo = legajo;
    }
    
    public Alumno(String nombre, String apellido, int legajo) {
        super(nombre, apellido);
        this.legajo = legajo;
    }
    
    @Override
    public String darPresentacion() {
        return "Soy el Alumno: " + this.getNombre() + " " + this.getApellido() + " y mi legajo es: " + this.legajo;
    }   
}
