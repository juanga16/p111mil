/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ui;

import java.util.ArrayList;
import javax.swing.table.AbstractTableModel;
import modelo.Localidad;

/**
 *
 * @author admin
 */
public class LocalidadTableModel extends AbstractTableModel {
    public static final String[] COLUMNAS = { "Nombre", "Codigo Postal", "Provincia" };
    
    private ArrayList<Localidad> localidades;
            
    public LocalidadTableModel(ArrayList<Localidad> localidades) {
        this.localidades = localidades;
    }
    
    @Override
    public int getRowCount() {
        return this.localidades.size();
    }

    @Override
    public int getColumnCount() {
        return COLUMNAS.length;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        Object value = null;
        Localidad localidad = localidades.get(rowIndex);
        
        switch(columnIndex) {
            case 0:
                value = localidad.getNombre();
                break;
            case 1:
                value = localidad.getCodigoPostal();
                break;
            case 2:
                value = localidad.getProvincia().getNombre();
                break;
        }
                
        return value;
    }    
    
    @Override
    public String getColumnName(int index) {
        return COLUMNAS[index];
    }
}
