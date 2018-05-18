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
public class MiClase {    
    /*
        Cuando sobre escribimos este metodo? Cuando nuestra clase utiliza recursos tales como:
        - Conexiones a bases de datos
        - Cuando se abren archivos
    
        Siempre es importante encargarse de cerrar las conexiones y los archivos
    */
    @Override
    public void finalize() {        
        System.out.println("Se esta liberando la memoria que ocupa este objeto");          
    }
}
