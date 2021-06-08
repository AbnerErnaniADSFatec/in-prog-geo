# Importações
import numpy as np
import indices
import processamentoImg

matriz_nir = np.array([[1, 1], [1, 1]])
matriz_red = np.array([[1, 1], [1, 1]])
matriz_green = np.array([[4, 3], [1, 10]])
matriz_nir_t2 = np.array([[4, 5], [10, 100]])

result = indices.calculo_ndvi(matriz_nir, matriz_red)
print(result)


matriz_nir = processamentoImg.preprocessa_matriz(matriz_nir)
matriz_nir_t2 = processamentoImg.preprocessa_matriz(matriz_nir_t2)

teste_shape = processamentoImg.verifica_shape(matriz_nir, matriz_nir_t2)
print(teste_shape)

matriz_dif = processamentoImg.calculo_dif_matrizes(matriz_nir, matriz_nir_t2)
print(matriz_dif)

teste_classif = processamentoImg.classificacao_dif_matriz(matriz_dif)
print(teste_classif)
