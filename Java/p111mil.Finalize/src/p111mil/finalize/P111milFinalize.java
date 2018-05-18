/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.finalize;

/**
 *
 * @author admin
 */
public class P111milFinalize {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*
            En Java el sistema se ocupa automaticamente de liberar la memoria
            de los objetos cuando perdieron la referencia. Porque quedo fuera de scope
            o bien porque se le asigno el valor null. Esto se llama Garbage Collection.                       
        */
        
        MiClase miClase = new MiClase();
        miClase = null;
        
        /* 
            Invoco al GarbageCollector, no es necesario que nos encarguemos de invocarlo. Es solamente para mostrar que se ejecuto el finalize
        */
        System.gc();
    }
    
}
