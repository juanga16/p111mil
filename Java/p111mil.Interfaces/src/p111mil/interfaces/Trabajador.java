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
public interface Trabajador {
    void registrarIngreso();
    
    void registrarSalida();
    
    void trabajar();
    
    int getSalario(int salario);
}
