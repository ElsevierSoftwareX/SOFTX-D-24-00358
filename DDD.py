# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 15:46:03 2023

@author: luico
"""
print('DDD15V3')
from random import choice
from symengine import symbols as dta_sym
import numpy as np
import time as tm
from time import time
import sys
import copy
from memory_profiler import profile
import gc
import multiprocessing as mp
import pandas as pd
global dic1, dic2#, DATA, trayectoria
dic1 = {}; dic2 = {}

 

#% layer 1 to k   ***********************************************************************************************************************************

def make_layer_1(herencia,elimina):
    child_layer = []

    for puntero in herencia:

        if puntero[1] != elimina[1]:
            paquete = [puntero[0]+1,puntero[1]]
            child_layer.append(paquete)

    nuevo_elimina = child_layer[0]
    return child_layer,len(child_layer),nuevo_elimina
#@profile
def operacion(sym_ob1,sym_ob2):
    #print(sys.getsizeof(self.n))
    #print('here!!!')
    global dic1
    prediccion1 = str(sym_ob1)+'*'+str(sym_ob2)
    prediccion2 = str(sym_ob2)+'*'+str(sym_ob1)
    #print('prediccion: ',prediccion1)
    #print('dic 1 before op',dic1)
    s1 = dic1.get(prediccion1)
    s2 = dic1.get(prediccion2)
    #print('s1',s1)
    #print('s2',s2)
    if s1 != None:
        op = s1
        #print('pasa')
    if s2 != None:
        op = s2
        #print('pasa')
    #if ((s1 != None) or (s2 != None)):
    #    op = s1
    #    print(':)')
    else:
        op = sym_ob1*sym_ob2
        #tamaño_dic = sys.getsizeof(dic1)#<------------------------- aqui
        #                                # cte to GB: 1,073,741,824 = 1073741824 
        #print('tamaño dic',tamaño_dic,'bytes')
        dic1[str(op)] = op
            
    #print('dic 1 after op',dic1)
    del prediccion1, prediccion2, s1, s2
    return op
#@profile
def operacion2(sym1,sym2):
    global dic2
    op = sym1*sym2
    dic2[str(op)] = op
    #return dic2
    del op


def send_dta(DATA_vec,old_obj,estatus_mult,mult_signo_old,a):
    #print('-------------------ok')  
    long_capa = len(DATA_vec[0])
               
 
    count_pos_layer_puntero = DATA_vec[5]
    #print('\n>>>>>>>>count_pos_layer_puntero: ',count_pos_layer_puntero,'|||| long_capa: ',long_capa)
    #print('*********long_capa:  ',long_capa,' level_layer: ',self.level)
    if long_capa >= 3:
        #print(DATA_vec)
        elimina = DATA_vec[0];
        DATA_vec[3] = estatus_mult
  
            
        elimina = elimina[count_pos_layer_puntero]
        simbolo_de_capa = a[elimina[0],elimina[1]]
        #print('simbolo de capa: ',simbolo_de_capa)
        #print('old obj: ',old_obj)
        if simbolo_de_capa != 0 and old_obj != 0: 
            
            multiplicacion_simbolos = operacion(old_obj*DATA_vec[3],simbolo_de_capa)
            #print('here_inicio!!',multiplicacion_simbolos,'       ',DATA_vec[3],',    old:',old_obj,'     , new',simbolo_de_capa)
        else:
        #simbolo_de_capa == 0:
            multiplicacion_simbolos = 0
                
        DATA_vec[1] = multiplicacion_simbolos
        DATA_vec[2] = elimina

        count_pos_layer_puntero += 1
        DATA_vec[5] = count_pos_layer_puntero
        DATA_vec[6] = count_pos_layer_puntero
        #print('>>>>>>>>count_pos_layer_puntero: ',self.count_pos_layer_puntero)
        if count_pos_layer_puntero == long_capa:
            #print(DATA_vec[5])
            DATA_vec[6] = count_pos_layer_puntero
            DATA_vec[4] = 1
            DATA_vec[5] = 0
                
        else:
            DATA_vec[4] = 0
    if long_capa == 2:
  
        
        elimina = DATA_vec[0];elimina[count_pos_layer_puntero]
        #print(elimina)
        #print(DATA_vec)
        elimina1_1 = elimina[0]
        elimina1_2 = elimina[1]
        elimina2_1 = [elimina1_1[0]+1,elimina1_1[1]]
        elimina2_2 = [elimina1_2[0]+1,elimina1_2[1]]
            
        ob_1_1 = a[elimina1_1[0],elimina1_1[1]]
        ob_1_2 = a[elimina1_2[0],elimina1_2[1]]
        ob_2_1 = a[elimina2_1[0],elimina2_1[1]]
        ob_2_2 = a[elimina2_2[0],elimina2_2[1]]

            
        if ob_1_1 != 0 and ob_2_2 !=0:
            multiplicacion_tempo1 = operacion(ob_1_1,ob_2_2)
            #print('mult:',multiplicacion_tempo1,'      simbol:',DATA_vec[3],)
        else:  
            multiplicacion_tempo1 = 0
        if ob_1_2 != 0 and ob_2_1 != 0:
            multiplicacion_tempo2 = operacion(ob_1_2,ob_2_1)
            #print('mult:',multiplicacion_tempo2,'      simbol:',DATA_vec[3],)
        else:
            multiplicacion_tempo2 = 0            
        
        
        if old_obj != 0 and multiplicacion_tempo1 != 0:
            operacion2(old_obj,multiplicacion_tempo1)
                
                
        if old_obj != 0 and multiplicacion_tempo2 != 0:
            operacion2(-1*old_obj,multiplicacion_tempo2)

            
            
        DATA_vec[4] = 1
        #DATA_vec[6] = self.count_pos_layer_puntero
            
        #print(dic2)
        count_pos_layer_puntero += 1
        DATA_vec[5] = count_pos_layer_puntero
        DATA_vec[6] = 2
        if count_pos_layer_puntero == long_capa:
            #print(DATA_vec[5])
            #DATA_vec[6] = count_pos_layer_puntero
            DATA_vec[4] = 1
            DATA_vec[5] = 0
        #    #print('dic2',dic2)

    return DATA_vec

def send_dta2(DATA_vec,old_obj,estatus_mult,mult_signo_old,a):
    #print('-------------------ok')  
    
    long_capa = len(DATA_vec[0])
    count_pos_layer_puntero = DATA_vec[5]
    if long_capa >= 3:
        elimina = DATA_vec[0];
        #-------------------------------------------     
        elimina = elimina[count_pos_layer_puntero]
        simbolo_de_capa = a[elimina[0],elimina[1]]
        #print('simbolo de capa: ',simbolo_de_capa)
        #print('old obj: ',old_obj)
        if simbolo_de_capa != 0 and old_obj != 0: 
            #print('here!!')
            
            
            signo = 1
            for puntero in DATA_vec[0]:
                if puntero[1] == elimina[1]:
                    DATA_vec[3] = copy.deepcopy(signo)
                    DATA_vec[3] *= estatus_mult
                if signo == -1:
                    signo = 1
                else:
                    signo = -1
            
            
            
            
            
            multiplicacion_simbolos = operacion(old_obj*DATA_vec[3],simbolo_de_capa)
            #print('here!!',DATA_vec[0],'elimina',elimina,'_mult_sym: ',multiplicacion_simbolos,'       ',DATA_vec[3],'estatus_mult:',estatus_mult,',    old:',old_obj,'     , new',simbolo_de_capa)
        else:
        #simbolo_de_capa == 0:
            multiplicacion_simbolos = 0         
        DATA_vec[1] = multiplicacion_simbolos
        DATA_vec[2] = elimina
        count_pos_layer_puntero += 1
        DATA_vec[5] = count_pos_layer_puntero
        DATA_vec[6] = count_pos_layer_puntero
        if count_pos_layer_puntero == long_capa:
            DATA_vec[6] = count_pos_layer_puntero
            DATA_vec[4] = 1
            DATA_vec[5] = 0         
        else:
            DATA_vec[4] = 0
    if long_capa == 2:
        elimina = DATA_vec[0];elimina[count_pos_layer_puntero]
        elimina1_1 = elimina[0]
        elimina1_2 = elimina[1]
        elimina2_1 = [elimina1_1[0]+1,elimina1_1[1]]
        elimina2_2 = [elimina1_2[0]+1,elimina1_2[1]]
            
        ob_1_1 = a[elimina1_1[0],elimina1_1[1]]
        ob_1_2 = a[elimina1_2[0],elimina1_2[1]]
        ob_2_1 = a[elimina2_1[0],elimina2_1[1]]
        ob_2_2 = a[elimina2_2[0],elimina2_2[1]]
         
        if ob_1_1 != 0 and ob_2_2 !=0:
            multiplicacion_tempo1 = operacion(ob_1_1,ob_2_2)
            #print('>>final1: ',multiplicacion_tempo1)
        else:  
            multiplicacion_tempo1 = 0
        if ob_1_2 != 0 and ob_2_1 != 0:
            multiplicacion_tempo2 = operacion(ob_1_2*-1,ob_2_1)
            #print('>>final2:',multiplicacion_tempo2)
        else:
            multiplicacion_tempo2 = 0            
         

        if old_obj != 0 and multiplicacion_tempo1 != 0:
            operacion2(old_obj,multiplicacion_tempo1)
            #print('>>final1: ',multiplicacion_tempo1)
        if old_obj != 0 and multiplicacion_tempo2 != 0:
            operacion2(old_obj,multiplicacion_tempo2)
            #print('>>final2:',multiplicacion_tempo2)
        DATA_vec[4] = 1

        count_pos_layer_puntero += 1
        DATA_vec[5] = count_pos_layer_puntero
        DATA_vec[6] = 2
        if count_pos_layer_puntero == long_capa:
            DATA_vec[4] = 1
            DATA_vec[5] = 0
    return DATA_vec  
 
    
def recursivo(y,DATA,a):
    C_t = 0; flag = 0
    while(True):

        inicio = y-2
        for y_puntero in range(y-2,0,-1): 
            if DATA[y_puntero,6] == DATA[y_puntero,7]:
                if y_puntero-1 != 0:
                    inicio = y_puntero-1
            else:
                break
                
        ####################################
        #for y_tempo in range(len(a)):      #
        DATA[inicio+1:y-1,3:4] = 1            #
        ####################################
        #print('inicio:',inicio,'inicio-1:',inicio-1,'DATA:',DATA[inicio:y-1,0:5])
#        if DATA[inicio-1,7] != 0:
#            print('padre:   ',inicio)
        for y_puntero in range(inicio,y-1,1):

            herencia = DATA[y_puntero-1,0]
            elimina = DATA[y_puntero-1,2]
            DATA[y_puntero,0],DATA[y_puntero,7],DATA[y_puntero,2] = make_layer_1(herencia,elimina) 
            DATA[y_puntero] = send_dta2(DATA[y_puntero],DATA[y_puntero-1,1],DATA[0,3],DATA[y_puntero-1,8],a)
            #####################tempo###############################
            #print('>>                        ',DATA[y_puntero,1])
            
            ####################################################
            if DATA[1,9] == 1 and y_puntero == y-2:
                DATA[2,9] = 1
                for busqueda in range(y-1,0,-1):
                    if DATA[busqueda,6] == DATA[busqueda,7]:
                        DATA[2,9] = 1
                    else:
                        DATA[2,9] = 0
                        break

            if DATA[1,6] == DATA[1,7]:
                DATA[1,9] = 1   
            else: 
                DATA[1,9] = 0
            ########################tempo########################
            #print('>>                        ',DATA[y_puntero,1],'padre:',DATA[y_puntero-1,1])
            if DATA[y_puntero,1] == 0:
                #print('>> dentro del if                       ',DATA[y_puntero,1])
                for busqueda in range(y-1,0,-1):
                    if DATA[busqueda,6] == DATA[busqueda,7]:
                        DATA[2,9] = 1
                    else:
                        DATA[2,9] = 0
                        break
                break
            ################################################
        if DATA[2,9] == 1:
            break
        #if C_t >= 10000000:#20160:
        #    break
        C_t += 1
  
#% layer trajectory... here! ****************************************************************************************************************************

#@profile    
def make_trajectory(a,trama):
    #print('***************TRAMA:*******************')
    #print(trama)
    global dic1, dic2
    #trayectoria = np.zeros((np.shape(a)[0],1),dtype=object)
    DATA = np.zeros((np.shape(a)[0],12),dtype=object)
    DATA[0] = trama
    y = np.shape(a)[0]
    #print(a)   
    for y_puntero in range(1,y-1,1):      
        herencia = DATA[y_puntero-1,0]
        elimina = DATA[y_puntero-1,2]
        DATA[y_puntero,0],DATA[y_puntero,7],DATA[y_puntero,2] = make_layer_1(herencia,elimina)
        DATA[y_puntero] = send_dta(DATA[y_puntero],DATA[y_puntero-1,1],DATA[0,3],DATA[y_puntero-1,8],a)#self.DATA[y_puntero-1,3],0)
        #print(DATA[:,4:11])
        #print('----------------**')
    p_rec ='-------------------------------------Recursivo-------------------------------------'
    #print(p_rec)
    
    
    
    if DATA[0,1] != 0:
        #print('estamos en diferente de cero: ')
#        for y_tempo in range(len(a)):
#            DATA[y_tempo,3] = 1
#        for y_tempo in range(len(a)):
#            print(DATA[y_tempo,3])
        recursivo(y,DATA,a)
#    else:
#        print('estamos en cero: ')
#        for y in range(len(a)):
#            print(DATA[y,3])
    #print(dic2)
def bloque1(a):
    M = copy.deepcopy(a)
    out = 0
    for y in range(len(a)):
        if M[y,y] == 0:
            ACU1 = []
            for elem in range(len(a)):
                if a[y,elem] != 0 and elem != y:
                    ACU1.append(elem)
        
            if len(ACU1) > 0:
                num = choice(ACU1)
                #print('num',num)
                U1 = copy.deepcopy(M[:,y:y+1])
                U2 = copy.deepcopy(M[:,num:num+1])
                #print('U1',U2)
                M[:,y:y+1] = U2
                M[:,num:num+1] = U1*-1
            
            
    for y in range(len(a)):
        #print(M[y,y])
        if M[y,y] == 0:
            ACU2 = []
            for elem in range(len(a)):
                if M[elem,y] != 0 and elem != y:
                    ACU2.append(elem)
            #print(ACU2)   
            if len(ACU2) > 0:
                num2 = choice(ACU2)
                H1 = copy.deepcopy(M[y])
                H2 = copy.deepcopy(M[num2])
                M[y] = H2
                M[num2] = H1*-1
    for y in range(len(a)):
        #print(M[y,y])
        if M[y,y] != 0:
            out = 1
        else:
            out = 0
            
            break
    return(M,out)


def ordena_diagonal(A): 
    A2 = copy.deepcopy(A)
    c = 0
    limit = np.shape(A)[0]
    while (c<=15*limit):
        A2,out = bloque1(A2)
        if out == 1:
            break
        c += 1
    return(A2)
#% formula los determinantes **************************************************************************************************************************
#@profile
def formula_dets(M,z):
    n = np.shape(M)[0]
    Dets =[0]
    A = copy.deepcopy(M)
    for y in range(n):
        tempo = copy.deepcopy(A)
        tempo[:,y:y+1] = copy.deepcopy(z)
        tempo2 = ordena_diagonal(copy.deepcopy(tempo))
        Dets.append(copy.deepcopy(tempo2))
    Dets = np.array((Dets),dtype=object)
    return(Dets)


#for determinante in Dets:
#    print(determinante)
#    print('\n\n\n')


def make_process(q,Dets,res,A,Z,pn):
    ###########################################################################
    ###########################################################################
#    inicio = time()
#    print('>>>>>>         inicio')
#    x = 0
#    for m in range(np.shape(A)[0]+1):
#        sig_init = 1
#        Mtemp = Dets[m];vector = make_vector_pos(len(Mtemp[0]))
#        for k in range(np.shape(A)[0]):
#            make_process2(k,m,Mtemp,vector,Dets,sig_init)
#            if sig_init == 1:
#                sig_init = -1
#            else:
#                sig_init = 1
#        nombres = list(dic2)
#        for fragmento in nombres:
#            res[x] += dic2.get(fragmento)
#        dic2 = {}
#        x += 1
#    incognitas = crammer(res)
#    show_d = pd.DataFrame(Dets[0])
#    show_d.columns = ['']*show_d.shape[1]
#    print(show_d.to_string(index=False))
#    print('serie: ',time()-inicio)
    ###########################################################################
    ###########################################################################
    global dic1,dic2
    #x = 0
    #for m in range(np.shape(A)[0]+1):
    sig_init = 1
    Mtemp = Dets[pn];vector = make_vector_pos(len(Mtemp[0]))
    for k in range(np.shape(A)[0]):
        make_process2(k,pn,Mtemp,vector,Dets,sig_init)
        if sig_init == 1:
            sig_init = -1
        else:
            sig_init = 1
#        
#    incognitas = crammer(res)
    dic2 = list(dic2.values())
    dic2 = sum(list(dic2))
    q.put(dic2)
    dic2 = {}
def make_process2(k,m,Mtemp,vector,Dets,signo):
    global dic1,dic2
    #k = 0
    #m = 0
    #Mtemp = Dets[m];vectores = Mtemp[0]
    #print('******iniciando*****')
    trama_dato = [vector,Mtemp[0,k],[0,k],signo,0,0,0,0,1,0,0,0]
    
    #print(trama_dato)
    #print('>>la matriz a calcular es:')
    #print(Dets[m])
    make_trajectory(Dets[m],trama_dato)
    
    #dic1,dic2 = traj.up_move()
    out=[dic1,dic2]
    
    
def foo(q,a,b,):
    #q.put('hello')
    #print('hello')
    c = b*a
    out = [c,'hello']
    q.put(out)
    #nq.put(a)
    
def make_vector_pos(long):
    out = []
    for x in range(long):
        tempo = [0,x]
        out.append(tempo)
    return out
def guada_dic(dic,nombre):
    f = open(nombre,'w')
    f.close()
    f = open(nombre,'a')
    for dato in dic:
        f.write('\n'+' '+str(dato))
    f.close()
    
def crammer(tupla):
    x1 = tupla[0]
    out = []
    #print('tupla,  numero de elementos: ',len(tupla))
    #for ren in tupla:
        #print(ren)
    #print('------------------------------------------------------------------')
    for op in range(1,len(tupla),1):
        tf = []
        tf.append(tupla[op]/x1)
        out.append(tf)
        
    #for ren in out:
    #    print('')
    #    print(ren)
    np.array(out,dtype=object)
    return(out)

#% Determinante de A ***********************************************************************************************************************************
#@profile
def main(modo,A,Z,x_p,n_procesos):
    #modo = 1
    #print(A)
    #print(Z)
    global dic1,dic2
    Dets = formula_dets(A,Z)
    
    n = copy.deepcopy(x_p); qa = []
    tupla = tuple(mp.Queue() for _ in range(1,n+1))
    for i, q in enumerate(tupla, start=1):
        qa.append(q)

    diag_0 = ordena_diagonal(A)
    Dets[0] = diag_0
    #print(qa)
    
    res = np.zeros((len(Z)+1),dtype=object)
    #print('res')
    #print(res)
    
    if modo == 1:
        inicio = time()
        #print('>>>>>>         inicio')
        x = 0 
#        n = copy.deepcopy(x_p); qa = []
#        tupla = tuple(mp.Queue() for _ in range(1,n+1))
#        for i, q in enumerate(tupla, start=1):
#            qa.append(q)
        for m in range(np.shape(A)[0]+1):
            sig_init = 1
            Mtemp = Dets[m];vector = make_vector_pos(len(Mtemp[0]))
            for k in range(np.shape(A)[0]):
                make_process2(k,m,Mtemp,vector,Dets,sig_init)
                if sig_init == 1:
                    sig_init = -1
                else:
                    sig_init = 1
            nombres = list(dic2)
            for fragmento in nombres:
                res[x] += dic2.get(fragmento)
            dic2 = {}
            x += 1

        incognitas = crammer(res)
        show_d = pd.DataFrame(Dets[0])
        show_d.columns = ['']*show_d.shape[1]

        #print(show_d.to_string(index=False))
        print('tiempo de calculo en serie por DDD: ',time()-inicio)

    if modo == 2:
        inicio_tiempo = time()
        #caso 0
        if x_p == n_procesos:
            print('CASO 0')
            
#            n = copy.deepcopy(x_p); qa = []
#            tupla = tuple(mp.Queue() for _ in range(1,n+1))
#            for i, q in enumerate(tupla, start=1):
#                qa.append(q)
            
            procesos = []; resultados = []
            for pn in range(n_procesos):
                proceso = mp.Process(target = make_process, args=(qa[pn],Dets,res,A,Z,pn))
                procesos.append(proceso)
            #print(procesos)
            for n_start in procesos:
                n_start.start()    
            for y_tempo in range(len(procesos)):
                #print('obteniendo datos de r:',y_tempo)
                tempo = qa[y_tempo].get()
                #tempo = qa[0].get()
                #print(tempo)
                resultados.append(tempo)
            for n_start in procesos:
                n_start.join()
            incognitas = crammer(resultados)
        #caso 1
        if x_p < n_procesos:
            #print('CASO 1')
            
#            n = copy.deepcopy(x_p); qa = []
#            tupla = tuple(mp.Queue() for _ in range(1,n+1))
#            for i, q in enumerate(tupla, start=1):
#                qa.append(q)
            
            procesos = []; resultados = []
            for pn in range(x_p):
                proceso = mp.Process(target = make_process, args=(qa[pn],Dets,res,A,Z,pn))
                procesos.append(proceso)
            for n_start in procesos:
                n_start.start()    
            for y_tempo in range(len(procesos)):
                #print('obteniendo datos de r:',y_tempo)
                tempo = qa[y_tempo].get()
                #print(tempo)
                resultados.append(tempo)
            for n_start in procesos:
                n_start.join()
            incognitas = crammer(resultados)
        #caso 2
        if x_p > n_procesos:
            #print('CASO 2')
            C = 0
#            n = copy.deepcopy(x_p); qa = []
#            tupla = tuple(mp.Queue() for _ in range(1,n+1))
#            for i, q in enumerate(tupla, start=1):
#                qa.append(q)
            
            total_p = copy.deepcopy(n_procesos)
            remanente = copy.deepcopy(x_p)
            inicio = 0;fin = 0
            procesos = []; resultados = []
            #print('remanente',remanente)
            
            for pn in range(x_p):
                #print('valor de pn:   ',pn)
                proceso = mp.Process(target = make_process, args=(qa[pn],Dets,res,A,Z,pn))
                procesos.append(proceso)
            
            while(True):
                #procesos = []
                
                #print('aqui')
                #>> remanente-total_p > total_p
                if remanente-total_p >= 0:
                    #print('aqui en t_p mayor zero')
                    for i in range(inicio,inicio+total_p):
                        n_start = procesos[i]
                        n_start.start()    
                    for y_tempo in range(inicio,inicio+total_p):
                        #print('obteniendo datos de r:',y_tempo)
                        tempo = qa[y_tempo].get()
                        #print(tempo)
                        resultados.append(tempo)
                    for i in range(inicio,inicio+total_p):
                        n_start = procesos[i]
                        n_start.join()
                    for i in range(inicio,inicio+total_p):
                        task = procesos[i]
                        task.terminate()
                        #task.close()
                        #task.kill()
                        
                    #print('procesos: ',procesos)
                    inicio = inicio + total_p
                    remanente = remanente - total_p
                    #print('remanente',remanente)
                    #fin = inicio+total_p
                   
                #>> remanente-total_p == total_p
           
                #>> remanente-total_p < total_p 
                if remanente-total_p < 0:
                    #print('aqui en t_p menor zero, inicio',inicio, remanente-total_p)
                    #print('remanente-total_p : ',remanente-total_p)
                    if (remanente <= total_p):
                        for i in range(inicio,inicio+abs(remanente)):#-total_p)):
                            n_start = procesos[i]
                            n_start.start()
                        for y_tempo in range(inicio,inicio+abs(remanente)):
                            #print('obteniendo datos de r:',y_tempo)
                            tempo = qa[y_tempo].get()
                            #print(tempo)
                            resultados.append(tempo)
                        for i in range(inicio,inicio+abs(remanente)):
                            n_start = procesos[i]
                            n_start.join()
                        for i in range(inicio,inicio+abs(remanente)):
                            task = procesos[i]
                            task.terminate()
                        remanente = 0
                    else:
                        for i in range(inicio,inicio+abs(remanente-total_p)):
                            n_start = procesos[i]
                            n_start.start()
                        for y_tempo in range(inicio,inicio+abs(remanente-total_p)):
                            #print('obteniendo datos de r:',y_tempo)
                            tempo = qa[y_tempo].get()
                            #print(tempo)
                            resultados.append(tempo)
                        for i in range(inicio,inicio+abs(remanente-total_p)):
                            n_start = procesos[i]
                            n_start.join()
                        for i in range(inicio,inicio+abs(remanente-total_p)):
                            task = procesos[i]
                            task.terminate()
                        #inicio = inicio + abs(remanente-total_p)
                        remanente = remanente - abs(remanente-total_p)
                        #fin = inicio+abs(remanente-total_p)
                    
                #print('remanente:  ',remanente)
                #print('total_p:  ',total_p)
                #print('inicio:  ',inicio)
                #print('fin:  ',fin)
                C += 1
                if remanente == 0:
                    break
                if C >= 10:
                    break
            incognitas = crammer(resultados)
            
        print('tiempo de calculo en paralelo por DDD: ',time()-inicio_tiempo)
        #print('inicio: ',inicio)
    if modo == 3:
        tiempo = time()
        sig_init = 1; m = 0
        Mtemp = Dets[m];vector = make_vector_pos(len(Mtemp[0]))

        #Dets[0] = copy.deepcopy(A)

        show_d = pd.DataFrame(Dets[m])
        show_d.columns = ['']*show_d.shape[1]
        #print(show_d.to_string(index=False))

        for k in range(np.shape(A)[0]):
            make_process2(k,m,Mtemp,vector,Dets,sig_init)
            if sig_init == 1:
                sig_init = -1
            else:
                sig_init = 1
        print('CPU tiempo: ',time()-tiempo,' s')
        
    #print('fin algoritmo')
#    for y in dic2:
#        print(y)
#    print('-------')
    #print(len(dic2))
 
    gc.collect()
    gc.collect(generation=2)
    gc.collect(generation=1)
   
    return incognitas
    ####################################################################################################

####################################################################################################    
def principal(A,x,z):


     ##########################################################################################################
    ##########################################################################################################
    #                                                                                                        #
    #     poner cualquier matriz Mnxx correspondiente con cualquiel vector Znxx                              #
    #     nota: asegurarse que los tamaños coinciadan ejemplo Mn4s2 ----> Zn4s                               #
    #                                                                                                        #
    #     a continuacion se dejan algunas sistemas precargados:                                              #
    #                                                                                                        #
    #     para Mnxx puedes usar: Mn4n Mn5n Mn8s Mn15s Mn4s Mn4s2 Mn10n Mn9n Mn8n Mn7n Mn6n Mn5n Mn7e         #
    #     para Znxx puedes usar: Zn4s Zn5s Zn8n Zn15n Zn4s Zn11n Zn10n Zn9n Zn8n Zn7n Zn6n Zn5n Zn7e         #
    #                                                                                                        #
    #     o tambien puedes definir un sistema simbolico que quieras resolver                                 #
    #                                                                                                        #
    ##########################################################################################################
    ##########################################################################################################
    #DATA_symbols = dta_sym(','.join(DATA_vars))
    #DATA_sympy = sympy.symbols(','.join(DATA_vars))

    #dic_0 = {}; dic_sympy = {}
    #for step in DATA_symbols:
    #     dic_0[str(step)] = step

   

    #print('**********************')
    #print(dic_0)
    #print('**********************')
    #print(DATA_symbols)
    #print(mna)

    #>> generando simbolo A n*n
    #print(mna)
    #print('type: ',type(mna[0,0]))
    #A = copy.deepcopy(mna)
    #z = copy.deepcopy(Z)
    #A = np.array(A,dtype=object)
    #z = np.array(z,dtype=object)
    #print(DATA_symbols)

    #*******************************************************************
    #*******************************************************************

    #print(type(A[0,0]))
    #print(type(DATA_symbols))
    #print(type(DATA_symbols[0]))

    #A = mna_to_symbolic2(A,dic_0)
    #z = mna_to_symbolic2(z,dic_0)
    #print('>>>>>>>>>>>>dd>>>>>>>>>>>>A2')
   


    modo = 0; procesos = 4; tamano_matriz = 60
    




    x_p = np.shape(A)[0]+1
    if x_p < tamano_matriz:
        modo = 1
    if x_p >= tamano_matriz:
        modo = 2
    #print('modo:',modo,'x_p:',x_p)
    main(modo,A,z,x_p,procesos)
    
    #print('fin')

#mna = [['R1', 0, 0, '-R1', 0, '-1', 0],
#        [0, 'C1', 0, 0, 0, '1', '1'],
#        [0, 0, 'R2', 0, 0, 0, '-1'],
#        ['-R1', 0, 0, 'R1', 1, 0, 0],
#        [0, 0, 0, 1, 0, 0, 0],
#        ['-1', '1', 0, 0, 0, 'L1S', 'SM'],
#        [0, '1', '-1', 0, 0, 'SM', 'L2S']]
#Z = [[0],
#    [0],
#    [0],
#    [0],
#    ['V1'],
#    [0],
#    [0]]
#DATA_vars = ['S', '-1', '1', 'V1', 'R1', 'C1', 'R2', 'K1', 'L1S', 'L2S', 'SM']
#principal(mna,Z,DATA_vars)

def DDDs(A,x,z):
    modo = 0; procesos = 4; tamano_matriz = 60
    x_p = np.shape(A)[0]+1
    if x_p < tamano_matriz:
        modo = 1
    if x_p >= tamano_matriz:
        modo = 2
    X = main(modo,A,z,x_p,procesos)

    return X



