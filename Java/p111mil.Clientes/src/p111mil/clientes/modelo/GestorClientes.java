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
    private ArrayList<Cliente> clientes = new ArrayList<Cliente>();
    
    public void agregarCliente(Cliente cliente) {
        clientes.add(cliente);
    }
    
    /**
     * Retorna el cliente con mayor promedio de facturacion
     * @return 
     */
    public Cliente obtenerClienteConMayorPromedio() {
        double mayorPromedio = 0;
        Cliente clienteConMayorPromedio = null;
        
        for (Cliente cliente : clientes) {
            double promedio = cliente.getPromedioFacturacion();
            
            if (promedio > mayorPromedio) {
                mayorPromedio = promedio;
                clienteConMayorPromedio = cliente;
            }
        }
        
        return clienteConMayorPromedio;        
    }
    
    /**
     * Ordena la lista de mayor a menor segun el total facturado.
     * Devuelve los primeros tres elementos
     * @return 
     */
    public List<Cliente> obtenerTresClientesConMayorFacturacion() {
        // Duplicamos la lista de clientes
        ArrayList<Cliente> clientesOrdenados = (ArrayList<Cliente>) clientes.clone();
        int tamanio = clientesOrdenados.size();
        
        for(int i = 0; i < tamanio - 1; i++) {
            for(int j = 1; j < tamanio - i; j++) {
                
                if (clientesOrdenados.get(j - 1).getTotalFacturado() < clientesOrdenados.get(j).getTotalFacturado()) {
                    // Guardo en una variable temporal el cliente antes de cambiarlo de posicion
                    // El metodo set sirve para insertar un elemento en una posicion especifica reemplazando al existente
                    Cliente clienteTemporal = clientesOrdenados.get(j - 1);
                    clientesOrdenados.set(j - 1, clientesOrdenados.get(j));
                    clientesOrdenados.set(j, clienteTemporal);
                }                
            }
        }
        
        // De la lista ordenada a partir de la posicion 0 tomo los primeros 3 elementos
        return clientesOrdenados.subList(0, 3);
    }
    
    /**
     * Devuelve la fecha del cliente con mayor antiguedad
     * @return 
     */
    public Date obtenerFechaUltimoCliente() {
        Date fechaUltimoCliente = null;
        
        // Las fechas en java se comparan con los metodos: after (posterior), before (anterior) o equals
        // f1.before(f2) -> estoy preguntando si f1 es anterior a f2
        for(Cliente cliente : clientes) {
            if (fechaUltimoCliente == null || fechaUltimoCliente.after(cliente.getFechaAlta())) {
                fechaUltimoCliente = cliente.getFechaAlta();
            }
        }
        
        return fechaUltimoCliente;
    }
    
    /**
     * Recorre la lista y si existe un cliente con ese nombre lo retorna
     * @param nombreCliente
     * @return 
     */
    public Cliente buscarPorNombre(String nombreCliente) {
        Iterator<Cliente> iterator = clientes.iterator();
        
        // Nunca olvidar de preguntar si hay elemento siguiente        
        while(iterator.hasNext()) {
            Cliente cliente = iterator.next();
            
            if (cliente.getNombre().toLowerCase().equals(nombreCliente.toLowerCase())) {
                return cliente;
            }
        }
        
        return null;
    }    
}