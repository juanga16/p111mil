/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.cursos;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author admin
 */
public class Unidad {
    private String tema;
    private List<Ejercicio> ejercicios;
    private List<List<String>> respuestasAlumnos;
    private List<String> alumnos;
    
    public Unidad(String tema) {
        this.tema = tema;
        
        this.ejercicios = new ArrayList<Ejercicio>();
        this.respuestasAlumnos = new ArrayList<List<String>>();
        this.alumnos = new ArrayList<String>();
    }
    
    public float calificarEjercicios(List<String> respuestas) {
        float calificacion = 0;
        
        for(int i=0; i<respuestas.size(); i++) {
            String respuesta = respuestas.get(i);
            Ejercicio ejercicio = this.ejercicios.get(i);
            
            calificacion = calificacion + ejercicio.getPuntaje(respuesta);            
        }
        
        return calificacion;
    }
}
