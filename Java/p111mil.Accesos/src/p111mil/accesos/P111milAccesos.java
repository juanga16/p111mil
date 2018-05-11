/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.accesos;

import modelo.*;

/**
 *
 * @author Invitado
 */
public class P111milAccesos {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        ClasePublica clasePublica = new ClasePublica();
        
        clasePublica.metodoPrivado();
        clasePublica.metodoProtegido();
        clasePublica.metodoPublico();
        
        ClaseProtegida claseProtegida = new ClaseProtegida();
    }
    
}
