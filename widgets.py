import pygame

# Funciones para dibujar elementos de forma automática
# Dibujar todos los elementos dentro de una lista
def dibujarObjetos(pantalla, objetos):
    for objeto in objetos:
        objeto.dibujar(pantalla)

# Vaciar una lista de todos sus elementos
def vaciarObjetos(objetos):
    objetos.clear()

# Eliminar un elemento de una lista
def eliminarObjeto(objetos, objeto):
    objetos.remove(objeto)

# Agregar un elemento a una lista
def agregarObjeto(objetos, objeto):
    objetos.append(objeto)

# Agregar un grupo de elementos (lista) a una lista
def agregarGrupo(objetos, grupo):
    for objeto in grupo:
        objetos.append(objeto)

# Clase para crear y modificar un botón
class Boton:
    # Inicializar botón y datos pertenecientes a él
    def __init__(self, objetos, texto, posX, posY, largo=50, alto=25, color=(200,200,200), tamanoFuente=25, colorTexto=(0,0,0)):
        # Ubicación del botón en la ventana
        self.posX = posX
        self.posY = posY
        # Dimensiones del botón
        self.largo = largo
        self.alto = alto
        # Creación del rectángulo que servirá para el botón
        self.rect = pygame.Rect(self.posX, self.posY, self.largo, self.alto)
        # Color del botón
        self.color = color
        # Tamaño de la fuente
        self.tamanoFuente = tamanoFuente
        # Creación de la fuente
        self.fuente = pygame.font.SysFont('calibri', self.tamanoFuente)
        # Color del texto
        self.colorTexto = colorTexto
        # Contenido del texto
        self.texto = texto
        # Etiqueta para mostrar el texto
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

        # Agregar el botón a una lista
        agregarObjeto(objetos, self)

    # Cambiar el color del botón
    def cambiarColor(self, color):
        self.color = color

    # Cambiar el color del texto
    def cambiarColorTexto(self, colorTexto):
        self.colorTexto = colorTexto
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

    # Cambiar el contenido del texto
    def cambiarTexto(self, texto):
        self.texto = texto
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

    # Cambiar el tamaño de la fuente
    def cambiarTamanoFuente(self, tamanoFuente):
        self.tamanoFuente = tamanoFuente
        self.fuente = pygame.font.SysFont('calibri', self.tamanoFuente)
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

    # Cambiar la posición del botón en la ventana
    def cambiarPosicion(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.rect = pygame.Rect(self.posX, self.posY, self.largo, self.alto)

    # Cambiar las dimensiones del botón
    def cambiarDimensiones(self, largo, alto):
        self.largo = largo
        self.alto = alto
        self.rect = pygame.Rect(self.posX, self.posY, self.largo, self.alto)

    # Dibujar el botón
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pantalla.blit(self.etiqueta, self.etiqueta.get_rect(center = self.rect.center))

    # Eliminar boton de una lista
    def eliminar(self, objetos):
        eliminarObjeto(objetos, self)

    # Agregar el botón a una lista
    def agregar(self, objetos):
        agregarObjeto(objetos, self)

# Clase para crear y modificar un cuadro de texto
class CuadroTexto:
    # Inicializar cuadro de texto y datos pertenecientes a él
    def __init__(self, objetos, posX, posY, largo=50, alto=25, color=(255,255,255), tamanoFuente=25, colorTexto=(0,0,0)):
        # Estado del cuadro de texto
        self.activo = False
        # Posición del cuadro de texto en la ventana
        self.posX = posX
        self.posY = posY
        # Dimensiones del cuadro de texto
        self.largo = largo
        self.alto = alto
        # Creación del rectángulo que servirá para el cuadro de texto
        self.rect = pygame.Rect(self.posX, self.posY, self.largo, self.alto)
        # Color del cuadro de texto
        self.color = color
        # Tamaño de la fuente
        self.tamanoFuente = tamanoFuente
        # Creación de la fuente
        self.fuente = pygame.font.SysFont('calibri', self.tamanoFuente)
        # Color del texto
        self.colorTexto = colorTexto
        # Contenido del texto
        self.texto = ''
        # Etiqueta para mostrar el texto
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

        # Agregar el cuadro de texto a una lista
        agregarObjeto(objetos, self)

    # Cambiar el color del cuadro de texto
    def cambiarColor(self, color):
        self.color = color

    # Cambiar el color del texto
    def cambiarColorTexto(self, colorTexto):
        self.colorTexto = colorTexto
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

    # Cambiar el contenido del texto
    def cambiarTexto(self, texto):
        self.texto = texto
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

    # Cambiar el tamaño de la fuente
    def cambiarTamanoFuente(self, tamanoFuente):
        self.tamanoFuente = tamanoFuente
        self.fuente = pygame.font.SysFont('calibri', self.tamanoFuente)
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

    # Cambiar la posición del cuadro de texto en la ventana
    def cambiarPosicion(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.rect = pygame.Rect(self.posX, self.posY, self.largo, self.alto)

    # Cambiar las dimensiones del cuadro de texto
    def cambiarDimensiones(self, largo, alto):
        self.largo = largo
        self.alto = alto
        self.rect = pygame.Rect(self.posX, self.posY, self.largo, self.alto)

    # Dibujar el cuadro de texto
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        pantalla.blit(self.etiqueta, self.etiqueta.get_rect(center = self.rect.center))

    # Eliminar el cuadro de texto de una lista
    def eliminar(self, objetos):
        eliminarObjeto(objetos, self)

    # Agregar el cuadro de texto a una lista
    def agregar(self, objetos):
        agregarObjeto(objetos, self)

# Clase para crear y modificar una etiqueta de texto
class Etiqueta:
    # Inicializar etiqueta de texto y datos pertenecientes a ella
    def __init__(self, objetos, texto, posX, posY, tamanoFuente=25, colorTexto=(0,0,0)):
        # Posición de la etiqueta de texto en la ventana
        self.posX = posX
        self.posY = posY
        # Tamaño de la fuente
        self.tamanoFuente = tamanoFuente
        # Creación de la fuente
        self.fuente = pygame.font.SysFont('calibri', self.tamanoFuente)
        # Color del texto
        self.colorTexto = colorTexto
        # Contenido del texto
        self.texto = texto
        # Etiqueta para mostrar el texto
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

        # Agregar etiqueta de texto a una lista
        agregarObjeto(objetos, self)

    # Cambiar contenido del texto
    def cambiarTexto(self, texto):
        self.texto = texto
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

    # Cambiar el color del texto
    def cambiarColorTexto(self, colorTexto):
        self.colorTexto = colorTexto
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

    # Cambiar el tamaño de la fuente
    def cambiarTamanoFuente(self, tamanoFuente):
        self.tamanoFuente = tamanoFuente
        self.fuente = pygame.font.SysFont('calibri', self.tamanoFuente)
        self.etiqueta = self.fuente.render(self.texto, True, self.colorTexto)

    # Dibujar la etiqueta de texto
    def dibujar(self, pantalla):
        pantalla.blit(self.etiqueta, (self.posX, self.posY))

    # Eliminar la etiqueta de texto de una lista
    def eliminar(self, objetos):
        eliminarObjeto(objetos, self)

    # Agregar la etiqueta de texto de una lista
    def agregar(self, objetos):
        agregarObjeto(objetos, self)