/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.table;

import java.util.ArrayList;
import javax.swing.UIManager;
import p111mil.table.model.Usuario;
import p111mil.table.ui.FormularioTable;

/**
 *
 * @author admin
 */
public class P111milTable {

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
        
        FormularioTable formularioTable = new FormularioTable();
        
        formularioTable.setLocationRelativeTo(null);
        formularioTable.setVisible(true);
    }
    
}
