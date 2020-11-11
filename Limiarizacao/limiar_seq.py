import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

import sys
import time

def parse_args(args):
	if (len(args) >= 1): img_name = args[0]
	else: quit("É necessário carregar uma imagem para executar a aplicação!")
	
	if (len(args) >= 2): l_inicial = int(args[1])
	else: l_inicial = 127
	
	if (len(args) >= 3): diff_limite = int(args[2])
	else: diff_limite = 5
	
	createHist = False
	is_diff_abs = True
	if (len(args) >= 4):
		for arg in args[3:]:
			print(arg)
			if (arg == "-h"): 
				createHist = True
			if (arg == "-dr"):
				is_diff_abs = False
			if (arg == "-da"):
				is_diff_abs = True
	return img_name, l_inicial, diff_limite, is_diff_abs, createHist 
	

def calc_limiar(img, n_linhas, n_colunas, l, err, is_diff_abs):
	somaMenor = somaMaior = contaMenor = contaMaior = 0
	diff = err
	while (diff >= err):
		for i in range(n_linhas):
			for j in range(n_colunas):
				if (img[i][j] < l):
					somaMenor += img[i][j]
					contaMenor += 1
				else:
					somaMaior += img[i][j]
					contaMaior += 1
		l_maior = somaMaior/contaMaior
		l_menor = somaMenor/contaMenor
		l1 = (l_maior+l_menor)/2
		if (is_diff_abs): 
			diff = abs(l1 - l)
		else:
			diff = abs(l1 - l)/l
		l = l1
	return l

def calc_hist(img, n_linhas, n_colunas):
	hist = [0]*256
	for i in range(n_linhas):
		for j in range(n_colunas):
			hist[img[i][j]] += 1
	return hist

def create_binary(img, n_linhas, n_colunas, l):
	new_img = np.array([np.array([0]*n_colunas)]*n_linhas)
	for i in range(n_linhas):
		for j in range(n_colunas):
			if (img[i][j] > l): 
				new_img[i][j] = 255
	return new_img

def main(argv):
	img_str, l_inicial, diff_limite, is_diff_abs, createHist = parse_args(argv)
	img = cv.imread(img_str, 0)
	n_linhas, n_colunas = img.shape

	l = calc_limiar(img, n_linhas, n_colunas, l_inicial, diff_limite, is_diff_abs)
	hist = calc_hist(img, n_linhas, n_colunas)
	new_img = create_binary(img, n_linhas, n_colunas, l)
	
	img_name, img_ext = img_str.split('.')
	if (createHist):
		plt.plot(hist, 'b-')
		plt.axvline(l, 0, max(hist), color='r')
		plt.savefig("{}_hist.jpg".format(img_name))
	cv.imwrite("b_{}.{}".format(img_name, img_ext), new_img)

if __name__ == "__main__":
	main(sys.argv[1:])