/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.dao;

import java.util.ArrayList;
import java.util.List;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;
import org.hibernate.Session;
import p111mil.peliculas.modelo.Pelicula;

/**
 *
 * @author admin
 */
public class PeliculaDao extends BaseDao {
    
    public PeliculaDao() {
        super();
    }
    
    public List<Pelicula> buscarTodas() {
        Session session = getSessionFactory().openSession();        
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Pelicula> query = builder.createQuery(Pelicula.class);
        Root<Pelicula> root = query.from(Pelicula.class);
        query.select(root);
        ArrayList<Pelicula> peliculas = (ArrayList<Pelicula>) session.createQuery(query).list();
        
        session.close();
        
        return peliculas;
    }    
}
