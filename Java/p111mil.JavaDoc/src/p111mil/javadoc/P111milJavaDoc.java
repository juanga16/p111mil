/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.javadoc;

/**
 *
 * @author admin
 */
public class P111milJavaDoc {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        
        /*
            Ir a Window -> Action Items (Control + 6)
        */
        
        // TODO: tarea para hacer
        
        // FIXME: arreglar esta linea
        
        // TODO: segunda tarea para hacer
        
        /*
            @author nombreDelAutor descripción. Indica quién escribió el código al que se refiere el comentario. Si son varias personas se escriben los nombres separados por comas o se repite el indicador, según se prefiera. Es normal incluir este indicador en el comentario de la clase y no repetirlo para cada método, a no ser que algún método haya sido escrito por otra persona. 
            @version númeroVersión descripción. Si se quiere indicar la versión. Normalmente se usa para clases, pero en ocasiones también para métodos. 
            @param nombreParámetro descripción. Para describir un parámetro de un método. 
            @return descripción. Describe el valor de salida de un método. 
            @see nombre descripción. Cuando el trozo de código comentado se encuentra relacionada con otra clase o método, cuyo nombre se indica en nombre. 
            @throws nombreClaseExcepción descripción. Cuando un método puede lanzar una excepción ("romperse" si se da alguna circunstancia) se indica así. 
            @deprecated descripción. Indica que el método (es más raro encontrarlos para una clase) ya no se usa y se ha sustituido por otro. 
        */
        
        Persona juan = new Persona();
        
        boolean puedeSacarRegistro = juan.puedeSacarRegistroConducir(37);
    }    
}
