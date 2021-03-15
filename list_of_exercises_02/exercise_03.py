"""
<https://prog-geo.github.io/listas/l02.html>

(3) Considere a equação dos seguintes índices espectrais:

NDWI = (Xgreen−Xnir)/(Xgreen+Xnir)
NDVI = (Xnir−Xred/(Xnir+Xred)

Onde:
 - Xgreen refere-se à banda espectral da faixa do verde (banda 04 do MODIS);
 - Xnir refere-se à banda do infravermelho próximo (banda 02 do MODIS);

Fonte: <https://doi.org/10.1029/2008GL035772>.

De acordo com as equações acima,
crie um programa que leia os valores de Xgreen, Xnir e Xred,
e imprima como resultados os valores de NDWI e NDVI.
"""

x_green = float(input("\n X green = "))
x_nir = float(input(" X nir = "))
x_red = float(input(" X red = "))

ndwi = (x_green - x_nir) / (x_green + x_nir)
ndvi = (x_nir - x_red) / (x_nir + x_red)

print("\n NDWI = " + str(ndwi), "NDVI = " + str(ndvi) + "\n", sep=", e ")