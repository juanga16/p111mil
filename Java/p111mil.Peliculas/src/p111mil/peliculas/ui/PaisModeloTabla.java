/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.ui;

import java.util.List;
import javax.swing.table.AbstractTableModel;
import p111mil.peliculas.modelo.Pais;

/**
 *
 * @author PC-MAESTRO
 */
public class PaisModeloTabla extends AbstractTableModel {
    public static final String[] COLUMNAS = { "Id", "Nombre", "Fecha Creacion" };
    
    private List<Pais> paises;
            
    public PaisModeloTabla(List<Pais> paises) {
        this.paises = paises;
    }
    
    // Tiene que retornar la cantidad de filas que tendra la grilla
    @Override
    public int getRowCount() {
        return paises.size();
    }

    // Tiene que retornar la cantidad de columnas
    @Override
    public int getColumnCount() {
        return COLUMNAS.length;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        Object value = null;
        Pais pais = paises.get(rowIndex);
        
        switch(columnIndex) {
            case 0:
                value = pais.getId();
                break;
            case 1:
                value = pais.getNombre();
                break;
            case 2:
                value = pais.getFechaCreacion();
                break;
        }
                
        return value;
    }
    
    // Devuelve el titulo de cada columna
    @Override
    public String getColumnName(int columnIndex) {
        return COLUMNAS[columnIndex];
    }    
}
