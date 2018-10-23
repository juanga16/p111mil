/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.clientes.modelo;

import java.util.Date;

/**
 *
 * @author PC-MAESTRO
 */
public class Cliente {
    private String nombre;
    private Date fechaAlta;
    private Double totalFacturado;
    private int cantidadFacturas;

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public Date getFechaAlta() {
        return fechaAlta;
    }

    public void setFechaAlta(Date fechaAlta) {
        this.fechaAlta = fechaAlta;
    }

    public Double getTotalFacturado() {
        return totalFacturado;
    }

    public void setTotalFacturado(Double totalFacturado) {
        this.totalFacturado = totalFacturado;
    }

    public int getCantidadFacturas() {
        return cantidadFacturas;
    }

    public void setCantidadFacturas(int cantidadFacturas) {
        this.cantidadFacturas = cantidadFacturas;
    }       
}
