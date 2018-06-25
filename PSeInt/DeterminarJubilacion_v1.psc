Algoritmo DeterminarJubilacion_v1
	jubilacionHombre <- 67
	jubilacionMujer <- 60
	
	Escribir 'Ingrese su sexo (M o F)'
	Leer sexo
	
	Escribir 'Ingrese su edad'
	Leer edad
	
	si sexo = 'F'
		si edad >= jubilacionMujer
			Escribir 'Usted ya puede jubilarse'
		SiNo
			Escribir 'A usted le faltan ' jubilacionMujer - edad ' años para jubilarse'
		FinSi
	SiNo 
		si edad >= jubilacionHombre
			Escribir 'Usted ya puede jubilarse'
		SiNo
			Escribir 'A usted le faltan ' jubilacionMujer - edad ' años para jubilarse'
		FinSi		
	FinSi
	
FinAlgoritmo
