/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.text.ParseException;
import java.util.ArrayList;
import javax.swing.DefaultComboBoxModel;
import javax.swing.DefaultListModel;
import javax.swing.JOptionPane;
import javax.swing.Timer;
import javax.swing.text.MaskFormatter;
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
        
        MaskFormatter maskFormatterNumeroCuit = new MaskFormatter();
        
        try {
            maskFormatterNumeroCuit.setMask("##-########-#");
            maskFormatterNumeroCuit.setPlaceholderCharacter(' ');
            maskFormatterNumeroCuit.setAllowsInvalid(false);
            maskFormatterNumeroCuit.setOverwriteMode(true);
        } catch (ParseException pe) {
            pe.printStackTrace();
        }
        
        maskFormatterNumeroCuit.install(formattedNumeroCuit);
        
        DefaultListModel<Localidad> defaultListModel = new DefaultListModel();
        
        for(Localidad localidad : localidades) {
            defaultListModel.addElement(localidad);
        }
        
        //listLocalidades.setd(defaultListModel);
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        buttonGroup = new javax.swing.ButtonGroup();
        comboLocalidades = new javax.swing.JComboBox<>();
        buttonMostrarValorSeleccionado = new javax.swing.JButton();
        buttonSetearValor = new javax.swing.JButton();
        jScrollPane2 = new javax.swing.JScrollPane();
        tableLocalidades = new javax.swing.JTable();
        checkBox = new javax.swing.JCheckBox();
        radioOpcion1 = new javax.swing.JRadioButton();
        radioOpcion2 = new javax.swing.JRadioButton();
        radioOpcion3 = new javax.swing.JRadioButton();
        toggleButton = new javax.swing.JToggleButton();
        passwordField = new javax.swing.JPasswordField();
        labelPassword = new javax.swing.JLabel();
        progressBar = new javax.swing.JProgressBar();
        buttonProgressBar = new javax.swing.JButton();
        formattedNumeroCuit = new javax.swing.JFormattedTextField();
        labelNumeroCuit = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        listLocalidades = new javax.swing.JList<>();

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

        checkBox.setText("Ejemplo de Check Box");
        checkBox.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                checkBoxActionPerformed(evt);
            }
        });

        buttonGroup.add(radioOpcion1);
        radioOpcion1.setSelected(true);
        radioOpcion1.setText("Opcion 1");

        buttonGroup.add(radioOpcion2);
        radioOpcion2.setText("Opcion 2");

        buttonGroup.add(radioOpcion3);
        radioOpcion3.setText("Opcion 3");

        toggleButton.setText("Toggle Button");
        toggleButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                toggleButtonActionPerformed(evt);
            }
        });

        labelPassword.setText("Password");

        buttonProgressBar.setText("Comenzar");
        buttonProgressBar.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonProgressBarActionPerformed(evt);
            }
        });

        labelNumeroCuit.setText("Numero de Cuit");

        jScrollPane1.setViewportView(listLocalidades);

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
                .addGap(18, 18, 18)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addComponent(checkBox, javax.swing.GroupLayout.PREFERRED_SIZE, 189, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(radioOpcion1)
                    .addComponent(radioOpcion2)
                    .addComponent(radioOpcion3)
                    .addComponent(buttonProgressBar)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                            .addComponent(toggleButton, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                            .addComponent(labelPassword)
                            .addComponent(passwordField, javax.swing.GroupLayout.DEFAULT_SIZE, 100, Short.MAX_VALUE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(labelNumeroCuit)
                            .addComponent(formattedNumeroCuit, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE)))
                    .addComponent(progressBar, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jScrollPane1))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(checkBox)
                        .addGap(47, 47, 47)
                        .addComponent(radioOpcion1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(radioOpcion2)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(radioOpcion3)
                        .addGap(28, 28, 28)
                        .addComponent(toggleButton)
                        .addGap(35, 35, 35)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(labelPassword)
                            .addComponent(labelNumeroCuit))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(passwordField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(formattedNumeroCuit, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                        .addGap(44, 44, 44)
                        .addComponent(progressBar, javax.swing.GroupLayout.PREFERRED_SIZE, 26, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(buttonProgressBar)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(comboLocalidades, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(buttonMostrarValorSeleccionado)
                            .addComponent(buttonSetearValor))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void buttonMostrarValorSeleccionadoActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonMostrarValorSeleccionadoActionPerformed
        Localidad localidadSeleccionadaComboBox = (Localidad) this.comboLocalidades.getSelectedItem();
        
        int selectedRow = tableLocalidades.getSelectedRow();
        int index = tableLocalidades.convertRowIndexToModel(selectedRow);
        
        if (index >= 0) {            
            Localidad localidadSeleccionadaTable = this.localidades.get(index);

            System.out.println(localidadSeleccionadaComboBox);
            System.out.println(localidadSeleccionadaTable);
        }
        
        if (listLocalidades.getSelectedIndices().length > 0) {
            for(int selectedIndex : listLocalidades.getSelectedIndices()) {
                Localidad localidad = listLocalidades.getm .getElementAt(selectedIndex);
                System.out.println(localidad);
            }
        }
    }//GEN-LAST:event_buttonMostrarValorSeleccionadoActionPerformed

    private void buttonSetearValorActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonSetearValorActionPerformed
        this.comboLocalidades.setSelectedItem(localidades.get(0));
        checkBox.setSelected(true);
        radioOpcion3.setSelected(true);
        formattedNumeroCuit.setText("12-34567890-1");
        String password = String.valueOf(passwordField.getPassword());
        if (! password.equals("")) {
            JOptionPane.showMessageDialog(this, "El password es: " + password);
        }
    }//GEN-LAST:event_buttonSetearValorActionPerformed

    private void checkBoxActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_checkBoxActionPerformed
        buttonSetearValor.setEnabled(checkBox.isSelected());
    }//GEN-LAST:event_checkBoxActionPerformed

    private void toggleButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_toggleButtonActionPerformed
        if (toggleButton.isSelected()) {
            checkBox.setSelected(true);
        }
        
        passwordField.requestFocus();
    }//GEN-LAST:event_toggleButtonActionPerformed

    private void buttonProgressBarActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonProgressBarActionPerformed
        progressBar.setValue(0);
        progressBar.setMinimum(0);
        progressBar.setMaximum(100);
        
        Timer timer = new Timer(100, null);
        ActionListener listener = new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent e) {
                progressBar.setValue(progressBar.getValue() + 1);     
                System.out.println(progressBar.getValue());                
                
                if (progressBar.getValue() == 100) {
                     timer.stop();
                }
            }
        };
        
        timer.addActionListener(listener);
        timer.setRepeats(true);
        timer.start();
    }//GEN-LAST:event_buttonProgressBarActionPerformed

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.ButtonGroup buttonGroup;
    private javax.swing.JButton buttonMostrarValorSeleccionado;
    private javax.swing.JButton buttonProgressBar;
    private javax.swing.JButton buttonSetearValor;
    private javax.swing.JCheckBox checkBox;
    private javax.swing.JComboBox<String> comboLocalidades;
    private javax.swing.JFormattedTextField formattedNumeroCuit;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JLabel labelNumeroCuit;
    private javax.swing.JLabel labelPassword;
    private javax.swing.JList<String> listLocalidades;
    private javax.swing.JPasswordField passwordField;
    private javax.swing.JProgressBar progressBar;
    private javax.swing.JRadioButton radioOpcion1;
    private javax.swing.JRadioButton radioOpcion2;
    private javax.swing.JRadioButton radioOpcion3;
    private javax.swing.JTable tableLocalidades;
    private javax.swing.JToggleButton toggleButton;
    // End of variables declaration//GEN-END:variables
}
