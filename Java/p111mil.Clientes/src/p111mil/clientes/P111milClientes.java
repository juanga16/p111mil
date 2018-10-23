/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.clientes;

import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import p111mil.clientes.modelo.Cliente;

/**
 *
 * @author PC-MAESTRO
 */
public class P111milClientes {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Calendar calendar = new GregorianCalendar(2018, 9, 22);
        Cliente coto = new Cliente();
        coto.setFechaAlta(calendar.getTime());
        
        System.out.println(coto.getFechaAlta());
        
        System.out.println(new Date());
    }    
}
