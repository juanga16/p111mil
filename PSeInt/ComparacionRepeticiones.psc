Algoritmo sin_titulo
	// Para
	// 0 a N iteraciones	
	Para i<-1 Hasta 10 Con Paso -1 Hacer		
		//Escribir  "Iteracion Para: ", i;
	Fin Para
	
	// Mientras
	// 0 a N iteraciones
	definir j como entero
	j <- 0
	
	Mientras j <= 10 Hacer
		//Escribir  "Iteracion Mientras: ", j;		
		j <- j + 1;
	Fin Mientras
	
	// Otro ejemplo
	
	Definir totalGastado como entero
	Definir gasto como entero
	Definir cantidadDeGastos como entero
	presupuesto <- 500;
	totalGastado <- 501;
	cantidadDeGastos <- 0;
	
	Mientras totalGastado <= 500 Hacer
		Escribir  "Cuanto te patinaste?: "
		Leer gasto
		
		totalGastado = totalGastado + gasto;
		cantidadDeGastos <- cantidadDeGastos + 1;
	Fin Mientras
	
	//Escribir "Este mes saliste: ", cantidadDeGastos, " veces";
	
	// Hasta
	// 1 a N iteraciones
	Definir totalFactura Como Real
	
	Repetir
		Escribir "Ingrese el total de la factura: ";
		Leer totalFactura
		
		Definir iva como real
		iva <- totalFactura * 21 / 100
		
		Escribir iva
	Hasta Que totalFactura <= 0
	
	
	Escribir "Fin";
FinAlgoritmo
