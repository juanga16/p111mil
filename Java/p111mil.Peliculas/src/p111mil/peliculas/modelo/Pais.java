/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.modelo;

import java.util.Date;
import java.util.List;

/**
 *
 * @author admin
 */
public class Pais {
    private int id;
    private String nombre;    
    private Date fechaCreacion;
    private List<Director> directores;
    private List<Actor> actores;
    private List<PeliculaPais> peliculasPais;
    
    public Pais() {
        
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }   

    public List<Director> getDirectores() {
        return directores;
    }

    public void setDirectores(List<Director> directores) {
        this.directores = directores;
    }    

    public Date getFechaCreacion() {
        return fechaCreacion;
    }

    public void setFechaCreacion(Date fechaCreacion) {
        this.fechaCreacion = fechaCreacion;
    }        

    public List<Actor> getActores() {
        return actores;
    }

    public void setActores(List<Actor> actores) {
        this.actores = actores;
    }

    public List<PeliculaPais> getPeliculasPais() {
        return peliculasPais;
    }

    public void setPeliculasPais(List<PeliculaPais> peliculasPais) {
        this.peliculasPais = peliculasPais;
    }        
}
