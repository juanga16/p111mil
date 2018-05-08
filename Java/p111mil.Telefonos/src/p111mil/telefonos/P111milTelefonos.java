/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.telefonos;

import java.util.ArrayList;
import modelo.Telefono;
import modelo.TelefonoCelular;
import modelo.TelefonoFijo;
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
        
        TelefonoPublico telefonoParque = new TelefonoPublico(451234);
        TelefonoFijo telefonoCasa = new TelefonoFijo(421212);
        TelefonoFijo telefonoAbuela = new TelefonoFijo(6452312);
        
        System.out.println(telefonoParque);
        System.out.println(telefonoCasa);
        System.out.println(telefonoAbuela);        
        
        
        /*
        TelefonoPublico telefonoHospital = new TelefonoPublico(423456);        
        TelefonoCelular telefonoJuan = new TelefonoCelular(104567);
        TelefonoCelular telefonoGustavo = new TelefonoCelular(657123);
        
        ArrayList<Telefono> telefonos = new ArrayList<Telefono>();
        
        telefonos.add(telefonoHospital);
        telefonos.add(telefonoJuan);
        telefonos.add(telefonoGustavo);
        
        for(Telefono telefono : telefonos) {
            telefono.llamar(421012);
        }
        
        telefonoJuan.setVibracion(true);
        for(Telefono telefono : telefonos) {
            telefono.sonar();
        }
        */
        
        /*
        telefonoJuan.setVibracion(true);
        
        telefonoJuan.sonar();
        telefonoGustavo.sonar();
                
        telefonoJuan.getCantidadTelefonos();
        
        System.out.println(Telefono.getCantidadTelefonos());
        
        TelefonoPublico.setCentavosPorPulso(50);
        */
        
        String nombre1 = "Juan";
        String nombre2 = "Valentina";
        String nombre3 = "Juan";
        
        /*
        System.out.println(nombre1.equals(nombre2));
        System.out.println(nombre1.equals(nombre3));
        */
        
        TelefonoCelular telefonoCelular1 = new TelefonoCelular(123);
        TelefonoCelular telefonoCelular2 = new TelefonoCelular(456);
        TelefonoCelular telefonoCelular3 = new TelefonoCelular(123);
        TelefonoCelular telefonoCelular4 = telefonoCelular1;
        
        System.out.println(telefonoCelular1.equals(telefonoCelular2));
        System.out.println(telefonoCelular1.equals(telefonoCelular3));
        System.out.println(telefonoCelular1.equals(telefonoCelular4));
        System.out.println(telefonoCelular1.equals(nombre1));
    }    
}
