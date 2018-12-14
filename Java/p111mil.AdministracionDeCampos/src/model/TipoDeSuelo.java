/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package model;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author admin
 */
public class TipoDeSuelo {
    private int idTipoDeSuelo;
    private String descripcion;
    private List<Lote> lotes;

    public TipoDeSuelo() {
        lotes = new ArrayList<Lote>();
    }
        
    public int getIdTipoDeSuelo() {
        return idTipoDeSuelo;
    }

    public void setIdTipoDeSuelo(int idTipoDeSuelo) {
        this.idTipoDeSuelo = idTipoDeSuelo;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public List<Lote> getLotes() {
        return lotes;
    }

    public void setLotes(List<Lote> lotes) {
        this.lotes = lotes;
    }
    
    @Override
    public String toString() {
       return this.getDescripcion();
    }    
}
