# Importações
import numpy as np
import indices

matriz_nir = np.array([[1, 1], [1, 1]])
matriz_red = np.array([[1, 1], [1, 1]])


result = indices.calculo_ndvi(matriz_nir, matriz_red)
print(result)
