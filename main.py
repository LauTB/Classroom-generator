from groups_generator import *
from read_file import *
from data_selector import *


def get_data_from_excel(path):
    sh = get_sheet(path)
    data = get_data(sh)
    return data


def create_groups(data, groups_count, categories):
    result = receive_data(data, categories)
    groups = generate_groups(groups_count, result)
    return groups

def main(path, n, categories):
    data = get_data_from_excel(path)
    groups = create_groups(data, n, categories)
    return groups


if __name__ == '__main__':
    """
    example 1
    """
    g = main('./data/data.xlsx', 4, [sexo, tipo_de_estudiante])
    for i, list in enumerate(g):
        print(f"grupo: {i+1}")
        for item in list:
            print(item)
        print()
        
    
