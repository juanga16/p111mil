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
        // Para setear que nuestros componentes graficos tomen los colores del sistema operativo en el que corro la aplicacion
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        }
        catch(Exception e) {
            e.printStackTrace();
        }
        
        FrameInicio frameInicio = new FrameInicio();
        
        // Lo muestra centrado en la pantalla
        frameInicio.setLocationRelativeTo(null); 
        
        // Deshabilito el boton para maximizar
        frameInicio.setResizable(false);
        // Seteo el titulo, puedo hacerlo aca o bien desde las propiedades (si fuera estatico)
        frameInicio.setTitle("Formulario de Inicio");
        
        /*
        Este metodo es para establecer que sucedera cuando clickee en la X para cerrar el frame
        
        JFrame.EXIT_ON_CLOSE — Cierra el progama
        JFrame.HIDE_ON_CLOSE — Oculta el Frame pero el programa sigue ejecutandose
        JFrame.DISPOSE_ON_CLOSE — Hace dispose del Frame pero el programa sigue ejecutandose
        JFrame.DO_NOTHING_ON_CLOSE — Ignora el click
        */
        
        frameInicio.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frameInicio.setVisible(true);
    }    
}
