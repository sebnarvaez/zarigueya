#!/bin/python3
import os
import json
import re
import argparse
from string import Template

tmplt_path = "template.txt"
out_path = "output.txt"

with open(tmplt_path, 'r') as tmplt_file:
	tmplt_str = tmplt_file.read()
	out_str = ""
	
	variables = [
		["Cedula", "0"],
		["Nombre", "1"],
		["Telefono", "2"],
		["Clave", "3"],
		["Email", "4"],
		["Dias", "5"],
		["Balance", "6"],
		["Liquidacion", "7"],
		["Descuento", "8"],
		["Credito", "9"],
		["Gastos", "10"],
		["Notificacion", "11"],
		["UltimoIngreso", "12"],
		#["Icono", "14"],
		["Saldo", "13"],
		["Mensualidad", "14"],
		["Quincena", "15"],
		["MensPagos", "16"],
		["QuinPagos", "17"],
		["Activo", "18"]

	]
	
	for elem in variables:
		out_str += tmplt_str.format(*variables)
		out_str += "\n"
		
	with open(out_path, 'w') as out_file:
		out_file.write(out_str)
	
