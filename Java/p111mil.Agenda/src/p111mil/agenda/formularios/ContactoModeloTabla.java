/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.agenda.formularios;

import java.util.List;
import javax.swing.table.AbstractTableModel;
import p111mil.agenda.modelo.Contacto;

/**
 *
 * @author Invitado
 */
public class ContactoModeloTabla extends AbstractTableModel {
    private static final String[] COLUMNAS = { "Id", "Apellido", "Nombre", "Telefono", "Ciudad" };
    
    private List<Contacto> contactos;
    
    public ContactoModeloTabla(List<Contacto> contactos) {
        this.contactos = contactos;
    }
    
    @Override
    public int getRowCount() {
        return contactos.size();
    }

    @Override
    public int getColumnCount() {
        return COLUMNAS.length;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        Object valor = null;
        Contacto contacto = contactos.get(rowIndex);
        
        switch(columnIndex) {
            case 0:
                valor = contacto.getId();
                break;
            case 1:
                valor = contacto.getApellido();
                break;
            case 2:
                valor = contacto.getNombre();
                break;
            case 3:
                valor = contacto.getTelefono();
                break;
            case 4:
                valor = contacto.getCiudad().getNombre();
                break;
        }
                
        return valor;
    }
    
    @Override
    public String getColumnName(int columnIndex) {
        return COLUMNAS[columnIndex];
    }    
}
