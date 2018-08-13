/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas;

import java.util.List;
import p111mil.peliculas.dao.ConfiguracionHibernate;
import p111mil.peliculas.dao.*;
import p111mil.peliculas.modelo.*;

/**
 *
 * @author Invitado
 */
public class P111milPeliculas {
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        ConfiguracionHibernate.configurar();        
        
        listarPaises();     
        imprimirPaisEstadosUnidos();
        //guardarNuevoPais();
        listarDirectores();
        listarPeliculas();
        
        ConfiguracionHibernate.cerrar();
    }
    
    private static void listarPaises() {
        PaisDao paisDao = new PaisDao();
        
        List<Pais> paises = paisDao.buscarTodos();
        
        System.out.println("Cantidad de paises: " + paises.size());
        for(Pais pais : paises) {
            System.out.println(pais.getId());
            System.out.println(pais.getNombre());
            System.out.println(pais.getDirectores().size());
            System.out.println(pais.getFechaCreacion());
        }
    }    
    
    private static void imprimirPaisEstadosUnidos() {
        PaisDao paisDao = new PaisDao();
        
        Pais estadosUnidos = paisDao.buscarPorNombre("Estados Unidos");
        
        System.out.println("Pais encontrado");
        if (estadosUnidos != null) {            
            System.out.println(estadosUnidos.getId());
            System.out.println(estadosUnidos.getNombre());
            System.out.println(estadosUnidos.getDirectores().size());
            System.out.println(estadosUnidos.getFechaCreacion());
        }
    }
    
    private static void guardarNuevoPais() {
        PaisDao paisDao = new PaisDao();
        
        Pais nuevoPais = new Pais();
        nuevoPais.setNombre("Canada");
        
        paisDao.guardar(nuevoPais);
    }    
    
    private static void listarDirectores() {
        DirectorDao directorDao = new DirectorDao();
        
        List<Director> directores = directorDao.buscarTodos();        
        
        System.out.println("Cantidad de directores: " + directores.size());
        for(Director director : directores) {
            System.out.println(director.getNombre());
            System.out.println(director.getApellido());
            System.out.println(director.getFechaNacimiento());
            System.out.println(director.getPais().getNombre());
            System.out.println(director.getPeliculas().size());
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
