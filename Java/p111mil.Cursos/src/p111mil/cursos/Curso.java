/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.cursos;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 *
 * @author admin
 */
public class Curso {
    private String nombre;
    private List<String> alumnos;
    private List<Unidad> unidades;
 
    public Curso(String nombre) {
        this.nombre = nombre;
        
        alumnos = new ArrayList<String>();
        unidades = new ArrayList<Unidad>();
    }
    
    public boolean addAlumno(String alumno) {
        return alumnos.add(alumno);
    }
    
    public boolean addUnidad(Unidad unidad) {
        return unidades.add(unidad);
    }
    
    public boolean addRespuestas(String temaUnidad, String alumno, List<String> respuestas) {
        Unidad unidad = getUnidadPorTema(temaUnidad);
        
        if (unidad == null) {
            unidad = new Unidad(temaUnidad);
        }
        
        return unidad.addRespuestas(alumno, respuestas);
    }
    
    private Unidad getUnidadPorTema(String temaUnidad) {
        Unidad unidadEncontrada = null;
        
        for(Unidad unidad : this.unidades) {
            if (unidad.esDeTema(temaUnidad)) {
                unidadEncontrada = unidad;
                break;
            }
        }
        
        return unidadEncontrada;
    }
    
    public List<String> getAlumnosConCalificacionMenor(String temaUnidad, float calificacion) {
        List<String> alumnosConCalificacionSuperior = new ArrayList<String>();
        Unidad unidad = this.getUnidadPorTema(temaUnidad);
        
        if (unidad != null) {
            for(String alumno : this.alumnos) {
                if (! (unidad.getCalificacion(alumno) > calificacion)) {
                    alumnosConCalificacionSuperior.add(alumno);
                }
            }
        }
        
        return alumnosConCalificacionSuperior;
    }
    
    public List<String> xxx(String alumno){
        List<String> xx = new ArrayList<String>();
        Iterator<Unidad> it = unidades.iterator();
        
        while(it.hasNext()){
            Unidad u = it.next();
            if(u.getCalificacion(alumno) > -1)
                xx.add(u.getTema());
        }
        
        return xx;
    }       
}
