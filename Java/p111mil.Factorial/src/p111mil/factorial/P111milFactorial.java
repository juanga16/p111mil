/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.factorial;

import java.util.Scanner;

/**
 *
 * @author admin
 */
public class P111milFactorial {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*
        Se necesita un programa que dado un numero calcule su factorial.
        https://factorialhr.es/numero-funcion-factorial        
        */
        
        System.out.println("Ingrese un numero para el calculo de su factorial:");
        
        // https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html
        
        Scanner scanner = new Scanner(System.in);
        long numeroBase = scanner.nextLong();
        
        for (long i = numeroBase - 1; i >= 1; i--) {
            numeroBase = numeroBase * i;            
        }
        
        System.out.println("El valor del factorial es: " + numeroBase);
    }    
}
