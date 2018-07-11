package practica10.escuela;

public class Boletin {
	private int[][] notas;
	private String [] materias;
	private Alumno alumno;
	
	public Boletin ()
	{
		this.notas = new int [12][3];
		this.materias = new String [12];
		this.alumno = new Alumno("Perez", "Juan");
	}
	
	public Boletin (String[] materias, Alumno alumno)
	{
		this.notas = new int [3][materias.length];
		this.materias = materias;
		this.alumno = alumno;
	}

	public int[][] getNotas() {
		return notas;
	}

	public void setNotas(int[][] notas) {
		this.notas = notas;
	}

	public String[] getMaterias() {
		return materias;
	}

	public void setMaterias(String[] materias) {
		this.materias = materias;
	}

	public Alumno getAlumno() {
		return alumno;
	}

	public void setAlumno(Alumno alumno) {
		this.alumno = alumno;
	}

	public void addNota(String materia, int nota, int trimestre)
	{
		boolean encontrada=false;
		int nroMateria =0;
		for(; nroMateria<this.materias.length && !encontrada;nroMateria++)
			if(this.materias[nroMateria].equals(materia))
				encontrada=true;
		
		this.notas[trimestre-1][nroMateria] =nota;
	}
	
	public int getNota (String materia, int trimestre)
	{
		boolean encontrada=false;
		int nroMateria =0;
		for(; nroMateria<this.materias.length && !encontrada;nroMateria++)
			if(this.materias[nroMateria].equals(materia))
				encontrada=true;
		
		 if (nroMateria<this.materias.length)
			return this.notas[trimestre][nroMateria];
		 else return 0;
	}
	
}
