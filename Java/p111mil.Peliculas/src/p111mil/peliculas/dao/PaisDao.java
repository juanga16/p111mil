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
import p111mil.peliculas.modelo.Pais;

/**
 *
 * @author admin
 */
public class PaisDao {        
    
    public List<Pais> buscarTodos() {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Pais> query = builder.createQuery(Pais.class);
        Root<Pais> root = query.from(Pais.class);
        query.select(root);
        ArrayList<Pais> paises = (ArrayList<Pais>) session.createQuery(query).list();
        
        session.close();
        
        return paises;
    }
    
    public Pais buscarPorId(int id) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Pais> query = builder.createQuery(Pais.class);
        Root<Pais> root = query.from(Pais.class);
        query.select(root);
        query.where(builder.equal(root.get("id"), id));
        Pais pais = (Pais) session.createQuery(query).uniqueResult();
        
        session.close();
        
        return pais;
    }
       
    public void guardar(Pais pais) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        session.beginTransaction();        
        session.saveOrUpdate(pais);
        session.getTransaction().commit();
        
        session.close();
    }
    
    public void eliminar(int id) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        session.beginTransaction();        
        Pais pais = session.get(Pais.class, id);
        session.delete(pais);
        session.getTransaction().commit();

        session.close();
    }
}
