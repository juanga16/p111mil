/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.interfaces;

/**
 *
 * @author admin
 */
public class Persona implements Trabajador, Futbolista {
    private int talleBotines;
    boolean usaCanilleras;
    int salario;
    
    @Override
    public void registrarIngreso() {
        System.out.println("Registrar Ingreso");
    }

    @Override
    public void registrarSalida() {
        System.out.println("Registrar Salida");
    }

    @Override
    public void trabajar() {
        System.out.println("Trabajar");
    }

    @Override
    public int getSalario(int salario) {
        return this.salario;
    }

    @Override
    public void preCalentar() {
        System.out.println("Pre Calentar");
    }

    @Override
    public void jugar() {
        System.out.println("Jugar");
    }

    @Override
    public void setTalleBotines(int talleBotines) {
        this.talleBotines = talleBotines;
    }

    @Override
    public void setUsaCanilleras(boolean usaCanilleras) {
        this.usaCanilleras = usaCanilleras;
    }
}
