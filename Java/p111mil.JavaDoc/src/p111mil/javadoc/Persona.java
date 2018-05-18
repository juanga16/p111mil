/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.javadoc;

/**
 * Clase que representa a una Persona
 * https://www.ecured.cu/Javadoc
 * 
 * @version 1.0
 * @author juan.desposito
 */
public class Persona {
    private String nombre;
    private String apellido;
    private int edad;

    /**
     * Devuelve el nombre de la persona
     * @return 
     */
    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getApellido() {
        return apellido;
    }

    public void setApellido(String apellido) {
        this.apellido = apellido;
    }

    public int getEdad() {
        return edad;
    }

    public void setEdad(int edad) {
        this.edad = edad;
    }
    
    /**
     * Este es el constructor por defecto
     * @see Persona
     */
    public Persona() {
        
    }
    
    public Persona(String nombre, String apellido) {
        this.nombre = nombre;
        this.apellido = apellido;
    }
    
    @Override
    public String toString() {
        // TODO implementar el metodo toString
        return super.toString();
    }
    
    /**
     * Define si la persona es mayor o no de Edad
     * 
     * @author juan.desposito
     * @return true si la edad es mayor o igual que 18   
     * @deprecated
    **/
    public boolean esMayorDeEdad() {
        // Comentario dentro del metodo. Este comentario no sale en el Javadoc
        return this.edad >= 18;
    }
    
    /**
     * Define si la persona puede o no sacar el carnet de conducir
     * @param edadMinima la edad minima para sacar el registro
     * @return true si la Edad es mayor que la edad minima
     */
    public boolean puedeSacarRegistroConducir(int edadMinima) {
        return this.edad >= edadMinima;
    }
}
