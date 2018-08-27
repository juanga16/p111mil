/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.utilidades;

import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

/**
 *
 * @author admin
 */
public class ConfiguracionLogger {
    private final static Logger LOGGER = Logger.getLogger("Peliculas");
    
    public static void configurar() {    
        try {
            FileHandler fileHandler = new FileHandler("Peliculas.log", true);
            fileHandler.setFormatter(new SimpleFormatter());
        LOGGER.addHandler(fileHandler);
        } catch(Exception exception) {
            System.out.println(exception.getStackTrace());
        }
    }
}
