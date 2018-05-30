/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.interfaces;

import java.util.ArrayList;

/**
 *
 * @author admin
 */
public class P111milInterfaces {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Persona juan = new Persona();
        
        juan.trabajar();
        
        ArrayList<Futbolista> futbolistas = new ArrayList<Futbolista>();
        futbolistas.add(juan);
        
        futbolistas.get(0).jugar();
    }    
}
