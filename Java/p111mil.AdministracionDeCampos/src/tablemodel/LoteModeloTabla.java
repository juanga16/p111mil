/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tablemodel;

import java.util.List;
import javax.swing.table.AbstractTableModel;
import model.Lote;

/**
 *
 * @author admin
 */
public class LoteModeloTabla extends AbstractTableModel {
    private static final String[] COLUMNAS = { "Número", "Superficie", "Tipo de Suelo" };
    
    private List<Lote> lotes;
    
    public LoteModeloTabla(List<Lote> lotes) {
        this.lotes = lotes;
    }

    @Override
    public int getRowCount() {
        return lotes.size();
    }

    @Override
    public int getColumnCount() {
        return COLUMNAS.length;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        Object valor = null;
        Lote lote = lotes.get(rowIndex);
        
        switch(columnIndex) {
            case 0:
                valor = lote.getNumeroLote();
                break;
            case 1:
                valor = lote.getSuperficie();
                break;
            case 2:
                valor = lote.getTipoDeSuelo();
                break;
        }
                
        return valor;
    }
    
    @Override
    public String getColumnName(int columnIndex) {
        return COLUMNAS[columnIndex];
    }    
}
