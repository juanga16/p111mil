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
    
    /**
     * Dado un conjunto de respuestas de ejercicios retorna la puntuacion de la unidad
     * @param respuestas
     * @return puntaje de la unidad segun esas respuestas
     */
    public float calificarEjercicios(List<String> respuestas) {
        float calificacion = 0;
        
        for(int i=0; i<respuestas.size(); i++) {
            String respuesta = respuestas.get(i);
            Ejercicio ejercicio = this.ejercicios.get(i);
            
            calificacion = calificacion + ejercicio.getPuntaje(respuesta);            
        }
        
        return calificacion;
    }
    
    public boolean esDeTema(String tema) {
        return this.tema.equals(tema);
    }
    
    public String getTema() {
        return this.tema;
    }
    
    public float getCalificacion(String alumno) {        
        float calificacion = -1;        
        int posicionAlumno = this.getPosicionAlumno(alumno);
        
        if (posicionAlumno != -1) {
            calificacion = calificarEjercicios(this.respuestasAlumnos.get(posicionAlumno));
        }
        
        return calificacion;        
    }
    
    private int getPosicionAlumno(String alumno) {
        int posicionAlumno = -1;
        
        for(int i = 0; i<this.alumnos.size(); i++) {
            if(this.alumnos.get(i).equals(alumno)) {
                posicionAlumno = i;
                break;
            }
        }
        
        return posicionAlumno;
    }
    
    public boolean addRespuestas(String alumno, List<String> respuestas) {
        // Me fijo si el alumno ya agrego sus respuestas. Hay un paralelismo entre las listas de alumnos y respuestas
        int posicionAlumno = this.getPosicionAlumno(alumno);
        
        if (posicionAlumno == -1) {
            // El alumno todavia no entrego sus respuestas asi que agrego a las listas
            this.alumnos.add(alumno);
            this.respuestasAlumnos.add(respuestas);
            
            return true;
        }
        
        // El alumno ya habia entregado las respuestas
        return false;
    }

    void addEjercicio(Ejercicio ejercicio) {
        this.ejercicios.add(ejercicio);
    }
}
