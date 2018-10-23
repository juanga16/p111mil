/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.clientes.modelo;

import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

/**
 *
 * @author PC-MAESTRO
 */
public class GestorClientes {
    ArrayList<Cliente> clientes = new ArrayList<Cliente>();
    
    public void agregarCliente(Cliente cliente) {
        clientes.add(cliente);
    }
    
    public Cliente obtenerClienteConMayorPromedio() {
        double mayorPromedio = 0;
        Cliente clienteConMayorPromedio = null;
        
        for (Cliente cliente : clientes) {
            double promedio = cliente.getTotalFacturado() / cliente.getCantidadFacturas();
            
            if (promedio > mayorPromedio) {
                mayorPromedio = promedio;
                clienteConMayorPromedio = cliente;
            }
        }
        
        return clienteConMayorPromedio;        
    }
    
    public List<Cliente> obtenerTresClientesConMayorFacturacion() {
        ArrayList<Cliente> clientesOrdenados = (ArrayList<Cliente>) clientes.clone();
        
        for(int i = 1; i < clientesOrdenados.size(); i++) {
            for(int j = 0; j < clientesOrdenados.size() - 1; j++) {
                if (clientesOrdenados.get(j).getTotalFacturado() > clientesOrdenados.get(i).getTotalFacturado()) {
                    Cliente clienteTemporal = clientesOrdenados.get(j);
                    clientesOrdenados.set(j, clientesOrdenados.get(j + 1));
                    clientesOrdenados.set(j + 1, clienteTemporal);                    
                }
            }
        }
        
        return clientesOrdenados.subList(0, 2);
    }
    
    public Date obtenerFechaUltimoCliente() {
        Date fechaUltimoCliente = null;
        
        for(Cliente cliente : clientes) {
            if (fechaUltimoCliente == null || fechaUltimoCliente.after(cliente.getFechaAlta())) {
                fechaUltimoCliente = cliente.getFechaAlta();
            }
        }
        
        return fechaUltimoCliente;
    }
    
    public Cliente buscarPorNombre(String nombreCliente) {
        Iterator<Cliente> iterator = clientes.iterator();
        
        while(iterator.hasNext()) {
            Cliente cliente = iterator.next();
            
            if (cliente.getNombre().equals(nombreCliente)) {
                return cliente;
            }
        }
        
        return null;
    }       
}