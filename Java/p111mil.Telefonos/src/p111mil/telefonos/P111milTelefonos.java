/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.telefonos;

import java.util.ArrayList;
import modelo.Telefono;
import modelo.TelefonoCelular;
import modelo.TelefonoPublico;

/**
 *
 * @author admin
 */
public class P111milTelefonos {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        TelefonoPublico telefonoHospital = new TelefonoPublico(423456);
        TelefonoCelular telefonoJuan = new TelefonoCelular(104567);
        TelefonoCelular telefonoGustavo = new TelefonoCelular(657123);
        
        ArrayList<Telefono> telefonos = new ArrayList<Telefono>();
        
        telefonos.add(telefonoHospital);
        telefonos.add(telefonoJuan);
        telefonos.add(telefonoGustavo);
        
        for(Telefono telefono : telefonos) {
            telefono.llamar(421012);
            System.out.println(telefono);
        }
        
        telefonoJuan.setVibracion(true);
        
        telefonoJuan.sonar();
        telefonoGustavo.sonar();
                
        System.out.println(Telefono.getCantidadTelefonos());
    }    
}
