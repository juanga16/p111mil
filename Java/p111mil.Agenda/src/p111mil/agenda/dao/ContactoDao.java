/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.agenda.dao;

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
}
