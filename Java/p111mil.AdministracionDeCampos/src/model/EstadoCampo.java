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
public class EstadoCampo {
    private int idEstadoCampo;
    private String descripcion;
    private List<Campo> campos;

    public EstadoCampo() {
        campos = new ArrayList<Campo>();
    }
    
    public int getIdEstadoCampo() {
        return idEstadoCampo;
    }

    public void setIdEstadoCampo(int idEstadoCampo) {
        this.idEstadoCampo = idEstadoCampo;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public List<Campo> getCampos() {
        return campos;
    }

    public void setCampos(List<Campo> campos) {
        this.campos = campos;
    }
    
   @Override
   public String toString() {
       return this.getDescripcion();
   }
}
