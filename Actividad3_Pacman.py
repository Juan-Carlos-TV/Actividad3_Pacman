from random import choice
from turtle import *
from freegames import floor, vector

#Comienza el score en 0
state = {'score': 0}

#Ni path ni la caja de texto son visibles
path = Turtle(visible=False)
writer = Turtle(visible=False)

#Movimiento inicial del pacman
aim = vector(5, 0)

#Posición inicial del Pacman
pacman = vector(-40, -80)

#Arreglo con las posiciones iniciales y movimientos iniciales
    #de cada fantasma
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

#Arreglo que representa el tablero.
    #Los 1 son los espacios por los cuales puede haber movimiento
    #Los 0 son espacios vacíos o paredes
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

#Función que dibuja un cuadrado dadas determinadas coordenadas
def square(x, y):
    "Draw square using path at (x, y)."
    #Toma la posición X y Y como punto de partida 
    path.up()
    path.goto(x, y)
    path.down()
    #Comienza el llenado
    path.begin_fill()

    #Al ser un cuadrado ejecuta el ciclo 4 veces
    for count in range(4):
        #Avanza 20 pixeles y gira 90°(360°/4) 
        path.forward(20)
        path.left(90)

    path.end_fill()

#Función que retornará el índice correspondiente a la casilla
    #del tablero donde se ubica terminada posición
def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

#Función que retorna un valor booleano dependiendo si determinda
    #posición es válida (una casilla donde se pueda mover)
    #dentro del tablero (>=1)
#Esta función será usada para comprobar que el siguiente movimiento
    #de pacman o los fantasmas no los saque del tablero
def valid(point):
    "Return True if point is valid in tiles."
    #Obtiene el índice en base a la ubicación del punto
    index = offset(point)

    #Verifica si es igual a 0, por lo cual la posición es invalida
    if tiles[index] == 0:
        return False
    
    #Obtiene el índice del punto desplazado en 19 px
    index = offset(point + 19)

    #Segunda verificación
    if tiles[index] == 0:
        return False

    #Retorna True si alguna de las coordenas es múltiplo de 20
    return point.x % 20 == 0 or point.y % 20 == 0

#Dibuja el tablero usando path
def world():
    "Draw world using path."
    #Establece el color del fondo como negro
    bgcolor('black')
    #Establece el color de path como azul
    path.color('blue')

    #Recorre cada uno de los elementos del arreglo del tablero
    for index in range(len(tiles)):
        tile = tiles[index]

        #Si el tile es mayor a 1
        if tile > 0:
            #Obtiene las coordenadas para dibujar el cuadrado
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            #Si la casilla tiene el valor de 1 se dibuja
                #el punto que podrá ser comido por pacman 
            if tile == 1:
                path.up()
                #Ubica el punto en el centro de la casilla
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

#Función encargada de ejecutar los movimientos de Pacman
    #y los fantasmas
def move():
    "Move pacman and all ghosts."
    #Deshace lo último escritoen writer y escribe
        #el score actual
    writer.undo()
    writer.write(state['score'])

    clear()

    #Si el siguiente movimiento de pacman es válido, lo mueve
    if valid(pacman + aim):
        pacman.move(aim)

    #Obtiene el índice de la posición de pacman
    index = offset(pacman)

    #Verifica si en la posición donde está pacman hay un 1
        #es decir, si hay un punto para comer
    if tiles[index] == 1:
        #Modifica el valor de la casilla para que siga siendo mayor
            #a 0 pero no contenga el punto
        tiles[index] = 2
        #Actualiza el score
        state['score'] += 1
        #Redibuja el cuadrado
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    #Coloca el punto medio de la casilla donde está pacman
        #y lo dibuja usando dot
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    #Recorre cada elemento del arreglo de fantasmas
    for point, course in ghosts:
        #Si el siguiente movimiento del fantasma es válido
            #continua movíendose
        if valid(point + course):
            point.move(course)
        else:
            #De otra manera, escogerá un moviento al azar
                #de la lista de opciones
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        #Toma la posición a la mitad de la casilla del fantastma
            #y lo dibuja usando dot
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    #Actualiza la imagen
    update()

    #Verifica que pacman no haya tocado a ninguno de los fantasmas
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            #De haberlo tocado, termina el juego
            return
    #Delay
    ontimer(move, 100)

#Función que actualiza el valor de aim
def change(x, y):
    "Change pacman aim if valid."
    #Si el movimiento dado es válido entonces realiza el cambio
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

#Establece el tamaño y la posición de la pantalla
setup(420, 420, 370, 0)
#Esconde el puntero de turtle
hideturtle()
#Esconde la linea de recorrido
tracer(False)
#Posiciona la caja de texto
writer.goto(160, 160)
#Establece el color del texto
writer.color('white')
#Escribe el score
writer.write(state['score'])

listen()
#Asigna un cambio de dirección a cada tecla
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
#Main loop
done()