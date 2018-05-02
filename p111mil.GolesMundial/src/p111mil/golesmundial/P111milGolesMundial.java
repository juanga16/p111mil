/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.golesmundial;

import java.text.DecimalFormat;
import java.util.Scanner;

/**
 *
 * @author admin
 */
public class P111milGolesMundial {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*
        Se necesita un programa que sirva para registrar los goles de las estrellas del futbol en el proximo mundial. 
        En un mundial un jugador puede disputar un minimo de 0 y un maximo de 7 partidos. Un jugador puede realizar 0 o mas goles en un partido.
        El jugador que no juega los 7 partidos es porque: su equipo no jugo la final o el tercer puesto, estuvo lesionado o bien no jugo porque el DT no lo puso.
        El programa se termina si se ingresaron los datos de los 7 partidos o si el usuario ingresa un valor menor a 0.
        */
        
        Scanner scanner = new Scanner(System.in);
        
        int partidosJugados = 0;
        int golesPartido = 0;
        int golesTotales = 0;
        
        while (golesPartido >= 0 && partidosJugados < 7) {                                    
            System.out.println("Ingrese los goles convertidos en el partido: " + (partidosJugados + 1));
            golesPartido = scanner.nextInt();                                      
            
            // Para no restar si el valor es negativo
            if (golesPartido >= 0) {
                golesTotales = golesTotales + golesPartido;
                partidosJugados++;
            }                        
        }    
        
        System.out.println("Cantidad de partidos jugados: " + partidosJugados);
        System.out.println("Cantidad de goles convertidos: " + golesTotales);

        double promedioGoles = golesTotales / (double) partidosJugados;
        DecimalFormat formatter = new DecimalFormat("#0.00");
        System.out.println("El promedio de goles es: " + formatter.format(promedioGoles));
    }    
}
