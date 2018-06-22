/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package juanga.p111mil.hibernatepeliculas.model;

import java.util.ArrayList;
import java.util.List;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;


/**
 *
 * @author admin
 */
public class Main {
    private static SessionFactory sessionFactory;
    private static ServiceRegistry serviceRegistry;
        
    public static void main(String[] args) {
        Configuration config = new Configuration();
        
        config.configure();
	config.addAnnotatedClass(Pais.class);
	config.addResource("Pais.hbm.xml");
			
        serviceRegistry = new StandardServiceRegistryBuilder().applySettings(config.getProperties()).build();
        sessionFactory = config.buildSessionFactory(serviceRegistry);
		
	listarPaises();	
        insertarPais();
    }
    
    private static void listarPaises() {
        Session session = sessionFactory.openSession();        
        session.beginTransaction();
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Pais> query = builder.createQuery(Pais.class);
        Root<Pais> root = query.from(Pais.class);
        query.select(root);
        query.orderBy(builder.desc(root.get("nombre")));
        ArrayList<Pais> paises = (ArrayList<Pais>) session.createQuery(query).list();
        
        System.out.println("Cantidad de paises: " + paises.size());
        for(Pais pais : paises) {
            System.out.println(pais.getNombre());
        }
        
        session.getTransaction().commit();
        session.close();        
    }
    
    private static void insertarPais() {
        Pais pais = new Pais();
        pais.setNombre("Zimbawe");
        
        Session session = sessionFactory.openSession();
        session.beginTransaction();
        session.save(pais);
        session.getTransaction().commit();
        session.close();
    }
}
