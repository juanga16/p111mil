/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.ui2;

import java.util.ArrayList;
import javax.swing.UIManager;
import modelo.*;
import ui.Formulario;

/**
 *
 * @author admin
 */
public class P111milUI2 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        }
        catch(Exception e) {
            e.printStackTrace();
        }
        
        ArrayList<Localidad> localidades = new ArrayList<Localidad>();
        
        Provincia buenosAires = new Provincia("Buenos Aires");
        Provincia cordoba = new Provincia("Córdoba");
        Provincia santaFe = new Provincia("Santa Fe");
        Provincia chubut = new Provincia("Chubut");
        
        localidades.add(new Localidad("Coronel Suárez", 7540, buenosAires));
        localidades.add(new Localidad("Mar del Plata", 7600, buenosAires));
        localidades.add(new Localidad("Bahía Blanca", 8000, buenosAires));
        localidades.add(new Localidad("Córdoba", 5000, cordoba));
        localidades.add(new Localidad("Santa Fe", 3000, santaFe));
        localidades.add(new Localidad("Rosario", 2000, santaFe));
        localidades.add(new Localidad("Comodoro Rivadavia", 9000, chubut));
        
        Formulario formularioComboBox = new Formulario(localidades);
        formularioComboBox.setLocationRelativeTo(null);
        formularioComboBox.setVisible(true);        
    }    
}