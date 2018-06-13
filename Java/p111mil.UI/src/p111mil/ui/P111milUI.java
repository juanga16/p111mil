/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.ui;

import interfaz.*;
import javax.swing.JFrame;
import javax.swing.UIManager;

/**
 *
 * @author Invitado
 */
public class P111milUI {

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
        
        FrameInicio frameInicio = new FrameInicio();
        
        // Lo muestra centrado en la pantalla
        frameInicio.setLocationRelativeTo(null); 
        
        // Seteo el titulo, puedo hacerlo aca o bien desde las propiedades (si fuera estatico)
        frameInicio.setTitle("Formulario de Inicio");
        
        /*
        setDefaultCloseOperation()
        The setDefaultCloseOperation() method is used to specify one of several options for the close button. 
        Use one of the following constants to specify your choice:

        JFrame.EXIT_ON_CLOSE — Exit the application.
        JFrame.HIDE_ON_CLOSE — Hide the frame, but keep the application running.
        JFrame.DISPOSE_ON_CLOSE — Dispose of the frame object, but keep the application running.
        JFrame.DO_NOTHING_ON_CLOSE — Ignore the click.                
        */
        
        frameInicio.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frameInicio.setVisible(true);
    }
    
}
