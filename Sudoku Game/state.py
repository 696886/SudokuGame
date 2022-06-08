import copy
def find_empty(bo):
    """ Encuentra el primer hueco vacio en la matriz """
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None 
def valid(bo, num, pos):
    """ Comprueba si la posicion elegida , en el tablero concreto, cumple las normas del sudoku """
    # Comprueba fila
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Comprueba Columna
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Comprueba subcuadricula
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True 
class SudokuState:
    """
    Esta clase es para representar el estado del problema del sudoku.
    Cada estado contiene una matriz con unos numeros que representan
    el tablero del sudoku.
    """
    
    def __init__(self,bo):
       
        self.bo = bo  
        
     
    def succ(self, action):
        """ Comprueba si un posible sucesor es válido o no """
        num = int (action[0])
        row = int (action[1])
        col = int (action[2])
        bo1 = copy.deepcopy(self.bo)
        
        if valid(bo1, num, (row, col)):
            bo1[row][col] = num
            estado = SudokuState(bo1)
            
            
            
            return estado
        return None
        
        
        
    def next_states(self):
        """ Dado un estado de tablero comprueba los posibles siguientes estados
        apartir de este. Los que sean válidos los devuelve en un string junto a
        la acción que ha generado ese nuevo estado """
        new_states = []
        row=0
        col=0
        find = find_empty(self.bo)
        if not find:
            print("error")
        else:
            row, col = find 
        
        action = ['1'+str(row)+str(col),'2'+str(row)+str(col),'3'+str(row)+str(col),'4'+str(row)+str(col),'5'+str(row)+str(col),'6'+str(row)+str(col),'7'+str(row)+str(col),'8'+str(row)+str(col),'9'+str(row)+str(col)]        
        for i in range(len(action)):
            estado = self.succ(action[i])
            if estado != None:
                
                new_states.append([estado, action[i]])
        
        return new_states  
    
    
