/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.constructores.model;

/**
 *
 * @author admin
 */
public class Persona {
    private String nombre;
    private String apellido;
    private int numeroDocumento;

    public void imprimirDatos()
    {
        System.out.println("Me llamo " + this.nombre + " " + this.apellido + " y mi numero de documento es: " + this.numeroDocumento);
    }
    
    /*
    Defino un constructor que recibe tres parametros: nombre, apellido y numero de documento
    Al definir al menos un constructor mio, anulo la posibilidad de utilizar el constructor por defecto a menos que lo defina nuevamente
    */
    public Persona(String nombre, String apellido, int numeroDocumento) {
        // Dado que el siguiente constructor recibe el nombre y apellido, puedo invocarlo con la palabra clave this
        this(nombre, apellido);
        this.numeroDocumento = numeroDocumento;
    }
    
    public Persona(String nombre, String apellido) {
        this.nombre = nombre;
        this.apellido = apellido;
    }
}
