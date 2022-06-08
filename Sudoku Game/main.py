import pygame
from pygame import Rect, mouse
from state import SudokuState
from sudoku import SudokuGenerator
from tkinter import *
from tkinter import messagebox
from search import show_solution, uniform_cost, greedy, a_star, depth_first, h1, breadth_first,h2
import search



pygame.font.init()
#Array para datos de la solución final representados en la interfaz
nodos = [0]*10
#Coordenadas y tamaños de los 2 botones
resolver = Rect(400,150,175,100)
generar = Rect(400,25,175,100)
#Fuentes definidas para los diferentes textos
myfont = pygame.font.SysFont("Calibri",40)
myfont2 = pygame.font.SysFont("Calibri",30)
myfont3 = pygame.font.SysFont("Calibri",20)
#Estado inicial de un tablero vacio
initial_board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
class Grid:
    """
    Esta clase reprensenta la matriz que va a ser dibujada en la interfaz.
    En ella se definen sus filas y columna, y los metodos para dibujar la interfaz
    """
    
    
    def __init__(self, rows, cols, width, height,board,solution):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.board = board
        self.solution = solution
        
        

  

    def draw(self, win):
        """ Dibuja toda la interfaz: lineas, subcuadriculas, botones y textos de solucion si se da las condiciones"""
        # Dibuja las lineas
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)
           
        # Dibuja las subcuadriculas
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)
        # Color de los botones segun si esta el raton encima o no
        if generar.collidepoint(mouse.get_pos()):
            pygame.draw.rect(win, (155,155,155), generar,5)
        else:            
            pygame.draw.rect(win, (0,0,0), generar,5)    
        
        if resolver.collidepoint(mouse.get_pos()):
            pygame.draw.rect(win, (155,155,155), resolver,5)
        else:            
            pygame.draw.rect(win, (0,0,0), resolver,5)     
        # Texto dentro de los botones  
        texto_generar = myfont.render("Generar", True,(0,0,0))
        texto_resolver = myfont.render("Resolver", True,(0,0,0)) 
        win.blit(texto_generar,(400+(generar.width- texto_generar.get_width())/2,
                                25+(generar.height - texto_generar.get_height())/2))   
        win.blit(texto_resolver,(400+(resolver.width- texto_resolver.get_width())/2,
                                 150+(resolver.height- texto_resolver.get_height())/2))
        # Si se cumple que ya se tiene la solución se dibuja toda la información de la misma
        if self.solution == True:
            titulo = myfont2.render("Búsquedas no informadas", True,(0,0,0))
            win.blit(titulo, (25, 375))
            titulo2 = myfont2.render("Búsquedas informadas", True,(0,0,0))
            win.blit(titulo2, (25, 515))      
            noinformadas1 = myfont3.render("Breadth First->  Expandidos:"+str(nodos[0])+"    Generados:"+str(nodos[1]),
                                           True,(0,0,0))
            win.blit(noinformadas1, (25, 416))
            noinformadas2 = myfont3.render("Depth First->     Expandidos:"+str(nodos[2])+"    Generados:"+str(nodos[3]),
                                           True,(0,0,0))
            win.blit(noinformadas2, (25, 447))
            noinformadas3 = myfont3.render("UniformCost->  Expandidos:"+str(nodos[4])+"    Generados:"+str(nodos[5]),
                                           True,(0,0,0))
            win.blit(noinformadas3, (25, 478))
            
            informadas1 = myfont3.render("Greedy->  Expandidos:"+str(nodos[6])+"    Generados:"+str(nodos[7]),
                                           True,(0,0,0))
            win.blit(informadas1, (25, 556))
            informadas2 = myfont3.render("A_Star->   Expandidos:"+str(nodos[8])+"    Generados:"+str(nodos[9]),
                                           True,(0,0,0))
            win.blit(informadas2, (25, 587))



class Cube:
    """
    En esta clase se va a definir las caracteristicas de las subcuadriculas en la interfaz
    y como se van a dibujar
    """
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        

    def draw(self, win):
        # Se dibuja la subcuadricula con el numero que contenga
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board):
    win.fill((255,255,255))
    # Dibujar el tablero y la matriz
    board.draw(win)
    




def main():
    """
    Este es el Main que estara en constante ejecución hasta que se cierre el programa.
    En él, se esta imprimiendo constantemente el estado del juego.
    También esta esperando eventos de botones a los cuales reaccionar.
    Con uno generara el sudoku y lo dibujara y con el otro lo solucionara y pondra los resultados también en el tablero.
    """
    win = pygame.display.set_mode((640,640))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 340, 340,initial_board,False)
    
    run = True
    
    
    while run:

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                
                if generar.collidepoint(mouse.get_pos()):
                   # Si se da al boton de generar
                    
                    new_puzzle = SudokuGenerator()
                    board2 = new_puzzle.grid
                    board = Grid(9, 9, 340, 340,board2,False)
                    
                   
                    
                     
                if resolver.collidepoint(mouse.get_pos()):
                    # Si se da al boton de generar
                    if board.board == initial_board:
                        #Si se intenta resolver con un sudoku vacio salta un error
                            Tk().wm_withdraw() #to hide the main window
                            messagebox.showinfo('Error','Genere un sudoku para poder resolver')
                    else:
                            board.solution=True
                            init_state = SudokuState(board.board)
                            # Se soluciona mediante todos los metodos de busqueda
                            solution_bf, expandedbf, generatedbf = search.breadth_first(init_state)
                            if solution_bf != None:
                                    print ("breadth_first found a solution...")
                            else:
                                    print ("breadth_first failed...")
                            show_solution(solution_bf, expandedbf, generatedbf)
                            
                            solution_df, expandeddf, generateddf = search.depth_first(init_state)
                            if solution_df != None:
                                    print ("depth_first found a solution...")
                            else:
                                    print ("depth_first failed...")
                            show_solution(solution_df, expandeddf, generateddf)         
                            
                            solution_uc, expandeduc, generateduc = search.uniform_cost(init_state)
                            if solution_uc != None:
                                    print ("uniform_cost found a solution...")
                            else:
                                    print ("uniform_cost failed...")
                            show_solution(solution_uc, expandeduc, generateduc)  
                            
                            solution_greedy, expandedg, generatedg = greedy(init_state, h1)
                            if solution_greedy != None:
                                print ("greedy found a solution...")
                            else:
                                print ("greedy failed...")
                            show_solution(solution_greedy, expandedg, generatedg)
                            
                            
                            solution_astar, expandedA, generatedA = a_star(init_state, h1)
                            if solution_astar != None:
                                print ("A* found a solution...")
                            else:
                                print ("A* failed...")
                            show_solution(solution_astar, expandedA, generatedA)
                            # Se guardan los datos de las soluciones
                            nodos[0]= expandedbf
                            nodos[1]= generatedbf
                            nodos[2]= expandeddf
                            nodos[3]= generateddf
                            nodos[4]= expandeduc
                            nodos[5]= generateduc
                            nodos[6]= expandedg
                            nodos[7]= generatedg
                            nodos[8]= expandedA
                            nodos[9]= generatedA
                            #Se asigna el tablero con la solución
                            finalboard = solution_bf.state.bo
                            
                            board = Grid(9, 9, 340, 340,finalboard,True)
        #Se actualiza el tablero constantemente
        redraw_window(win, board)
        pygame.display.update()


main()
pygame.quit()
