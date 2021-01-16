#!/usr/bin/python3
#-*- coding: utf-8 -*-


import os
import py7zr

def packIdcConnectors():

	files = []

	# 3D models
	for file in os.listdir('3d_models'):
		if file.endswith('.step'):
			if file.startswith('BH-'): files.append('3d_models\{0}'.format(file))
			if file.startswith('BHR-'): files.append('3d_models\{0}'.format(file))

	files.append('IDC Connectors.eli')
	files.append('IDC Connectors.lib')

	with py7zr.SevenZipFile('IDC Connectors.7z', 'w') as archive:
		for file in files:
			archive.write(file)

	py7zr.pack_7zarchive('IDC Connectors',)


if __name__ == "__main__":
	packIdcConnectors()