/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.ejemplos;

import java.util.Scanner;

/**
 *
 * @author admin
 */
public class P111milEjemplos {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        
        // Declaro una variable de tipo ENTERO y la inicializo
        int edad = 37;
        
        // Asigno un nuevo valor a edad
        edad = 25;
        
        // Imprimo el valor de la variable en la Consola
        System.out.println("La edad es: " + edad);
        
        
        // Para. For. 
        for (int i=0; i<= 10; i++) {
            System.out.println("Para: " + i);
        }
        
        // While. Mientras
        while (edad < 50) {
            System.out.println("Mientras: " + edad);
            edad++; // Incrementamos edad en 1. Igual que hacer edad = edad + 1
        }
        
        // Hasta. Do While
        do {
            System.out.println("Hasta: " + edad);
            edad++; // Incrementamos edad en 1. Igual que hacer edad = edad + 1
        } while (edad < 75);
        
        // Si. If
        if (edad < 80) {
            System.out.println("La edad es menor que 80");
        }
        
        // Si con sino. If y else
        if (edad < 95) {
            System.out.println("La edad es menor que 95");
        } else {
            System.out.println("La edad es mayor o igual que 95");
        }
        
        // Si con sino si. If y else if
        if (edad < 85) {
            System.out.println("La edad es menor que 85");
        } else if (edad < 90) {
            System.out.println("La edad es menor que 90");
        } else {
            System.out.println("La edad es mayor o igual que 90");
        }
        
        // Si con Y (AND)
        if (edad > 0 && edad < 18) {
            System.out.println("Soy menor de edad");
        }
        
        // Si con O (OR)
        if (edad < 0 || edad < 99) {
            System.out.println("La edad es invalida");
        }
        
        // Declaro las variables en convencion lowerCamelCase: https://es.wikipedia.org/wiki/CamelCase
        int numeroMes = 8;
        String nombreMes;
        
        // Segun. Switch
        switch (numeroMes) {
            case 1:  nombreMes = "January";
                     break;
            case 2:  nombreMes = "February";
                     break;
            case 3:  nombreMes = "March";
                     break;
            case 4:  nombreMes = "April";
                     break;                    
            default: nombreMes = "Otro mes";
                     break;
        }
        
        System.out.println("Nombre del mes: " + nombreMes);
        
        // Lectura por teclado
        Scanner teclado = new Scanner(System.in);
        int cantidad = teclado.nextInt();
        System.out.println("El valor de cantidad es: " + cantidad);
        String marcaAuto = teclado.next();
        System.out.println("La marca del auto es: " + marcaAuto);
    }
    
}
