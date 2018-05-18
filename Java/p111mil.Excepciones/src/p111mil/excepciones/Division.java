/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.excepciones;

import java.util.Arrays;

/**
 *
 * @author admin
 */
public class Division {
    // Si existe la posibilidad de que mi metodo lance una Exception agrego el "throws" y el tipo de excepcion al final
    public int calcular(int dividendo, int divisor) throws MiExcepcion {
        int resultado = 0;
        
        try {
            /*
                El codigo dentro de try esta vigilado: si se produce un error y se lanza una exepcion,
                el control pasa al bloque catch. Se pueden incluir tantos catchs como se deseen.
                Luego si esta presente se ejecuta el bloque finally
            */
            resultado = dividendo / divisor;
        }
        
        catch(ArithmeticException arithmeticException) {
            /*
                Acabo de capturar una Exception del tipo Aritmetica
            
            */
            System.out.println(arithmeticException);
            System.out.println(arithmeticException.getMessage());
            System.out.println(Arrays.toString(arithmeticException.getStackTrace()));
            
            throw new MiExcepcion();            
        }
        catch(Exception exception) {
            /*
                Acabo de capturar una Exception generica. Puedo poner mas de un catch pero el primero tiene
                que capturar la exception mas especifica y el segundo mas generica.            
            */
            System.out.println(exception);
            System.out.println(exception.getMessage());
            System.out.println(Arrays.toString(exception.getStackTrace()));
            
            throw new MiExcepcion();            
        }        
        finally {
            /* 
                Este bloque es opcional.
                Este codigo se va a ejecutar siempre: ya sea porque lo que esta dentro de try se ejecuto sin problemas
                o bien porque ocurrio un error y se capturo el error en el catch
            
            */
        }        
        
        return resultado;
    }
}
