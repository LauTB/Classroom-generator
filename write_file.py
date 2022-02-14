import openpyxl 
from dataclasses import dataclass
from read_file import *
import os
import errno

def stud_to_tuple(stud):
    a = [
        stud.ci,
        stud.nombre,
        stud.apellidos,
        stud.pais,
        stud.provincia,
        stud.municipio,
        stud.situcion_academica,
        stud.estado,
        stud.direccion,
        stud.fecha_de_nacimiento,
        "", #stud.grupo,
        stud.carrera,
        stud.facultad,
        stud.tipo_de_curso,
        stud.correo,
        stud.fuente_de_ingreso,
        stud.origen_academico,
        stud.regimen_de_estudio,
        stud.natural_de,
        stud.telefono,
        stud.fecha_de_ingreso_a_la_es,
        stud.estado_civil,
        stud.organizacion_politica,
        stud.fecha_de_ingreso_al_ces,
        stud.fecha_de_matricula,
        stud.sexo,
        stud.color_de_piel,
        stud.tipo_de_estudiante,
        stud.anno_de_estudio,
        stud.centro_de_trabajo,
        stud.nombre_padre,
        stud.na_padre,
        stud.nombre_madre,
        stud.na_madre,
        stud.tipo_servicio_militar,
        stud.edad
    ]
    return tuple(a)

def define_data_base(list_):
    database = []
    for item in list_:
        database.append(stud_to_tuple(item))
    return database

def create_sheet(database, headers, id):
    wb = openpyxl.Workbook()
    hoja = wb.active
    
    hoja.append(tuple(headers))
    for producto in database:
        hoja.append(producto)

    try:
        os.mkdir('Grupos')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    wb.save(f'Grupos/Grupo-C11{id + 1}.xlsx')