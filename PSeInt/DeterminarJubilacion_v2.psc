Algoritmo DeterminarJubilacion_v1
	jubilacionHombre <- 67
	jubilacionMujer <- 60
	
	Escribir 'Ingrese su sexo (M o F)'
	Leer sexo
	
	Escribir 'Ingrese su edad'
	Leer edad
	
	edadJubilacion <- jubilacionMujer
	si sexo = 'F'
		edadJubilacion <- jubilacionHombre
	FinSi
	
	si edad >= edadJubilacion
		Escribir 'Usted ya puede jubilarse'
	SiNo
		Escribir 'A usted le faltan ' edadJubilacion - edad ' años para jubilarse'
	FinSi	
	
FinAlgoritmo
