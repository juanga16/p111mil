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
public class ClasePublicaHija extends ClasePublica {    
    @Override
    public void metodoPublico() {
        this.variablePrivada = 0;
        this.variableProtegida = 0;
        super.variableProtegida = 0;
        this.variablePublica = 0;
        super.variablePublica = 0;        
    }
    
    private class ClasePrivada {
    
    }
}
