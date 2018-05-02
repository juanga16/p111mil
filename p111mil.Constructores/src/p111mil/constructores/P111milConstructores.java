/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.constructores;

import p111mil.constructores.model.Persona;

/**
 *
 * @author admin
 */
public class P111milConstructores {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // En la linea 8 esta el import para poder usar la clase Persona, que se encuentra en otro package
        Persona diegoMaradona = new Persona("Diego", "Maradona");
        diegoMaradona.imprimirDatos();
        
        Persona manuGinobil = new Persona("Manu", "Ginobili", 27123456);
        manuGinobil.imprimirDatos();
        
        // Da error porque no defini el constructor sin parametros
        Persona guillermoVilas = new Persona();
    }    
}
