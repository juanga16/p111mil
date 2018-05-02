/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.banco;

import p111mil.banco.modelo.CajaAhorro;

/**
 *
 * @author Invitado
 */
public class P111milBanco {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        CajaAhorro cajaAhorro = new CajaAhorro(100);
        
        cajaAhorro.depositar(10000);
        cajaAhorro.extraer(1000);
        cajaAhorro.extraer(2000);
        cajaAhorro.depositar(150);        
        cajaAhorro.extraer(1000);
        cajaAhorro.extraer(3000);
        System.out.println(cajaAhorro.getSaldo());
    }
    
}
