/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package p111mil.modelo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 *
 * @author Invitado
 */
public class Grupo extends EtapaMundial {

    @Override
    public List<Equipo> getEquiposQueAvanzan() {
        Map<Equipo, Integer> equipos = new HashMap<Equipo, Integer>();
        
        for(Partido partido : this.getPartidos()) {
            Resultado resultado = partido.getResultado();
            
            if (resultado.ganoLocal()) {
                agregarPuntos(equipos, partido.getLocal(), 3);
            } else if (resultado.empate()) {
                agregarPuntos(equipos, partido.getLocal(), 1);
                agregarPuntos(equipos, partido.getVisitante(), 1);
            } else {
                agregarPuntos(equipos, partido.getVisitante(), 3);
            }
        }
        
        return obtenerEquiposQueAvanzan(equipos);
    }
    
    private void agregarPuntos(Map<Equipo, Integer> equipos, Equipo equipo, int puntos) {
        if (equipos.containsKey(equipo)) {
            equipos.put(equipo, equipos.get(equipo) + puntos);
        } else {
            equipos.put(equipo, puntos);
        }
    }
    
    private List<Equipo> obtenerEquiposQueAvanzan(Map<Equipo, Integer> equipos) {
        // Obtengo el equipo que gano el grupo
        Equipo primero = null;
        int puntosPrimero = 0;
        for (Map.Entry<Equipo, Integer> equipo : equipos.entrySet()) {
            if (equipo.getValue() > puntosPrimero) {
                primero = equipo.getKey();
                puntosPrimero = equipo.getValue();
            }
        }
        
        Equipo segundo = null;
        int puntosSegundo = 0;
        for (Map.Entry<Equipo, Integer> equipo : equipos.entrySet()) {
            if (equipo.getValue() > puntosSegundo && equipo.getValue() != puntosPrimero) {
                segundo = equipo.getKey();
                puntosSegundo = equipo.getValue();
            }
        }
        
        List<Equipo> equiposQueAvanzan = new ArrayList<Equipo>();
        equiposQueAvanzan.add(primero);
        equiposQueAvanzan.add(segundo);
        
        return equiposQueAvanzan;
    }
}
