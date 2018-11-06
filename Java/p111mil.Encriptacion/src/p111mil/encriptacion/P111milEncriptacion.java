/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.encriptacion;

import org.mindrot.jbcrypt.BCrypt;

/**
 *
 * @author Invitado
 */
public class P111milEncriptacion {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Encriptador encriptador = new Encriptador();
        
        String passwordPlana = "esta es una password larga1";
        String hashPassword = encriptador.hashPassword(passwordPlana);
        
        System.out.println(passwordPlana);
        System.out.println(hashPassword);
        encriptador.verificarPassword(passwordPlana, hashPassword);
        encriptador.verificarPassword("otra password", hashPassword);        
    }           
}
