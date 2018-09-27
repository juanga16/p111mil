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
import javax.persistence.criteria.Root;
import org.hibernate.Session;
import p111mil.agenda.modelo.Ciudad;

/**
 *
 * @author Invitado
 */
public class CiudadDao {
    public List<Ciudad> buscarTodos() {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();                
        ArrayList<Ciudad> ciudades = new ArrayList<Ciudad>();
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Ciudad> query = builder.createQuery(Ciudad.class);
        Root<Ciudad> root = query.from(Ciudad.class);
        query.select(root);
        query.orderBy(builder.asc(root.get("nombre")));
        // Ejecuto la consulta y guardo el resultado en una lista de Pais
        ciudades = (ArrayList<Ciudad>) session.createQuery(query).list();
            
        session.close();

        return ciudades;        
    }
}
