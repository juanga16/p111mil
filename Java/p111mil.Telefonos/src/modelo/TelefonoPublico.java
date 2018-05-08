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
public class TelefonoPublico extends Telefono {
    // TelefonoPublico hereda de Telefono, un TelefonoPublico a su vez "es un" telefono
    
    private String Ubicacion;
    private static int centavosPorPulso = 25;

    public static void setCentavosPorPulso(int centavosPorPulso) {
        TelefonoPublico.centavosPorPulso = centavosPorPulso;
    }

    public TelefonoPublico(int numero) {
        super(numero);
    }

    public String getUbicacion() {
        return Ubicacion;
    }

    public void setUbicacion(String Ubicacion) {
        this.Ubicacion = Ubicacion;
    }
    
    public void recibirCredito(float moneda) {
        System.out.println("Recibiendo credito ...");
    }
    
    public void controlarCredito() {
        System.out.println("Controlando credito");
    }
    
    @Override
    public String toString() {
        return "Soy un Telefono Público y mi numero es: " + PREFIJO_SUAREZ + " " + super.getNumero();
    }
        
    @Override
    public void llamar(int numero) {
        System.out.println("Llamando desde un Telefono Publico al ... " + numero);
    }    
}
