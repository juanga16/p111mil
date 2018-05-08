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
public class TelefonoFijo extends Telefono {

    public TelefonoFijo(int numero) {
        super(numero);
    }

    @Override
    public void llamar(int numero) {
        System.out.println("Llamando desde un Telefono Fijo al ... " + numero);
    }
    
}
