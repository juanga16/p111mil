/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.mundial;

import java.util.GregorianCalendar;
import java.util.List;
import p111mil.modelo.*;

/**
 *
 * @author Invitado
 */
public class P111milMundial {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // Grupo de Argentina de Mexico '86
        Equipo argentina = new Equipo("Argentina");
        Equipo italia = new Equipo("Italia");
        Equipo corea = new Equipo("Corea");
        Equipo bulgaria = new Equipo("Bulgaria");
        
        /*
        Encuentros
        Bulgaria vs Italia 1 - 1
        Corea del Sur vs Bulgaria 1 - 1
        Corea del Sur vs Italia	2 - 3
        Argentina vs Corea del Sur 3 - 1
        Italia vs Argentina 1 - 1
        Argentina vs Bulgaria 2 - 0        
        */
        
        Grupo grupo = new Grupo();
                
        Partido bulgariaVsItalia = new Partido(new GregorianCalendar(1986, 4, 31).getTime(), bulgaria, italia);
        bulgariaVsItalia.setResultado(new Resultado(1,1));
        grupo.addPartido(bulgariaVsItalia);
        
        Partido coreaVsBulgaria = new Partido(new GregorianCalendar(1986, 5, 5).getTime(), corea, bulgaria);
        coreaVsBulgaria.setResultado(new Resultado(1,1));
        grupo.addPartido(coreaVsBulgaria);
        
        Partido coreaVsItalia = new Partido(new GregorianCalendar(1986, 5, 10).getTime(), corea, italia);
        coreaVsItalia.setResultado(new Resultado(2,3));
        grupo.addPartido(coreaVsItalia);
        
        Partido argentinaVsCorea = new Partido(new GregorianCalendar(1986, 5, 2).getTime(), argentina, corea);
        argentinaVsCorea.setResultado(new Resultado(3,1));
        grupo.addPartido(argentinaVsCorea);
        
        Partido argentinaVsItalia = new Partido(new GregorianCalendar(1986, 5, 5).getTime(), argentina, italia);
        argentinaVsItalia.setResultado(new Resultado(1,1));
        grupo.addPartido(argentinaVsItalia);
        
        Partido argentinaVsBulgaria = new Partido(new GregorianCalendar(1986, 5, 10).getTime(), argentina, bulgaria);
        argentinaVsBulgaria.setResultado(new Resultado(2,0));
        grupo.addPartido(argentinaVsBulgaria);
        
        List<Equipo> equiposQueAvanzanGrupo = grupo.getEquiposQueAvanzan();
        
        System.out.println("Equipos que avanzan del grupo:");
        for(Equipo equipo : equiposQueAvanzanGrupo) {
            System.out.println(equipo.getNombre());
        }
        
        // Cuartos de Final. Argentina vs Inglaterra 2-1
        Equipo inglaterra = new Equipo("Inglaterra");
        Llave llave = new Llave();
        
        Partido argentinaVsInglaterra = new Partido(new GregorianCalendar(1986, 5, 22).getTime(), argentina, inglaterra);
        argentinaVsInglaterra.setResultado(new Resultado(2,1));
        llave.addPartido(argentinaVsInglaterra);
        
        List<Equipo> equiposQueAvanzanLlave = llave.getEquiposQueAvanzan();
        
        System.out.println("Equipos que avanzan de la llave:");
        for(Equipo equipo : equiposQueAvanzanLlave) {
            System.out.println(equipo.getNombre());
        }
    }    
}