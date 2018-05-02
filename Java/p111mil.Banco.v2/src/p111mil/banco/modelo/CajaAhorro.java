/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.banco.modelo;

import java.text.DecimalFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

/**
 *
 * @author Invitado
 */
public class CajaAhorro {
    private float saldo;
    
    private ArrayList<Movimiento> ingresos = new ArrayList<Movimiento>();
    private ArrayList<Movimiento> egresos = new ArrayList<Movimiento>();
    
    public CajaAhorro(float saldoInicial) {
        Movimiento ingreso = new Movimiento();
        ingreso.setFecha(LocalDateTime.now());
        ingreso.setMonto(saldoInicial);

        this.ingresos.add(ingreso);        
        this.saldo = saldoInicial;
    }
    
    public void depositar(LocalDateTime fecha, float deposito) {
        Movimiento ingreso = new Movimiento();
        ingreso.setFecha(fecha);
        ingreso.setMonto(deposito);

        this.ingresos.add(ingreso);
        this.saldo = this.saldo + deposito;
    }
    
    public void extraer(LocalDateTime fecha, float egreso) {
        if (egreso <= this.saldo)
        {
            Movimiento egresos = new Movimiento();
            egresos.setFecha(fecha);
            egresos.setMonto(egreso);

            this.egresos.add(egresos);
            
            this.saldo = this.saldo - egreso;
        }
    }
    
    public void imprimirResumenCuenta() {
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss dd-MM-yyyy");
        DecimalFormat decimalFormatter = new DecimalFormat(("0.00"));
        
        System.out.println("Ingresos");
        for (Movimiento ingreso : this.ingresos) {
            System.out.println("Fecha: " + ingreso.getFecha().format(dateTimeFormatter) + " - Monto: " + decimalFormatter.format(ingreso.getMonto()));
        }
        
        System.out.println("");
        System.out.println("Egresos");
        for (Movimiento egreso : this.egresos) {
            System.out.println("Fecha: " + egreso.getFecha().format(dateTimeFormatter) + " - Monto: " + decimalFormatter.format(egreso.getMonto()));
        }
        
        System.out.println("");
        System.out.println("Saldo");
        System.out.println(decimalFormatter.format(this.saldo));
    }
}
