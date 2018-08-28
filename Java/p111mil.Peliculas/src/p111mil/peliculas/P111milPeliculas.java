/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas;

import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.List;
import p111mil.peliculas.dao.ConfiguracionHibernate;
import p111mil.peliculas.dao.*;
import p111mil.peliculas.modelo.*;
import p111mil.peliculas.utilidades.ConfiguracionLogger;

/**
 *
 * @author Invitado
 */
public class P111milPeliculas {
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // Invoco el metodo configurar una sola vez al comienzo de la ejecucion del programa        
        // Se van a leer los parametros de configuracion de hibernate
        ConfiguracionHibernate.configurar();
        ConfiguracionLogger.configurar();
        
        //crearEliminarUnaPelicula();
        listarPaises();
        //listarPeliculas();

        // Invoco el cerrar justo antes de salir del programa
        // para liberar los recursos de la conexion con la base de datos
        ConfiguracionHibernate.cerrar();
    }
    
    private static void crearEliminarUnaPelicula() {
        PaisDao paisDao = new PaisDao();
        PeliculaDao peliculaDao = new PeliculaDao();
        DirectorDao directorDao = new DirectorDao();
        ActorDao actorDao = new ActorDao();
        
        Pais nuevoPais = new Pais();
        nuevoPais.setNombre("Italia");         
        paisDao.guardar(nuevoPais);
        
        Director nuevoDirector = new Director();
        nuevoDirector.setNombre("Roberto");
        nuevoDirector.setApellido("Benigni");
        nuevoDirector.setGenero("M");
        nuevoDirector.setFechaNacimiento(new GregorianCalendar(1952, Calendar.OCTOBER, 27).getTime());
        nuevoDirector.setPais(nuevoPais);
        directorDao.guardar(nuevoDirector);
        
        Actor nuevoActor1 = new Actor();
        nuevoActor1.setNombre("Roberto");
        nuevoActor1.setApellido("Benigni");
        nuevoActor1.setGenero("M");
        nuevoActor1.setFechaNacimiento(new GregorianCalendar(1952, Calendar.OCTOBER, 27).getTime());
        nuevoActor1.setPais(nuevoPais);
        actorDao.guardar(nuevoActor1);
        
        Actor nuevoActor2 = new Actor();
        nuevoActor2.setNombre("Nicoletta");
        nuevoActor2.setApellido("Braschi");
        nuevoActor2.setGenero("F");
        nuevoActor2.setFechaNacimiento(new GregorianCalendar(1960, Calendar.APRIL, 19).getTime());
        nuevoActor2.setPais(nuevoPais);
        actorDao.guardar(nuevoActor2);        
        
        Pelicula nuevaPelicula = new Pelicula();
        nuevaPelicula.setTitulo("La vita e bella");
        nuevaPelicula.setAnio(1997);
        nuevaPelicula.setPuntuacion(8.6f);
        nuevaPelicula.setDirector(nuevoDirector);
        nuevaPelicula.getActores().add(nuevoActor1);
        nuevaPelicula.getActores().add(nuevoActor2);
        
         // Actuar
         peliculaDao.guardar(nuevaPelicula);
        
        // Eliminar
        actorDao.eliminar(nuevoActor1.getId());
        actorDao.eliminar(nuevoActor2.getId());
        peliculaDao.eliminar(nuevaPelicula.getId());
        directorDao.eliminar(nuevoDirector.getId());
        paisDao.eliminar(nuevoPais.getId());        
    }
    
    private static void listarPaises() {
        PaisDao paisDao = new PaisDao();
        
        List<Pais> paises = paisDao.buscarTodos();

        for(Pais pais : paises) {
            System.out.println(pais.getId());
            System.out.println(pais.getNombre());
            System.out.println(pais.getFechaCreacion());
        }
    }    
    
    private static void listarPeliculas() {
        PeliculaDao peliculaDao = new PeliculaDao();
        
        List<Pelicula> peliculas = peliculaDao.buscarTodas();
        
        System.out.println("Cantidad de peliculas: " + peliculas.size());
        for(Pelicula pelicula : peliculas) {
            System.out.println(pelicula.getId());
            System.out.println(pelicula.getTitulo());
            System.out.println(pelicula.getPuntuacion());
            System.out.println(pelicula.getAnio());
            System.out.println(pelicula.getDirector());
            System.out.println(pelicula.getPaises().size());
            
            for(Pais pais : pelicula.getPaises()) {
                System.out.println("--> " + pais.getNombre());                
            }
            
            System.out.println(pelicula.getActores().size());
            for(Actor actor : pelicula.getActores()) {
                System.out.println("--> " + actor);                
            }
            
            System.out.println(pelicula.getGeneros().size());
            for(Genero genero : pelicula.getGeneros()) {
                System.out.println("--> " + genero.getNombre());                
            }
            
            System.out.println(pelicula.getFechaCreacion());
            System.out.println("---------------------------------------------");
        }
    }    
}
