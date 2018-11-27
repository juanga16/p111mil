/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.modelo;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Invitado
 */
public abstract class EtapaMundial {
    private String descripcion;
    private List<Partido> partidos;

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }
    
    public EtapaMundial() {
        this.partidos = new ArrayList<Partido>();
    }

    public List<Partido> getPartidos() {
        return partidos;
    }

    public void setPartidos(List<Partido> partidos) {
        this.partidos = partidos;
    }
    
    public void addPartido(Partido partido) {
        this.partidos.add(partido);
    }
    
    public abstract List<Equipo> getEquiposQueAvanzan();    
}
