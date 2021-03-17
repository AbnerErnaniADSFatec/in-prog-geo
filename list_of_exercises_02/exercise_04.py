"""
<https://prog-geo.github.io/listas/l02.html>

(4) Escreva um programa que pergunte ao usuário as coordenadas de latitude e longitude, em grau-decimal,
de dois pontos quaisquer na esfera terrestre e que apresente a distância entre eles.
Essa distância deverá ser calculada de acordo com a fórmula de Haversine:

<https://en.wikipedia.org/wiki/Haversine_formula>

Obs.: Lembre-se que todas as funções trigonométricas e suas inversas,
bem como funções para conversão entre graus e radianos encontram-se na biblioteca matemática do Python.

<https://docs.python.org/3/library/math.html>

Dados de teste:

<https://arthur-e.github.io/Wicket/sandbox-gmaps3.html>

São Paulo: Lat -23.54753994162255 Lon -46.64472359303465
São José dos Campos: Lat -23.224858796012942 Lon -45.91413277272215
Resultado esperado: ~ 82.75 km
"""

import math

p_lat_decimal = float(input("\n Latitude de p (grau decimal) ° = "))
p_lon_decimal = float(input(" Longitude de p (grau decimal) ° = "))

print("\n p(%.2f,%.2f)" %(p_lat_decimal, p_lon_decimal))

q_lat_decimal = float(input("\n Latitude de q (grau decimal) ° = "))
q_lon_decimal = float(input(" Longitude de q (grau decimal) ° = "))

print("\n q(%.2f,%.2f)" %(q_lat_decimal, q_lon_decimal))

p_lat_radian = math.radians(p_lat_decimal)
p_lon_radian = math.radians(p_lon_decimal)
q_lat_radian = math.radians(q_lat_decimal)
q_lon_radian = math.radians(q_lon_decimal)

distancia = 2 * 6371 * math.asin(
    math.sqrt(
        (
            math.sin(
                (q_lat_radian - p_lat_radian) / 2
            ) ** 2
        ) + (
            math.cos(p_lat_radian) * math.cos(q_lat_radian) * (
                math.sin(
                    (q_lon_radian - p_lon_radian) / 2
                ) ** 2
            )
        )
    )
)

print("\n Distância (p,q) = {d:,.10f} Km\n".format(d=distancia))