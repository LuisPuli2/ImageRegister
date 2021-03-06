from PIL import Image
import random

# Variables globales.
# Arreglo de individuos.
poblacion = []
# Tamaño horizontal de la imagen en pixéles.
tam_horizontal = 0
# Tamaño vertical de la imagen en pixeles.
tam_vertical = 0
# La imagen inicial
source = None
# La imagen a la que se quiere llegar 
target = None


# Clase para representar las tripletas (individuos) del AG.
class Individuo:
	# Valores iniciales.
	angulo = 0
	desp_x = 0
	desp_y = 0

	# Constructor.
	def __init__(self,angulo,desp_x,desp_y):
		self.angulo = angulo
		self.desp_x = desp_x
		self.desp_y = desp_y

	# Método para imprimir en consola.
	def toString(self):
		return "["+ str(self.angulo) + "," + str(self.desp_x) +"," + str(self.desp_y) + "]"

# Fin de clase Individuo.

# El algoritmo genético.
def AG ():
	# Las generaciones que tendremos.
	generaciones = 0
	# Ciclo principal.
	while generaciones < 40:
		# Seleccionamos a los padres para cruzarlos.
		padres = selecciona_padres()
		# Los indices de los padres, para buscarlo en los arreglos.
		i = padres[0]
		j = padres[1]
		# Debug.
		# print("Padres: " + poblacion[i].toString() + ","+ poblacion[j].toString())
		# Los cruzamos
		hijos = cruza(poblacion[i],poblacion[j])
		# Seleccionamos a los individuos para eliminarlos.
		peores = selecciona_peores()
		# Reutilizamos las variables de los índices.
		i = peores[0]
		j = peores[1]
		# Debug.
		# print("Eliminados: " + poblacion[i].toString() + ","+ poblacion[j].toString())
		# Sustituimos a los nuevos pobladores (hijos).
		poblacion[i] = hijos[0]
		poblacion[j] = hijos[1]
		# Se muta con probabilidad 1/5 a los nuevos pobladores.
		if hayQueMutar():
			# print("Antes de la mutación: " + poblacion[i].toString())
			muta (poblacion[i])
			# print("Después de la mutación: " + poblacion[i].toString())
		# Lo mismo para el otro hijo
		if hayQueMutar():
			# print("Antes de la mutación: " + poblacion[j].toString())
			muta (poblacion[j])
			# print("Después de la mutación: " + poblacion[j].toString())
		# Debug.
		# print("Nuevos: " + poblacion[i].toString() + ","+ poblacion[j].toString())
		# Aumentamos en uno la generación
		generaciones += 1
		Image.blend(target,source.rotate(generaciones*10),.5).show()


# Genera un número aleatorio entre 0 y 359 para representar el ángulo.
def angulo_aleatorio ():
	return random.uniform(0,360)

# Genera un número aleatorio entre 0 y el tamaño horizontal de la imagen.
def x_aleatorio ():
	return random.randint(0,tam_horizontal)

# Genera un número aleatorio entre 0 y el tamaño horizontal de la imagen.
def y_aleatorio ():
	return random.randint(0,tam_vertical)

# Regresa true con probabilidad 1/5
def hayQueMutar():
	aleatorio = random.randint(1,5)
	return aleatorio == 1

# Calcula la función fitness de un individuo.
def fitness (individuo):
	# Imagen temporal bajo la transformación inducida por el individuo para calcular el fitness.
	temp = source.rotate(individuo.angulo)
	# Falta desplazarla
	# Accedemos a la matriz de pixéles de ambas imágenes.
	pixel_temp = temp.load()
	pixel_target = target.load()
	# La suma de las diferencias de los pixéles.
	suma = 0
	# Iteramos sobre cada pixel y comparamos.
	for i in range(0,source.size[0]):
		for j in range(0,source.size[1]):
			# Si los pixéles en la posciión (i,j) son diferentes.
			suma += diferencia(pixel_target[i,j],pixel_temp[i,j])
	# 1/2 de la suma total
	return suma*(.5)

# Calcula la "diferencia" entre dos pixéles.
def diferencia (pixel_1,pixel_2):
	diferencia = 0
	# Calcula la diferencia entre cada color(R,G,B).
	for i in range(0,len(pixel_1)):
		# El valor absoluto de la resta.
		diferencia += abs(pixel_1[i] - pixel_2[i])
	# Regresa la diferencia al cuadrado
	return diferencia**2

# Regresa el mejor individuo de la población.
def selecciona_mejor():
	best = 10000000
	index = 0
	for i in range(0,len(poblacion)):
		fit = fitness(poblacion[i])
		if fit < best:
			best = fit
			index = i
	return i
# Selecciona dos individuos para cruzarlos utilizando implementación por ruleta.
def selecciona_padres():
	# Un arreglo que simulará a la ruleta
	ruleta = [None]*len(poblacion)
	# Llenamos el arreglo.
	for i in range(0,len(ruleta)):
		# Si se encontró el óptimo.
		if fitness(poblacion[i]) == 0:
			print("Se encontró el óptimo! ángulo: " + str(poblacion[i].angulo))
			source.rotate(poblacion[i].angulo).show()
			return
		# Para no salirse del arreglo.
		if i != 0:
			ruleta[i] = 1/fitness(poblacion[i]) + ruleta[i-1]
		else:
			ruleta[i] = 1/fitness(poblacion[i])

	# Guardará la suma de cada entrada de la ruleta
	total = ruleta[len(ruleta)-1] 
	# Los padres que vamos a regresar
	padres = [None]*2
	# Para el primer padre.
	aleatorio = random.uniform(0,total)
	# Vemos donde cae el aleatorio, para seleccionar al padre.	
	for i in range(0,len(ruleta)):
		# Si el aleatorio cae dentro del rango
		if ruleta[i] >= aleatorio:
			padres[0] = i
			break
	# Para el segundo padres
	aleatorio = random.uniform(0,total)
	# Vemos donde cae el aleatorio, para seleccionar al padres.	
	for i in range(0,len(ruleta)):
		# Si el aleatorio cae dentro del rango
		if ruleta[i] >= aleatorio:
			padres[1] = i
			break
	# Para evitar repetidos.
	while(padres[1] == padres[0]):
		aleatorio = random.uniform(0,total)
		# Vemos donde cae el aleatorio, para seleccionar al padres.	
		for i in range(0,len(ruleta)):
			# Si el aleatorio cae dentro del rango
			if ruleta[i] >= aleatorio:
				padres[1] = i
				break

	return padres

# Selecciona dos individuos para eliminarlos utilizando implementación por ruleta.
def selecciona_peores():
	# Un arreglo que simulará a la ruleta
	ruleta = [None]*len(poblacion)
	# Llenamos el arreglo.
	for i in range(0,len(ruleta)):
		# Para no salirse del arreglo.
		if i != 0:
			ruleta[i] = fitness(poblacion[i]) + ruleta[i-1]
		else:
			ruleta[i] = fitness(poblacion[i])

	# Guardará la suma de cada entrada de la ruleta
	total = ruleta[len(ruleta)-1] 
	# Los padres que vamos a regresar
	peores = [None]*2
	# Para el primer padre.
	aleatorio = random.uniform(0,total)
	# Vemos donde cae el aleatorio, para seleccionar al padre.	
	for i in range(0,len(ruleta)):
		# Si el aleatorio cae dentro del rango
		if ruleta[i] >= aleatorio:
			peores[0] = i
			break
	# Para el segundo peores
	aleatorio = random.uniform(0,total)
	# Vemos donde cae el aleatorio, para seleccionar al peores.	
	for i in range(0,len(ruleta)):
		# Si el aleatorio cae dentro del rango
		if ruleta[i] >= aleatorio:
			peores[1] = i
			break
	# Para evitar repetidos.
	while(peores[1] == peores[0]):
		aleatorio = random.uniform(0,total)
		# Vemos donde cae el aleatorio, para seleccionar al peores.	
		for i in range(0,len(ruleta)):
			# Si el aleatorio cae dentro del rango
			if ruleta[i] >= aleatorio:
				peores[1] = i
				break
	return peores

# Inicializa una población aleatoria de n individuos.
def inicializa_poblacion (n):
	# Inicializamos el arreglo.
	global poblacion
	poblacion = [None]*n
	for i in range(0,n):
		# Creación de un individuo aleatorio.
		poblacion[i] = Individuo(angulo_aleatorio(),x_aleatorio(),y_aleatorio())

# Abre las imágenes a procesar
def inicializa_imagenes ():
	# Imagen a transformar
	#nombre_s = input('Ingresa el nombre de la imagen a transformar: ')
	# Imagen objetivo
	#nombre_t =  input('Nombre de la imagen objetivo: ')
	nombre_s = "rubio.png"
	nombre_t = "rotado.png"
	# Para manejar excepciones
	try:
		# Trata de abrir las imágenes.
		global source
		source = Image.open(nombre_s)
		global target
		target = Image.open(nombre_t)
		# Inicializamos valores de los tamaños de la imagen.
		# global tam_horizontal 
		#tam_horizontal = source.size[1] 
		# global tam_vertical
		#tam_vertical = source.size[2]
	# Si se genera una excepción, la cachamos.
	except:
		print("No pude abrir las imágenes, revisa los nombres.")
		# Intentamos de nuevo.
		inicializa_imagenes()

# Aplica el operador de cruza de dos individuos.
def cruza (padre_1,padre_2):
	# Se crea un número aleatorio para ver el punto de cruce.
	aleatorio = random.randint(1,4)
	# Modificamos el ángulo.
	if aleatorio == 1:
		hijo_1 = Individuo(padre_2.angulo,padre_1.desp_x,padre_1.desp_y)
		hijo_2 = Individuo(padre_1.angulo,padre_2.desp_x,padre_2.desp_y)
	# Modificamos el desplazamiento en x.
	elif aleatorio == 2:
		hijo_1 = Individuo(padre_1.angulo,padre_2.desp_x,padre_1.desp_y)
		hijo_2 = Individuo(padre_2.angulo,padre_1.desp_x,padre_2.desp_y)
	# Modificamos el desplazamiento en y.
	else: 
		hijo_1 = Individuo(padre_1.angulo,padre_1.desp_x,padre_2.desp_y)
		hijo_2 = Individuo(padre_2.angulo,padre_2.desp_x,padre_1.desp_y)

	return [hijo_1,hijo_2] 


# Aplica el operador de mutación a un individuo en cualquiera de sus tres valores (Ángulo,Desp_X,Desp_Y).
def muta (individuo):
	# Creamos un número aleatorio entre 1 y 3 para saber que entrada modificar.
	aleatorio = random.randint(1,3)
	# Creamos un epsilon para realizar la mutación
	epsilon = random.uniform(-1,-1)
	# Modificamos el ángulo.
	if aleatorio == 1:
		individuo.angulo += epsilon
	# Modificamos el desplazamiento en x.
	elif aleatorio == 2:
		individuo.desp_x += epsilon
	# Modificamos el desplazamiento en y.
	else: 
		individuo.desp_y += epsilon

# Aplica el operador de reemplazo.
def remplaza (hijo_1,hijo_2):
	print("Dick")


# Método principal
def main ():
	# Abre imágenes
	inicializa_imagenes()
	# Crea la población
	inicializa_poblacion(30)
	# Debug
	selecciona_padres()
	# Algoritmo Genpetico
	AG();


if __name__ == '__main__':
	main()
	# Parametros de pruebirri
	"""	
	tam_vertical = 100
	tam_horizontal = 100
	incializa_poblacion(100);
	i = Individuo()
	print(i.desp_x)
	best_angle = 0
	
	#Ángulo que corre de 0 a 359 grados
	for angulo in range(50,59):
		new = source.rotate(angulo)
		pixel_s = new.load()
		contador = 0
		for i in range(0,source.size[0]):
			for j in range(0,source.size[1]):
				# Si son diferentes
				if pixel_t[i,j] != pixel_s[i,j]:
					contador += 1
		
		if contador < minimo:
			print("Se econtró uno nuevo minimo, anterior: "+ str(minimo)+ " actual: " + str(contador) + " con valor del ángulo: " + str(angulo))
			minimo = contador
			best_angle = angulo
	

	Image.blend(target, source.rotate(90),.5).show()

	#alpha = 0.0
	#out = target * (1.0 - alpha) + target * alpha
		# print("Con " + str(angulo)  + " tiene " + str(contador))
	# im.show()
	#new.show()
	#new.save("Prueba.jpg")
	#new.save("Liz","JPG")
	#im.rotate(45).show()

	"""