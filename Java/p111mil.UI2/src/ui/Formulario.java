/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ui;

import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.ArrayList;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JOptionPane;
import modelo.Localidad;

/**
 *
 * @author admin
 */
public class Formulario extends javax.swing.JFrame {
    private ArrayList<Localidad> localidades;
    /**
     * Creates new form FormularioComboBox
     */
    public Formulario(ArrayList<Localidad> localidades) {
        this.localidades = localidades;
        
        initComponents();                
        
        ItemListener itemListener = new ItemListener() {
            @Override
            public void itemStateChanged(ItemEvent itemEvent) {                
                if (itemEvent.getStateChange() == ItemEvent.SELECTED) {
                    Localidad localidadSeleccionada = (Localidad) itemEvent.getItem();
                    System.out.println(localidadSeleccionada);
                }                
            }
        };
    
        comboLocalidades.addItemListener(itemListener);        
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        comboLocalidades = new javax.swing.JComboBox<>();
        buttonMostrarValorSeleccionado = new javax.swing.JButton();
        buttonSetearValor = new javax.swing.JButton();
        jScrollPane2 = new javax.swing.JScrollPane();
        tableLocalidades = new javax.swing.JTable();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        comboLocalidades.setModel(new DefaultComboBoxModel(this.localidades.toArray()));

        buttonMostrarValorSeleccionado.setText("Mostrar valor seleccionado");
        buttonMostrarValorSeleccionado.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonMostrarValorSeleccionadoActionPerformed(evt);
            }
        });

        buttonSetearValor.setText("Setear valor");
        buttonSetearValor.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonSetearValorActionPerformed(evt);
            }
        });

        tableLocalidades.setModel(new LocalidadTableModel(this.localidades));
        jScrollPane2.setViewportView(tableLocalidades);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(comboLocalidades, javax.swing.GroupLayout.PREFERRED_SIZE, 254, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(buttonMostrarValorSeleccionado)
                        .addGap(18, 18, 18)
                        .addComponent(buttonSetearValor))
                    .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap(236, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(comboLocalidades, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(buttonMostrarValorSeleccionado)
                    .addComponent(buttonSetearValor))
                .addGap(18, 18, 18)
                .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void buttonMostrarValorSeleccionadoActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonMostrarValorSeleccionadoActionPerformed
        Localidad localidadSeleccionadaComboBox = (Localidad) this.comboLocalidades.getSelectedItem();
        
        int selectedRow = tableLocalidades.getSelectedRow();
        int index = tableLocalidades.convertRowIndexToModel(selectedRow);
        Localidad localidadSeleccionadaTable = this.localidades.get(index);
        
        System.out.println(localidadSeleccionadaComboBox);
        System.out.println(localidadSeleccionadaTable);
    }//GEN-LAST:event_buttonMostrarValorSeleccionadoActionPerformed

    private void buttonSetearValorActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonSetearValorActionPerformed
        this.comboLocalidades.setSelectedItem(localidades.get(0));
    }//GEN-LAST:event_buttonSetearValorActionPerformed

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton buttonMostrarValorSeleccionado;
    private javax.swing.JButton buttonSetearValor;
    private javax.swing.JComboBox<String> comboLocalidades;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JTable tableLocalidades;
    // End of variables declaration//GEN-END:variables
}