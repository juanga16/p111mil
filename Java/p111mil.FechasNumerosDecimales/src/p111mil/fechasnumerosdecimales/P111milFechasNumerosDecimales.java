/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.fechasnumerosdecimales;

import java.text.DecimalFormat;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.Month;
import java.time.format.DateTimeFormatter;

/**
 *
 * @author admin
 */
public class P111milFechasNumerosDecimales {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // Fechas
        LocalDate nacioMaradona = LocalDate.of(1960, Month.OCTOBER, 30);
        System.out.println(nacioMaradona);
        
        /*
        LocalDate: solo fecha
        LocalTime: solo hora
        LocalDateTime: fecha y hora
        */
        
        LocalDateTime volverAlFuturo = LocalDateTime.of(1955, Month.NOVEMBER, 5, 8, 30);
        System.out.println(volverAlFuturo);
        
        // Imprime la hora actual
        System.out.println(LocalTime.now()); 
        
        // Formato de Fechas
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss dd-MM-yyyy");
        
        LocalDateTime fechaHoy = LocalDateTime.now();
        System.out.println(fechaHoy.format(dateTimeFormatter));
        
        /*
        http://www.oracle.com/technetwork/es/articles/java/paquete-java-time-2390472-esa.html
        http://blog.eddumelendez.me/2016/07/conociendo-la-nueva-date-api-en-java-8-parte-i/
        */
        
        // Formato de numeros decimales
        DecimalFormat decimalFormat = new DecimalFormat(("0.00"));
        
        Float saldo = 432.129f;
        System.out.println(decimalFormat.format(saldo));
        
        /*
        https://java-spain.com/formateando-numeros-numberformat
        https://javiergarciaescobedo.es/programacion-en-java/29-trucos/113-formato-de-numeros-monedas-y-porcentajes2
        */
    }
    
}
