/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.modelo;

/**
 *
 * @author Invitado
 */
public class Resultado {
    private int golesLocal;
    private int golesVisitante;

    public int getGolesLocal() {
        return golesLocal;
    }

    public void setGolesLocal(int golesLocal) {
        this.golesLocal = golesLocal;
    }

    public int getGolesVisitante() {
        return golesVisitante;
    }

    public void setGolesVisitante(int golesVisitante) {
        this.golesVisitante = golesVisitante;
    }
    
    public boolean ganoLocal() {
        return this.golesLocal > this.golesVisitante;
    }
    
    public boolean empate() {
        return this.golesLocal == this.golesVisitante;
    }

    public Resultado(int golesLocal, int golesVisitante) {
        this.golesLocal = golesLocal;
        this.golesVisitante = golesVisitante;
    }
}
