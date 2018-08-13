/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.dao;

import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistry;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;

/**
 *
 * @author Invitado
 */
public class ConfiguracionHibernate {
    private static SessionFactory sessionFactory;
    private static ServiceRegistry serviceRegistry;

    public static SessionFactory getSessionFactory() {
        return sessionFactory;
    }

    public static void configurar() {
        Configuration config = new Configuration();        
        
        //serviceRegistry = new StandardServiceRegistryBuilder().applySettings(config.getProperties()).build();                
        
        serviceRegistry = new StandardServiceRegistryBuilder()
			.configure("p111mil/peliculas/hibernate/hibernate.cfg.xml") // configures settings from hibernate.cfg.xml
			.build();
        
        sessionFactory = config.buildSessionFactory(serviceRegistry);
    }
    
    public static void cerrar() {
        sessionFactory.close();
    }    
}
