/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 *
 * @author admin
 */
public class Curso {
    private ArrayList<Alumno> alumnos = new ArrayList<Alumno>();
    private ArrayList<Profesor> profesores = new ArrayList<Profesor>();
    
    public void AgregarAlumno(Alumno alumno) {
        alumnos.add(alumno);
    }
    
    // Este metodo tiene el mismo nombre que el anterior, pero diferentes parametros, lo estoy sobrecargando
    public void AgregarAlumno(Alumno alumno1, Alumno alumno2) {
        alumnos.add(alumno1);
        alumnos.add(alumno2);
    }
    
    public void AgregarProfesor(Profesor profesor) {
        profesores.add(profesor);
    }
    
    public void ListarPersonas() {
        ArrayList<Persona> personas = new ArrayList<Persona>();
        
        personas.addAll(alumnos);
        personas.addAll(profesores);
        
        List<Persona> personasOrdenadas = personas.stream()
                                            .sorted((x1, x2) -> x1.getApellido().compareTo(x2.getApellido()))
                                            .collect(Collectors.toList());
        
        System.out.println("Listado de personas:");
        for(Persona persona : personasOrdenadas) {
            System.out.println(persona.darPresentacion());
        }
    }
}
