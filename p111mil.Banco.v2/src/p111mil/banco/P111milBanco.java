/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.banco;

import java.time.LocalDateTime;
import java.time.Month;
import p111mil.banco.modelo.CajaAhorro;

/**
 *
 * @author admin
 */
public class P111milBanco {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        CajaAhorro cajaAhorro = new CajaAhorro(100);
        
        cajaAhorro.depositar(LocalDateTime.of(2018, Month.MARCH, 20, 13, 30), 10000);
        cajaAhorro.extraer(LocalDateTime.of(2018, Month.MARCH, 20, 19, 30), 1000.50f);
        cajaAhorro.extraer(LocalDateTime.of(2018, Month.MARCH, 26, 8, 0), 2000);
        cajaAhorro.depositar(LocalDateTime.of(2018, Month.MARCH, 29, 11, 15), 150);        
        cajaAhorro.extraer(LocalDateTime.of(2018, Month.APRIL, 5, 7, 30), 1000);
        cajaAhorro.extraer(LocalDateTime.of(2018, Month.APRIL, 8, 12, 19), 3000);
        cajaAhorro.imprimirResumenCuenta();
    }    
}
