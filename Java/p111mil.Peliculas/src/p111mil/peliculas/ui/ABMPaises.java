/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.peliculas.ui;

import java.util.List;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTable;
import javax.swing.ListSelectionModel;
import javax.swing.table.DefaultTableCellRenderer;
import p111mil.peliculas.dao.ConfiguracionHibernate;
import p111mil.peliculas.dao.PaisDao;
import p111mil.peliculas.modelo.Pais;

/**
 *
 * @author PC-MAESTRO
 */
public class ABMPaises extends javax.swing.JFrame {

    /**
     * Creates new form ABMActores
     */
    public ABMPaises() {
        initComponents();
        cargarTabla();               
        
        // Solamente se pueden seleccionar de a una fila
        tablaPaises.setRowSelectionAllowed(true);
        tablaPaises.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
    }
    
    private void deshabilitarBotones() {
        botonEliminar.setEnabled(false);
        botonMostrar.setEnabled(false);
        botonEditar.setEnabled(false);        
    }
    
    private void habilitarBotones() {
        // Si tengo una fila seleccionada, habilito los botones
        if (tablaPaises.getSelectedRow() >= 0) {
            botonEliminar.setEnabled(true);
            botonMostrar.setEnabled(true);
            botonEditar.setEnabled(true);
        }
    }
    
    private void cargarTabla() {
        deshabilitarBotones();
        
        PaisDao paisDao = new PaisDao();
        List<Pais> paises = paisDao.buscarTodos();
                        
        // Para alinear los numeros a la derecha
        DefaultTableCellRenderer rightRenderer = new DefaultTableCellRenderer();
        rightRenderer.setHorizontalAlignment(JLabel.RIGHT);

        tablaPaises.setModel(new PaisModeloTabla(paises));
        
        // Establece un ancho de 20 para la columna 0
        tablaPaises.getColumnModel().getColumn(0).setPreferredWidth(20);
        tablaPaises.getColumnModel().getColumn(0).setCellRenderer(rightRenderer);
        // Establece un ancho de 50 para la columna 1
        tablaPaises.getColumnModel().getColumn(1).setPreferredWidth(50);
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        botonNuevo = new javax.swing.JButton();
        botonEliminar = new javax.swing.JButton();
        botonEditar = new javax.swing.JButton();
        botonMostrar = new javax.swing.JButton();
        jScrollPane1 = new javax.swing.JScrollPane();
        tablaPaises = new javax.swing.JTable();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent evt) {
                formWindowClosing(evt);
            }
        });

        botonNuevo.setText("Nuevo");
        botonNuevo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                botonNuevoActionPerformed(evt);
            }
        });

        botonEliminar.setText("Eliminar");
        botonEliminar.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                botonEliminarActionPerformed(evt);
            }
        });

        botonEditar.setText("Editar");
        botonEditar.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                botonEditarActionPerformed(evt);
            }
        });

        botonMostrar.setText("Mostrar");
        botonMostrar.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                botonMostrarActionPerformed(evt);
            }
        });

        tablaPaises.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null}
            },
            new String [] {
                "Title 1", "Title 2", "Title 3", "Title 4"
            }
        ));
        tablaPaises.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                tablaPaisesMouseClicked(evt);
            }
        });
        tablaPaises.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyReleased(java.awt.event.KeyEvent evt) {
                tablaPaisesKeyReleased(evt);
            }
        });
        jScrollPane1.setViewportView(tablaPaises);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                    .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 0, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(botonNuevo)
                        .addGap(18, 18, 18)
                        .addComponent(botonEliminar)
                        .addGap(18, 18, 18)
                        .addComponent(botonEditar)
                        .addGap(18, 18, 18)
                        .addComponent(botonMostrar)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        layout.linkSize(javax.swing.SwingConstants.HORIZONTAL, new java.awt.Component[] {botonEditar, botonEliminar, botonMostrar, botonNuevo});

        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 439, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(botonNuevo)
                    .addComponent(botonEliminar)
                    .addComponent(botonEditar)
                    .addComponent(botonMostrar))
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void formWindowClosing(java.awt.event.WindowEvent evt) {//GEN-FIRST:event_formWindowClosing
        // Invoco el cerrar justo antes de salir del programa
        // para liberar los recursos de la conexion con la base de datos
        ConfiguracionHibernate.cerrar();
    }//GEN-LAST:event_formWindowClosing

    private void botonNuevoActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_botonNuevoActionPerformed
        String nombrePais = JOptionPane.showInputDialog(this, "Ingrese el nombre del nuevo pais");
        
        if (nombrePais == null) {
            return;
        }
        
        if (nombrePais.isEmpty()) {
            JOptionPane.showMessageDialog(this, "El nombre del pais no puede estar vacio", "Alta de pais", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        if (nombrePais.length() > 50) {
            JOptionPane.showMessageDialog(this, "El pais no puede tener mas de 50 caracteres", "Alta de pais", JOptionPane.WARNING_MESSAGE);
            return;
        }
       
        PaisDao paisDao = new PaisDao();
        
        if (paisDao.buscarPorNombre(nombrePais) != null) {
            JOptionPane.showMessageDialog(this, "Ya existe un pais con el mismo nombre", "Alta de pais", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        Pais nuevoPais = new Pais();
        nuevoPais.setNombre(nombrePais);
        
        paisDao.guardar(nuevoPais);
        cargarTabla();
                
        JOptionPane.showMessageDialog(this, "El pais se ha creado exitosamente", "Alta de pais", JOptionPane.INFORMATION_MESSAGE);            
    }//GEN-LAST:event_botonNuevoActionPerformed

    private void tablaPaisesMouseClicked(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_tablaPaisesMouseClicked
        habilitarBotones();
    }//GEN-LAST:event_tablaPaisesMouseClicked

    private void tablaPaisesKeyReleased(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_tablaPaisesKeyReleased
        habilitarBotones();
    }//GEN-LAST:event_tablaPaisesKeyReleased

    private void botonEditarActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_botonEditarActionPerformed
        // Si no tengo nada seleccionado me voy
        if (tablaPaises.getSelectedRow() < 0) {
            return;
        }
        
        int filaSeleccionada = tablaPaises.getSelectedRow();
        
        // Usamos el metodo getValueAt para obtener el ID (que es la columna 0)
        int idPais = (int) tablaPaises.getValueAt(filaSeleccionada, 0);
        
        PaisDao paisDao = new PaisDao();        
        Pais paisParaEditar = paisDao.buscarPorId(idPais);
        
        String nombreNuevoDelPais = JOptionPane.showInputDialog(this, "Ingrese el nuevo nombre del pais", paisParaEditar.getNombre());
        
        if (nombreNuevoDelPais == null) {
            return;
        }
        
        if (nombreNuevoDelPais.isEmpty()) {
            JOptionPane.showMessageDialog(this, "El nombre del pais no puede estar vacio", "Edicion de pais", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        if (nombreNuevoDelPais.length() > 50) {
            JOptionPane.showMessageDialog(this, "El pais no puede tener mas de 50 caracteres", "Edicion de pais", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        Pais paisExistente = paisDao.buscarPorNombre(nombreNuevoDelPais);
                
        if (paisExistente != null) {           
            // Si los IDs son iguales, en este caso no modifique el nombre
            // Si los IDs son diferentes no puedo continuar porque estaria generando un duplicado
            if (paisParaEditar.getId() != paisExistente.getId()) {
                JOptionPane.showMessageDialog(this, "Ya existe un pais con el nombre: " + nombreNuevoDelPais, "Edicion de pais", JOptionPane.WARNING_MESSAGE);
                return;
            }
        }
        
        // El pais cambio de nombre, debemos actualizar en la BD
        paisParaEditar.setNombre(nombreNuevoDelPais);

        paisDao.guardar(paisParaEditar);
        cargarTabla();
                
        JOptionPane.showMessageDialog(this, "El pais se ha editado exitosamente", "Edicion de pais", JOptionPane.INFORMATION_MESSAGE);                    
    }//GEN-LAST:event_botonEditarActionPerformed

    private void botonEliminarActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_botonEliminarActionPerformed
        if (tablaPaises.getSelectedRow() < 0) {
            return;
        }
        
        int filaSeleccionada = tablaPaises.getSelectedRow();
        int idPais = (int) tablaPaises.getValueAt(filaSeleccionada, 0);
        String nombrePaisParaEliminar = (String) tablaPaises.getValueAt(filaSeleccionada, 1);
                
        PaisDao paisDao = new PaisDao();
        Pais paisParaEliminar = paisDao.buscarPorId(idPais);
        
        // Para eliminar un pais verificamos que no tenga registros relacionados
        if (paisParaEliminar.getActores().size() > 0 || 
                paisParaEliminar.getPeliculas().size() > 0 || 
                paisParaEliminar.getDirectores().size() > 0) {
            JOptionPane.showMessageDialog(this, "El pais no puede ser eliminado, ya que tiene informacion relacionada", "Borrado de paises", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        int respuesta = JOptionPane.showConfirmDialog(this, "¿Desea eliminar el pais " + nombrePaisParaEliminar + " ?", "Borrado de paises", JOptionPane.YES_NO_OPTION);
        
        if (respuesta == JOptionPane.YES_OPTION) {
            paisDao.eliminar(idPais);
        
            cargarTabla();
            JOptionPane.showMessageDialog(this, "El pais " + nombrePaisParaEliminar + " fue eliminado", "Borrado de paises", JOptionPane.WARNING_MESSAGE);
        }
    }//GEN-LAST:event_botonEliminarActionPerformed

    private void botonMostrarActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_botonMostrarActionPerformed
        if (tablaPaises.getSelectedRow() < 0) {
            return;
        }
        
        int filaSeleccionada = tablaPaises.getSelectedRow();
        int idPais = (int) tablaPaises.getValueAt(filaSeleccionada, 0);
        
        PaisDao paisDao = new PaisDao();
        Pais pais = paisDao.buscarPorId(idPais);
        
        JOptionPane.showMessageDialog(this, "El pais " + pais.getNombre() + " tiene " + pais.getActores().size() + " actores relacionados" );
        
    }//GEN-LAST:event_botonMostrarActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(ABMPaises.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(ABMPaises.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(ABMPaises.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(ABMPaises.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new ABMPaises().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton botonEditar;
    private javax.swing.JButton botonEliminar;
    private javax.swing.JButton botonMostrar;
    private javax.swing.JButton botonNuevo;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JTable tablaPaises;
    // End of variables declaration//GEN-END:variables
}
