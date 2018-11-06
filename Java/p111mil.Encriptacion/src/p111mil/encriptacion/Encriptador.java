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
public class Encriptador {
    public String hashPassword(String passwordPlana){
        return BCrypt.hashpw(passwordPlana, BCrypt.gensalt());
    }
    
    public void verificarPassword(String passwordPlana, String hashedPassword) {
        if (BCrypt.checkpw(passwordPlana, hashedPassword)) {
            System.out.println("Los passwords coinciden.");
        } else {
            System.out.println("Los passwords no coinciden.");
        }
    }
}
