/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.excepciones;

/**
 * 
 * @author admin
 */
public class MiExcepcion extends Exception {
   /*
        Esta clase es una excepcion personalizada, es decir "hereda de" la clase base Excepcion
        En el constructor tenemos un mensaje de error personalizado
        Una Exception es una clase que representa un tipo de error
    */ 
    public MiExcepcion() {
        super("Mensaje de error personalizado");
    }    
}
