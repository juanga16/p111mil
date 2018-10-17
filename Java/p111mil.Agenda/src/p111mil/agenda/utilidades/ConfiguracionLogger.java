/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.agenda.utilidades;

/**
 *
 * @author Invitado
 */
public class ConfiguracionLogger {
    private static final org.apache.log4j.Logger LOGGER = org.apache.log4j.Logger.getLogger("Agenda");    
    
    public static void info(String message) {
        LOGGER.info(message);
    }
    
    public static void debug(Exception exception) {
        LOGGER.debug(exception);
    }
}
