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
import javax.persistence.criteria.Root;
import model.TipoDeSuelo;
import org.hibernate.Session;

/**
 *
 * @author admin
 */
public class TipoDeSueloDao {
    /**
     * Retorna todos los tipos de suelo ordenados por descripcion
     * @return 
     */
    public List<TipoDeSuelo> buscarTodos() {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();                
        ArrayList<TipoDeSuelo> tipoSuelos = new ArrayList<TipoDeSuelo>();
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<TipoDeSuelo> query = builder.createQuery(TipoDeSuelo.class);
        Root<TipoDeSuelo> root = query.from(TipoDeSuelo.class);
        query.select(root);
        query.orderBy(builder.asc(root.get("descripcion")));
        // Ejecuto la consulta y guardo el resultado en una lista de Pais
        tipoSuelos = (ArrayList<TipoDeSuelo>) session.createQuery(query).list();
            
        session.close();

        return tipoSuelos;        
    }
}
