/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dao;

import hibernate.ConfiguracionHibernate;
import java.util.ArrayList;
import java.util.List;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import model.EstadoCampo;
import org.hibernate.Session;

/**
 *
 * @author admin
 */
public class EstadoCampoDao {
    
    /**
     * Retorna el valor por default que se asigna a los campos nuevos
     * @return 
     */
    public EstadoCampo buscarPorDefault() {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();                        
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<EstadoCampo> query = builder.createQuery(EstadoCampo.class);
        Root<EstadoCampo> root = query.from(EstadoCampo.class);
        query.select(root);
        
        Predicate predicate = builder.equal(root.get("descripcion"), "Creado");
        query.where(predicate);  
        
        // Ejecuto la consulta y guardo el resultado en un Optional
        EstadoCampo estadoCampo = session.createQuery(query).uniqueResult();
            
        session.close();
        
        return estadoCampo;
    }   
}
