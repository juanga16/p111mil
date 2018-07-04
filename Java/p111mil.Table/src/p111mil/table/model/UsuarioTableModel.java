/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.table.model;

import java.util.ArrayList;
import javax.swing.table.AbstractTableModel;

/**
 *
 * @author admin
 */
public class UsuarioTableModel extends AbstractTableModel {    
    public static final String[] COLUMNAS = { "Id", "Nombre", "Apellido", "Email", "Numero de Telefono" };
    
    private ArrayList<Usuario> usuarios;
            
    public UsuarioTableModel(ArrayList<Usuario> usuarios) {
        this.usuarios = usuarios;
    }
    
    @Override
    public int getRowCount() {
        return this.usuarios.size();
    }

    @Override
    public int getColumnCount() {
        return COLUMNAS.length;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        Object value = null;
        Usuario usuario = usuarios.get(rowIndex);
        
        switch(columnIndex) {
            case 0:
                value = usuario.getId();
                break;
            case 1:
                value = usuario.getNombre();
                break;
            case 2:
                value = usuario.getApellido();
                break;
            case 3:
                value = usuario.getEmail();
                break;                
            case 4:
                value = usuario.getNumeroTelefono();
                break;                
        }
                
        return value;
    }    
    
    @Override
    public String getColumnName(int index) {
        return COLUMNAS[index];
    }
    
    public void removeRow(int row) {
        usuarios.remove(row);
    }
}
