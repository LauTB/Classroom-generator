from webbrowser import get
from read_file import *
from data_selector import *

lambda_list = [ci, nombre, apellidos, pais, provincia, municipio, situacion_academica, estado, direccion, fecha_de_nacimiento, grupo, carrera, facultad, tipo_de_curso, correo, fuente_de_ingreso, origen_academico, regimen_de_estudio, natural_de, telefono, fecha_de_ingreso_a_la_es, estado_civil, organizacion_politica, fecha_de_ingreso_al_ces, fecha_de_matricula, sexo, color_de_piel, tipo_de_estudiante, anno_de_estudio, centro_de_trabajo, nombre_padre, na_padre, nombre_madre, na_madre, tipo_servicio_militar, edad]

def sort_and_divide(list):
    temp_list = [i for i in list]
    temp_list.sort()
    list_of_lists = []

    # category name from the first elem in the list
    elem = temp_list[0][0]
    # temp list for the future list of lists
    temp = [temp_list[0]]

    for item in temp_list[1:]:
        if item[0] == elem:
            temp.append(item)
        else:
            list_of_lists.append([i for i in temp])
            temp = [item]
            elem = item[0]
    else:
        list_of_lists.append([i for i in temp])
    return list_of_lists

# return an unique list from a list of lists
# list of lists to list
def lol_to_list(list):
    result = []
    for item in list:
        result.extend(item)
    return result     


def generate_list_by_cat(dict, id, cat):
    result = []
    for id_ in id:
        temp_stud = dict[id_]
        result.append((cat(temp_stud), id_))
    return result

def get_id_list(list_):
    return [i for (_, i) in list_]

def order_by_cat(dict, id_list, cat_list, i):
    if not cat_list:
        return id_list
    cat_list_ = generate_list_by_cat(dict, id_list, cat_list[0])
    temp_list = sort_and_divide(cat_list_)
    result = []
    for item in temp_list:
        result = _concat_list_(result, order_by_cat(dict, get_id_list(item), cat_list[1:], i+1))
    return result
    

def receive_data(data, categories):
    dic = {}
    for i, item in enumerate(data):
        dic[i] = item
    
    id_list = [i for i in range(len(dic))]

    result = order_by_cat(dic, id_list, categories, 0)

    return [dic[item] for item in result]

def _concat_list_(list1, list2):
        result = [i for i in list1]
        for i in list2:
            if i not in result:
                result.append(i)
        return result

def generate_groups(n, list, s1):
    list_ = [[] for _ in range(n)]
    if s1 == n:
        for i, item in enumerate(list):
            list_[i % n].append(item)
    else: 
        amount = int(len(list) / n)
        count = len(list) - (s1*amount)
        for i in range(s1*amount):
            list_[i % s1].append(list[i])
        for i in range(count):
            list_[s1 + (i % (n - s1))].append(list[count + i])
    return list_