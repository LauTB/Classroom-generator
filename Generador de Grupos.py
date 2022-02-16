from groups_generator import *
from read_file import *
from data_selector import *
from write_file import * 

import sys
from visual.win import *
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox, QCheckBox, QVBoxLayout, QWidget, QDialog, QFormLayout, QLabel, QGroupBox
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
				wd2 = generate_checkbox(categories, self.ui.scrollArea_2)
				wd3 = generate_checkbox(categories, self.ui.scrollArea_3)
				self.ui.scrollArea.setWidget(wd)
				self.ui.scrollArea_2.setWidget(wd2)
				self.ui.scrollArea_3.setWidget(wd3)
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
			if QMessageBox.question(self, "Confirmación", f"Esta seguro que desea crear {self.ui.group_counter.value() + self.ui.group_counter2.value()} grupos?", \
				QMessageBox.Ok | QMessageBox.Cancel,QMessageBox.Cancel)\
					 == QMessageBox.Ok:

				sh = get_sheet(self.direccion)
				data = get_data(sh)
				wd = self.ui.scrollArea.widget()
				wd2 = self.ui.scrollArea_2.widget()
				wd3 = self.ui.scrollArea_3.widget()
				categories1 = asign_lambda_from_checkbox_list(wd)
				categories2 = asign_lambda_from_checkbox_list(wd2)
				categories3 = asign_lambda_from_checkbox_list(wd3)
				categories_temp = concat_list(categories1, categories2) 
				categories = concat_list(categories_temp, categories3)
				self.headers = categories
				result = receive_data(data, categories)
				# print('\n'.join([str(i.tipo_de_estudiante)+'----'+str(i.sexo) for i in result]))
				groups_count = self.ui.group_counter.value() + self.ui.group_counter2.value()
				groups = generate_groups(groups_count, result, self.ui.group_counter.value())
				for id, gr in enumerate(groups):
						db = define_data_base(gr)
						create_sheet(db, get_header_from_data(sh), id, self.ui.group_counter.value())
    						
				return None
				# generate the diferents groups

		except Exception as e:
			print(e)
			QMessageBox.about (self,'Información', 'No se ha seleccionado ningun archivo aún.')
			return None
		

class Dialog(QDialog):
		def __init__(self, *args, **kwargs):
			super(Dialog, self).__init__(*args, **kwargs)
			self.setWindowTitle("Confirmación")
			self.create_formulary(args[0], args[1])
			self.setFixedSize(200, 100)


		def create_formulary(self, groupcount, categories):
			self.gbx_control = QGroupBox("BasicData")
			layout = QFormLayout()
			layout.addRow(QLabel(f"Esta seguro que desea conformar {groupcount} grupos"))
			if categories:
					layout.addRow(QLabel("Las categorías escogidas fueron:"))
					for cat in categories:
						layout.addRow(QLabel(f"{cat}"))
			self.gbx_control.setLayout(layout)


class Confirmation_Dialog(QtWidgets.QDialog):
	def __init__(self, groupcount, categories):
		super().__init__()
		self.initUI(groupcount, categories)
	
	def initUI(self,groupcount, categories):
			self.setWindowTitle("Confirmación para el registro")
			self.create_formulary(groupcount, categories)
	
	def create_formulary(self, groupcount, categories):
		self.gbx_control = QGroupBox("BasicData")
		layout = QFormLayout()
		layout.addRow(QLabel(f"Esta seguro que desea conformar {groupcount} grupos"))
		if categories:
				layout.addRow(QLabel("Las categorías escogidas fueron:"))
				for cat in categories:
					layout.addRow(QLabel(f"{cat}"))
		self.gbx_control.setLayout(layout)

def generate_checkbox(categ_list, environment):
	vbox = QVBoxLayout()
	widget = QWidget()
	for cat in categ_list:
		cb = QCheckBox(cat, environment)
		vbox.addWidget(cb)
	widget.setLayout(vbox)
	return widget

def asign_lambda_from_checkbox_list(widget):
		result = []
		for pos, item in enumerate(widget.children()[1:]):
				if item.isChecked():
					result.append(lambda_list[pos])
		return result
    		 

def get_header_from_data(sheet):
    for row in sheet.iter_rows(min_row=1,values_only = True):
    	return row

def concat_list(list1, list2):
	result = [i for i in list1]
	for i in list2:
		if i not in result:
			result.append(i)
	return result


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    sys.exit(app.exec_())

