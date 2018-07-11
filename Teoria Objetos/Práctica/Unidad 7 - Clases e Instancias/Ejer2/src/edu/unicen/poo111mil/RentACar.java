package edu.unicen.poo111mil;

public class RentACar {
	private Auto autos[];
	
	public RentACar(Auto[] autos){
		this.autos = autos;
	}
	
	public boolean alquilarAuto(Cliente cliente, int auto, int dias) {
		return this.autos[auto].alquilar(cliente,dias);
	}
	
	public double liquidarAlquiler(int auto){
		return autos[auto].liquidar();
	}
	
	public boolean retornarAuto(Cliente cliente, int auto, int dias) {
		return this.autos[auto].retornar();
	}
	
	public void setAuto(int pos, Auto auto) { 
		this.autos[pos] = auto;
	}
	
	public Auto getAuto(int pos) {
		return this.autos[pos];
	}
}
