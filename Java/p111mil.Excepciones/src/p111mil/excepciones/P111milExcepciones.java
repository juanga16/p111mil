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
public class P111milExcepciones {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Division division = new Division();
        
        /*
            Dos clases de errores:
            - Compilacion
            - Ejecucion
        */
        
        /*
            Como el metodo "calcular" puede lanzar una exepcion, 
            me veo obligado a invocarlo dentro de un try/catch
        */
        
        
        // https://www.programcreek.com/2009/02/diagram-for-hierarchy-of-exception-classes/
        
        try {
            division.calcular(25, 0);
        } catch (MiExcepcion miExcepcion) {
            System.out.println(miExcepcion.getMessage());
        }
    }
    
}
