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
    if list_of_lists:
        return (True, list_of_lists) 
    else: return (False, temp_list)

# return an unique list from a list of lists
# list of lists to list
def lol_to_list(list):
    result = []
    for item in list:
        result.extend(item)
    return result     


def generate_list_by_cat(dict, id, cat):
    result = []
    for item in id:
        temp_stud = dict[item]
        result.append((cat(temp_stud), item))
    return result

def get_id_list(list_):
    return [i for (_, i) in list_]

def order_by_cat(dict, id_list, cat_list):
    if not cat_list: 
        return id_list
    
    cat_list_ = generate_list_by_cat(dict, id_list, cat_list[0])
    is_lol, temp_list = sort_and_divide(cat_list_)
    if is_lol:
        result = []
        for item in temp_list:
            result.extend(order_by_cat(dict, get_id_list(item), cat_list[1:]))
        return result
    return get_id_list(temp_list)


def receive_data(data, categories):
    dic = {}
    for i, item in enumerate(data):
        dic[i] = item
    
    id_list = [i for i in range(len(dic))]

    result = order_by_cat(dic, id_list, categories)

    return [dic[item] for item in result]

def generate_groups(n, list):
    list_ = [[] for _ in range(n)]

    for i, item in enumerate(list):
        list_[i % n].append(item)

    return list_