import random
import copy

def print_board(bo):
    """Imprime en pantalla el estado de la matriz insertada, es decir sus numeros colocados en el tablero"""
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")
class SudokuGenerator:
    """
    Esta clase sirve para generar estados iniciales del sudoku.
    En ella se genera una matriz vacia, despues se añaden numeros aleatorios
    y se resuelve el sudoku sobre ello.Una vez comprobado que tiene 1 unica solucion
    se remueven numeros aleatoriamente dejando al menos 17 numeros iniciales
    """
    def __init__(self,grid=None):
        self.counter = 0
      
        self.grid = [[0 for i in range(9)] for j in range(9)]
        self.generate_puzzle()
        self.original = copy.deepcopy(self.grid)


    def generate_puzzle(self):
        """Genera un nuevo sudoku ,lo resuelve y le quita numeros"""
        self.generate_solution(self.grid)
        self.remove_numbers_from_grid()
        
        return


    def valid_location(self,grid,row,col,number):
        """
        Comprueba que un numero en una posicion concreta es correcto respecto
        a las normas del sudoku
        """
        #Comprueba fila
        for i in range(len(grid[0])):
            if grid[row][i] == number and col != i:
                return False

        #Comprueba columna
        for i in range(len(grid)):
            if grid[i][col] == number and row != i:
                return False

        #Comprueba las subcuadriculas
        box_x = col // 3
        box_y = row // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if grid[i][j] == number and (i,j) != (row,col):
                    return False

        return True
     
    def find_empty_square(self,grid):
        """Devuelve las coordenadas de la siguiente posicion vacia"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i,j)
        return

    def solve_puzzle(self, grid):
        """Resuelve el sudoku con backtracking"""
        for i in range(0,81):
            row=i//9
            col=i%9
            if grid[row][col]==0:
                for number in range(1,10):
                    if self.valid_location(grid,row,col,number):
                        grid[row][col]=number
                        if not self.find_empty_square(grid):
                            self.counter+=1
                            break
                        else:
                            if self.solve_puzzle(grid):
                                return True
                break
        grid[row][col]=0  
        return False

    def generate_solution(self, grid):
        """Genera una solución con backtracking"""
        number_list = [1,2,3,4,5,6,7,8,9]
        for i in range(0,81):
            row=i//9
            col=i%9
            if grid[row][col]==0:
                random.shuffle(number_list)      
                for number in number_list:
                    if self.valid_location(grid,row,col,number):
                        grid[row][col]=number
                        if not self.find_empty_square(grid):
                            return True
                        else:
                            if self.generate_solution(grid):
                                return True
                break
        grid[row][col]=0  
        return False

    def get_non_empty_squares(self,grid):
        """Devuelve una lista de las posiciones ocupadas en el sudoku"""
        non_empty_squares = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0:
                    non_empty_squares.append((i,j))
        random.shuffle(non_empty_squares)
        return non_empty_squares

    def remove_numbers_from_grid(self):
        """
        Quita numeros de la matriz aleatoriamente comprobando que se queden al menos 17 numeros inicialez 
        y que no tenga mas de una solución el sudoku
        """
        non_empty_squares = self.get_non_empty_squares(self.grid)
        non_empty_squares_count = len(non_empty_squares)
        rounds = 3
        while rounds > 0 and non_empty_squares_count >= 17:
            #Al menos 17 numeros iniciales
            row,col = non_empty_squares.pop()
            non_empty_squares_count -= 1
            #Numero borrado que se puede necesitar poner otra vez
            removed_square = self.grid[row][col]
            self.grid[row][col]=0
            #Copia del problema a resolver
            grid_copy = copy.deepcopy(self.grid)
            #Contador de soluciones
            self.counter=0      
            self.solve_puzzle(grid_copy)   
            #si hay mas de una solucion se pone el ultimo numero borrado
            if self.counter!=1:
                self.grid[row][col]=removed_square
                non_empty_squares_count += 1
                rounds -=1
        return