import time
import pygame
import random
import sys
from pygame.locals import *

'''
    PROYECTO PRESENTADO POR:
        Brandon David Palacio Alvarez
        Andrés Camilo Gaitán Jimenez
'''

''' EN ESTE APARTADO SE ENCONTRARÁN LAS VARIABLES DONDE SE CONFIGURAN LOS ASPECTOS BASICOS 
                    DE LA PANTALLA, LAS IMAGENES, LOS SONIDOS, ENTRE OTROS.'''

#Tamaño de la ventana:
widht_window = 600
height_window = 500

#Variables que se van a usar en el programa:
main_window = pygame.display.set_mode((widht_window, height_window))
elevation = height_window * 0.8
images = {}
sounds = {}
fps = 60
#Imagenes
pipe_image = 'graphics\\pipe.png'
player_image = 'graphics\\player.png'
background_image = 'graphics\\backgroundLevel4.png'
sealevel_image = 'graphics\\surface.png'
start_Text = 'graphics\\textoInicio.png'
name_text = 'graphics\\nombreJuego.png'
game_over_image = 'graphics\\gameOver.png'
score_text = 'graphics\scoreText.png'
#Sonido:
player_jump_sound = 'audio\\Jump.wav'
player_bump_sound = 'audio\\playerDead.wav'
win_sound = 'audio\\winSound.wav'

'''
    Nombre Funcion: bumppipesGame()
    Objetivo:       Función encargada de la ejecución del juego, además, es donde se generán todas las acciones y los obstaculos que 
                    haya dentro del juego, llama a la función de crear los obstaculos y la de game over, para juntarlos
                    en una sola función.
    Parametros:     No aplica.
    Retorno:        Retorna true si el juego termina y vuelve al menú principal.
    Ejemplo:        Al momento del Usuario apretar la barra espaciadora, esta función se llamará y empezará la ejecución del juego.
'''

def bumppipesGame():

    print('estoy en la otra funcion ')
    score = 0
    horizontal = int(widht_window/5)
    vertical = int(widht_window/2)
    ground = 0
    mytempheight = 100
  
    #Generacion de dos tubos en la ventana:
    first_pipe = createPipe()
    second_pipe = createPipe()
  
    #Lista que contiene los tubos de abajo:
    down_pipes = [
        {'x': widht_window + 300 - mytempheight,
         'y': first_pipe[1]['y']},
        {'x': widht_window + 300 - mytempheight + (widht_window/2),
         'y': second_pipe[1]['y']},
    ]
  
    #Lista que contiene los tubos de arriba:
    up_pipes = [
        {'x': widht_window + 300 - mytempheight,
         'y': first_pipe[0]['y']},
        {'x': widht_window + 200 - mytempheight + (widht_window/2),
         'y': second_pipe[0]['y']},
    ]
  
    #Velocidad de los tubos en el eje X:
    pipeVelX = -4
  
    #Velocidad de la nave en general:
    player_velocity_y = -9
    player_Max_Vel_Y = 10
    player_Min_Vel_Y = -8
    playerAccY = 1
  
    player_flap_velocity = -8
    player_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    pygame.mixer.Sound.play(sounds['jump'])
                    player_velocity_y = player_flap_velocity
                    player_flapped = True
  
        #Esta funcion retorna True si el jugador se choca:
        game_over = gameOver(horizontal,
                               vertical,
                               up_pipes,
                               down_pipes)
  
        #Puntaje:
        playerMidPos = horizontal + images['player'].get_width()/2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + images['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Puntaje: {score}")
  
        if player_velocity_y < player_Max_Vel_Y and not player_flapped:
            player_velocity_y += playerAccY
  
        if player_flapped:
            player_flapped = False
        playerHeight = images['player'].get_height()
        vertical = vertical + \
            min(player_velocity_y, elevation - vertical - playerHeight)
  
        #Movimiento de los tubos hacia la izquierda:
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):     #!ESTA FUNCION ME EMPAQUETA LOS DOS OBSTACULOS, TANTO SUPERIOR COMO SUPERIOR
            upperPipe['x'] += pipeVelX                             #!PARA QUE LOS OBSTACULOS SALGAN ALINEADOS.
            lowerPipe['x'] += pipeVelX
  
        #Añade otra tubería tan pronto la que esta al final se va:
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
  
        #Si la tuberia se sale de la pantalla se elimina con esta función:
        if up_pipes[0]['x'] < - images['pipe'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
  
        #Blit de las imagenes del juego:
        main_window.blit(images['background'], (0, 0))
        #Aca salen las imagenes de las tuberias aleatoriamente.
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            main_window.blit(images['pipe'][0],(upperPipe['x'], upperPipe['y']))
            main_window.blit(images['pipe'][1],(lowerPipe['x'], lowerPipe['y']))
  
        main_window.blit(images['sea_level'], (ground, elevation))
        main_window.blit(images['player'], (horizontal, vertical))

        if game_over:
            pygame.mixer.Sound.play(sounds['bump'])
            print('Game Over...')
            main_window.blit(images['game_over'],(20, 60))
            main_window.blit(images['score_text_img'],(140, 260))
            main_window.blit(images['scoreimages'][num],(280, 350))
            pygame.display.update()
            fps_clock.tick(fps)
            time.sleep(3)
            return
  
        #Obtención de digitos de la puntuación:
        numbers = [int(x) for x in list(str(score))]
        width = 0
  
        #Encontrar el tamaño de las imagenes del puntaje:
        for num in numbers:
            width += images['scoreimages'][num].get_width()
        Xoffset = (widht_window - width)/1.1
  
        #Colocando las imagenes en pantalla del puntaje:
        for num in numbers:
            main_window.blit(images['scoreimages'][num],(Xoffset, widht_window * 0.02))
            Xoffset += images['scoreimages'][num].get_width()
  
        #Refrescando la pantalla:
        pygame.display.update()
        fps_clock.tick(fps)

'''
    Nombre Funcion: gameOver()
    Objetivo:       Función encargada de finalizar el juego, y cerrar la función del juego.
    Parametros:     horizontal, vertical, up_pipes, down_pipes -> Encargados de formar los objetos tipo imagen dentro del juego para 
                    formar las colisiones con los objetos.
    Retorno:        Retorna true en caso tal de que haya alguna colisión contra lo obstáculos dentro de la función del juego, ya sea con
                    la roca superior o inferior
    Ejemplo:        Si el usuario se choca con alguno de los obstaculos, este retorna true y vuelve a la ventana de menú principal.
'''

def gameOver(horizontal, vertical, up_pipes, down_pipes):
    #Verificando que la nave esta por encima de la supercicie:
    if vertical > elevation - 25 or vertical < 0:
        return True

    #Verificando que la nave toca el tubo de arriba:
    for pipe in up_pipes:
        pipe_height = images['pipe'][0].get_height()
        if (vertical < pipe_height + pipe['y'] and abs(horizontal - pipe['x']) < images['pipe'][0].get_width()):
            print('Game over Arriba')
            return True

    #Verificando que la nave toca el tubo de abajo:
    for pipe in down_pipes:
        if (vertical + images['player'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < images['pipe'][0].get_width():
            print('Game over Abajo')
            return True
        return False

'''
    Nombre Funcion: createPipe()
    Objetivo:       Función encargada de crear las rocas y generar el movimiento en el eje X, además de generarlas aleatoriamente 
                    en una posición diferente en la pantalla mientras estas se van generando.
    Parametros:     No Aplica.
    Retorno:        Retorna un obstaculo en una posición aleatoria en la pantalla.
    Ejemplo:        Al momento de iniciar el juego, se verá como se empezarán a generar obstaculos aleatoriamente que se van 
                    acercando a la nave que el jugador esta controlando.
'''

def createPipe():
    offset = height_window/3
    pipe_height = images['pipe'][0].get_height()

    #Generador de tamaños aleatorios de tubos:
    y2 = offset + random.randrange(0, int(height_window - images['sea_level'].get_height() - 1.2 * offset))
    pipeX = widht_window + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        #Tubo que sale por arriba:
        {'x': pipeX, 'y': -y1},
        #Tubo que sale por abajo:
        {'x': pipeX, 'y': y2}
    ]
    return pipe

'''
    Nombre Funcion: funcion Principal
    Objetivo:       Encargada de manejar todas las imagenes que apareceran en pantalla y los sonidos, además de incluír el menú principal
                    antes de ingresar al juego.
    Parametros:     No Aplica.
    Retorno:        Menú principal.
    Ejemplo:        Cuando Iniciamos la aplicación aparecerá la pantalla principal, la cual me ingresará dentro del juego y recibirá
                    la primera orden del usuario, en este caso 'Espacio', si es así el juego llamará bumppipesGame() y el juego empezará
                    a ejecutarse.
'''

#FUnción principal:
if __name__ == "__main__":

    #Inicializacion de los modulos Pygame:
    pygame.init()
    pygame.mixer.init()
    fps_clock = pygame.time.Clock()

    #Título del juego:
    pygame.display.set_caption('Bumppipes.    Programado por: Brandon Palacio & Andres Gaitan')
    icon = pygame.image.load('graphics\\icon.png')
    pygame.display.set_icon(icon)

    #Carga de todas las imagenes que se van usar en el programa:
    #Imagenes que mostrarán el puntaje:
    images['scoreimages'] = (
        pygame.image.load('graphics\\0.png').convert_alpha(),
        pygame.image.load('graphics\\1.png').convert_alpha(),
        pygame.image.load('graphics\\2.png').convert_alpha(),
        pygame.image.load('graphics\\3.png').convert_alpha(),
        pygame.image.load('graphics\\4.png').convert_alpha(),        
        pygame.image.load('graphics\\5.png').convert_alpha(),
        pygame.image.load('graphics\\6.png').convert_alpha(),
        pygame.image.load('graphics\\7.png').convert_alpha(),
        pygame.image.load('graphics\\8.png').convert_alpha(),
        pygame.image.load('graphics\\9.png').convert_alpha()
    )
    images['player'] = pygame.image.load(player_image).convert_alpha()
    images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
    images['background'] = pygame.image.load(background_image).convert_alpha()
    images['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe_image).convert_alpha(), 180), pygame.image.load(pipe_image).convert_alpha())
    images['start_game'] = pygame.image.load(start_Text).convert_alpha()
    images['name_game'] = pygame.image.load(name_text).convert_alpha()
    images['game_over'] = pygame.image.load(game_over_image).convert_alpha()
    images['score_text_img'] = pygame.image.load(score_text).convert_alpha()
    #Carga de sonidos:
    sounds['jump'] = pygame.mixer.Sound(player_jump_sound)
    sounds['bump'] = pygame.mixer.Sound(player_bump_sound)

    print("BIENVENIDOS A BUMPPIPES GAME")
    print("Por favor, presiona espacio o entrar para iniciar el juego")

    #Inicialización del ciclo principal que mantiene el juego en ejecución:
    while True:
        #Establecer las coordenadas del jugador en pantalla:
        horizontal = int(widht_window/5)
        vertical = int((height_window - images['player'].get_height())/2)
        ground = 0
        while True:
            for event in pygame.event.get():
                #Cerrar ventana en caso de que el usuario le de en la X
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                #?SI EL USUARIO PRESIONA ESPACIO EL JUEGO EMPEZARÁ:
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):

                    pygame.mixer.Sound.play(sounds['jump'])
                    print('salto a la otra funcion ')
                    bumppipesGame()

                #?Si el usuario no presiona ninguna tecla, se quedará en la pantalla principal del juego:
                else:
                    main_window.blit(images['background'], (0, 0))
                    main_window.blit(images['player'], (horizontal, vertical))
                    main_window.blit(images['sea_level'], (ground, elevation))
                    main_window.blit(images['name_game'], (20, 60))
                    main_window.blit(images['start_game'], (100, 350))
                    pygame.display.update()
                    fps_clock.tick(fps)
            