/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.anses2;

import java.util.Scanner;

/**
 *
 * @author admin
 */
public class P111milAnses2 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*
        La pagina web de la ANSES requiere informar los años necesarios de aporte para que las personas puedan solicitar su jubilacion. 
        Se necesita un programa que pida al usuario su genero (M o F) y su edad (entre 0 y 120). Si algun valor invalido es ingresado, debe mostrarse un mensaje de error.
        Las mujeres pueden solicitar la jubilacion a los 60 años y los hombres a partir de los 70 años.
        */
        
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Ingrese su genero (m o f)");
        String genero = scanner.nextLine();
        System.out.println("Ingrese su edad (0 a 99)");
        int edad = scanner.nextInt();        
        
        int edadJubilacion = genero.equals("m") ? 65 : 60;
        
        if (edad >= edadJubilacion) {
            System.out.println("Usted se puede jubilar");
        } else {
            System.out.println("Le restan " + (edadJubilacion - edad) + " años de aportes");
        }     
    }    
}
