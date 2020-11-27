import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pymp
import sys
import time

def parse_args(args):
    if (len(args) >= 1): img_name = args[0]
    else: quit("É necessário carregar uma imagem para executar a aplicação!")
    create_hist = False
    is_diff_abs = True
    is_verbose = False
    l_inicial = 127
    diff_limite = 5
    n_threads = pymp.config.num_threads[0]
    for i in range(1, len(args)):
        if (args[i] == "-l" and args[i+1] is not None):
            l_inicial = int(args[i+1])
        if (args[i] == "-dl" and args[i+1] is not None):
            diff_limite = float(args[i+1])
        if (args[i] == "-h"):
            create_hist = True
        if (args[i] == "-dr"):
            is_diff_abs = False
        if (args[i] == "-da"):
            is_diff_abs = True
        if (args[i] == "-v"):
            is_verbose = True
        if (args[i] == "-nt" and args[i+1] is not None):
            n_threads = int(args[i+1])
    if (is_verbose):
        print("Limiar inicial:", l_inicial)
        print("Diferença limite:", diff_limite)
        print("Diferença absoluta?", is_diff_abs)
        print("Número de threads utilizados:", n_threads)
    return img_name, l_inicial, diff_limite, is_diff_abs, create_hist, is_verbose, n_threads

def calc_limiar(hist, l, err, is_diff_abs):
	diff = err
	while (diff >= err):
		somaMenor = somaMaior = contaMenor = contaMaior = 0
		for i in range(int(l)):
			somaMenor += hist[i]*i
			contaMenor += hist[i]
		for i in range(int(l), 256):
			somaMaior += hist[i]*i
			contaMaior += hist[i]
		l1 = (somaMaior/contaMaior+somaMenor/contaMenor)/2
		if (is_diff_abs): 
			diff = abs(l1 - l)
		else:
			diff = abs(l1 - l)/l
		l = l1
	return l

def calc_hist(img, img_size, n_threads): # Fazer o cálculo com True e False?
    hist = pymp.shared.array((256,), dtype='uint32')
    with pymp.Parallel(n_threads) as p:
        p_hist = [0]*256
        for i in p.range(img_size):
            p_hist[img[i]] += 1
        for i in range(256):
            with p.lock:
                hist[i] += p_hist[i]
    return hist

def create_binary(img, img_size, l, n_threads):
    new_img = pymp.shared.array((img_size,), dtype='uint8')
    with pymp.Parallel(n_threads) as p:
        for i in p.range(img_size):
            if (img[i] > l): 
                new_img[i] = 255
            else: 
                new_img[i] = 0
    return new_img

def main(argv):
	img_path, l_inicial, diff_limite, is_diff_abs, create_hist, is_verbose, n_threads = parse_args(argv)
	img = cv.imread(img_path, 0)
	n_linhas, n_colunas = img.shape
	img_v = img.reshape(n_linhas*n_colunas)
    
	if (is_verbose):
		print("-------------------------------------------------------")
		print("Iniciando...")
		start = start_total = time.perf_counter()
		hist = calc_hist(img_v, img_v.size, n_threads)
		finish = time.perf_counter()
		print("Cálculo do histograma feito em {} segundos".format(finish-start))
	else:
		hist = calc_hist(img_v, img_v.size, n_threads)
	
	if (is_verbose):
		start = time.perf_counter()
		l = calc_limiar(hist, l_inicial, diff_limite, is_diff_abs)
		finish = time.perf_counter()
		print("Limiar: ", l)
		print("Cálculo do limiar feito em {} segundos".format(finish - start))
	else:
		l = calc_limiar(hist, l_inicial, diff_limite, is_diff_abs)
    
	if (is_verbose):
		start = time.perf_counter()
		new_img = create_binary(img_v, img_v.size, l, n_threads)
		finish = finish_total = time.perf_counter()
		print("Binarização da imagem feita em {} segundos".format(finish-start))
		print("Tempo de execução total: {} segundos".format(finish_total-start_total))
	else:
		new_img = create_binary(img_v, img_v.size, l, n_threads)
	
	new_img = new_img.reshape((n_linhas, n_colunas))
	img_name, img_ext = img_path.split('.')[-2:]
	img_name = img_name.split('/')[-1]
	if (create_hist):
		plt.plot(hist, 'b-')
		plt.axvline(l, 0, max(hist), color='r')
		plt.savefig("{}_hist.jpg".format(img_name))
	cv.imwrite("b_{}.{}".format(img_name, img_ext), new_img)

if __name__ == "__main__":
	main(sys.argv[1:])