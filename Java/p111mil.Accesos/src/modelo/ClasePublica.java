/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package modelo;

/**
 *
 * @author Invitado
 */
public class ClasePublica {
    private int variablePrivada;
    protected int variableProtegida;
    public int variablePublica;
    
    public void metodoPublico() {
        System.out.println("Método Publico");
    }
    
    protected void metodoProtegido() {
        System.out.println("Método Protegido");
    }
    
    private void metodoPrivado() {
        System.out.println("Método Privado");
    }
}
