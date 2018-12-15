/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.cursos;

/**
 *
 * @author admin
 */
public class Ejercicio {
    private String consigna;
    private String respuesta;
    private float puntaje;
    
    public Ejercicio(String consigna, String respuesta, float puntaje) {
        this.consigna = consigna;
        this.respuesta = respuesta;
        this.puntaje = puntaje;
    }
    
    public boolean esCorrecto(String respuesta) {
        return this.respuesta.equals(respuesta);
    }
    
    public float getPuntaje(String respuesta) {
        if (esCorrecto(respuesta)) {
            return this.puntaje;
        }
        
        return 0;
    }
}
