# CET107-Processamento_Paralelo-Exercicios

## Sobre o algoritmo de Limiarização  
O algoritmo de limiarização está na pasta Limiarizacao junto com algumas imagens utilizadas para teste.  

### Dependências  
O código foi desenvolvido com o Python3. As bibliotecas utilizadas no código foram:
- OpenCV
- Numpy
- Pyplot derivada do matplotlib,

Para a criação dos códigos paralelos foram feitos com o PyMP. A instalação na minha máquina foi feita utilizando o Pip com o comando:  
`pip install pymp-pypi`
 
### Como executar o código
Para executar o código basta apenas executar o comando:  
`python3 limiar_seq.py nome_img.extensao_img`  
Foram testadas imagens de diferentes resoluções e formatos, entre eles o .png, .jpg, .jpeg e .jfif.

Além do comando básico, também podem ser passados dois argumentos para definir o limiar inicial e a diferença de limite. Estes dois parâmetros precisam estar em ordem para evitar  que os valores fiquem trocados.  
`python3 limiar_seq.py nome_img.jpg limiar diff`    
Os valores default do limiar e da diferença limite são, respectivamente, `127` e `5`.

Por fim, também podem ser passados os parâmetros `-h`, `-dr` e `-da` em qualquer ordem depois dos argumentos anteriores.
O `-h` fará com que o código salve o histograma em uma imagem.  
Os parâmetro `-dr`(diferença relativa) e `-da`(diferença absoluta) definirão qual tipo de cálculo de diferença será feito para critério de parada. O valor default desse parâmetro é `-da`.    
Vale notar que estes parâmetros só funcionarão caso venham depois de todos os anteriores, como no exemplo abaixo:  
`python3 limiar_seq.py img.png 127 5 -h -ra`  

### Problemas encontrados  
Por causa de um problema com o display do WSL não foi possível testar a funcionalidade do salvamento da imagem do histograma, porém o algoritmo sempre o calcula, mesmo que não seja passado o parâmetro `-h`.  
  
Antes de decidirmos utilizar o PyMP, foram desperdiçadas **muitas** horas tentando implementar o algoritmo sequencial em C utilizando a extensão de C do Python. Depois de muitos problemas, por causa da dificuldade de se compreender o código e do tempo curto, tomamos a decisão de optar pelo caminho mais fácil. Porém, por causa desses diversos contratempos, não foi possível testar se as funcionalidades de processamento paralelo do PyMP estão funcionando nas máquinas, então o código sequencial foi feito assumindo que o PyMP funcionará sem problemas, mas não foram feitos nenhum teste conclusivo.
