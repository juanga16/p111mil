/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.comisionventas;

import java.text.DecimalFormat;
import java.util.Formatter;
import java.util.Scanner;

/**
 *
 * @author admin
 */
public class P111milComisionVentas {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*
        Una empresa mayorista de Lacteos tiene vendedores que recorren la zona tratando de vender productos a supermercados, colegios y clubes de la zona. 
        Con el objetivo de incentivar las ventas y premiar el esfuerzo la gerencia determino los siguientes porcentajes de comision.
        4% quien venda hasta 20.000 pesos, 6% quien venda hasta 40.000 pesos y el 6% hasta 40.000 pesos ademas del 10% de cada peso que supere esa cifra.
        Se necesita un programa que dado el total de ventas por mes informe la comision correspondiente al vendedor.
        */
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Ingrese el total de ventas:");
        double totalVentas = scanner.nextDouble();
        
        double comision = 0;
        
        if (totalVentas > 20000) {
            if (totalVentas <= 40000) {
                comision = totalVentas * 0.06;
            } else {
                comision = 40000 * 0.06 + (totalVentas - 40000) * 0.1;
            }
        } else {
            comision = totalVentas * 0.04;
        }
        
        DecimalFormat formatter = new DecimalFormat("#0.00");
        System.out.println("La comision es de: " + formatter.format(comision));
    }    
}
