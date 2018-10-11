/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.agenda.utilidades;

import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

/**
 *
 * @author Invitado
 */
public class ConfiguracionLogger {
    private final static Logger LOGGER = Logger.getLogger("Agenda");
    
    public static void configurar() {    
        try {
            // Estoy diciendo que voy a loguear en un archivo de texto y con el parametro true significa que se agrega la informacion al final
            FileHandler fileHandler = new FileHandler("Agenda.log", true);
            fileHandler.setFormatter(new SimpleFormatter());
            LOGGER.addHandler(fileHandler);
        } catch(Exception exception) {
            System.out.println(exception.getStackTrace());
        }
    } 
    
    public static Logger getLogger() {
        return LOGGER;    
    }
}
