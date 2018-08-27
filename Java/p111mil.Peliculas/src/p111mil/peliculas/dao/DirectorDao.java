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
import p111mil.peliculas.modelo.Director;

/**
 *
 * @author Invitado
 */
public class DirectorDao {
    
    public List<Director> buscarTodos() {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Director> query = builder.createQuery(Director.class);
        Root<Director> root = query.from(Director.class);
        query.select(root);
        ArrayList<Director> directores = (ArrayList<Director>) session.createQuery(query).list();
        
        session.close();
        
        return directores;
    }
            
    public void guardar(Director director) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        session.beginTransaction();        
        session.saveOrUpdate(director);        
        session.getTransaction().commit();

        session.close();
    }
    
    public void eliminar(int id) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        Director director = session.get(Director.class, id);
        
        if (director != null)
        {
            session.beginTransaction();                     
            session.delete(director);
            session.getTransaction().commit();            
        }
        
        session.close();
    }
}
