/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.clientes;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.List;
import p111mil.clientes.modelo.*;

/**
 *
 * @author PC-MAESTRO
 */
public class P111milClientes {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Calendar calendar = new GregorianCalendar(1995, 9, 22);
        Cliente coto = new Cliente();
        coto.setFechaAlta(calendar.getTime());
        coto.setCantidadFacturas(50);
        coto.setTotalFacturado(125456.95);
        coto.setNombre("Coto");
        
        calendar = new GregorianCalendar(2004, 3, 20);
        Cliente carrefour = new Cliente();
        carrefour.setFechaAlta(calendar.getTime());
        carrefour.setCantidadFacturas(39);
        carrefour.setTotalFacturado(97585d);
        carrefour.setNombre("Carrefour");
        
        calendar = new GregorianCalendar(2007, 11, 5);
        Cliente dia = new Cliente();
        dia.setFechaAlta(calendar.getTime());
        dia.setCantidadFacturas(15);
        dia.setTotalFacturado(57135.22);
        dia.setNombre("Dia");
        
        calendar = new GregorianCalendar(2013, 5, 17);
        Cliente wallmart = new Cliente();
        wallmart.setFechaAlta(calendar.getTime());
        wallmart.setCantidadFacturas(10);
        wallmart.setTotalFacturado(195123d);
        wallmart.setNombre("Wallmart");
        
        GestorClientes gestorClientes = new GestorClientes();
        
        gestorClientes.agregarCliente(coto);
        gestorClientes.agregarCliente(wallmart);
        gestorClientes.agregarCliente(dia);
        gestorClientes.agregarCliente(carrefour);
        
        System.out.println("Cliente con mayor promedio:");
        System.out.println(gestorClientes.obtenerClienteConMayorPromedio());
        
        System.out.println("Fecha del cliente mas antiguo:");
        System.out.println(gestorClientes.obtenerFechaUltimoCliente());
        
        System.out.println("Buscar cliente que se llama 'Coto'");
        System.out.println(gestorClientes.buscarPorNombre("coto"));
        
        System.out.println("Buscar cliente que se llama 'Oriente'");
        Cliente oriente = gestorClientes.buscarPorNombre("oriente");
        if (oriente != null) {
            System.out.println(oriente);
        }
        
        List<Cliente> clientesConMayorFacturacion = gestorClientes.obtenerTresClientesConMayorFacturacion();
        int orden = 1;
        
        for(Cliente cliente : clientesConMayorFacturacion) {
            System.out.println("Cliente: " + cliente.getNombre());
            System.out.println("Orden: " + orden);
            System.out.println("Total facturacion: " + cliente.getTotalFacturado());
            System.out.println("--------------------------------------");
            
            orden = orden + 1;
        }
        
        Cliente cooperativaObrera1 = new Cliente();
        cooperativaObrera1.setNombre("Cooperativa Obrera");
        Cliente cooperativaObrera2 = new Cliente();
        cooperativaObrera2.setNombre("Cooperativa Obrera");
        System.out.println("Ejemplo de equals");
        System.out.println(cooperativaObrera1.equals(cooperativaObrera2));
    }    
}
