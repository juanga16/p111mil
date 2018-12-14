/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dao;

import hibernate.ConfiguracionHibernate;
import java.util.Optional;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import model.Campo;
import org.apache.log4j.Logger;
import org.hibernate.Session;

/**
 *
 * @author admin
 */
public class CampoDao {
    private static final Logger LOGGER = org.apache.log4j.Logger.getLogger("AdministracionDeCampos");
    
    /**
     * Inserta un nuevo campo y sus lotes en la base de datos
     * @param campo 
     */
    public void guardar(Campo campo) {                      
        LOGGER.info("Comenzando");
        
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();
        session.beginTransaction();        
        
        try {
            session.saveOrUpdate(campo);        
            session.getTransaction().commit();        
        } catch(Exception exception) {
            LOGGER.error("Excepcion:", exception);
        }
        
        session.close();                
        LOGGER.info("Finalizando");
    }   
    
    /**
     * Retorna verdadero si ya existe un campo con ese mismo nombre
     * @param nombre
     * @return boolean
     */
    public boolean existeConMismoNombre(String nombre) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();                        
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Campo> query = builder.createQuery(Campo.class);
        Root<Campo> root = query.from(Campo.class);
        query.select(root);
        
        Predicate predicate = builder.equal(root.get("nombre"), nombre);
        query.where(predicate);  
        
        // Ejecuto la consulta y guardo el resultado en un Optional
        Optional<Campo> campo = session.createQuery(query).uniqueResultOptional();
            
        session.close();
        
        return campo.isPresent();
    }    
}