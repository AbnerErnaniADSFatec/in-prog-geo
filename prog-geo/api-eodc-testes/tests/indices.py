
# Função para cálculo do índice NDVI
def calculo_ndvi(nir, red, cte_delta=1e-10):
    ndvi = (nir - red) / (nir + red + cte_delta)
    return ndvi


# Função para cálculo do índice NDWI
def calculo_ndwi(nir, green, cte_delta=1e-10):
    ndwi = (green - nir) / (green + nir + cte_delta)
    return ndwi


# Função para cálculo do índice NDBI
def calculo_ndbi(nir, swir1, cte_delta=1e-10):
    ndbi = (swir1 - nir) / (swir1 + nir + cte_delta)
    return ndbi


if __name__ == '__main__':

    import numpy as np

    matriz_nir = np.array([[1, 1], [1, 1]])
    matriz_red = np.array([[1, 1], [1, 1]])
    matriz_green = np.array([[1, 1], [1, 1]])
    matriz_swir1 = np.array([[1, 1], [1, 1]])

    assert (calculo_ndvi(matriz_nir, matriz_red) == np.zeros([2, 2])).all()
    assert (calculo_ndwi(matriz_nir, matriz_green) == np.zeros([2, 2])).all()
    assert (calculo_ndbi(matriz_nir, matriz_swir1) == np.zeros([2, 2])).all()

    assert calculo_ndvi(2, 2) == np.zeros((1,))
