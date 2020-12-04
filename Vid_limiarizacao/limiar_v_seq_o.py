import cv2 as cv
import numpy as np
import sys
import time
from limiar import calc_hist, calc_limiar, create_binary

def parse_args(args):
    if (len(args) >= 1): vid_path = args[0]
    else: quit("É necessário carregar um vídeo para executar a aplicação!")
    create_hist = False
    is_diff_abs = True
    is_verbose = False
    l_inicial = 127
    diff_limite = 5
    for i in range(1, len(args)):
        if (args[i] == "-l" and args[i+1] is not None):
            l_inicial = int(args[i+1])
        if (args[i] == "-dl" and args[i+1] is not None):
            diff_limite = float(args[i+1])
        if (args[i] == "-dr"):
            is_diff_abs = False
        if (args[i] == "-da"):
            is_diff_abs = True
        if (args[i] == "-v"):
            is_verbose = True
    if (is_verbose):
        print("Limiar inicial: ", l_inicial)
        print("Diferença limite: ", diff_limite)
        print("Diferença absoluta? ", is_diff_abs)
    return vid_path, l_inicial, diff_limite, is_diff_abs, is_verbose

def get_vid_info(cap):
  vid_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
  vid_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
  vid_fps = cap.get(cv.CAP_PROP_FPS)
  return vid_width, vid_height, vid_fps

def main(argv):
    vid_path, l_inicial, diff_limite, is_diff_abs, is_verbose = parse_args(argv)

    # Criando o objeto que irá capturar os frames do vídeo de entrada
    cap = cv.VideoCapture(vid_path)
    vid_width, vid_height, vid_fps = get_vid_info(cap)

    # Criando o escritor para arquivos .mp4 ou .avi
    vid_name, vid_ext = vid_path.split('.')[-2:]
    vid_name = vid_name.split('/')[-1]
    if (vid_ext == "mp4"): fourcc = cv.VideoWriter_fourcc(*'mp4v')
    elif (vid_ext == "avi"): fourcc = cv.VideoWriter_fourcc(*'XVID')
    else: quit("Formato de vídeo não reconhecido.\nAbortando o programa...")
    out = cv.VideoWriter('{0}_binary.{1}'.format(vid_name, vid_ext), fourcc, vid_fps, (vid_width, vid_height), isColor=False)

    if (is_verbose):
        count = 1
        t_sum = 0
        start_total = time.perf_counter()
    while(True):
        success, frame = cap.read()
        if (success):
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            n_linhas, n_colunas = gray.shape
            v_gray = gray.reshape(n_linhas*n_colunas)

            # Calculando o Histograma
            if (is_verbose):
                print("-------------------------------------------------------------")
                start = start_frame = time.perf_counter()
                hist = calc_hist(v_gray, v_gray.size)
                finish = time.perf_counter()
                print("Cálculo do histograma do frame {0} feito em {1} segundos".format(count, (finish-start)))
            else:
                hist = calc_hist(v_gray, v_gray.size)
            
            # Calculando o limiar
            if (is_verbose):
                start = time.perf_counter()
                l = calc_limiar(hist, l_inicial, diff_limite, is_diff_abs)
                finish = time.perf_counter()
                print("Cálculo do limiar do frame {0} feito em {1} segundos".format(count, (finish-start)))
                print("Limiar: ", l)
            else:
                l = calc_limiar(hist, l_inicial, diff_limite, is_diff_abs)
            
            # Criando a imagem binária
            if (is_verbose):
                start = time.perf_counter()
                new_img_v = create_binary(v_gray, v_gray.size, l)
                finish = finish_frame = time.perf_counter()
                t_sum += (finish_frame - start_frame)
                print("Binarização do frame {0} feita em {1} segundos".format(count, (finish-start)))
                print("Tempo de processamento do frame {0}: {1} segundos".format(count, finish_frame-start_frame))
                count += 1
            else:
                new_img_v = create_binary(v_gray, v_gray.size, l)
            
            # O Frame precisa ser redimensionado antes de ser escrito
            new_img = new_img_v.reshape((n_linhas, n_colunas))  

            # Escrevendo frame no arquivo de saída
            out.write(new_img)
        else: 
            break
    if (is_verbose):
        finish_total = time.perf_counter()
        print("-------------------------------------------------------------")
        print("Tempo gasto fora das etapas chave: {}".format((finish_total-start_total) - t_sum))
        print("Tempo de execução total do algoritmo: {} segundos".format(finish_total-start_total))
    cap.release()
    out.release()
#Fim

if __name__ == "__main__":
    main(sys.argv[1:])