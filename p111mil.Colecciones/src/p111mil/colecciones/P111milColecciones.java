/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.colecciones;

import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
import java.util.stream.Collectors;
import p111mil.colecciones.modelo.Auto;

/**
 *
 * @author admin
 */
public class P111milColecciones {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // Arreglos: son estaticos, es decir su longitud no puede cambiar
        String[] colonias = { "Santa Trinidad", "San Jose", "Santa Maria" };
        
        for (int i = 0; i < colonias.length; i++){
            System.out.println(colonias[i]);
        }
        
        colonias[0] = "San Martin";
        
        // Arreglos declarados de otra forma. Arrancan en 0 y si trato de acceder un indice mas alla del maximo, da error
        int[] numerosPrimos = new int[5];
        numerosPrimos[0] = 2;
        numerosPrimos[1] = 3;
        numerosPrimos[2] = 5;
        numerosPrimos[3] = 7;
        numerosPrimos[4] = 11;
        //numerosPrimos[5] = 13;
        
        for (int numeroPrimo : numerosPrimos) {
            System.out.println(numeroPrimo);
        }
        
        // Colecciones. Tamaño variable. ArrayList
        Auto fordFairlane = new Auto("Ford", "Fairlane");
        Auto peugeot404 = new Auto("Peugeot", "404");
        Auto dodgePolara = new Auto("Dogde", "Polara");
        Auto renaultGordini = new Auto("Renault", "Gordini");
        Auto fiat125 = new Auto("Fiat", "125");
        
        ArrayList<Auto> autos = new ArrayList<Auto>();
        autos.add(fordFairlane);
        autos.add(0, peugeot404);
        autos.add(dodgePolara);
        autos.add(renaultGordini);
        autos.add(fiat125);
        
        // autos.isEmpty()
        // autos.size()        
        
        // Iterar
        System.out.println("Imprimo la lista de autos");
        for(Auto auto : autos) {
            auto.imprimirDatos();
        }
        
        // Armo una nueva lista de autos, esta vez ordenada ascendente por Marca
        List<Auto> autosOrdenados = autos.stream()
                                        .sorted((x1, x2) -> x1.getMarca().compareTo(x2.getMarca()))
                                        .collect(Collectors.toList());        
        
        System.out.println("Imprimo la lista de autos ordenada por marca");
        for(Auto auto : autosOrdenados) {
            auto.imprimirDatos();
        }
        
        // Armo una nueva lista de autos, esta vez solo los que empiezan con F
        List<Auto> autosQueEmpiezanConF = autos.stream()
                                        .filter(x -> x.getMarca().startsWith("F"))
                                        .collect(Collectors.toList());        
        
        System.out.println("Imprimo la lista de autos cuya marca empieza con F");
        for(Auto auto : autosQueEmpiezanConF) {
            auto.imprimirDatos();
        }
        
        // Elimino dos items
        autos.remove(0);
        autos.remove(1);
        
        // Iterar de otra forma
        System.out.println("Imprimo la lista de filtrada");
        autos.forEach(x -> x.imprimirDatos());       
        
        // Pilas
        Stack<String> pila = new Stack<String>();
        pila.push("Argentina");
        pila.push("Brasil");
        pila.push("Uruguay");
        System.out.println(pila.pop());
        System.out.println(pila.pop());
        System.out.println(pila.pop());                              
    }    
}
