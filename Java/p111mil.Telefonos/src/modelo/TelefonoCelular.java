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
public class TelefonoCelular extends Telefono {
    private String antena;
    private boolean vibracion;    
    
    public TelefonoCelular(int numero) {
        super(numero);
    }

    public String getAntena() {
        return antena;
    }

    public void setAntena(String Antena) {
        this.antena = Antena;
    }
    
    // Cuando el getter es boolean se pone "is" en vez de "get"
    public boolean isVibracion() {
        return vibracion;
    }

    public void setVibracion(boolean vibracion) {
        this.vibracion = vibracion;
    }
    
    public void enviarMensaje(String mensaje, int numero) {
        System.out.println("Enviando mensaje: " + mensaje + " al " + numero);
    }
    
    @Override
    public String toString() {
        return "Soy un Telefono Celular y mi numero es: " + PREFIJO_SUAREZ + " " + super.getNumero();
    }
    
    // Con la palabra clave Override digo que estoy sobreescribiendo / redefiniendo un metodo
    @Override 
    public void sonar() {
        if (this.vibracion) {
            System.out.println("Estoy vibrando");
        } else {
            super.sonar();
        }
    }

    @Override
    public void llamar(int numero) {
        System.out.println("Llamando desde un Telefono Celular al ... " + numero);
    }
}
