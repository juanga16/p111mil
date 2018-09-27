/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.agenda.dao;

import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;

/**
 *
 * @author Invitado
 */
public class ConfiguracionHibernate {
    private static SessionFactory sessionFactory;
    
    /**
     * El sessionFactory se utiliza cada vez que 
     * leemos o escribimos en la base de datos
     * @return 
     */
    public static SessionFactory getSessionFactory() {
        return sessionFactory;
    }
    
    /**
     * Este metodo se ejecuta una sola vez,
     * cuando se inicia el programa en el metodo main
     */
    public static void configurar() {
        Configuration configuration = new Configuration();        
        
        // Es importante revisar y configurar la correcta ubicacion del archivo hibernate.cfg.xml
        ServiceRegistry serviceRegistry = new StandardServiceRegistryBuilder().configure("p111mil/agenda/hibernate/hibernate.cfg.xml").build();
        
        sessionFactory = configuration.buildSessionFactory(serviceRegistry);        
    }
    
    /**
     * Este metodo se llama en el momento en el que se cierra el programa
     */
    public static void cerrar() {
        sessionFactory.close();
    }
    
    
    
}
