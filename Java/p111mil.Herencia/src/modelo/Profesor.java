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
public class Profesor extends Persona {
    // Uso la palabra Extends para decir que Profesor hereda de Persona o sea que el Profesor "es una" Persona
    private String telefono;

    public Profesor(String nombre, String apellido, String telefono) {
        super(nombre, apellido);
        this.telefono = telefono;
    }

    public String getTelefono() {
        return telefono;
    }

    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }

    // En este caso estoy redefiniendo el metodo darPresentacion, el comportamiento que tiene en Persona lo sobre escribo para Profesor
    @Override
    public String darPresentacion() {
        return "Soy el Profesor: " + this.getNombre() + " " + this.getApellido() + " y mi telefono es: " + this.getTelefono();
    }        
}
