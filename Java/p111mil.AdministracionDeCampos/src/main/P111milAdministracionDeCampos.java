/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package main;

import hibernate.ConfiguracionHibernate;
import java.awt.Dimension;
import java.awt.Frame;
import java.awt.Toolkit;
import javax.swing.UIManager;
import ui.FormularioPrincipal;
import ui.FormularioRegistrarCampo;

/**
 *
 * @author admin
 */
public class P111milAdministracionDeCampos {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        ConfiguracionHibernate.configurar();
        
        // Para setear que nuestros componentes graficos tomen los colores del sistema operativo en el que corro la aplicacion
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        }
        catch(Exception e) {
            e.printStackTrace();
        }
        
        FormularioPrincipal formularioPrincipal = new FormularioPrincipal();
                
        // Deshabilito el boton para maximizar
        formularioPrincipal.setResizable(false);        
        
        // Para que el formulario ocupe toda la pantalla
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        formularioPrincipal.setSize(screenSize.width, screenSize.height);
        
        // Lo muestra centrado en la pantalla
        formularioPrincipal.setLocationRelativeTo(null); 
        
        formularioPrincipal.setVisible(true);
    }    
}
