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
    
    @Override
    public boolean equals(Object object) {
        //1. Me fijo si es nulo
        if (object == null) {
            return false;
        }
        
        //2. Me fijo que object sea una instancia de Alumno
        if (! (object instanceof Alumno)) {
            return false;
        }
        
        //3. Casteo object a Alumno y comparo segun los valores
        Alumno alumno = (Alumno) object;
        
        //4. Comparo segun el numero de legajo
        return this.legajo == alumno.legajo && super.getApellido().equals(alumno.getApellido());
    }
}
