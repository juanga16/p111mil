/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.combobox.model;

/**
 *
 * @author admin
 */
public class Usuario {
    private int id;
    private String email;
    private String nombreUsuario;
    private String nombre;
    private String apellido;
    private String numeroTelefono;

    public Usuario(int id, String email, String nombreUsuario, String nombre, String apellido, String numeroTelefono) {
        this.id = id;
        this.email = email;
        this.nombreUsuario = nombreUsuario;
        this.nombre = nombre;
        this.apellido = apellido;
        this.numeroTelefono = numeroTelefono;
    }
    
    /**
     * Vamos a devolver el nombre de usuario para mostrar en el combo
     * @return 
     */
    @Override
    public String toString() {
        return this.nombreUsuario;
    }
}
