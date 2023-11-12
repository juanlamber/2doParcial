import numpy as np
from funciones import *
from validaciones import *
from CLASES import *
from menu import *
from collections import deque

hola = np.array([[1, 2, 3], [1, 2, 6]])

print([hola[1] for n in hola])

algo = sum([hola[1] for n in hola])

print(algo)
