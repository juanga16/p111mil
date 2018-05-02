/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.banco.modelo;

/**
 *
 * @author Invitado
 */
public class CajaAhorro {
    private float saldo;
    
    public CajaAhorro(float saldoInicial) {
        this.saldo = saldoInicial;
    }
    
    public float getSaldo() {
        return this.saldo;
    }
    
    public void depositar(float deposito) {
        this.saldo = this.saldo + deposito;
    }
    
    public void extraer(float extraccion) {
        if (extraccion <= this.saldo)
        {
            this.saldo = this.saldo - extraccion;
        }
    }
}
