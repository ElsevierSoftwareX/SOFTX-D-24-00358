"""
Created on Sun Jan 29 07:53:51 2023

@author: luico
"""


"""
Created on Fri Jan 27 04:58:27 2023

@author: luico
"""


#import catalogo

import pandas as pd
import numpy as np
from sympy import *
from symengine import symbols as DDDSym
import DDD
from time import time
init_printing()
def genera_simbolos():
    global dictionary,dict_R,dict_C,dict_L,dict_V,dict_I,dict_E,dict_F,dict_G,dict_H,dict_O,dict_K,dict_J,dict_V_,dict_Iv_,dict_I_OAmp_,dict_I_E,dict_I_H,dict_I_,dict_S
    dictionary,dict_R,dict_C,dict_L,dict_V,dict_I,dict_E,dict_F,dict_G,dict_H,dict_O,dict_K,dict_J,dict_V_,dict_Iv_,dict_I_OAmp_,dict_I_E,dict_I_H,dict_I_,dict_S = catalogo.simbolos()
def MNAf(name):  
    global_array = []
    A = []
    mna_ren = []

    

    global_array = []
    A = []
    mna_ren = []
    global dta, mna, space, space2
    global np_tupla_horizontal_O,np_tupla_vertical_O
    global orden,search,np_tupla_horizontal_E,np_tupla_vertical_E
    global search,np_tupla_horizontal_H,np_tupla_vertical_H
    global mna, vector_corrientes_J, numero_giradores
    global numero_transformadores, vector_corrientes
    global search,np_tupla_horizontal_F,np_tupla_vertical_F
    global search,np_tupla_horizontal_G,np_tupla_vertical_G
    global search,np_tupla_horizontal_O,np_tupla_vertical_O
    dta = 'B'
    #Salida_resistencias = 'B'
    
    num = len(name)-4
    
    name2 = name[:num]
    space = '======================================== New_Line_@author: luico'



    ################################
    ################################
    ################################      considera separar desde aqui
    ################################
    ################################
    def Verifica_transformador():
        global pd_netlist
        #es una funcion que permite observar si hay un transformador, reordenar y tranformar el netlist
        print('estamos verificando..')
        #print(pd_netlist)
        temporal_netlist = pd_netlist.to_numpy()
        #print(temporal_netlist)
        tempo_ext_count = 0  
        for renglon in temporal_netlist:
            #print('###############################')
            #print(renglon)
            elemento = renglon[0]
            long = len(elemento)
            long = long-(long-1)
            elemento = elemento[:long]
            #temporal_netlist[tempo_ext_count,4]
            #print(elemento)
            if (str(elemento) == 'K') or (str(elemento) == 'k'):
                primario = renglon[1]
                secundario = renglon[2]
                tempo_prim = []
                tempo_sec = []
                gain = renglon[3]
                tempo_counter = 0
                for renglon in temporal_netlist:
                    if str(renglon[0]) == str(primario):
                        tempo_prim = renglon
                        temporal_netlist[tempo_counter,0] = 'NaN_L_'
                    if str(renglon[0]) == str(secundario):
                        tempo_sec = renglon
                        temporal_netlist[tempo_counter,0] = 'NaN_L_'
                    
                    tempo_counter = tempo_counter + 1

                temporal_netlist[tempo_ext_count,8] = temporal_netlist[tempo_ext_count,1]
                temporal_netlist[tempo_ext_count,9] = temporal_netlist[tempo_ext_count,2]
                
                temporal_netlist[tempo_ext_count,1] = int(tempo_prim[1])
                temporal_netlist[tempo_ext_count,2] = int(tempo_prim[2])
                
                temporal_netlist[tempo_ext_count,5] = float(tempo_prim[3])
                
                temporal_netlist[tempo_ext_count,3] = int(tempo_sec[1])
                temporal_netlist[tempo_ext_count,4] = int(tempo_sec[2])

                temporal_netlist[tempo_ext_count,6] = float(tempo_sec[3])

                temporal_netlist[tempo_ext_count,7] = gain
                
            tempo_ext_count = tempo_ext_count + 1
                
        #print(temporal_netlist)
        pd_netlist = pd.DataFrame(temporal_netlist, columns=['elemento','nodo1 +','nodo2 -','nodo3 +','nodo4 -','miu','miu2','miu3','t1','t2'])
        #print(pd_netlist)
    def read_cir(name):
        global pd_elemento, pd_n1, pd_n2, pd_netlist, pd_conjunto
        global np_elemento, np_n1, np_n2, np_netlist, np_conjunto
        global np_polaridad, pd_polaridad,pd_n3,np_n3,nodo4,nodo5
        #y = x.astype(np.float)
        pd_netlist = pd.read_csv(name, sep=' ', header=None,names=['elemento','nodo1 +','nodo2 -','nodo3 +','nodo4 -','miu','miu2','miu3','t1','t2'])
        Verifica_transformador()
        pd_netlist['nodo1 +'] = pd_netlist['nodo1 +'].astype('int64')
        pd_netlist['nodo2 -'] = pd_netlist['nodo2 -'].astype('int64')
        #pd_conjunto = pd.read_csv(name, sep=' ', header=None,names=['elemento','nodo1 +','nodo2 -','nodo3 +','nodo4 -','miu','miu2','miu3','miu4','miu5'])
        #print('here')
        pd_conjunto = pd_netlist
        pd_polaridad = pd.read_csv(name, sep=' ', header=None,names=['elemento','nodo1 +','nodo2 -','nodo3 +','nodo4 -','miu','miu2','miu3','t1','t2'])
        ########print(pd_netlist)
        
        pd_conjunto = pd_conjunto.drop(['nodo3 +','nodo4 -','miu'], axis=1) # eliminamos al nodo 3 del conjunto, porque este es tomado en la formulacion
        pd_elemento = pd_netlist['elemento']
        pd_n1 = pd_netlist['nodo1 +']
        pd_n2 = pd_netlist['nodo2 -']
        pd_n3 = pd_netlist['nodo3 +']
        #pd_conjuntos = pd_conjunto['elemento','nodo1 +','nodo2 -']
        
        np_netlist = pd_netlist.to_numpy()
        np_elemento = pd_elemento.to_numpy()
        np_n1 = pd_n1.to_numpy()
        np_n2 = pd_n2.to_numpy()
        np_conjunto = pd_conjunto.to_numpy()
        np_polaridad = pd_polaridad.to_numpy()
        np_n3 = pd_n3.to_numpy()
        np_n1 = np_n1.astype(np.int32)
        np_n2 = np_n2.astype(np.int32)
        #print(np_netlist)
        


        

    def IdentificaNumeroMayor():
        #author: dta
        #funcion generica para
        #identificar el numero mayor de nodos para elementos de dos term..

        ##y = x.astype(np.float)
        global MaximoNodo1, MaximoNodo2, MaximoNodo3, Orden_NA
        #print('okkkkk')
        MaximoNodo1 = np.amax(np_n1)
        #MaximoNodo1 = MaximoNodo1.astype(np.int32)
        #print('okkkkk')
        MaximoNodo2 = np.amax(np_n2)
        
        #print('MaximoNodo1')
        #print(MaximoNodo1)
        tempArray = np.array([[MaximoNodo1],[MaximoNodo2]])
        #print(tempArray)
        #print('okkkkk')
        Orden_NA = np.amax(tempArray)
        #print('okkkkk')
        #print('orden MNA = ' + str(Orden_NA))
        #print('okkkkk')
        return(Orden_NA)
        
    def formulaVectores(numeroNodos):
        matrix_formula = []
        for columnas in range(numeroNodos):
            temp = []
            matrix_formula.append(temp)
        #print(matrix_formula)
        return(matrix_formula)

    read_cir(name)

    print(pd_netlist)
    #print('okkkkkkkkkk')
    global orden
    orden = IdentificaNumeroMayor()
    #print('okkkkkkkkkk')
    #print('orden------------------->'+str(orden))
    matriz_vacia = formulaVectores(orden)
    #print(matriz_vacia)




    def formula_tamano_n_m(x,y):
        matriz = []
        for i in range(x):
            vector = []
            for temp in range(y):
                vector.append(0)
                #print(temp)
            matriz.append(vector)
            np_matriz = np.array(matriz,dtype=object)
        return(matriz,np_matriz)

    G_vacia,np_G = formula_tamano_n_m(orden,orden)
    #print(G_vacia)


    def busca_elemento_mayor(elemento,lista):
        #esta funcion toma una lista de elementos y busca el elemento seleccionado en string
        #para encontrar su valor maximo
        memoria_numero = 0
        for dato in lista:
            #print(dato)
            numero = ''
            old_numero = 0
            for word in dato:
                #print(word)
                if word != elemento:
                    #print(word)
                    numero = str(numero) + str(word)
            try:
                numero = int(numero)
            except:
                pass
            if type(numero) == str:
                numero = 0                  
            #print(numero)
            if numero > old_numero:
                memoria_numero = numero
            old_numero = numero
        #print(memoria_numero)
        return(memoria_numero)




    def reformula_corrientes(M):
        pass

    def invierte_un_string(string):
        rev = string[::-1]
        return(rev)

    def make_a_tuple(tamano,valor):
        regresa = []
        for x in range(tamano):
            regresa.append(valor)
        return(regresa)
    ################################
    ################################
    ################################      considera separar desde aqui
    ################################


    def len_vector_juts_if_difference_to_zero(vector):
        temporal_counter = 0
        for x in vector:
            if x != 0:
                temporal_counter = temporal_counter + 1
        return(temporal_counter)

    ################################## En esta seccion se formula el la matriz G para resistores ##############################################



    def make_matrix_G_pre_002(matrix,variable_por_ordenar):
        #print(matrix)
        #esta funcion hace lo siguiente:
                #[['V1', 'G1'],
                #['G1', 'G2'],
                #['G2', 'G3'],
                #['G3', 'G4', 'G5'],
                #['G5', 'G6', 'G7'],
                #['G7', 'G8', 'G9'],
                #['G9', 'G10', 'G11'],
                #['G11', 'G12', 'V2'],
                #['G12', 'G13']]
        #pas omportante para ser retomado en la funcion:   Make_G_Matrix_pre001
        global dta
        #print('----------------------------conjunto-----------------------')
        #print(np_conjunto)
        for i in range(orden):
            
            temporalVector = []
            
            for data in np_conjunto:
                tempo_counter = 0
                
                for element in data:
                    
                    if tempo_counter == 0:
                        tempo = element
                        
                    ii = int(i)+1
                    if str(element) == str(ii):
                        concatena = ''
                        for pivote in tempo:
                            if pivote == variable_por_ordenar:
                                pivote = dta
                            concatena = str(concatena) + str(pivote)
                            
                        temporalVector.append(str(concatena))
                    tempo_counter = tempo_counter+1
                    
                matrix[i]=temporalVector
        #print(space)
        #print('-----------------------------matrix------------------------')
        #print(matrix)
        #print(space)
        return(matrix)






    def Make_G_Matrix_pre001(matrix,tipo,m,n):
        #print('m: '+ str(m))
        #print('n: '+ str(n))
        #m=3
        #n=5
        #aqui ordena y SOLO ordena del tipo: 
        #array([[1, 0, 0, 0, 0, 0, 7],
        #       [0, 2, 0, 0, 5, 0, 0],
        #       [0, 0, 3, 4, 0, 0, 0],
        #       [0, 0, 0, 0, 0, 0, 0],
        #       [0, 0, 0, 0, 0, 0, 7]])
        #
        #de acuerdo con un modelo del tipo:
        #
        #
        #   v1 = ['G7', 'G1']
        #   v2 = ['i1', 'G2','G5']
        #   v3 = ['i5', 'G3', 'G4']
        #   v4 = ['i6', 'G40']
        #   v5 = ['sim6', 'G7']
        #
        #con la entrada:      'G'
        #
        # y devuelve datos en tupla, numpy & pandas
        #
        # requiere una matriz, una entrada string y el tamaño para G
        #print(matrix)
        #print(tipo)
        G_tupla = []
        renglon_counter = 0
        numero = 0
        for renglon in matrix:
            vector = []
            for columna in range(n):
                for elemento in renglon:
                    temp_num = ''
                    for pre_elemento in elemento:
                        if pre_elemento != tipo:
                            temp_num = temp_num + pre_elemento
                    if type(temp_num) == str:
                        try:
                            temp_num = int(temp_num)
                        except:
                            pass
                    if type(temp_num) == str:
                        temp_num = 0
                    if int(temp_num) == columna+1:
                        numero = int(temp_num)   
                        break
                    if int(temp_num) != columna+1:
                        numero = 0
                vector.append(numero)            
            renglon_counter = renglon_counter + 1                         
            G_tupla.append(vector)
        G_np = np.array(G_tupla) 
        G_pd = pd.DataFrame(G_tupla)
        
        return(G_tupla,G_pd,G_np)


    def Make_G_Matrix_pre003(matrix,m_llenado,salida):
        global dta
        negativo = '-'
        positivo = '+'
        end = ''
        matrix_trans = matrix.transpose()
        counter_renglon = 0

        
            
        
        for renglon in matrix:
            #print('######################'+str(counter_renglon+1))
            for elemento in renglon:
                if elemento != 0:
                    #print(elemento)
                    renglon_traspuesto = matrix_trans[elemento-1]
                    #print('transpuesto: ' + str(renglon_traspuesto) )
                    counter_signal = 0
                    for punto in renglon_traspuesto:
                        if punto != 0:
                            #print()
                            if counter_renglon == counter_signal:
                                #dato = punto
                                dato = salida + str(punto) + end
                                #print(dato)
                                #dato = dictionary.get(dato)
                                
                            if counter_renglon != counter_signal:
                                #dato = punto*-1
                                dato = negativo + salida + str(punto) + end
                            #print('ecuacion: '+str(dato)+'  pos_ren  '+str(counter_signal)+' , '+str(counter_renglon))
                            verifica = np_G[counter_signal,counter_renglon]
                            if verifica == 0:
                                np_G[counter_signal,counter_renglon] = ''
                            verifica_signo = np_G[counter_signal,counter_renglon]
                            if len(verifica_signo) > 0:
                                np_G[counter_signal,counter_renglon] = np_G[counter_signal,counter_renglon] + positivo + dato
                            if len(verifica_signo) == 0:
                                #print('no c q pasa en npG')
                                #print(np_G[counter_signal,counter_renglon])
                                #print('n c q pasa n dato')
                                #print(dato)
                                #print(type(np_G))
                                np_G[counter_signal,counter_renglon] = np_G[counter_signal,counter_renglon] + dato
                        counter_signal = counter_signal + 1
            counter_renglon = counter_renglon + 1
        #print('matrix',np_G)


     
    ## en esta parte formulamos para C y L
    numero_n_R = busca_elemento_mayor('R',np_elemento)
    numero_n_L = busca_elemento_mayor('C',np_elemento)
    numero_n_C = busca_elemento_mayor('L',np_elemento)
    numero_n_O = busca_elemento_mayor('O',np_elemento)
    numero_n = numero_n_R + numero_n_L + numero_n_C + numero_n_O 

    #print('numero_n: ' + str(numero_n))
    matrix = make_matrix_G_pre_002(matriz_vacia,'R')
    #print(matrix)
    G_matrix,G_matrix_pd,Gmatrix_np = Make_G_Matrix_pre001(matrix,dta,orden,numero_n)
    Make_G_Matrix_pre003(Gmatrix_np,G_vacia,'R')#1/Rn
    


    #print('numero_n: ' + str(numero_n))
    matrix_C = make_matrix_G_pre_002(matriz_vacia,'C') 
    G_matrix_C,G_matrix_pd_C,Gmatrix_np_C = Make_G_Matrix_pre001(matrix,dta,orden,numero_n)
    Make_G_Matrix_pre003(Gmatrix_np_C,G_vacia,'C')#Cn*S




    #print('numero_n: ' + str(numero_n))
    matrix_L = make_matrix_G_pre_002(matriz_vacia,'L') 
    G_matrix_L,G_matrix_pd_L,Gmatrix_np_L = Make_G_Matrix_pre001(matrix,dta,orden,numero_n)
    Make_G_Matrix_pre003(Gmatrix_np_L,G_vacia,'L')#1/Ln

    

    ################################## En esta seccion se formula el analisis de OpAmps#######################################################

    #¿Cuantos opamps?
    numero_n_O = busca_elemento_mayor('O',np_elemento)
    numero_n_V = busca_elemento_mayor('V',np_elemento)
    #print('numero de OAmp:   '+str(numero_n_O))
    #>>busca opamps e identifica positivo, negativo y salida y lo guarda en una tupla
    def identifica_OpAmp(numero_n_O,extra_tamano):
        global orden,search,np_tupla_horizontal_O,np_tupla_vertical_O
        matrix_return = []
        
        if numero_n_O > 0:
            tupla,np_tupla_horizontal_O = formula_tamano_n_m(numero_n_O,orden+extra_tamano)
            tupla,np_tupla_vertical_O = formula_tamano_n_m(numero_n_O,orden+extra_tamano)
            #print('hay algo')
            #print(np_tupla)
            external_count = 0
            for search in np_netlist:
                elemento = search[0]
                if (elemento[0] == 'O') or (elemento[:4] == 'OAmp'):
                    positivo = int(search[1]) - 1
                    negativo = int(search[2]) - 1
                    salida = int(search[3]) - 1
                    
                    #>>aqui hacemos el llenado horizontal
                    if positivo >= 0:
                        np_tupla_horizontal_O[external_count, positivo] = 1
                    if negativo >= 0:
                        np_tupla_horizontal_O[external_count, negativo] = -1
                    #>>aqui hacemos el llenado vertival
                    if salida >= 0:
                        np_tupla_vertical_O[external_count, salida] = 1
                    #print(search)
                    external_count = external_count + 1
                #print(np_tupla)
                
            #print(np_tupla_horizontal_O)
            #print(np_tupla_vertical_O)
        if numero_n_O == 0:
            pass




    ################################## En esta seccion se formula el analisis de vccs#######################################################
    ## Te quedaste aqui:
    #¿Cuantos vccs?
    numero_n_G = busca_elemento_mayor('G',np_elemento)
    numero_n_V = busca_elemento_mayor('V',np_elemento)


    def identifica_vccs(numero_n_G,extra_tamano):
        global orden,search,np_tupla_horizontal_G,np_tupla_vertical_G
        #matrix_return = []
        #print(space)
        #print(numero_n_G)
        #print(space)
        if numero_n_G > 0:
            tupla,np_tupla_horizontal_G = formula_tamano_n_m(numero_n_G,orden+extra_tamano)
            tupla,np_tupla_vertical_G = formula_tamano_n_m(numero_n_G,orden+extra_tamano)
            #print('hay algo')
            #print(np_tupla)
            external_count = 0
            for search in np_netlist:
                elemento = search[0]
                if (elemento[0] == 'G') or (elemento[:4] == 'Ga'):
                    uno = int(search[1]) - 1
                    dos = int(search[2]) - 1
                    tres = int(search[3]) - 1
                    cuatro = int(search[4]) - 1

                    #print('aqui................')
                    #print(uno)
                    #print(tres)
                    if (uno >= 0 and tres >= 0):
                        if str(mna[uno,tres]) != '0':
                            mna[uno,tres] = str(mna[uno,tres])+'+G'+str(external_count+1)
                        if str(mna[uno,tres]) == '0':
                            mna[uno,tres] = 'G'+str(external_count+1)

                    if (uno >0 and cuatro >=0):
                        if str(mna[uno,cuatro]) != '0':
                            mna[uno,cuatro] = str(mna[uno,cuatro])+'-G'+str(external_count+1)
                        if str(mna[uno,cuatro]) == '0':
                            mna[uno,cuatro] = '-G'+str(external_count+1)

                    if (dos >= 0 and tres >= 0):
                        if str(mna[dos,tres]) != '0':
                            mna[dos,tres] = str(mna[dos,tres])+'-G'+str(external_count+1)
                        if str(mna[dos,tres]) == '0':
                            mna[dos,tres] = '-G'+str(external_count+1)

                    if (dos >= 0 and cuatro >= 0):
                        if str(mna[dos,cuatro]) != '0':
                            mna[dos,cuatro] = str(mna[dos,cuatro])+'+G'+str(external_count+1)
                        if str(mna[dos,cuatro]) == '0':
                            mna[dos,cuatro] = 'G'+str(external_count+1)
                    #>>aqui hacemos el llenado horizontal
                    #if uno >= 0:
                    #    np_tupla_horizontal_O[external_count, positivo] = '1'
                    #if dos >= 0:
                    #    np_tupla_horizontal_O[external_count, negativo] = '-1'
                    #>>aqui hacemos el llenado vertival
                    #if tres >= 0:
                    #    np_tupla_vertical_O[external_count, salida] = '1'
                    #print(search)
                    external_count = external_count + 1
                #print(np_tupla)
                
            #print(np_tupla_horizontal_O)
            #print(np_tupla_vertical_O)
        if numero_n_O == 0:
            pass




    ######>> empezar desde aqui con las cccs
        # :)
    ################################## En esta seccion se formula el analisis de cccs#######################################################

    #¿Cuantas fuentes cccs?
    numero_n_F = busca_elemento_mayor('F',np_elemento)
    numero_n_V = busca_elemento_mayor('V',np_elemento)
    #print('numero de OAmp:   '+str(numero_n_O))
    #>>busca opamps e identifica positivo, negativo y salida y lo guarda en una tupla
    def identifica_cccs(numero_n_F,extra_tamano):
        global orden,search,np_tupla_horizontal_F,np_tupla_vertical_F
        matrix_return = []
        
        if numero_n_F > 0:
            tupla,np_tupla_horizontal_F = formula_tamano_n_m(numero_n_F,orden+extra_tamano)
            tupla,np_tupla_vertical_F = formula_tamano_n_m(numero_n_F,orden+extra_tamano)
            #print('hay algo')
            #print(np_tupla)
            external_count = 0
            for search in np_netlist:
                elemento = search[0]
                numero_cte = elemento[1:]
                if (elemento[0] == 'F') or (elemento[:4] == 'Fa'):
                    positivo = int(search[1]) - 1
                    negativo = int(search[2]) - 1
                    fuente = str(search[3])
                    try:
                        for busqueda in np_netlist:
                            V = busqueda[0]
                            if str(V) == fuente:
                                nodo1_en_V = int(busqueda[1]) -1 
                                nodo2_en_V = int(busqueda[2]) -1
                                
                    except:
                        print('incongruencia en ele elemento 3 nodo 3 de F')
                    #print(V_matrix_np_T)
                    #print('positivo: '+str(positivo))
                    #print('negativo: '+str(negativo))
                    if len(V_matrix_np) > 0:
                        if external_count > len(V_matrix_np_T[0])-1:
                            external_count = len(V_matrix_np_T[0])-1
                        #print(len(V_matrix_np_T[0]))
                        valor = str(V_matrix_np_T[positivo,external_count])



                        if valor != '0':
                            if positivo >= 0:
                                V_matrix_np_T[positivo,external_count] = V_matrix_np_T[positivo,external_count] + '+F' + str(numero_cte)
                            if negativo >= 0:
                                V_matrix_np_T[positivo,external_count] = V_matrix_np_T[positivo,external_count] + '-F' + str(numero_cte)
                        if valor == '0':
                            if positivo >= 0:
                                V_matrix_np_T[positivo,external_count] = 'F' + str(numero_cte)
                            if negativo >= 0:
                                V_matrix_np_T[negativo,external_count] = '-F' + str(numero_cte)
                        

                    #####################################################################################################################    
                    if (len(V_matrix_np) == 0) and (len(I_matrix_np) > 0):
                        I_matrix_np_T = I_matrix_np.transpose()
                        if external_count > len(I_matrix_np_T[0])-1:
                            external_count = len(I_matrix_np_T[0])-1
                        #print(len(I_matrix_np_T[0]))
                        valor = str(I_matrix_np_T[positivo,external_count])
                        if valor != '0':
                            if positivo >= 0:
                                I_matrix_np_T[positivo,external_count] = I_matrix_np_T[positivo,external_count] + '+F' + str(numero_cte)
                            if negativo >= 0:
                                I_matrix_np_T[positivo,external_count] = I_matrix_np_T[positivo,external_count] + '-F' + str(numero_cte)
                        if valor == '0':
                            if positivo >= 0:
                                I_matrix_np_T[positivo,external_count] = 'F' + str(numero_cte)
                            if negativo >= 0:
                                I_matrix_np_T[negativo,external_count] = '-F' + str(numero_cte)
                    #mna[]
                    #>>aqui hacemos el llenado horizontal
                    #if positivo >= 0:
                    #    np_tupla_horizontal_O[external_count, positivo] = '1'
                    #if negativo >= 0:
                    #    np_tupla_horizontal_O[external_count, negativo] = '-1'
                    #>>aqui hacemos el llenado vertival
                    #if salida >= 0:
                    #    np_tupla_vertical_O[external_count, salida] = '1'
                    #print(search)
                    external_count = external_count + 1
                #print(np_tupla)
                
            #print(np_tupla_horizontal_O)
            #print(np_tupla_vertical_O)
        if numero_n_O == 0:
            pass


    ################################## En esta seccion se formulan fuentes de voltaje controladas por voltaje#######################################################

    #¿Cuantas vcvs?
    numero_n_E = busca_elemento_mayor('E',np_elemento)
    #numero_n_V = busca_elemento_mayor('V',np_elemento)
    #print('numero de fuentes :   '+str(numero_n_E))
    #>>busca fuentes e identifica positivo, negativo y salida y lo guarda en una tupla
    def identifica_E(numero_n_E,extra_tamano):
        global orden,search,np_tupla_horizontal_E,np_tupla_vertical_E
        matrix_return = []
        mas = '+' 
        if numero_n_E > 0:
            tupla,np_tupla_horizontal_E = formula_tamano_n_m(numero_n_E,orden+extra_tamano)
            tupla,np_tupla_vertical_E = formula_tamano_n_m(numero_n_E,orden+extra_tamano)
            #print('hay algo')
            #print(np_tupla)
            #print('miau miau ....')
            external_count = 0
            for search in np_netlist:
                elemento = search[0]
                if (elemento[0] == 'E'):
                    positivo_source = int(search[1]) - 1
                    negativo_source = int(search[2]) - 1
                    positivo_controlled = int(search[3]) - 1
                    negativo_controlled = int(search[4]) - 1
                    #miu = int(search[5]) - 1
                    
                    #>>aqui hacemos el llenado horizontal
                    if positivo_source >= 0:
                        valor = np_tupla_horizontal_E[external_count, positivo_source]
                        #print(valor)
                        if str(valor) != '0':
                            np_tupla_horizontal_E[external_count, positivo_source] = int(np_tupla_horizontal_E[external_count, positivo_source]) + mas + 1
                        if str(valor) == '0':
                            np_tupla_horizontal_E[external_count, positivo_source] = 1
                            
                    if negativo_source >= 0:
                        valor = np_tupla_horizontal_E[external_count, negativo_source]
                        if str(valor) != '0':
                            np_tupla_horizontal_E[external_count, negativo_source] = int(np_tupla_horizontal_E[external_count, negativo_source]) + -1
                        if str(valor) == '0':
                            np_tupla_horizontal_E[external_count, negativo_source] = -1
                            
                    if positivo_controlled >= 0:
                        valor = np_tupla_horizontal_E[external_count, positivo_controlled]
                        if str(valor) != '0':
                            np_tupla_horizontal_E[external_count, positivo_controlled] = str(np_tupla_horizontal_E[external_count, positivo_controlled]) + '-E' + str(external_count+1) + ''
                        if str(valor) == '0':
                            np_tupla_horizontal_E[external_count, positivo_controlled] = '-E' + str(external_count+1) + ''
                            
                    if negativo_controlled >= 0:
                        valor = np_tupla_horizontal_E[external_count, negativo_controlled]
                        if valor != '0':
                            np_tupla_horizontal_E[external_count, negativo_controlled] = str(np_tupla_horizontal_E[external_count, negativo_controlled]) + mas + 'E' + str(external_count+1) + ''
                        if valor == '0':
                            np_tupla_horizontal_E[external_count, negativo_controlled] = 'E' + str(external_count+1) + ''


                    #>>aqui hacemos el llenado vertival
                    if positivo_source >= 0:
                        valor = np_tupla_vertical_E[external_count, positivo_source]
                        if str(valor) != '0':
                            np_tupla_vertical_E[external_count, positivo_source] = int(np_tupla_vertical_E[external_count, positivo_source]) + mas + 1
                        if str(valor) == '0':
                            np_tupla_vertical_E[external_count, positivo_source] = 1
                            
                    if negativo_source >= 0:
                        valor = np_tupla_vertical_E[external_count, negativo_source]
                        if valor != '0':
                            np_tupla_vertical_E[external_count, negativo_source] = int(np_tupla_vertical_E[external_count, negativo_source]) + -1
                        if valor == '0':
                            np_tupla_vertical_E[external_count, negativo_source] = -1
                            
                    #print(search)
                    external_count = external_count + 1
                #print(np_tupla)
                
            #print(np_tupla_horizontal_E)
            #print(np_tupla_vertical_E)
        if numero_n_O == 0:
            pass





    #empezar aqui con las ccvs:



    #¿Cuantas vcvs?
    numero_n_H = busca_elemento_mayor('H',np_elemento)
    #numero_n_V = busca_elemento_mayor('V',np_elemento)
    #print('numero de fuentes :   '+str(numero_n_E))
    #>>busca fuentes e identifica positivo, negativo y salida y lo guarda en una tupla
    def identifica_H(numero_n_H,extra_tamano):
        global orden,search,np_tupla_horizontal_H,np_tupla_vertical_H
        matrix_return = []
        mas = '+'
        #print('imprime el valor del mna')
        #print(mna)
        if numero_n_H > 0:
            tupla,np_tupla_horizontal_H = formula_tamano_n_m(numero_n_H,orden+extra_tamano)
            tupla,np_tupla_vertical_H = formula_tamano_n_m(numero_n_H,orden+extra_tamano)
            #print('hay algo')
            #print(np_tupla)
            #print('miau miau ....')
            external_count = 0
            for search in np_netlist:
                elemento = search[0]
                if (elemento[0] == 'H'):
                    positivo_source = int(search[1]) - 1
                    negativo_source = int(search[2]) - 1
                    fuente = str(search[3])
                    
                    try:
                        for busqueda in np_netlist:
                            #print(busqueda[0])
                            #print(search[3])
                            #print(type(busqueda[0]))
                            #print(type(search[3]))
                            if (str(busqueda[0]) == search[3]):
                                positivo_controlled = int(busqueda[1]) -1
                                negativo_controlled = int(busqueda[2]) - 1
                            
                    #miu = int(search[5]) - 1
                    except:
                        print('error en la congruencia del tipo:')
                        print('Hn    nodo1    nodo2    fuente_controladora    factor_de_control')

                    


                    #print(positivo_controlled)
                    #print(negativo_controlled)
                    #>>aqui hacemos el llenado horizontal
                    if positivo_source >= 0:
                        valor = np_tupla_horizontal_H[external_count, positivo_source]
                        #print(valor)
                        if str(valor) != '0':
                            np_tupla_horizontal_H[external_count, positivo_source] = int(np_tupla_horizontal_H[external_count, positivo_source]) + mas + 1
                        if str(valor) == '0':
                            np_tupla_horizontal_H[external_count, positivo_source] = 1
                            
                    if negativo_source >= 0:
                        valor = np_tupla_horizontal_H[external_count, negativo_source]
                        if str(valor) != '0':
                            np_tupla_horizontal_H[external_count, negativo_source] = int(np_tupla_horizontal_H[external_count, negativo_source]) + -1
                        if str(valor) == '0':
                            np_tupla_horizontal_H[external_count, negativo_source] = -1
                            
                    if positivo_controlled >= 0:
                        valor = np_tupla_horizontal_H[external_count, positivo_controlled]
                        if str(valor) != '0':
                            np_tupla_horizontal_H[external_count, positivo_controlled] = int(np_tupla_horizontal_H[external_count, positivo_controlled]) + -H + str(external_count+1) + ''
                        if str(valor) == '0':
                            #print(np_tupla_horizontal_H)
                            #print('x: '+str(external_count))
                            #print('y: '+str(external_count+orden))
                            #print(-1+len(np_tupla_horizontal_H.transpose()))
                            #-1+len(np_tupla_horizontal_H.transpose())
                            #external_count+orden
                            position = external_count+orden
                            if (position >= -1+len(np_tupla_horizontal_H.transpose())):
                                position = -1+len(np_tupla_horizontal_H.transpose())
                            np_tupla_horizontal_H[external_count, position] = '-H' + str(external_count+1) + ''
    #########                        
                    #if negativo_controlled >= 0:
                    #    valor = np_tupla_horizontal_E[external_count, negativo_controlled]
                    #    if valor != '0':
                    #        np_tupla_horizontal_E[external_count, negativo_controlled] = str(np_tupla_horizontal_E[external_count, negativo_controlled]) + mas + '(m' + str(external_count+1) + ')'
                    #    if valor == '0':
                    #        np_tupla_horizontal_E[external_count, negativo_controlled] = '(m' + str(external_count+1) + ')'


                    #>>aqui hacemos el llenado vertival
                    if positivo_source >= 0:
                        valor = np_tupla_vertical_H[external_count, positivo_source]
                        if str(valor) != '0':
                            np_tupla_vertical_H[external_count, positivo_source] = str(np_tupla_vertical_H[external_count, positivo_source]) + mas + '1'
                        if str(valor) == '0':
                            np_tupla_vertical_H[external_count, positivo_source] = '1'
                            
                    if negativo_source >= 0:
                        valor = np_tupla_vertical_H[external_count, negativo_source]
                        if valor != '0':
                            np_tupla_vertical_H[external_count, negativo_source] = str(np_tupla_vertical_H[external_count, negativo_source]) + '-1'
                        if valor == '0':
                            np_tupla_vertical_H[external_count, negativo_source] = '-1'
                            
                    #print(search)
                    external_count = external_count + 1
                #print(np_tupla)
                
            #print(np_tupla_horizontal_E)
            #print(np_tupla_vertical_E)




    def girador():
        global mna, vector_corrientes_J, numero_giradores
        x = len(mna)
        y = 2
        C_matrix, C_matrix_np = formula_tamano_n_m(y,x)
        B_matrix, B_matrix_np = formula_tamano_n_m(x,y)
        D_matrix, D_matrix_np = formula_tamano_n_m(2,2)

        vector_corrientes = []

        counter01 = 0
        counter02 = 0

        for renglon in np_netlist:
            elemento = renglon[0]
            elemento02 = renglon[0]
            elemento02 = elemento02[1:]
            #print(elemento02)
            elemento = elemento[:1]
            #print(elemento)
            if str(elemento) == 'J': 
                #print(elemento)
                nod1 = int(renglon[1])-1
                nod2 = int(renglon[2])-1
                nod3 = int(renglon[3])-1
                nod4 = int(renglon[4])-1

                C_matrix_np[0,nod3] = 'J'+str(elemento02)
                C_matrix_np[1,nod1] = '-J'+str(elemento02)

                B_matrix_np[0,nod1] = '1'
                B_matrix_np[1,nod3] = '1'

                D_matrix_np[0,0] = '-1'
                D_matrix_np[1,1] = '-1'
                

                counter01 = counter01+1

                pivote = np.concatenate((B_matrix_np,D_matrix_np))
                temporal_MNA = np.concatenate((mna,C_matrix_np))
                mna = np.concatenate((temporal_MNA,pivote),axis = 1)

                

                vector_corrientes.append('I_Ja'+str(counter01))
                vector_corrientes.append('I_Jb'+str(counter01+1))
                vector_corrientes_J = vector_corrientes
        numero_giradores = counter01
        #print(C_matrix_np)
        #print(B_matrix_np)
        #print(D_matrix_np)


    ## transformer

    def transformer(G_matrix):
        global mna, numero_transformadores, vector_corrientes
        x = len(mna)
        y = 2
        vector_corrientes = []
        C_matrix, np_C_matrix = formula_tamano_n_m(y,x)
        #B_matrix, np_B_matrix = formula_tamano_n_m(x,y)
        D_matrix, np_D_matrix = formula_tamano_n_m(2,2)
        numero_transformadores = 0
        #print(np_C_matrix)
        #print(np_B_matrix)
        #print(np_D_matrix)
        formula_tamano_n_m(x,y)#devuelve una tupla y una numpy
        for renglon in np_netlist:
            
            elemento = renglon[0]
            elemento = elemento[:1]

            if (str(elemento) == 'k') or (str(elemento) == 'K'):
                posL1 = int(renglon[1])-1
                negL1 = int(renglon[2])-1
                posL2 = int(renglon[3])-1
                negL2 = int(renglon[4])-1

                
                #np_C_matrix[y1,x1] = 1
                if posL1 >=0:
                    np_C_matrix[0,posL1] = '-1'
                if negL1 >=0:
                    np_C_matrix[0,negL1] = '1'
                    
                if posL2 >= 0:
                    np_C_matrix[1,posL2] = '-1'
                if negL2 >= 0:
                    np_C_matrix[1,negL2] = '1'

                np_B_matrix = np_C_matrix.transpose()
                
                np_D_matrix[0,0] = str(renglon[8])+'S'
                np_D_matrix[1,1] = str(renglon[9])+'S'
                np_D_matrix[0,1] = 'SM'
                np_D_matrix[1,0] = 'SM'

                #mna2 = np.concatenate((mna2,np_tupla_horizontal_O))
                #mna2 = np.concatenate((mna,np_tupla_vertical_O_transpose),axis = 1)
                pivote = np.concatenate((np_B_matrix,np_D_matrix))
                temporal_MNA = np.concatenate((mna,np_C_matrix))
                mna = np.concatenate((temporal_MNA,pivote),axis = 1)

                numero_transformadores = numero_transformadores + 1

                vector_corrientes.append('I_'+str(renglon[8]))
                vector_corrientes.append('I_'+str(renglon[9]))
                #print(temporal_MNA)
                #print(pivote)
                #print(np_C_matrix)
                #print(np_D_matrix)
                #print(np_B_matrix)
            #print(renglon)
        #print(vector_corrientes)





    ################################## En esta seccion se formula el vector de corrientes por fuentes de V#####################################
    numero_n_v = busca_elemento_mayor('V',np_elemento)
    V_matrix,V_matrix_pd,V_matrix_np = Make_G_Matrix_pre001(matrix,'V',orden,numero_n)
    I_matrix,I_matrix_pd,I_matrix_np = Make_G_Matrix_pre001(matrix,'I',orden,numero_n)
    #print(''+str(V_matrix_np))

    #formulamos, y buscamos la polaridad del elemento:
    def formula(matrix_np,Elemento,nodo_de_busqueda):
        matrix_np = matrix_np.transpose()
        #print(matrix_np)
        temp = []
        #print(Elemento)
        for renglon in matrix_np:
            if sum(renglon) > 0:
                tempo_Vec = []
                pos_renglon = 0
                for pos in renglon:
                    if pos >= 1:
                        temporal_delete = Elemento+str(pos)
                        delete_counter = 0
                        for search in np_conjunto:
                            #print(search)
                            if search[0] == temporal_delete:
                                #print('search[nodo_de_busqueda]: ' + str(search[nodo_de_busqueda]))
                                #
                                #print('pos_renglon+1: '+str(pos_renglon+1))
                                if search[nodo_de_busqueda] > pos_renglon+1:##Aqui podemos cambiar el modo de busqueda 1)para V, 2)para I
                                    
                                    if Elemento == 'V' or Elemento == 'I':
                                        
                                        pos = pos*-1
                                
                            delete_counter = delete_counter + 1
                        #print(pos)
                        pos = pos/abs(pos)
                        pos = int(pos)
                        pos = str(pos)
                    tempo_Vec.append(int(pos))
                    pos_renglon = pos_renglon + 1 
                temp.append(tempo_Vec)
        
        matrix_np = np.array(temp,dtype=object)
        #print(matrix_np)
        #if nodo_de_busqueda == 2:
            
            #print(matrix_np)
            
        return(matrix_np)
            
    ################################# Formula el MNA sol fuentes de V       #######################################################################
    def rectifica_V():
        #print(np_conjunto)
        simple_counter = 0
        for search in np_conjunto:
            #print(search)
            V = search[0]
            V = V[:-len(V)+1]
            #print(V)
            if str(V) == 'V':
                #print(search)
                positivo = search[1]-1
                negativo = search[2]-1
                if positivo >= 0:
                    V_matrix_np[simple_counter,positivo] = 1
                if negativo >= 0:
                    V_matrix_np[simple_counter,negativo] = -1
                
                simple_counter = simple_counter + 1
    V_matrix_np = formula(V_matrix_np,'V',1)#nodo de busqueda = 1 es tomado como negativo
    I_matrix_np = formula(I_matrix_np,'I',2)
    rectifica_V()
    #print('here')
    #print(V_matrix_np)
    if len(V_matrix_np) == 0:
        mna = np_G
    if len(V_matrix_np) > 0:
        mna = np.concatenate((np_G,V_matrix_np))
    #print(mna)

    def make_D(V_matrix_np):
        D = []
        limit = len(V_matrix_np)
        #print(limit)
        for x in range(limit):
            temp = []
            for y in range(limit):
                temp.append(0)
            D.append(temp)
        D = np.array(D)
        return(D)


    D = make_D(V_matrix_np)

    V_matrix_np_T = V_matrix_np.transpose()
    #print(V_matrix_np_T)
    #print(len(I_matrix_np))
    if len(V_matrix_np) > 0:
        identifica_cccs(numero_n_F,len(V_matrix_np)) # aqui añadimos las ganancias de cccs
    if len(I_matrix_np) > 0:
        identifica_cccs(numero_n_F,len(I_matrix_np))
    V_matrix_np_T = np.concatenate((V_matrix_np_T,D))

    if len(V_matrix_np_T) > 0:
        mna = np.concatenate((mna,V_matrix_np_T), axis=1)

    #>>________________________________añadimos los OAmps al MNA________________________________________
    identifica_OpAmp(numero_n_O,len(V_matrix_np))
    enable_opAmp = 0
    if numero_n_O > 0:
        #print(np_tupla_horizontal_O)
        D_O = make_D(np_tupla_horizontal_O)
        np_tupla_horizontal_O = np.concatenate((np_tupla_horizontal_O,D_O),axis = 1)
        #print(np_tupla_horizontal_O)
        np_tupla_vertical_O_transpose = np_tupla_vertical_O.transpose()
        #print(np_tupla_vertical_O_transpose)
        #print(mna)
        mna2 = np.concatenate((mna,np_tupla_vertical_O_transpose),axis = 1)
        mna2 = np.concatenate((mna2,np_tupla_horizontal_O))
        mna = mna2
        enable_opAmp = 1
    #    for renglones in np_tupla_orizontal:
    #        D_O = make_D(renglones)
    #        print('------------------------D_O-------------------------')
    #        print(D_O)
            #np_tupla_orizontal = np.concatenate((np_tupla_orizontal,D), axis=1)
            #print(np_tupla_orizontal)

    #>>_____________añadimos la fuente de voltaje controlada por voltaje (vcvs) al MNA__________________
    identifica_E(numero_n_E,len(V_matrix_np))
    enable_vcvs = 0
    if numero_n_E > 0:
        D_vcvs = make_D(np_tupla_horizontal_E)
        np_tupla_horizontal_E = np.concatenate((np_tupla_horizontal_E,D_vcvs),axis = 1)
        np_tupla_vertical_E_transpose = np_tupla_vertical_E.transpose()
        mna2E = np.concatenate((mna,np_tupla_vertical_E_transpose),axis = 1)
        mna2E = np.concatenate((mna2E,np_tupla_horizontal_E))
        #print(mna2E)
        mna = mna2E
        enable_vcvs = 1

    identifica_H(numero_n_H,len(V_matrix_np))
    enable_vcvs = 0
    if numero_n_H > 0:
        
        D_vcvs = make_D(np_tupla_horizontal_H)
        
        np_tupla_horizontal_H = np.concatenate((np_tupla_horizontal_H,D_vcvs),axis = 1)
        
        np_tupla_vertical_H_transpose = np_tupla_vertical_H.transpose()
        mna2H = np.concatenate((mna,np_tupla_vertical_H_transpose),axis = 1)
        #print('here!!!!!!!!!!!!!!!!!!!!!11')
        mna2H = np.concatenate((mna2H,np_tupla_horizontal_H))
        #print(mna2E)
        mna = mna2H
        enable_vcvs = 1
        

    identifica_vccs(numero_n_G,len(V_matrix_np))
    #añadimos el girador
    girador()
    #añadimos el transformador
    transformer(mna)
    ################################## En esta seccion se formula el vector de corrientes por fuentes de V#####################################
    #print('numero de opamps:      '+ str(numero_n_O))

    ##################################           En esta seccion se formula el vector X        #####################################
    def vector_X(enable_opAmp,numero_n_O):
        global pivote_v, numero_transformadores, vector_corrientes, numero_giradores
        global vector_corrientes_J
        pivote_v = []
        X = []
        v = 'V_'
        i = 'Iv_'
        O = 'I_OAmp_'
        E = 'I_E'
        H = 'I_H'
        i_empty = 'I_'
        counter = 0
        temporal = ''
        x = []
        index = []
        counter_H = 0
        counter_E = 0
        counter_K = 0
        counter_J = 0
        for pos_X in range(len(mna)):
            tempo = []
            counter = counter +1 
            if counter <= len(np_G):
                temporal = v + str(counter)
                pivote_v.append(0)
                tempo.append(temporal)
            if counter > len(np_G):
                temporal = i + str(counter-len(np_G))
                #tempo.append(temporal)
                ######>> aqui añadimos el opamp al vector de incognitas
                if numero_n_O > 0:
                    #print('here!!!!'+'  counter: '+str(counter))
                    if counter > (len(np_G) + numero_n_V):
                        temporal = O + str(counter-len(np_G)-numero_n_V)
                #####>> aqui añadimos la vcvs al vector de incognitas
                if numero_n_E > 0:
                    if counter > (len(np_G) + numero_n_V + numero_n_O):
                        counter_E = counter_E + 1
                        temporal = E + str(counter_E)
                #####>> aqui añadimos la ccvs al vector de incognitas
                if numero_n_H >0:
                    if counter > (len(np_G) + numero_n_V + numero_n_O + numero_n_E):
                        #print('counter_here!!!!!!!!')
                        #print(counter)
                        counter_H = counter_H + 1
                        temporal = H + str(counter_H)

                if numero_giradores > 0:
                    if len(vector_corrientes_J) > 0:
                        if counter > (len(np_G) + numero_n_V + numero_n_O + numero_n_E + numero_n_H):
                            temporal = vector_corrientes_J[counter_J]
                            counter_J = counter_J + 1
                            
                if numero_transformadores > 0:
                    if len(vector_corrientes) > 0:
                        if counter > (len(np_G) + numero_n_V + numero_n_O + numero_n_E + numero_n_H + numero_giradores):
                            #print(counter_K)
                            temporal = vector_corrientes[counter_K]
                            counter_K = counter_K + 1
                
                tempo.append(temporal)
            X.append(tempo)
            index.append(counter)
            x.append(temporal)
        Xsal = np.array(X,dtype=object)
        return(Xsal,index,x) 
    global i_ndex,X,Z    
    X,i_ndex,x = vector_X(enable_opAmp,numero_n_O)

    #print('imprime salidas')




    A = mna
    #print('//////')
    #print(A)
    pd_A = pd.DataFrame(A, columns=i_ndex, index = i_ndex)




    pd_X = pd.DataFrame(X, columns=['Vector x'],index=i_ndex)
    #print(space)
    #print(pd_A) #><<<<<<<< aqui
    #no usado: #pd_A.to_csv('A.csv', header=None, index=None, sep=' ', mode='a')
    pd_A.to_csv(str(name2) + '.csv',header=None, index=None)
    #pd_A.to_csv
    #print(space)
    #print(pd_X) #><<<<<<<< aqui




    ###########################################################################################################################################
    ##################################           En esta seccion se formula el vector Z        #####################################
    #
    def make_vector_sice_scalar(scalar):
        V = scalar
        counter = 0
        Z = []
        for z in range(numero_n_v):
            counter = counter + 1
            Z.append(counter)
        return(Z)
    def make_vector_symbolic_I(valor,vector):
        
        salida = []
        temporal = ''
        menos = '-'
        mas = '+'
        I = 'I'
        if len(vector) == 1:
            vector = vector[0]
            for i in vector:
                if i != 0:
                    if i < 1:
                        temporal = menos + valor + str(abs(i))
                    if i >= 1:
                        temporal = valor + str(abs(i))
                if i == 0:
                    temporal = 0
                salida.append(temporal)
                
            salida = np.array([salida], dtype=object)
            salida = salida.transpose()
            return(salida)
        if len(vector) > 1:
            external_counter = 0
            salida2 = []
            for internal_vector in vector:
                salida2 = make_a_tuple(len(internal_vector),0)
                break
            for internal_vector in vector:         
                counter = 0
                valor = ''
                for i in internal_vector:
                    if i != 0:
                        if str(salida2[counter]) == '0':
                            salida2[counter] = ''
                        if (i < 0):
                            valor = menos + I  + str(external_counter+1)
                        if (i > 0):
                            valor = mas + I + str(external_counter+1)
                        salida2[counter] = salida2[counter] + valor
                    counter = counter + 1
                external_counter = external_counter + 1
            salida2 = np.array([salida2], dtype=object)
            salida2 = salida2.transpose()
            return(salida2)

    def make_vector_symbolic_V(valor,vector):
        #print(vector)
        salida = []
        temporal = ''
        menos = '-'
        for i in vector:
            #print(i)
            if i != 0:
                if i < 1:
                    temporal = menos + valor + str(abs(i))
                if i >= 1:
                    temporal = valor + str(abs(i))
            salida.append(temporal)
        salida = np.array([salida], dtype=object)
        salida = salida.transpose()
        return(salida)
    global Z, z
    def vector_Z(i_ndex):
        global V_matrix_np, I_matrix_np,Z,V,I,pivote_v
        global pd_Z, Z, numero_transformadores, numero_giradores
        pivote_v = np.array([pivote_v])
        
        numero_n_v = busca_elemento_mayor('V',np_elemento)
        V_matrix_np = make_vector_sice_scalar(numero_n_v)
        V = make_vector_symbolic_V('V',V_matrix_np)
        
        numero_n_i = busca_elemento_mayor('I',np_elemento)
        I_matrix,I_matrix_pd,I_matrix_np = Make_G_Matrix_pre001(matrix,'I',orden,numero_n)
        tempo = I_matrix
        
        I_matrix_np = formula(I_matrix_np,'I',2) # nodo = 2, es tomado como nodo negativo
        I_matrix_np = I_matrix_np.astype(np.int32)
        if len(I_matrix_np) == 0:
            I_matrix_np = pivote_v
        
        I = make_vector_symbolic_I('I',I_matrix_np)
        #print(I)
        #print(space)
        
        I_np = np_netlist.transpose()
        I_np = I_np[0]
        #print(I_np)
        counter_i = 0
        for i in I_np:
            ##print(i)
            ii = i[:1]
            #print(ii)
            if ii == 'I':
                positivo = np_netlist[counter_i,2]-1
                negativo = np_netlist[counter_i,1]-1
                #print('positivo' + str(positivo))
                #print('negativo' + str(negativo))
                if positivo >= 0:
                    I[positivo] = i
                if negativo >= 0:
                    #print('here')
                    I[negativo] = '-'+str(i)
            counter_i = counter_i + 1
        #I_counter = 0
        #for elemento_I in I:
        #    #print(elemento_I[0])
        #    I_counter_netlist = 0
        #    for busqueda_009 in I_np:
        #        if str(elemento_I[0]) == str(busqueda_009):
        #            print(str(elemento_I[0])+'       '+str(busqueda_009)+'         '+str(I_counter_netlist)+'                         '+str(I_counter))
        #            I[np_netlist[1]-1] = '-'+str(busqueda_009)                    
        #        I_counter_netlist = I_counter_netlist + 1
        #    I_counter = I_counter + 1
        if numero_n_O == 0:
            Z = np.concatenate([I,V])
            #print(Z)
            
        if numero_n_O > 0:
            opAmps_volt = make_a_tuple(numero_n_O,0)
            #print(opAmps_volt)
            #print(I)
            #print(V)
            opAmps_volt = np.array([opAmps_volt])
            opAmps_volt = opAmps_volt.transpose()
            Z = np.concatenate([I,V,opAmps_volt])
            #print(Z)
        if numero_n_E > 0:
            vcvs_volt = make_a_tuple(numero_n_E,0)
            vcvs_volt = np.array([vcvs_volt])
            vcvs_volt = vcvs_volt.transpose()
            Z = np.concatenate([Z,vcvs_volt])
        if numero_n_H > 0:
            ccvs_volt = make_a_tuple(numero_n_H,0)
            ccvs_volt = np.array([ccvs_volt])
            ccvs_volt = ccvs_volt.transpose()
            Z = np.concatenate([Z,ccvs_volt])

        if numero_giradores > 0:
            temp_g = 2*numero_giradores
            np_tempo_gir = np.array([make_a_tuple(temp_g,0)])
            Z = np.concatenate([Z,np_tempo_gir.transpose()])
           
        if numero_transformadores > 0:
            temp_L = 2*numero_transformadores
            np_tempo_transformer = np.array([make_a_tuple(temp_L,0)])
            Z = np.concatenate([Z,np_tempo_transformer.transpose()])
            #print(np_tempo_transformer)
        #print(Z)
        #print(numero_transformadores)
        pd_Z = pd.DataFrame(Z, columns=['Vector z'],index=i_ndex)
        #print(pd_Z) #><<<<<<<< aqui

    vector_Z(i_ndex)

    #print(space)
    #print(space)
    #print(space)
    #print(space)
    #print(space)
    #print(space)
    #print(space)
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
    #print(mna)
    #print(X)
def mna_to_symbolic(mna):
    
    space2 = ('**************************************************************************')
    y_mna = 0
    global dictionary,dict_R,dict_C,dict_L,dict_V,dict_I,dict_E,dict_F,dict_G,dict_H,dict_O,dict_K,dict_J,dict_V_,dict_Iv_,dict_I_OAmp_,dict_I_E,dict_I_H,dict_I_,dict_S
    #print('mna')
    #print(mna)
    for renglon in mna:
        x_mna = 0
    
        for cadena in renglon:
            counter = 0
            count_inf = 0
            count_sup = 0
            paquete = []
            temporal = ''
            temporal2 = ''
 
            if type(cadena) == str:
                for letra in cadena:
                    if (counter == 0):
  
                        if (str(letra) != '+'):
                            temporal = '+'
                        if (str(letra) != '-'):
                            temporal = '+'
                        if (str(letra) == '+') or (str(letra) == '-'):
                            temporal = ''
 
                    temporal = temporal+letra
                    counter = counter + 1

            #print(temporal)
            signo = ''
            if len(temporal) > 0:
                #print('>>cadena:    '+str(temporal))
                cadena_simbolica = 0
                #print(temporal)
                for letra in temporal:
                    #print('letra   '+str(letra))
                    if str(letra) == '+':
                        
                        S = dictionary.get('S')
                   
                  
                        variable = temporal[count_inf:count_sup]
                        #print('>>             variable'+str(variable))
                        symbol_var = dictionary.get(variable[1:])
                        if str(variable) == '-1':#<------------------------------------------revisa aqui, esto no tendria que ser, funciona pero no va
                            symbol_var = dictionary.get('-1')
                            #print('salida del if:     ' + str(symbol_var))
                        signo = variable[:1]
                    
                    
                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'R':
                    
                                symbol_var = 1/symbol_var
                      
                        except:
                            pass

                        try:
     
                            simbolo = str(variable[1])
                            if simbolo == 'C':
                                symbol_var = symbol_var * S 
                       
                        except:
                            pass

                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'L':
                                symbol_var = 1/(symbol_var * S)
                            
                   
                        except:
                            pass
                    
                        if str(symbol_var) != 'None':
                            #print('symbol_var       ' + str(symbol_var))
                            cadena_simbolica = cadena_simbolica + symbol_var
                        count_inf = count_sup



                    #########################################################################################
                    if str(letra) == '-':
                        
                        S = dictionary.get('S')
                        #symbol_var = None
                    
                   
                        variable = temporal[count_inf:count_sup]
                        #print('>>             variable'+str(variable))
                        symbol_var = dictionary.get(variable[1:])
                        signo = variable[:1]
                        if str(symbol_var) != 'None':
                            symbol_var = -1*symbol_var
                
                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'R':
                                symbol_var = 1/symbol_var
                        
                        
                        
                        except:
                            pass
                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'C':
                                symbol_var = symbol_var * S

                        
                        except:
                            pass

                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'L':
                                symbol_var = 1/(symbol_var * S)
                            
                        
                        except:
                            pass
                    
                        if str(symbol_var) != 'None':
                            #print(symbol_var)
                            cadena_simbolica = cadena_simbolica + symbol_var
                        count_inf = count_sup
                    count_sup = count_sup + 1



                    #########################################################################################
                    if len(temporal) == count_sup:
                        
                        symbol_var = None
                    
                        variable = temporal[count_inf:count_sup]
                        #print(temporal)
                        #print('>>             variable'+str(variable))
                        symbol_var = dictionary.get(variable[1:])
                        
                        S = dictionary.get('S')
                        
                        signo = variable[:1]
                        #print(symbol_var)
                        if signo == '-':
                            #print(symbol_var)
                            symbol_var = symbol_var*-1
                        tempo_var = variable[1:]
                        tipo_var = tempo_var[:1]
                    
                        simbolo = str(variable[1])
                    
                        try:
                        
                            #if signo == '-':
                            #    symbol_var = symbol_var*-1
                            tempo_var = variable[1:]
                            tipo_var = tempo_var[:1]
                        
                            if simbolo == 'R': 
                                symbol_var = 1/symbol_var
                        
                        except:
                            pass
                        
                        try:
                        
                            #if signo == '-':
                            #    symbol_var = -1*symbol_var
                            tempo_var = variable[1:]
                            tipo_var = tempo_var[:1]
                            if simbolo == 'C':
                                symbol_var = symbol_var * S
                        
                        except:
                            pass
                        
                        try:
                            #print(signo)
                            #if signo == '-':
                            #    symbol_var = -1*symbol_var
                            #print('symbol_var:  ' + str(symbol_var))
                            tempo_var = variable[1:]
                            tipo_var = tempo_var[:1]
                            if simbolo == 'L':
                                symbol_var = 1/(symbol_var * S)
                           
                        except:
                            pass


                        
                        if str(variable) == '+L2S':#<------------------------------------------revisa aqui, esto no tendria que ser, funciona pero no va
                            symbol_var = dictionary.get('L2S')
                        if str(variable) == '+L1S':#<------------------------------------------revisa aqui, esto no tendria que ser, funciona pero no va
                            symbol_var = dictionary.get('L1S')
                        if str(symbol_var) != 'None':
                            #print(symbol_var)

                            
                            cadena_simbolica = cadena_simbolica + symbol_var
                #print(cadena_simbolica)
                #print('x: ' + str(x_mna))
                #print('y: ' + str(y_mna))
                mna[y_mna,x_mna] = cadena_simbolica
            x_mna = x_mna + 1 
        
        y_mna = y_mna + 1
    return(mna)

####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################




####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
def X_to_symbolic(mna):
    space2 = ('**************************************************************************')
    y_mna = 0
    for renglon in mna:
        x_mna = 0
    
        for cadena in renglon:
            counter = 0
            count_inf = 0
            count_sup = 0
            paquete = []
            temporal = ''
            temporal2 = ''
            print(cadena)
            print(type(cadena))
            if type(cadena) == str:
                for letra in cadena:
                    print('aqui')
                    print(letra)
                    if (counter == 0):
  
                        if (str(letra) != '+'):
                            temporal = '+'
                        if (str(letra) != '-'):
                            temporal = '+'
                        if (str(letra) == '+') or (str(letra) == '-'):
                            temporal = ''
 
                    temporal = temporal+letra
                    counter = counter + 1

            print('temporal:    ' + str(temporal))
            signo = ''
            if len(temporal) > 0:
                print('>>cadena:    '+str(temporal))
                cadena_simbolica = 0
                for letra in temporal:
          
                    if str(letra) == '+':
                    
                        S = dictionary.get('S')
                   
                  
                        variable = temporal[count_inf:count_sup]
                    
                        symbol_var = dictionary.get(variable[1:])
                        signo = variable[:1]
                    
                    
                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'R':
                    
                                symbol_var = 1/symbol_var
                      
                        except:
                            pass

                        try:
     
                            simbolo = str(variable[1])
                            if simbolo == 'C':
                                symbol_var = symbol_var * S 
                       
                        except:
                            pass

                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'L':
                                symbol_var = 1/(symbol_var * S)
                            
                   
                        except:
                            pass
                    
                        if str(symbol_var) != 'None':
                            #print(symbol_var)
                            cadena_simbolica = cadena_simbolica + symbol_var
                        count_inf = count_sup



                    #########################################################################################
                    if str(letra) == '-':
                        S = dictionary.get('S')
                        #symbol_var = None
                    
                   
                        variable = temporal[count_inf:count_sup]
                    
                        symbol_var = dictionary.get(variable[1:])
                        signo = variable[:1]
                        if str(symbol_var) != 'None':
                            symbol_var = -1*symbol_var
                
                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'R':
                                symbol_var = 1/symbol_var
                        
                        
                        
                        except:
                            pass
                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'C':
                                symbol_var = symbol_var * S

                        
                        except:
                            pass

                        try:
                        
                            simbolo = str(variable[1])
                            if simbolo == 'L':
                                symbol_var = 1/(symbol_var * S)
                            
                        
                        except:
                            pass
                    
                        if str(symbol_var) != 'None':
                            #print(symbol_var)
                            cadena_simbolica = cadena_simbolica + symbol_var
                        count_inf = count_sup
                    count_sup = count_sup + 1



                    #########################################################################################
                    if len(temporal) == count_sup:
                        symbol_var = None
                    
                        variable = temporal[count_inf:count_sup]
                    
                        symbol_var = dictionary.get(variable[1:])
                        S = dictionary.get('S')
                    
                        signo = variable[:1]
                    
                        if signo == '-':
                            symbol_var = symbol_var*-1
                        tempo_var = variable[1:]
                        tipo_var = tempo_var[:1]
                    
                        simbolo = str(variable[1])
                    
                        try:
                        
                            #if signo == '-':
                            #    symbol_var = symbol_var*-1
                            tempo_var = variable[1:]
                            tipo_var = tempo_var[:1]
                        
                            if simbolo == 'R': 
                                symbol_var = 1/symbol_var
                        
                        except:
                            pass
                        
                        try:
                        
                            #if signo == '-':
                            #    symbol_var = -1*symbol_var
                            tempo_var = variable[1:]
                            tipo_var = tempo_var[:1]
                            if simbolo == 'C':
                                symbol_var = symbol_var * S
                        
                        except:
                            pass
                        
                        try:
                            #print(signo)
                            #if signo == '-':
                            #    symbol_var = -1*symbol_var
                            #print('symbol_var:  ' + str(symbol_var))
                            tempo_var = variable[1:]
                            tipo_var = tempo_var[:1]
                            if simbolo == 'L':
                                symbol_var = 1/(symbol_var * S)
                           
                        except:
                            pass
                       
                        if str(symbol_var) != 'None':
                            #print(symbol_var)
                            cadena_simbolica = cadena_simbolica + symbol_var
                #print(cadena_simbolica)
                #print('x: ' + str(x_mna))
                #print('y: ' + str(y_mna))
                mna[y_mna,x_mna] = cadena_simbolica
            x_mna = x_mna + 1 
        
        y_mna = y_mna + 1
    return(mna)
####################################################################################################
####################################################################################################
####################################################################################################
def conv(dato):
    signo = ''
    salida = ''
    remanente = ''
    c = 0
    while(1):
        #print(dato)
        for k in range(len(dato)):
            if k < len(dato)-1:
                #print('k',k)
                if (dato[k] == '+' or dato[k] == '-') and (dato[k+1] == '+' or dato[k+1] == '-'):
                    if dato[k] == '+' and dato[k+1] == '+':
                        dato = dato[:k] +'+'+ dato[k+2:]
                        break
                    if dato[k] == '+' and dato[k+1] == '-':
                        dato = dato[:k] +'-'+ dato[k+2:]
                        break
                    if dato[k] == '-' and dato[k+1] == '+':
                        dato = dato[:k] +'-'+ dato[k+2:]
                        break
                    if dato[k] == '-' and dato[k+1] == '-':
                        dato = dato[:k] +'+'+ dato[k+2:]
                        break
        if len(dato)-1 == k:
            #print(dato)
            return dato
            break
        c += 1             
        if c == 500:  
            print('salida de emergencia')
            return dato
            break
####################################################################################################
####################################################################################################
def charTOSymbols(A):
    global dictionary,dict_R,dict_C,dict_L,dict_V,dict_I,dict_E,dict_F,dict_G,dict_H,dict_O,dict_K,dict_J,dict_V_,dict_Iv_,dict_I_OAmp_,dict_I_E,dict_I_H,dict_I_,dict_S
    y,x = np.shape(A)
    #print('x',x,'   y',y)
    s = symbols('s')
    #print(A)
    #print('*********************',s)
    for yy in range(y):
        for xx in range(x):
            #print(A[yy,xx],type(A[yy,xx]))
            if type(A[yy,xx]) == str:
                #print('string')
                tempo = A[yy,xx]
                tempo += '+'
                
                if tempo[:1] != '-':
                    tempo = '+' + tempo
                tempo = conv(tempo)
                A[yy,xx] = tempo
                #print('tempo: ',tempo)
    for yy in range(y):
        for xx in range(x):
            palabra = A[yy,xx]
            signo = ''
            variable = ''
            simbolo = 0
            out = 0
            if type(palabra) == str:
                for k in range(len(palabra)):
                    #print('k: ',k)
                    if k == 0:
                        signo = palabra[k]
                    if (k > 0) and (palabra[k] != '+' and palabra[k] != '-'):
                        #print('condicion2: ',palabra[k])
                        variable += palabra[k]
                    if (k > 0) and (palabra[k] == '+' or palabra[k] == '-') and (k < len(palabra)):
                        #print('aqui')
                        simbolo = symbols(variable)
                        #print('variable',variable)
                        #print('simbolo',simbolo)
                        #print('signo',signo)
                        if signo == '-':
                            simbolo = simbolo*-1
                        if variable[:1] == 'R':
                            simbolo = 1/simbolo
                        if variable[:1] == 'C':
                            simbolo = simbolo * s
                        if variable[:1] == 'L':
                            t = variable[1]
                            if t == '0' or t == '1' or t == '2' or t == '3' or t == '4' or t == '5' or t == '6' or t == '7' or t == '8' or t == '9':
                               simbolo = 1/(simbolo*s) 
                        out = out+simbolo
                        signo = palabra[k]
                        variable = ''
                    A[yy,xx] = out
                    
    return A
####################################################################################################
def charTOSymbols2(A):
    global dictionary,dict_R,dict_C,dict_L,dict_V,dict_I,dict_E,dict_F,dict_G,dict_H,dict_O,dict_K,dict_J,dict_V_,dict_Iv_,dict_I_OAmp_,dict_I_E,dict_I_H,dict_I_,dict_S
    y,x = np.shape(A)
    #print('x',x,'   y',y)
    s = DDDSym('s')
    #print(s,type(s))
    #print(A)
    #print('*********************',s)
    for yy in range(y):
        for xx in range(x):
            #print(A[yy,xx],type(A[yy,xx]))
            if type(A[yy,xx]) == str:
                #print('string')
                tempo = A[yy,xx]
                tempo += '+'
                
                if tempo[:1] != '-':
                    tempo = '+' + tempo
                tempo = conv(tempo)
                A[yy,xx] = tempo
                #print('tempo: ',tempo)
    for yy in range(y):
        for xx in range(x):
            palabra = A[yy,xx]
            signo = ''
            variable = ''
            simbolo = 0
            out = 0
            if type(palabra) == str:
                for k in range(len(palabra)):
                    #print('k: ',k)
                    if k == 0:
                        signo = palabra[k]
                    if (k > 0) and (palabra[k] != '+' and palabra[k] != '-'):
                        #print('condicion2: ',palabra[k])
                        variable += palabra[k]
                    if (k > 0) and (palabra[k] == '+' or palabra[k] == '-') and (k < len(palabra)):
                        #print('aqui')
                        simbolo = DDDSym(variable)
                        #print('variable',variable)
                        #print('simbolo',simbolo)
                        #print('signo',signo)
                        if signo == '-':
                            simbolo = simbolo*-1
                        if variable[:1] == 'R':
                            simbolo = 1/simbolo
                        if variable[:1] == 'C':
                            simbolo = simbolo * s
                        if variable[:1] == 'L':
                            t = variable[1]
                            if t == '0' or t == '1' or t == '2' or t == '3' or t == '4' or t == '5' or t == '6' or t == '7' or t == '8' or t == '9':
                               simbolo = 1/(simbolo*s) 
                        out = out+simbolo
                        signo = palabra[k]
                        variable = ''
                    A[yy,xx] = out
                    
    return A
####################################################################################################



def formula_sympy():
    global mna,x,z, i_ndex,X,A,x,z,pd_A,pd_x,pd_z
    #mna = mna_to_symbolic(mna)
    mna = charTOSymbols(mna)
    A = mna
    pd_A = pd.DataFrame(A, columns=i_ndex, index = i_ndex)
    A = Matrix(A)
    #print(pd_A)



    #x = mna_to_symbolic(X)
    x = charTOSymbols(X)
    pd_x = pd.DataFrame(x, columns=['Vector x'],index=i_ndex)
    x = Matrix(x)
    #print(pd_x)


    #z = mna_to_symbolic(Z)
    z = charTOSymbols(Z)
    pd_z = pd.DataFrame(z, columns=['Vector z'],index=i_ndex)
    z = Matrix(z)
    #print(pd_z)
    return(A,x,z)


def formula_DDD():
    global mna,x,z, i_ndex,X,A,x,z,pd_A,pd_x,pd_z
    #mna = mna_to_symbolic(mna)
    mna = charTOSymbols2(mna)
    A = mna
    pd_A = pd.DataFrame(A, columns=i_ndex, index = i_ndex)
    #A = Matrix(A)
    #print(pd_A)



    #x = mna_to_symbolic(X)
    x = charTOSymbols2(X)
    pd_x = pd.DataFrame(x, columns=['Vector x'],index=i_ndex)
    #x = Matrix(x)
    #print(pd_x)


    #z = mna_to_symbolic(Z)
    z = charTOSymbols2(Z)
    pd_z = pd.DataFrame(z, columns=['Vector z'],index=i_ndex)
    #z = Matrix(z)
    #print(pd_z)
    return(A,x,z)

    #############################SOLUCION SIMBOLICA#####################################################
    ####################################################################################################
    ####################################################################################################
    ####################################################################################################
    ####################################################################################################
    ####################################################################################################
    ####################################################################################################
    
    #from numpy.linalg import inv
#case 1, if a matriz is a dense matrix
def resuelve_GE(A,x,z):#gaus
    tiempo = time()
    global Z,space,space2
    #print(A)
    A = Matrix(A)
    x = Matrix(x)
    z = Matrix(z)
    G = A.inv(method='GE')
    X = G * Z
    counter_x = 0
    print('tiempo de calculo en sympy GE: ',time()-tiempo)
    return(X)


def resuelve_ADJ(A,x,z):
    tiempo = time()
    global Z,space,space2
    #print(A)
    A = Matrix(A)
    x = Matrix(x)
    z = Matrix(z)
    G = A.inv(method='ADJ')
    X = G * Z
    print('tiempo de calculo en sympy ADJ: ',time()-tiempo)
    return(X)

def resuelve_LU(A,x,z):
    tiempo = time()
    global Z,space,space2
    #print(A)
    A = Matrix(A)
    x = Matrix(x)
    z = Matrix(z)
    G = A.inv(method='LU')
    X = G * Z
    print('tiempo de calculo en sympy LU: ',time()-tiempo)
    return X


#case 2, if the matrix is a sparce matrix Cholesky or LDL (default)
def resuelve_CH(A,x,z):
    global Z,space,space2
    #print(A)
    A = Matrix(A)
    x = Matrix(x)
    z = Matrix(z)
    G = A.inverse_CH()
    X = G * Z
    counter_x = 0
    for pos in X:
        #print(space)
        #print(str(x[counter_x]) + ' = ' + str(pos))
        counter_x = counter_x + 1
    return(X)
def resuelve_LDL(A,x,z):
    global Z,space,space2
    #print(A)
    A = Matrix(A)
    x = Matrix(x)
    z = Matrix(z)
    G = A.inverse_LDL()
    X = G * Z
    counter_x = 0
    for pos in X:
        #print(space)
        #print(str(x[counter_x]) + ' = ' + str(pos))
        counter_x = counter_x + 1
    return(X)
def simplifica(entrada):
    salida = simplify(entrada)
    return(salida)

def resuelve_serie_DDD(A,x,z):
    X = DDD.DDDs(A,x,z)
    X = Matrix(X)
    return X

def resuelve_paralelo_DDD(A,x,z,N_procesos):
    
    print(N_procesos)
            
