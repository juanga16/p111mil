/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.colecciones.modelo;

/**
 *
 * @author admin
 */
public class Auto {
    private String marca;
    private String modelo;

    public String getMarca() {
        return marca;
    }

    public String getModelo() {
        return modelo;
    }

    public Auto(String marca, String modelo) {
        this.marca = marca;
        this.modelo = modelo;
    }
    
    public void imprimirDatos() {
        System.out.println(this.marca + " " + this.modelo);
    }
}
