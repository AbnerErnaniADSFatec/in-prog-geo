#!/usr/bin/env python
# coding: utf-8

# **Bounding Box:** representa uma é área definida por duas longitudes e duas latitudes, onde:
# 
# - A latitude é um número decimal entre -90.0 e 90.0
# 
# - A longitude é um número decimal entre -180.0 e 180.0
# 
# **Observação:** O formato segue o padrão: bbox = [min Longitude , min Latitude , max Longitude , max Latitude]

# In[18]:


while True:   
    
    var_long_min = float(input("Digite a longitude mínima [-180º a +180º]:"))
    
    if((var_long_min > 180) or (var_long_min < -180)):
        print("Erro: o valor digitado é inválido.")
        
    else:    
        var_lat_min = float(input("Digite a latitude mínima [-90º a +90º]:"))
        
        if((var_lat_min > 90) or (var_lat_min < -90)):
            print("Erro: o valor digitado é inválido.")
            
        else:    
            var_long_max = float(input("Digite a longitude máxima [-180º a +180º]:"))
        
            if((var_long_min > 180) or (var_long_min < -180)):
                print("Erro: o valor digitado é inválido.")
                
            else:    
                var_lat_max = float(input("Digite a latitude máxima [-90º a +90º]:"))
                
                if((var_lat_max > 90 ) or (var_lat_max < -90)):
                    print("Erro: o valor digitado é inválido.")
        
        
        # Sair do while e continuar as demais instruções
        break             

# Atribuir as entradas do usuário em uma lista
bbox = [var_long_min, var_lat_min, var_long_max, var_lat_max]

print("\nbbox:", bbox)

