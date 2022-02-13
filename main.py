from groups_generator import *
from read_file import *
from data_selector import *
from write_file import * 

import sys
from visual.win import *
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox, QCheckBox, QVBoxLayout, QWidget
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

	def open_file(self):
			try:
				file = QFileDialog.getOpenFileName(self,"Abrir Archivo Excel", "","Excel Files (*.xlsx) ;; All Files (*)")
				self.direccion = file[0]
				sh = get_sheet(self.direccion)
				categories = get_header_from_data(sh)
				wd = generate_checkbox(categories, self.ui.scrollArea)
				self.ui.scrollArea.setWidget(wd)
			except: pass

	def create_table(self):
		try:	
			df = pd.read_excel(self.direccion)

			columnas = list(df.columns)
			df_fila = df.to_numpy().tolist()
			x = len(columnas)
			y = len(df_fila)

		except ValueError:
			QMessageBox.about (self,'Información', 'Formato incorrecto')
			return None			

		except FileNotFoundError:
			QMessageBox.about (self,'Información', 'El archivo esta \n malogrado')
			return None
		#
		# (x, y)
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
				wd = self.ui.scrollArea.widget()
				categories = asign_lambda_from_checkbox_list(wd)
				self.headers = categories
				result = receive_data(data, categories)
				groups = generate_groups(self.ui.group_counter.value(), result)
				print(categories)
				for id, gr in enumerate(groups):
						db = define_data_base(gr)
						create_sheet(db, get_header_from_data(sh), id)
    						
				return None
				# generate the diferents groups
		except:
			QMessageBox.about (self,'Información', 'No se ha seleccionado ningun archivo aún.')
			return None

def generate_checkbox(categ_list, environment):
	vbox = QVBoxLayout()
	widget = QWidget()
	for cat in categ_list:
		cb = QCheckBox(cat, environment)
		vbox.addWidget(cb)
	widget.setLayout(vbox)
	return widget

def asign_lambda_from_checkbox_list(widget):
		checkbox_list = widget.children()[0]
		result = []
		for pos, item in enumerate(checkbox_list.children()):
			if item.isChecked():
				result.append(lambda_list[pos])
		return result
    		 

def get_header_from_data(sheet):
    for row in sheet.iter_rows(min_row=1,values_only = True):
    	return row



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    sys.exit(app.exec_())

