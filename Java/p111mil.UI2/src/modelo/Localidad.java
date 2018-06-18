/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

/**
 *
 * @author admin
 */
public class Localidad {
    private String nombre;
    private int codigoPostal;
    private Provincia provincia;

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public int getCodigoPostal() {
        return codigoPostal;
    }

    public void setCodigoPostal(int codigoPostal) {
        this.codigoPostal = codigoPostal;
    }

    public Provincia getProvincia() {
        return provincia;
    }

    public void setProvincia(Provincia provincia) {
        this.provincia = provincia;
    }

    public Localidad(String nombre, int codigoPostal, Provincia provincia) {
        this.nombre = nombre;
        this.codigoPostal = codigoPostal;
        this.provincia = provincia;
    }
    
    @Override
    public String toString() {
        return this.getNombre() + " (" + this.provincia.getNombre() + ")";
    }
}
