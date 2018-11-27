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
public class Equipo {
    private String nombre;
    private List<Partido> partidosJugados;

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public List<Partido> getPartidosJugados() {
        return partidosJugados;
    }

    public void setPartidosJugados(List<Partido> partidosJugados) {
        this.partidosJugados = partidosJugados;
    }

    public Equipo(String nombre) {
        this.partidosJugados = new ArrayList<Partido>();
        this.nombre = nombre;
    }    
}