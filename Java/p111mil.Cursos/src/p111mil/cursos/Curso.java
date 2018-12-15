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
public class Curso {
    private String nombre;
    private List<String> alumnos;
    private List<String> unidades;
 
    public Curso(String nombre) {
        this.nombre = nombre;
        
        alumnos = new ArrayList<String>();
        unidades = new ArrayList<String>();
    }
    
    public boolean addAlumno(String alumno) {
        return alumnos.add(alumno);
    }
    
    public boolean addUnidad(String unidad) {
        return unidades.add(unidad);
    }
    
    public boolean addRespuestas(String temaUnidad, String alumno, List<String> respuestas) {
        
    }
}
