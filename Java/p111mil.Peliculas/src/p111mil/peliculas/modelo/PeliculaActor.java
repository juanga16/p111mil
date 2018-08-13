/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.modelo;

/**
 *
 * @author admin
 */
public class PeliculaActor {
    private Pelicula Pelicula;
    private Actor Actor;
    
    public PeliculaActor() {
        
    }

    public Pelicula getPelicula() {
        return Pelicula;
    }

    public void setPelicula(Pelicula Pelicula) {
        this.Pelicula = Pelicula;
    }

    public Actor getActor() {
        return Actor;
    }

    public void setActor(Actor Actor) {
        this.Actor = Actor;
    }        
}
