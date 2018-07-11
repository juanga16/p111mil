package practica10.escuela;

public class TestPersona {

	public static void main(String[] args) {
		//ejercicio 4.4
		double [] descuentos = new double [4];
		descuentos[0]=7;
		descuentos[1]=10;
		descuentos[2]=5;
		descuentos[3]=2;
		
		Persona Persona1 = new Persona();
		Persona Persona2 = new Persona("Juan");
		Persona Persona3 = new Persona("Juan Pedro",65);
		Persona Persona4 = new Persona("Carlos", 45);
		
		Persona1.setSalario(1500 - (1500*descuentos[0]/100));
		Persona2.setSalario(890 - (890*descuentos[1]/100));
		Persona3.setSalario(500 - (500*descuentos[2]/100));
		Persona4.setEdad(5000);
		
		
		
		//ejercicio 4.5
		Persona[] personas = new Persona[4];
		personas[0]= Persona1;
		personas[1]= Persona2;
		personas[2]= Persona3;
		personas[3]= Persona4;
		
		
		for (int i=0; i<personas.length;i++)
			personas[i].setSalario(personas[i].getSalario() - (personas[i].getSalario()*descuentos[personas.length-i]/100));
			
		
	}

}
