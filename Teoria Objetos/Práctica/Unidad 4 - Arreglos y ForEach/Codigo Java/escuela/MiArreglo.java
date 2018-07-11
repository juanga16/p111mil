package practica10.escuela;

public class MiArreglo {
	

public static void main(String [] args){
	// ejercicio 1 a 
	char [] letras = new char [5];
	letras[0]='a';
	letras[1]='b';
	letras[2]='c';
	letras[3]='d';
	letras[4]='e';
	
	//ejercicio 1 b
	int [] numeros = new int [5];
	numeros[0]=5;
	numeros[1]=6;
	numeros[2]=7;
	numeros[3]=8;
	numeros[4]=9;
	
	//ejercicio 2 a
	
	int [] num_consecutivos = new int [1000];
	
	for (int i=0; i<num_consecutivos.length;i++)
		num_consecutivos[i]=i;
	
	for (int num: num_consecutivos)
		System.out.println("Valores: "+num);
	
	
	//ejercicio 2 b
	for (int num: num_consecutivos)
		System.out.println(num+5000);
	
	
	//ejercicio 2 c
	for (int num: num_consecutivos)
		System.out.println((num*2)+5000);
	
	//ejercicio 3
	
	String [] paises = new String [5];
	String [] copiaPaises = new String [6];
	int indice =0;
	paises[0]="Argentina";
	paises[1]="Brasil";
	paises[2]="Uruguay";
	paises[3]="Paraguay";
	paises[4]="Chile";
	
	for (;indice<paises.length; indice++)
		copiaPaises[indice]=paises[indice];
	
	copiaPaises[indice]="Bolivia";
	
}
	
}
