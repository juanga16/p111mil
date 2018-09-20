/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.agenda;

import javax.swing.UIManager;
import p111mil.agenda.formularios.Listado;

/**
 *
 * @author PC-MAESTRO
 */
public class P111milAgenda {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ex) {
            
        }
        
        Listado listado = new Listado();
        listado.setLocationRelativeTo(null);
        listado.setVisible(true);
    }    
}
