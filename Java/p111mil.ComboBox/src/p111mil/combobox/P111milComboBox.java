/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.combobox;

import javax.swing.UIManager;

/**
 *
 * @author admin
 */
public class P111milComboBox {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        try
        {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        }
        catch(Exception e) {
            e.printStackTrace();
        }
        
        Formulario formulario = new Formulario();
        formulario.setVisible(true);
    }    
}
