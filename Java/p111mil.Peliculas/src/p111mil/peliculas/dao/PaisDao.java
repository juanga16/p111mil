/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.dao;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;
import org.hibernate.Session;
import p111mil.peliculas.modelo.Pais;

/**
 *
 * @author admin
 */
public class PaisDao {        
    private final static Logger LOGGER = Logger.getLogger("Peliculas");
    
    public List<Pais> buscarTodos() {
        LOGGER.log(Level.INFO, "Comienzo ejecucion buscarTodos");
        
        // Obtengo una nueva session y la abro
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        ArrayList<Pais> paises = new ArrayList<Pais>();
        
        try {        
            // Hago una consulta para obtener todos los paises de la tabla pais
            CriteriaBuilder builder = session.getCriteriaBuilder();
            CriteriaQuery<Pais> query = builder.createQuery(Pais.class);
            Root<Pais> root = query.from(Pais.class);
            query.select(root);
            query.orderBy(builder.asc(root.get("nombre")));
            // Ejecuto la consulta y guardo el resultado en una lista de Pais
            paises = (ArrayList<Pais>) session.createQuery(query).list();
        }
        catch(Exception excepcion) {
            LOGGER.log(Level.SEVERE, excepcion.getMessage());
        }
        finally {
            // Antes de salir, debo cerrar la session
            session.close();
        }
        
        LOGGER.log(Level.INFO, "Termino la ejecucion buscarTodos: {0} resultados", paises.size());
        
        return paises;
    }
    
    public Pais buscarPorId(int id) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Pais> query = builder.createQuery(Pais.class);
        Root<Pais> root = query.from(Pais.class);
        query.select(root);
        query.where(builder.equal(root.get("id"), id));
        Pais pais = (Pais) session.createQuery(query).uniqueResult();
        
        session.close();
        
        return pais;
    }
    
    public Pais buscarPorNombre(String nombre) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();

        CriteriaBuilder builder = session.getCriteriaBuilder();
        CriteriaQuery<Pais> query = builder.createQuery(Pais.class);
        Root<Pais> root = query.from(Pais.class);
        query.select(root);
        query.where(builder.equal(root.get("nombre"), nombre));
        Pais pais = (Pais) session.createQuery(query).uniqueResult();
        
        session.close();
        
        return pais;
    }
       
    public void guardar(Pais pais) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        session.beginTransaction();        
        session.saveOrUpdate(pais);
        session.getTransaction().commit();
        
        session.close();
    }
    
    public void eliminar(int id) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();        
        
        session.beginTransaction();        
        Pais pais = session.get(Pais.class, id);
        session.delete(pais);
        session.getTransaction().commit();

        session.close();
    }
}
