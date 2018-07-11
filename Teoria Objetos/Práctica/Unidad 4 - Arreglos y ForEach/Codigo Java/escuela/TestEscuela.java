package practica10.escuela;

public class TestEscuela {

	public static void main(String[] args) {
		Alumno alumno = new Alumno("Fernandez", "Maria");
		String[] materias = new String[5];
		materias[0]="Matematica";
		materias[1]="Fisica";
		materias[2]="Lengua";
		materias[3]="Musica";
		materias[4]="Ed. Fisica";
		
		Boletin boletin = new Boletin(materias, alumno);
		
		boletin.addNota("Matematica", 5, 1);
		boletin.addNota("Fisica", 8, 2);
		boletin.addNota("Musica", 10, 3);
		
		System.out.println(alumno.getNombre() + " " + alumno.getApellido());
		
		for(String materia: materias)
			System.out.print(materia+"\t");
		
		System.out.println();
		
		for(int j=0; j<3; j++)
		{
			for (int i=0; i<materias.length;i++)
			{
				System.out.print(boletin.getNota(materias[i], j));
				System.out.print("\t");
			}
		   System.out.println();
		}

	}

}
