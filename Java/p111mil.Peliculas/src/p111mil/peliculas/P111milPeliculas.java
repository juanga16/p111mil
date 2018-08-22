/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas;

import java.util.Arrays;
import java.util.Date;
import java.util.List;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;
import org.hibernate.Session;
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
        
        PaisDao paisDao = new PaisDao();
        PeliculaDao peliculaDao = new PeliculaDao();
        
        /*
        List<Pais> paises = paisDao.buscarTodos();
        
        for(Pais pais : paises) {        
            System.out.println(pais.getNombre());
        }
                
        Pais pais = paisDao.buscarPorId(2);
        
        if (pais != null) {
            System.out.println(pais.getNombre());
        }
        
        Pais nuevoPais = new Pais();
        nuevoPais.setNombre("Rusia");
        paisDao.guardar(nuevoPais);
        
        Pais actualizarPais = new Pais();
        actualizarPais.setId(1);
        actualizarPais.setNombre("Argentina");
        paisDao.guardar(actualizarPais);
        */
        
        /*        
        paisDao.eliminar(4);
        */
        
        /*
        PeliculaDao peliculaDao = new PeliculaDao();
        
        Pelicula metegol = new Pelicula();
        
        Director campanella = new Director();
        campanella.setId(1);
        
        Genero comedia = new Genero();
        comedia.setId(4);
        
        Pais argentina = new Pais();
        argentina.setId(1);
        
        Actor darin = new Actor();
        darin.setId(1);
        
        Actor francella = new Actor();
        francella.setId(2);
        
        metegol.setTitulo("Metegol");
        metegol.setPuntuacion(6.6f);
        metegol.setAnio(2013);
        metegol.setFechaCreacion(new Date());
        metegol.setDirector(campanella);
        metegol.setGeneros(Arrays.asList(comedia));
        metegol.setPaises(Arrays.asList(argentina));
        metegol.setActores(Arrays.asList(darin, francella));
        
        peliculaDao.guardar(metegol);
        */
                
        peliculaDao.eliminar(5);
        
        ConfiguracionHibernate.cerrar();
    }
    
    private static void listarPaises() {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Pais> query = builder.createQuery(Pais.class);
        Root<Pais> root = query.from(Pais.class);
        query.select(root);
        // Ordeno por nombre
        query.orderBy(builder.asc(root.get("nombre")));
        // Filtro los que comienzan con I
        query.where(builder.like(root.get("nombre"), "I%"));
        List<Pais> paises = (List<Pais>) session.createQuery(query).list();
        
        for(Pais pais : paises) {
            System.out.println(pais.getId());
            System.out.println(pais.getNombre());
            System.out.println(pais.getFechaCreacion());
        }
        
        session.close();
    }
    
    private static void listarPaises2() {
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
