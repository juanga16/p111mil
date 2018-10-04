/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.agenda.dao;

import java.util.ArrayList;
import java.util.List;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Order;
import javax.persistence.criteria.Root;
import org.hibernate.Session;
import p111mil.agenda.modelo.Contacto;

/**
 *
 * @author Invitado
 */
public class ContactoDao {
    public void guardar(Contacto contacto) {                      
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        session.beginTransaction();        
        session.saveOrUpdate(contacto);        
        session.getTransaction().commit();
        
        session.close();        
    }   
    
    public List<Contacto> buscarTodos() {
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
        
        return contactos;
    }    
}
