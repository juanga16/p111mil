package edu.unicen.poo111mil;

import java.util.ArrayList;
import java.util.Iterator;

public class ListaContactos {
	
	private ArrayList<Contacto> contactos = new ArrayList<>();
	
	public void agregarContacto(Contacto c) {
		this.contactos.add(c);
	}
	
	public void borrarContacto(Contacto c) {
		this.contactos.remove(c);
	}
	
	public void mostrarContactos(){
		for(Contacto c: this.contactos)
			System.out.println(c);
	}
	
	public int cantContactos() {
		return this.contactos.size();
	}
	
	public double promedioEdad(){ //uso double para más precisión
		double resultado = 0.0d;
		for(Contacto c: this.contactos)
			resultado += c.getEdad();
		return resultado/this.cantContactos();
	}
	
	public ArrayList<ArrayList<Contacto>> repetidos(){
		//Creo el retorno
		ArrayList<ArrayList<Contacto>> resultado = new ArrayList<>();
		//Creo una copia para llevar control de que contactos procese y descarte
		//como repetidos, sin tener que modificar el atributo. 
		ArrayList<Contacto> aux = new ArrayList<>(this.contactos); 
		//Mientras no haya terminado de procesar
		while(!aux.isEmpty()) {
			//extraigo el contacto a procesar
			Contacto aProcesar = aux.remove(0);
			//Creo un auxiliar para ir llevando los repetidos
			ArrayList<Contacto> repetidos = new ArrayList<>();
			repetidos.add(aProcesar); //agrego el que estoy procesando
			//Ahora voy procesando los contactos restantes
			//uso un iterador porq es la forma más facil de eliminar y
			//recorrer al mismo tiempo
			Iterator<Contacto> it = aux.iterator();
			while(it.hasNext()) { //mientras tenga siguiente
				Contacto siguiente = it.next(); //lo obtengo
				if (aProcesar.repetido(siguiente)) {
					//Si es repetido lo agrego a la lista de repetidos
					repetidos.add(siguiente);
					//Además lo considero procesado, por lo que lo remuevo 
					//del auxiliar
					it.remove();
				}
			}
			//Si la lista de repetidos tiene más de un elemento, significa que
			//hay repetidos, por lo que es parte de nuestro retorno
			resultado.add(repetidos);
		}
		return resultado;
	}
	
	/*
	 * Código muy similar al anterior. Queda  como propuesta
	 * usar herencia para unificarlos.
	 */
	public ArrayList<ArrayList<Contacto>> telefonoRepetido(){
		//Creo el retorno
		ArrayList<ArrayList<Contacto>> resultado = new ArrayList<>();
		//Creo una copia para llevar control de que contactos procese y descarte
		//como repetidos, sin tener que modificar el atributo. 
		ArrayList<Contacto> aux = new ArrayList<>(this.contactos); 
		//Mientras no haya terminado de procesar
		while(!aux.isEmpty()) {
			//extraigo el contacto a procesar
			Contacto aProcesar = aux.remove(0);
			//Creo un auxiliar para ir llevando los repetidos
			ArrayList<Contacto> repetidos = new ArrayList<>();
			repetidos.add(aProcesar); //agrego el que estoy procesando
			//Ahora voy procesando los contactos restantes
			//uso un iterador porq es la forma más facil de eliminar y
			//recorrer al mismo tiempo
			Iterator<Contacto> it = aux.iterator();
			while(it.hasNext()) { //mientras tenga siguiente
				Contacto siguiente = it.next(); //lo obtengo
				if (aProcesar.getNumeroTel().equals(siguiente.getNumeroTel())) {
					//Si es repetido lo agrego a la lista de repetidos
					repetidos.add(siguiente);
					//Además lo considero procesado, por lo que lo remuevo 
					//del auxiliar
					it.remove();
				}
			}
			//Si la lista de repetidos tiene más de un elemento, significa que
			//hay repetidos, por lo que es parte de nuestro retorno
			resultado.add(repetidos);
		}
		return resultado;
	}
}
