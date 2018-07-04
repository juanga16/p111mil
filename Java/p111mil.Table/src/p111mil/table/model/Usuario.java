/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.table.model;

/**
 *
 * @author admin
 */
public class Usuario {
    private int id;
    private String email;
    private String nombre;
    private String apellido;

    public int getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public String getNombre() {
        return nombre;
    }

    public String getApellido() {
        return apellido;
    }

    public String getNumeroTelefono() {
        return numeroTelefono;
    }
    private String numeroTelefono;

    public Usuario(int id, String nombre, String apellido, String email, String numeroTelefono) {
        this.id = id;
        this.email = email;
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
        return this.email;
    }
}
