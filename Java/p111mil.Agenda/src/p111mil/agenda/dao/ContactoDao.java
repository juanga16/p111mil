/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.agenda.dao;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Order;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import org.hibernate.Session;
import p111mil.agenda.modelo.Contacto;
import p111mil.agenda.utilidades.ConfiguracionLogger;

/**
 *
 * @author Invitado
 */
public class ContactoDao {    
    
    public void guardar(Contacto contacto) {                      
        ConfiguracionLogger.getLogger().log(Level.INFO, "Comenzando");                
        
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        
        session.beginTransaction();        
        
        try {
            session.saveOrUpdate(contacto);        
            session.getTransaction().commit();        
        } catch(Exception exception) {
            session.getTransaction().rollback();            
            ConfiguracionLogger.getLogger().log(Level.SEVERE, exception.getMessage());
            ConfiguracionLogger.getLogger().log(Level.SEVERE, exception.getLocalizedMessage());
            ConfiguracionLogger.getLogger().log(Level.SEVERE, exception.getStackTrace().toString());
        }
        session.close();        
        
        ConfiguracionLogger.getLogger().log(Level.INFO, "Finalizando");
    }   
    
    public List<Contacto> buscarTodos() {
        ConfiguracionLogger.getLogger().log(Level.INFO, "Comenzando");
        
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();                
        ArrayList<Contacto> contactos = new ArrayList<Contacto>();
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Contacto> query = builder.createQuery(Contacto.class);
        Root<Contacto> root = query.from(Contacto.class);
        query.select(root);
        // Para que ordene por dos campos
        List<Order> orders = new ArrayList<Order>();
        orders.add(builder.asc(root.get("apellido")));
        orders.add(builder.asc(root.get("nombre")));        
        query.orderBy(orders);
        // Ejecuto la consulta y guardo el resultado en una lista de Pais
        contactos = (ArrayList<Contacto>) session.createQuery(query).list();
            
        session.close();
        ConfiguracionLogger.getLogger().log(Level.INFO, "Finalizando");                
                
        return contactos;
    }    
    
    public List<Contacto> buscarPor(String criterio) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();                
        ArrayList<Contacto> contactos = new ArrayList<Contacto>();
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Contacto> query = builder.createQuery(Contacto.class);
        Root<Contacto> root = query.from(Contacto.class);
        query.select(root);
        // Para que ordene por dos campos
        List<Order> orders = new ArrayList<Order>();
        orders.add(builder.asc(root.get("apellido")));
        orders.add(builder.asc(root.get("nombre")));        
        query.orderBy(orders);
        
        // Filtro segun el criterio
        criterio = "%" + criterio + "%";
        Predicate predicate = builder.or(builder.like(root.get("nombre"), criterio), builder.like(root.get("apellido"), criterio));
        query.where(predicate);  
        
        // Ejecuto la consulta y guardo el resultado en una lista de Pais
        contactos = (ArrayList<Contacto>) session.createQuery(query).list();
            
        session.close();
        
        return contactos;        
    }
    
    public void eliminar(int id) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        session.beginTransaction();
        // Busco el contacto por el id
        Contacto contacto = session.get(Contacto.class, id);
         
        // Elimino fisicamente el contacto
        session.delete(contacto);
        session.getTransaction().commit();

        session.close();
    }

    public Contacto buscarPorId(int id) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();                
        Contacto contacto = session.get(Contacto.class, id);        
        session.close();
        
        return contacto;
    }
}
