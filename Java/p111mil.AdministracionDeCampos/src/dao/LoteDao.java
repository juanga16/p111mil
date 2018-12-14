/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dao;

import hibernate.ConfiguracionHibernate;
import model.Lote;
import org.hibernate.Session;

/**
 *
 * @author admin
 */
public class LoteDao {
    /**
     * Retorna verdadero si ya existe un lote con ese mismo numero
     * @param numeroLote
     * @return boolean
     */
    public boolean existeConMismoNumero(int numeroLote) {
        Session session = ConfiguracionHibernate.getSessionFactory().openSession();                
        Lote lote = session.get(Lote.class, numeroLote);        
        session.close();
        
        return lote != null;
    }
}
