from datastructures import Stack,PriorityQueue,Queue
from state import find_empty
from sudoku import print_board

#----------------------------------------------------------------------

class Node:
    """
    Esta clase representa los nodos de un arbol. Cada nodo contiene una representacion
    del estado del problema, una referencia al nodo padre, un string que describe la accion
    que genero el nodo desde el nodo padre y el coste de camino g desde el origen.
    """
    def __init__(self, state, parentPosition, action):
        self.state = state
        self.parentPosition = parentPosition
        self.action = action
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        if other:
            return self.state == other.state
        else:
            return False

    def expand(self):
        successors = []
        for (newState, action) in self.state.next_states():
            newNode = Node(newState, self, action)
            successors.append(newNode)
        return successors

#----------------------------------------------------------------------

def uninformed_search(initial_state, frontier):

    """
    Parametros:
       initial_state: estado inicial de busqueda (objeto de clase State)
       frontier: estructura de datos para contener los estados de la frontera (objeto de clase
           contenida en el modulo DataStructures)
    """
    
    initial_node = Node(initial_state, None, None)   
    expanded = 0
    generated = 0
    nodo_explorado = None
    nuevos_expandidos = None
    
    explorados = []
    #Cola para los nodos explorados.
    frontier.insert(initial_node)

    while True:
        
    
        if frontier.is_empty():
            print("mal")
            return None
        
        #Se elimina el primer nodo de la frontera y se asigna como nodo actual.
        nodo_explorado = frontier.remove()
      
        find = find_empty(nodo_explorado.state.bo)
        if not find:
            
            return (nodo_explorado, expanded, generated)
                  
        #Se añade el nodo explorado a la cola
        explorados.append(nodo_explorado)
        #En la variable nuevos_expandidos  se guarda el nodo expandido.
        nuevos_expandidos = nodo_explorado.expand()
        
        #Se actualiza expanded.
        expanded = expanded + 1
               
        for nodo_nuevo in nuevos_expandidos:
            
            if not frontier.contains(nodo_nuevo) and not explorados.__contains__(nodo_nuevo):
                generated = generated + 1
                nodo_nuevo.g = nodo_nuevo.parentPosition.g +1
                frontier.insert(nodo_nuevo) 
                              
    return (None, expanded, generated)

#----------------------------------------------------------------------
# Uninformed search

def breadth_first(initial_state):
    frontier = Queue()
    return uninformed_search(initial_state, frontier)

def depth_first(initial_state):
    frontier = Stack()
    return uninformed_search(initial_state, frontier)

def uniform_cost(initial_state):
    frontier = PriorityQueue(lambda x: x.g)
    return uninformed_search(initial_state, frontier)

#----------------------------------------------------------------------

def informed_search(initial_state,frontier, heuristic):
    
    """
    Parametros:
       initial_state: estado inicial de busqueda (objeto de clase State)
       frontier: estructura de datos para contener los estados de la frontera (objeto de clase
           contenida en el modulo DataStructures)
       heuristic: funcion heuristica utilizada para guiar el proceso de busqueda.    
    """
    initial_node = Node(initial_state, None, None)
    expanded = 0
    generated = 0
    nodo_explorado = None
    nuevos_expandidos = None

    explorados = []
    frontier.insert(initial_node)

    while True:
        if frontier.is_empty():
            return None
        nodo_explorado = frontier.remove()
        find = find_empty(nodo_explorado.state.bo)
        if not find:
            
            return (nodo_explorado, expanded, generated)

        explorados.append(nodo_explorado)
        nuevos_expandidos = nodo_explorado.expand()
        expanded = expanded + 1
        

        for nodo_nuevo in nuevos_expandidos:
            if not frontier.contains(nodo_nuevo) and not explorados.__contains__(nodo_nuevo):
                generated = generated + 1
                #.g hace referencia al coste desde el nodo inicial hasta el nodo actual
                nodo_nuevo.g = nodo_nuevo.parentPosition.g +1
                #.h hace referencia al coste heuristico desde el nodo actual al nodo objetivo
                nodo_nuevo.h = heuristic(nodo_nuevo)
                frontier.insert(nodo_nuevo)
        
    return (nodo_explorado, expanded, generated)

#----------------------------------------------------------------------
# Informed search

def greedy(initial_state, heuristic):
    frontier = PriorityQueue(lambda x: x.h )
    return informed_search(initial_state, frontier, heuristic)

def a_star(initial_state, heuristic):
    frontier = PriorityQueue(lambda x: x.g + x.h)
    return informed_search(initial_state, frontier, heuristic)

#---------------------------------------------------------------------
# Heuristicas

def h1(node):
    """ Heuristica basada en el numero de huecos vacios restantes """
    current_state = node.state
    empty_squares = 0
    for i in range(len(current_state.bo)):
        for j in range(len(current_state.bo)):
            if current_state.bo[i][j] == 0:
                empty_squares = empty_squares +1
    
    return empty_squares

def h2(node):
    """ Heuristica basada en el numero de nodos expandibles que tiene cada nodo """
    nuevos_expandidos = None
    nuevos_expandidos = node.expand()
    
    return len(nuevos_expandidos)

#----------------------------------------------------------------------
#Imprimir por consola los resultados
def show_solution(node, expanded, generated):
    path = []
    
    while node != None:
        
        path.insert(0, node)
        node = node.parentPosition
    if path:
        
        print ("Solution took %d steps" % (len(path) - 1))
        print_board(path[0].state.bo)
        
        for n in path[1:]:
            
            print ('Num:%s Row:%s Col:%s' % (n.action[0], n.action[1], n.action[2]))
            print_board(n.state.bo)
            print("\n")
            print("\n")
    print ("Nodes expanded:  %s" % expanded)
    print ("Nodes generated: %s\n" % generated)