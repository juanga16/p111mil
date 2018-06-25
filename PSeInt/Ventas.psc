Algoritmo RegistroDeVentas
	Definir cantidadDeVentas Como Entero
	Definir totalVendido Como Entero
	Definir venta Como Entero
	Definir mayorVenta como Entero
	
	cantidadDeVentas <- -1
	totalVendido <- 0
	mayorVenta <- 0
	
	Repetir
		Escribir "Ingrese la venta"
		Leer venta
		
		cantidadDeVentas <- cantidadDeVentas + 1
		totalVendido <- totalVendido + venta
		
		Si venta > mayorVenta Entonces
			mayorVenta <- venta			
		FinSi
	Hasta Que venta <= 0
	
	Escribir "Cantidad de ventas: ", cantidadDeVentas
	Escribir "Total vendido: ", totalVendido
	Escribir "Mayor venta: ", mayorVenta
FinAlgoritmo
