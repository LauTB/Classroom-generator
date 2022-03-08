import random as rand
from data_selector import *

class GeneticAlgorithm:
    def __init__(self, students, population_length, categories, ss1_count, ss2_count, ss1_cat_count, gb_cat_count):
        self.students = students
        self.total = len(students)
        self.group_count_by_session = ss1_count, ss2_count
        self.amount_of_groups = ss1_count + ss2_count 

        #categorias
        self.ss1_cat_count = ss1_cat_count
        self.gb_cat_count = gb_cat_count
        
        # toma la parte entera por debajo de la cant de estudiantes por aula
        self.groups_len = int(self.total / (ss1_count + ss2_count))

        # [[primera sesion], [global]]
        self.categories = self.filter_categories(categories)
        self.population = self.generate_population(population_length)
        self.categorizer_dict = {}
        self.create_categorizer_dict()


    def filter_categories(self, categories):
        return [
            [i for i in categories[0] if i not in categories[1]],
            categories[1]
        ]


    def generate_population(self, amount):
        population = []
        for _ in range(amount):
            population.append(rand.sample(range(self.total)), self.total)
        return population

    def create_categorizer_dict(self):
        fst_ss = self.categories[0]
        gb_ss = self.categories[1]
        for (name, cat) in (fst_ss + gb_ss):
            current_cat = []
            for st in self.students:
                current_cat.append(cat(st))
            current_cat.sort()
            self.categorizer_dict[name] = current_cat[0]
      

    def order_population(self):
        new_population = []
        temp_population = []
        for cromo in self.population:
            pass

    
    def categorize(self, cromosome):
        pass


    def _get_value_from_cromosome_with_cat_(self, cromosome, current_cat):
        value = []
        for id_ in cromosome:
            try:
                self.create_categorizer_dic[current_cat(self.students[id_])]
                value.append(1)
            except: value.append(-1)
        return value

    def get_value_from_cromosome(self, cromosome):
        fst_ss = self.categories[0]
        gb_ss = self.categories[1]
        cromo_value = [[] for _ in range(len(cromosome))]
        for (_, cat) in (fst_ss + gb_ss):
            value = self._get_value_from_cromosome_with_cat_(cromosome, cat) 
            for pos, val in enumerate(value):
                cromo_value[pos].append(val)
        return cromo_value

    def first_session_value(self, cromosome_values):
        stud_amount = self.groups_by_session[0] * self.groups_len
        fs_cromo_value = []
        for i in range(stud_amount):
            fs_cromo_value.append([cromosome_values[i] for _ in range(self.ss1_cat_count)])

    def get_more_unbalance_group_pair(self, cromo, cat_id):
        temp_cromo = [c[cat_id] for c in cromo]
        temp_sum = [0 for _ in range(self.amount_of_groups)]
        for pos, item in enumerate(temp_cromo):
            temp_sum[self._get_group_(pos)[0]] += item

        # retorna los grupos con mayor y menor balance
        return temp_sum.index(min(temp_sum)), temp_sum.index(max(temp_sum))

    # grupo, pos inicial, pos final
    def _get_group_(self, pos):
        group = int(pos / self.amount_of_groups)
        init = group * self.group_length
        end = ((group + 1) * self.group_length) - 1
        return group, init, end


    def get_best_cromosome(self, cromo_1, cromo_2):
        cromo1, cromo1_pos = cromo_1
        cromo2, cromo2_pos = cromo_2
        values1 = self.get_value_from_cromosome(cromo1)
        values2 = self.get_value_from_cromosome(cromo2)

        # grupos_inits = [self.group_len * pos for pos in len(self.amount_of_groups)]

        values_by_groups1 = [[0 for _ in range(self.amount_of_groups)] for _ in range(values1[0])]
        values_by_groups2 = [[0 for _ in range(self.amount_of_groups)] for _ in range(values1[0])]
        
        for std_pos, val in enumerate(values1):
            for pos, v in enumerate(val):
                values_by_groups1[pos][self._get_group_(std_pos)] += v
        
        for std_pos, val in enumerate(values2):
            for pos, v in enumerate(val):
                values_by_groups2[pos][self._get_group_(std_pos)] += v
        
        comparison_values = 0, 0
        
        for cat_pos, values in enumerate(values_by_groups1):
            min1 = min(values)
            max1 = max(values)
            min2 = min(values_by_groups2[cat_pos])
            max2 = max(values_by_groups2[cat_pos])
            
            if max1 - min1 < max2 - min2:
                comparison_values[1] += 1
            else: comparison_values[0] += 1
        
        return (cromo1, cromo1_pos) if comparison_values[0] < comparison_values[1] else (cromo2, cromo2_pos)

            
    # parent(1/2) ([ids], [[valores de categorias],...,[]])
    def generate_new_best_cromosome(self, parent_1, parent_2):
        parent1, parent1_pos = parent_1[1]
        parent2, parent2_pos = parent_2[1]
        _, cat = rand.choice(self.categories[0] + self.categories[1])
        min1, max1 = self.get_more_unbalance_group_pair(parent1, cat)
        min2, max2 = self.get_more_unbalance_group_pair(parent2, cat)
        
        # creando el primer hijo del parent1 
        pos1 = rand.choice(range(self._get_group_(min1)[1], self._get_group_(min1)[2]))
        pos2 = rand.choice(range(self._get_group_(max1)[1], self._get_group_(max1)[2]))
        temp_id1 = parent1[pos1]
        temp_id2 = parent1[pos2]

        temp_id1_pos = parent1_pos[pos1]
        temp_id2_pos = parent1_pos[pos2]

        child1 = [i for i in parent1]
        child1[pos1] = temp_id2
        child1[pos2] = temp_id1
        
        child1_pos = [i for i in parent1_pos]
        child1_pos[pos1] = temp_id2_pos
        child1_pos[pos2] = temp_id1_pos

        # creando el 2do hijo del parent2
        pos1 = rand.choice(range(self._get_group_(min2)[1], self._get_group_(min2)[2]))
        pos2 = rand.choice(range(self._get_group_(max2)[1], self._get_group_(max2)[2]))

        temp_id1 = parent1[pos1]
        temp_id2 = parent1[pos2]
        temp_id1_pos = parent1_pos[pos1]
        temp_id2_pos = parent1_pos[pos2]

        child2 = [i for i in parent2]
        child2[pos1] = temp_id2
        child2[pos2] = temp_id1

        child2_pos = [i for i in parent2_pos]
        child2_pos[pos1] = temp_id2_pos
        child2_pos[pos2] = temp_id1_pos


        # seleccionando el mejor cromosoma de los 4
        temp_best_cromo = self.get_best_cromosome((parent1, parent1_pos), (parent2, parent2_pos))
        temp_best_cromo = self.get_best_cromosome(temp_best_cromo, (child1, child1_pos))
        temp_best_cromo = self.get_best_cromosome(temp_best_cromo, (child2, child2_pos))

        return temp_best_cromo

    def get_final_cromosome(self):
        cromo1 = self.population[0]
        for cromo in self.population[1:]:
            cromo1 = self.generate_new_best_cromosome(\
                (cromo1, self.get_value_from_cromosome(cromo1)), \
                    (cromo, self.get_value_from_cromosome(cromo)))
        return cromo1[0]

    def get_groups(self):
        groups = []
        cromosome = self.get_final_cromosome()
        for group in len(self.amount_of_groups):
            groups.append([item for item in cromosome[(group * self.groups_len): (((group + 1) * self.groups_len) - 1)]])
        return groups




# class Quicksort:
#     def __init__(self, list_):
#         self.quicksort(list_, 0, len(list_) - 1)

#     def quicksort(self, list_, left, right):
#         if left < right:
#             indiceParticion = self.particion(list_, left, right)
#             self.quicksort(list_, left, indiceParticion)
#             self.quicksort(list_, indiceParticion + 1, right)

#     def particion(self, list_, left, right):
#         pivot = list_[left]
#         while True:
#             # Mientras cada elemento desde la left esté en orden (sea menor que el
#             # pivot) continúa avanzando el índice
#             while list_[left] < pivot:
#                 left += 1

#             # Mientras cada elemento desde la right esté en orden (sea mayor que el
#             # pivot) continúa disminuyendo el índice
#             while list_[right] > pivot:
#                 right -= 1

#             """
#                 Si la left es mayor o igual que la right significa que no
#                 necesitamos hacer ningún intercambio
#                 de variables, pues los elementos ya están en orden (al menos en esta
#                 iteración)
#             """
#             if left >= right:
#                 # Indicar "en dónde nos quedamos" para poder dividir el list_ de nuevo
#                 # y ordenar los demás elementos
#                 return right
#             else:
#                 # Nota: yo sé que el else no hace falta por el return de arriba, pero así el algoritmo es más claro
#                 """
#                     Si las variables quedaron "lejos" (es decir, la left no superó ni
#                     alcanzó a la right)
#                     significa que se detuvieron porque encontraron un valor que no estaba
#                     en orden, así que lo intercambiamos
#                 """
#                 list_[left], list_[right] = list_[right], list_[left]
#                 """
#                     Ya intercambiamos, pero seguimos avanzando los índices
#                 """
#                 left += 1
#                 right -= 1

# """
# Modo de uso:
# """

# list_ = [5, 1, 2, 1, 1, 3, 5, 1, 5, 1, 99, 231, 234, 12, 121,
#            312, 123, 123, 12, 312, 321, 312, 31, 23, 12, 3123, 123, ]
# print("Antes de ordenarlo: ")
# print(list_)
# Quicksort(list_)
# print("Después de ordenarlo: ")
# print(list_)