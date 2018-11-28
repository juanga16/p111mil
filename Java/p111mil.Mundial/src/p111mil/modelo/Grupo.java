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
public class Grupo extends EtapaMundial {
    // Listas paralelas para armar la tabla de posiciones
    List<Equipo> equiposGrupo;
    List<Integer> puntosEquipos;
    
    /**
     * Calcula la tabla de posiciones y retorna los dos equipos clasificados
     * @return Lista de equipos
     */
    @Override
    public List<Equipo> getEquiposQueAvanzan() {
        // Inicializo las listas
        equiposGrupo = new ArrayList<Equipo>();
        puntosEquipos = new ArrayList<Integer>();
        
        // Recorro todos los partidos para generar una lista con todos los equipos
        for(Partido partido : this.getPartidos()) {
            addEquipoEnListaSiNoExiste(partido.getLocal());
            addEquipoEnListaSiNoExiste(partido.getVisitante());
        }
        
        // Recorro los equipos y sumo en la lista paralela los puntos segun el resultado
        for(int i=0; i < equiposGrupo.size(); i++) {
            for(Partido partido : this.getPartidos()) {
                if (equiposGrupo.get(i).getNombre().equals(partido.getLocal().getNombre())) {
                    if (partido.getResultado().ganoLocal()) {
                        puntosEquipos.set(i, puntosEquipos.get(i) + 3);
                    } else if (partido.getResultado().empate()) {
                        puntosEquipos.set(i, puntosEquipos.get(i) + 1);
                    }                    
                } else if (equiposGrupo.get(i).getNombre().equals(partido.getVisitante().getNombre())) {
                    if (partido.getResultado().empate()) {
                        puntosEquipos.set(i, puntosEquipos.get(i) + 1);
                    } else if (! partido.getResultado().ganoLocal()) {
                        puntosEquipos.set(i, puntosEquipos.get(i) + 3);
                    }
                }
            }
        }
        
        ordenarPosiciones();

        // Retornamos los primeros dos equipos segun las posiciones
        return equiposGrupo.subList(0, 2);
    }
    
    /**
     * Se fija si el equipo no fue todavia agregado en la lista interna y de ser asi lo agrega.
     * Si el equipo ya existe no hace nada
     * @param equipoParaAgregar 
     */    
    private void addEquipoEnListaSiNoExiste(Equipo equipoParaAgregar) {
        for(Equipo equipoExistente : equiposGrupo) {
            if (equipoExistente.getNombre().equals(equipoParaAgregar.getNombre())) {
                return;
            }
        }
        
        equiposGrupo.add(equipoParaAgregar);
        puntosEquipos.add(0);
    }
        
    /**
     * Ordena las listas paralelas de puntos y de equipos segun los puntos en forma descendente
     */
    private void ordenarPosiciones() {
        for(int j = 0; j < puntosEquipos.size(); j++){
            for(int i = j + 1; i < puntosEquipos.size(); i++){
                if(puntosEquipos.get(i) > puntosEquipos.get(j)){
                    int puntos = puntosEquipos.get(j);
                    puntosEquipos.set(j, puntosEquipos.get(i));
                    puntosEquipos.set(i, puntos);
                    
                    Equipo equipo = equiposGrupo.get(j);
                    equiposGrupo.set(j, equiposGrupo.get(i));
                    equiposGrupo.set(i, equipo);                    
                }
            }
        }
    }
}
