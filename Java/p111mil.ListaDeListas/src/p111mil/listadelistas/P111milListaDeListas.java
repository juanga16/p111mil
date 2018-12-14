/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.listadelistas;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author admin
 */
public class P111milListaDeListas {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // Lista de listas : en este ejemplo serian paises por continente
        List<List<String>> paisesPorContinente = new ArrayList<List<String>>();
        
        List<String> america = new ArrayList<String>();
        america.add("Argentina");
        america.add("Uruguay");
        america.add("Brasil");
        paisesPorContinente.add(america);
        
        List<String> europa = new ArrayList<String>();
        europa.add("Italia");
        europa.add("Francia");
        europa.add("España");
        europa.add("Alemania");
        paisesPorContinente.add(europa);
        
        List<String> asia = new ArrayList<String>();
        asia.add("China");
        asia.add("Japon");
        paisesPorContinente.add(asia);
        
        System.out.println("Imprimir todos los paises de todos los continentes");
        for(List<String> paises : paisesPorContinente) {
            for(String pais : paises) {
                System.out.println(pais);
            }
        }
    }    
}
