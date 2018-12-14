/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package model;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 *
 * @author admin
 */
public class Campo {
    private int idCampo;
    private String nombre;
    private int superficie;
    private List<Lote> lotes;
    private Date fechaCreacion;
    private EstadoCampo estadoCampo;

    public Campo() {
        lotes = new ArrayList<Lote>();
    }
    
    public int getIdCampo() {
        return idCampo;
    }

    public void setIdCampo(int idCampo) {
        this.idCampo = idCampo;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public int getSuperficie() {
        return superficie;
    }

    public void setSuperficie(int superficie) {
        this.superficie = superficie;
    }

    public List<Lote> getLotes() {
        return lotes;
    }

    public void setLotes(List<Lote> lotes) {
        this.lotes = lotes;
    }

    public Date getFechaCreacion() {
        return fechaCreacion;
    }

    public void setFechaCreacion(Date fechaCreacion) {
        this.fechaCreacion = fechaCreacion;
    }
    
    public EstadoCampo getEstadoCampo() {
        return estadoCampo;
    }

    public void setEstadoCampo(EstadoCampo estadoCampo) {
        this.estadoCampo = estadoCampo;
    }    
}
