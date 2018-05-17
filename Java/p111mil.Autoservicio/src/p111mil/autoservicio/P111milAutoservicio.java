/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.autoservicio;

import modelo.*;

/**
 *
 * @author Invitado
 */
public class P111milAutoservicio {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*
        Los productos sin descuento son:
	- Fideos por 1 kg, precio $ 25
	- Yerba por 1 kg, precio $ 75
	
        Los productos con descuento son:
	- Shampoo por 200 ml, precio $ 60
	- Aceite por 900 ml, precio $ 80
	- Arroz por 1 kg, precio: $ 25
	
        Los productos sin iva son:
	- Leche por 1 litro, $ 20
	- Queso por 1 kilo, $ 170
        */
        ProductoSinDescuento fideos = new ProductoSinDescuento("Fideos x 1kg", 25);
        ProductoSinDescuento yerba = new ProductoSinDescuento("Yerba x 1kg", 75);
        
        ProductoConDescuento shampoo = new ProductoConDescuento("Shampoo x 200ml", 60);
        ProductoConDescuento aceite = new ProductoConDescuento("Aceite x 900ml", 80);
        ProductoConDescuento arroz = new ProductoConDescuento("Arroz x 1kg", 25);
        
        ProductoSinIva leche = new ProductoSinIva("Leche x 1lt", 20);
        ProductoSinIva queso = new ProductoSinIva("Queso x 1kg", 170);
        
        /*
        Factura 1:
        - 2 paquetes de Fideos
        - 1 paquete de Yerba
        - 3 botellas de Aceite
        - 1 paquete de Arroz
        - 5 litros de Leche
        */
        
        Factura factura1 = new Factura();
        factura1.agregarItemCompra(fideos, 2);
        factura1.agregarItemCompra(yerba, 1);
        factura1.agregarItemCompra(aceite, 3);
        factura1.agregarItemCompra(arroz, 1);
        factura1.agregarItemCompra(leche, 5);
        factura1.imprimir();
    }
    
}
