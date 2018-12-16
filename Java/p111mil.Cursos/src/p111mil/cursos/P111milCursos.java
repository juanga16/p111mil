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
public class P111milCursos {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Ejercicio ejercicio1 = new Ejercicio("", "", 0);
        Ejercicio ejercicio2 = new Ejercicio("", "", 0);
        Ejercicio ejercicio3 = new Ejercicio("", "", 0);
        Ejercicio ejercicio4 = new Ejercicio("", "", 0);
        
        List<String> respuestasPedro = new ArrayList<String>();
        respuestasPedro.add("");
        List<String> respuestasLuis = new ArrayList<String>();
        respuestasLuis.add("");
        List<String> respuestasLuisTexto = new ArrayList<String>();
        respuestasLuisTexto.add("");
        
        Curso c = new Curso("Computación Primero");
        c.addAlumno("pedro");
        c.addAlumno("luis");

        Unidad u1 = new Unidad("uso de procesador de texto");
        u1.addEjercicio(ejercicio1); //asumir que ejercicio1 ya se encuentra creado
        u1.addEjercicio(ejercicio2); //asumir que ejercicio2 ya se encuentra creado

        Unidad u2= new Unidad("uso de planilla de cálculo");
        u2.addEjercicio(ejercicio3); //asumir que ejercicio3 ya se encuentra creado
        u2.addEjercicio(ejercicio4); //asumir que ejercicio4 ya se encuentra creado

        c.addUnidad(u1);
        c.addUnidad(u2);

        c.addRespuestas("uso de procesador de texto", "pedro", respuestasPedro); //asumir que respuestasPedro ya se encuentra creada
        c.addRespuestas("uso de planilla de cálculo", "luis", respuestasLuis); //asumir que respuestasLuis ya se encuentra creada
        c.addRespuestas("uso de planilla de cálculo", "luis", respuestasLuis); //asumir que respuestasLuis ya se encuentra creada

        c.addRespuestas("uso de procesador de texto", "luis", respuestasLuisTexto); //asumir que respuestasLuisTexto ya se encuentra creada

        System.out.println(c.xxx("luis"));
        System.out.println(c.xxx("pedro"));
    }    
}
