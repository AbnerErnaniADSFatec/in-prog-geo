# Importações
import numpy as np


# Função para pré-processar matrizes
def preprocessa_matriz(matriz):
    return matriz.astype(float)


# Função para verificar se as dimensões das matrizes são equivalentes
def verifica_shape(matriz_t1, matriz_t2):
    return matriz_t1.shape == matriz_t2.shape


# Função para cálculo das diferenças entre duas matrizes
def calculo_dif_matrizes(matriz_t1, matriz_t2):
    matriz_resultante = matriz_t2 - matriz_t1
    return matriz_resultante


# Função para classificar as diferenças de uma matriz
def classificacao_dif_matriz(matriz_resultante, limiar_min=0, limiar_max=0):
    if limiar_min > 0:
        raise Exception("LimiarMinInvalido")
    if limiar_max < 0:
        raise Exception("LimiarMaxInvalido")

    # Criar uma matriz de zeros (com o mesmo shape da matriz_resultante)
    matriz_aux = np.zeros_like(matriz_resultante)

    n_linhas = matriz_resultante.shape[0]
    n_colunas = matriz_resultante.shape[1]

    for i in range(0, n_linhas):
        for j in range(0, n_colunas):
            # Critério de mudança:
            if limiar_min <= matriz_resultante[i][j] <= limiar_max:
                matriz_aux[i][j] = 1  # As matrizes são consideradas iguais ou muito semelhantes
            else:
                matriz_aux[i][j] = 2  # As matrizes sofreram "grandes" alterações
    return matriz_aux


if __name__ == '__main__':
    # Check if check_tolerance works as expected:
    assert (classificacao_dif_matriz(np.zeros((2, 2))) == np.array([[1, 1], [1, 1]])).all()

    matriz_teste = np.array([[2, 0], [-3, 1]])

    assert (classificacao_dif_matriz(matriz_teste) == np.array([[2, 1], [2, 2]])).all()
    assert (classificacao_dif_matriz(matriz_teste, limiar_min=-1, limiar_max=1) == np.array([[2, 1], [2, 1]])).all()

    print("Finished ", __file__)
