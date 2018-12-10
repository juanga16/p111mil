/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.herencia;

import modelo.Alumno;
import modelo.Curso;
import modelo.Persona;
import modelo.Profesor;

/**
 *
 * @author admin
 */
public class P111milHerencia {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*
        Profesor sergio = new Profesor("Sergio", "Schro", "412345");                
        Profesor juan = new Profesor("Juan", "D'Esposito", "423456");
        
        // No puedo instanciar personas porque es una clase abstracta
        //Persona miguel = new Persona();
        
        Alumno juanPerez = new Alumno("Juan", "Perez", 123);
        Alumno joseGarcia = new Alumno("Jose", "Garcia", 345);
        Alumno estebanQuito = new Alumno("Esteban", "Quito", 678);
        Alumno luciaGomez = new Alumno("Lucia", "Gomez", 901);
        
        Curso curso = new Curso();
        curso.AgregarProfesor(sergio);
        curso.AgregarProfesor(juan);
        curso.AgregarAlumno(juanPerez);
        curso.AgregarAlumno(joseGarcia);
        curso.AgregarAlumno(estebanQuito, luciaGomez);
        
        System.out.println(sergio.darPresentacion());
        System.out.println(juanPerez.darPresentacion());
        curso.ListarPersonas();
        */
        
        Alumno leo = new Alumno("Leo", "Espinoza", 1);
        Alumno nacho = new Alumno("Nacho", "Coria", 2);
        Alumno leo2 = leo;
        Alumno leo3 = new Alumno("Leo", "Espinoza", 1);
        Alumno leo4 = new Alumno("Leonardo Emanuel", "Espinoza", 5);
        
        System.out.println(leo.equals(nacho));
        System.out.println(leo.equals(leo2));
        System.out.println(leo.equals(leo3));
        System.out.println(leo.equals(leo4));
        
        String nombre = "Juan";
        String nombre2 = "juan";
        String nombre3 = "juan;leo;nico";
        
        String[] arreglo = nombre3.split(";");
        
        
        System.out.println(nombre.startsWith("ju"));
        System.out.println(nombre.substring(2));
    }    
}
