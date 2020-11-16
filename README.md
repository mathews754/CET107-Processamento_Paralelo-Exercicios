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

#### Parâmetros de entrada  
Além do comando básico, o algoritmo também aceita os seguintes parâmetros como descritos abaixo:  
- `-l x` -> Define o valor do limiar inicial igual a x. Seu valor default é 127.  
- `-dl x` -> Define o valor da diferença limite igual a x. Seu valor default é 5.  
- `-h` -> Define se o algoritmo criará o arquivo do histograma. O histograma em si sempre será calculado, este parâmetro só define se a saída conterá a imagem do histograma ou não.  
- `-dr ou -da` -> Define que o tipo de cálculo para critério de parada do cálculo do limiar. `dr = diferença relativa` e `da = diferença absoluta`  
- `-v` -> Executa o código em modo verboso, printando as configurações iniciais, os tempos de cada etapa e o tempo de execução total das etapas de maior custo de performance.  
- `-nt x (Apenas para a versão paralela)` -> Define que um número de threads usadas na execução igual a x. O valor default é o número máximo de threads da máquina.  

#### Exemplos
`python3 limiar_seq.py nome_img.extensao_img -v -h`  
Executa o código sequencial no modo verboso e com a criação da imagem do histograma.

`python3 limiar_par.py nome_img.extensao_img -nt 8 -dr -dl 0.05`  
Executa o código paralelo com 8 threads e utilizando uma diferença relativa de 0.05 como critério de parada.   

### Problemas encontrados  
Por causa de um problema com o display do WSL não foi possível testar a funcionalidade do salvamento da imagem do histograma, porém o algoritmo sempre o calcula, mesmo que não seja passado o parâmetro `-h`.  
  
Antes de decidirmos utilizar o PyMP, foram desperdiçadas **muitas** horas tentando implementar o algoritmo sequencial em C utilizando a extensão de C do Python. Depois de muitos problemas, por causa da dificuldade de se compreender o código e do tempo curto, tomamos a decisão de optar pelo caminho mais fácil. Porém, por causa desses diversos contratempos, não foi possível testar se as funcionalidades de processamento paralelo do PyMP estão funcionando nas máquinas, então o código sequencial foi feito assumindo que o PyMP funcionará sem problemas, mas não foram feitos nenhum teste conclusivo.  


