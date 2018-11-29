/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.modelo;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Invitado
 */
public class Llave extends EtapaMundial {

    @Override
    public List<Equipo> getEquiposQueAvanzan() {
        List<Equipo> equipos = new ArrayList<Equipo>();
        
        if (this.getPartidos().size() > 0) {
            Partido partido = this.getPartidos().get(0);
            
            if (partido.getResultado().ganoLocal()) {
                equipos.add(partido.getLocal());
            } else {
                equipos.add(partido.getVisitante());
            }
        }
        
        return equipos;
    }    
}
