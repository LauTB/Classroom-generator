from groups_generator import *
from read_file import *
from data_selector import *

import sys
from visual.win import *
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox
import PyQt5.QtWidgets as QtWidgets
import pandas as pd

class MiApp(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow() 
		self.ui.setupUi(self)		
		self.ui.btn_open.clicked.connect(self.open_file)
		self.ui.btn_show.clicked.connect(self.create_table)
		self.ui.btn_generate.clicked.connect(self.create_groups)
		self.ui.group_counter.value

	def open_file(self):
		file = QFileDialog.getOpenFileName(self,"Abrir Archivo Excel", "","Excel Files (*.xlsx) ;; All Files (*)")
		self.direccion = file[0]

	def create_table(self):
		try:	
			df = pd.read_excel(self.direccion)

			columnas = list(df.columns)
			df_fila = df.to_numpy().tolist()
			x = len(columnas)
			y = len(df_fila)

		except ValueError:
			QMessageBox.about (self,'Informacion', 'Formato incorrecto')
			return None			

		except FileNotFoundError:
			QMessageBox.about (self,'Informacion', 'El archivo esta \n malogrado')
			return None
		#print(x, y)
		self.ui.tableWidget.setRowCount(y)
		self.ui.tableWidget.setColumnCount(x)

		for j in range(x):
			#print(columnas[j])
			encabezado = QtWidgets.QTableWidgetItem(columnas[j])
			self.ui.tableWidget.setHorizontalHeaderItem(j,encabezado )
			for i in range(y):
				dato = str(df_fila[i][j])
				if dato == 'nan':
					dato =''
				self.ui.tableWidget.setItem(i,j, QTableWidgetItem(dato))
		#print(df_fila)

	def create_groups(self):
            try:
                sh = get_sheet(self.direccion)
                data = get_data(sh)
                result = receive_data(data, [sexo])
                groups = generate_groups(self.ui.group_counter.value, result)
            except: pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    sys.exit(app.exec_())


'''


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

    
'''