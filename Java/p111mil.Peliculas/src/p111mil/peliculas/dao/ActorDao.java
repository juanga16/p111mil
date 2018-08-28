/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.dao;

import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;
import org.hibernate.Session;
import p111mil.peliculas.modelo.Actor;
import p111mil.peliculas.modelo.Pelicula;

/**
 *
 * @author admin
 */
public class ActorDao {                
    
    private final static Logger LOGGER = Logger.getLogger("Peliculas");
    
    public Actor buscarPorId(int id) {                
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Actor> query = builder.createQuery(Actor.class);
        Root<Actor> root = query.from(Actor.class);
        query.select(root);
        query.where(builder.equal(root.get("id"), id));
        Actor actor = (Actor) session.createQuery(query).uniqueResult();
        
        session.close();
        
        return actor;
    }
    
    public void guardar(Actor actor) {                      
        LOGGER.log(Level.INFO, "Guardando actor");
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        try {
            session.beginTransaction();        
            session.saveOrUpdate(actor);        
            session.getTransaction().commit();
            LOGGER.log(Level.INFO, "Guardado actor: {0}", actor.getId());
        } catch(Exception exception) {
            session.getTransaction().rollback();
            LOGGER.log(Level.SEVERE, exception.getMessage());
        } finally {
            session.close();
        }               
    }
    
    public void eliminar(int id) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        session.beginTransaction();        
        Actor actor = session.get(Actor.class, id);
         
        for(Pelicula pelicula : actor.getPeliculas()) {            
            pelicula.getActores().remove(actor);        
        }
        
        actor.getPeliculas().clear();
        actor.getPais().getActores().remove(actor);
        
        session.saveOrUpdate(actor);                                
        session.delete(actor);                                        
        session.getTransaction().commit();

        session.close();
    }
}
