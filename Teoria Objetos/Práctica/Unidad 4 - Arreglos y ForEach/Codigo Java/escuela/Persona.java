package practica10.escuela;


//ejercicio 4
public class Persona {
	
	private String nombre;
	private int edad;
	private double salario;
	
	
	public double getSalario() {
		return salario;
	}

	public void setSalario(double salario) {
		this.salario = salario;
	}

	public Persona()
	{
		this.nombre="Maria";
		this.edad=30;
	
		
	}
	
	public Persona(String name)
	{
		this.nombre=name;
		this.edad=30;
		
	}
	
	public Persona(String name, int age)
	{
		this.nombre=name;
		this.edad=age;
		
	}
	

	public String getNombre() {
		return nombre;
	}

	public void setNombre(String nombre) {
		this.nombre = nombre;
	}

	public int getEdad() {
		return edad;
	}

	public void setEdad(int edad) {
		this.edad = edad;
	}

	public static void main(String[] args) {
		
		//ejercicio 4.1
		Persona Persona1 = new Persona();
		Persona Persona2 = new Persona("Juan");
		Persona Persona3 = new Persona("Juan Pedro",65);
		System.out.println(Persona1.getNombre() + " - " + Persona1.getEdad());
		System.out.println(Persona2.getNombre() + " - " + Persona2.getEdad());
		System.out.println(Persona3.getNombre() + " - " + Persona3.getEdad());
		
		//ejercicio 4.2
		
		Persona [] personas = new Persona [3];
		for (Persona p: personas)
			System.out.println(p.getNombre() + " - " + p.getEdad());
		
		//ejercicio 4.3
		Persona1.setSalario(1500);
		Persona2.setSalario(890);
		Persona3.setSalario(500);
		
		

	}

}
