/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.ui;

import java.util.List;
import javax.swing.table.AbstractTableModel;
import p111mil.peliculas.modelo.Actor;

/**
 *
 * @author PC-MAESTRO
 */
public class ActorModeloTabla extends AbstractTableModel {
    public static final String[] COLUMNAS = { "Id", "Nombre", "Apellido", "Genero", "Fecha de Nacimiento", "Pais" };
    
    private List<Actor> actores;
            
    public ActorModeloTabla(List<Actor> actores) {
        this.actores = actores;
    }
    
    @Override
    public int getRowCount() {
        return actores.size();
    }

    @Override
    public int getColumnCount() {
        return COLUMNAS.length;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        Object value = null;
        Actor actor = actores.get(rowIndex);
        
        switch(columnIndex) {
            case 0:
                value = actor.getId();
                break;
            case 1:
                value = actor.getNombre();
                break;
            case 2:
                value = actor.getApellido();
                break;
            case 3:
                value = actor.getGenero();
                break;
            case 4:
                value = actor.getFechaNacimiento();
                break;
            case 5:
                value = actor.getPais().getNombre();
                break;                
        }
                
        return value;
    }
    
    @Override
    public String getColumnName(int columnIndex) {
        return COLUMNAS[columnIndex];
    }
}
