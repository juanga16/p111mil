/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111geometria;

/**
 *
 * @author Invitado
 */
public class P111Geometria {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        
        Triangulo triangulo = new Triangulo();
        
        triangulo.setAltura(25);
        triangulo.setBase(45);
        
        System.out.println("La superficie es " + triangulo.calcularAltura());
    }
    
}
