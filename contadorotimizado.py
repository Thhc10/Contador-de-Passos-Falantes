import RPi.GPIO as GPIO
import time 
from espeak import espeak
from threading import Timer,Thread,Event
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(20 , GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Recebe as oscilacoes
GPIO.setup(19 , GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Reseta
GPIO.setup(16 , GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Total voltas

espeak.set_voice('brazil')
espeak.set_parameter(espeak.Parameter.Rate, 175, 0)
GPIO.setup(26 , GPIO.OUT)

cont = 0
cont_total = 0

# Encontrando a frequência de rotação 
def frequencia():
    global cont, cont_total
    GPIO.wait_for_edge(20, GPIO.RISING)
    t_inicio = time.time()
    GPIO.wait_for_edge(20, GPIO.RISING)
    t_fim = time.time()
    tempo = t_fim - t_inicio # Tempo de uma rotacao
    freq = 1/tempo
    cont = cont + 2
    cont_total = cont_total + 2
    return freq

# Resetando a contagem
def reset_save():
    global cont
    while(1):
        if(GPIO.input(19) == 1):  # Verificação de borda
            cont = 0
            time.sleep(0.5)

# Retornando a contagem total de passos
def get_rot_total():
    global cont_total
    while(1):
        if(GPIO.input(16) == 1):  # Verificação de borda
            espeak.set_parameter(espeak.Parameter.Rate, 150, 0)
            espeak.synth("Foram dadas" + str(cont_total) + "voltas.")
            espeak.set_parameter(espeak.Parameter.Rate, 150, 0)
            time.sleep(0.5)
             
			 
# Se GPIO(19) acionado -> Reseta e Salva o intervalo
t1 = threading.Thread(target=reset_save)
t1.start()

# Se GPIO(16) acionado -> Retorna a distancia total
t2 = threading.Thread(target=get_rot_total)
t2.start()

freq = frequencia();

# Definindo conjuntos de frequências e retornando em áudio
while(freq < 1500):    
       
    if(freq >= 500):
        GPIO.wait_for_edge(20, GPIO.RISING)
        cont = cont + 1
        cont_total = cont_total + 1
        
        if(cont % 500 == 0):
		
			# Retornando contagens em áudio
            espeak.synth(str(cont)) 
        
    elif(freq  >= 200):
            GPIO.wait_for_edge(20, GPIO.RISING)
            cont = cont + 1
            cont_total = cont_total + 1
            
            if(cont % 200 == 0):
                espeak.synth(str(cont))
        
    elif(freq >= 75):
            GPIO.wait_for_edge(20, GPIO.RISING)
            cont = cont + 1
            cont_total = cont_total + 1
            
            if(cont % 75 == 0):
                espeak.synth(str(cont))
                   
    elif(freq >= 25):
            GPIO.wait_for_edge(20, GPIO.RISING)
            cont = cont + 1
            cont_total = cont_total + 1
            
            if(cont % 25 == 0):
                espeak.synth(str(cont))

    elif(freq >= 10):
            GPIO.wait_for_edge(20, GPIO.RISING)
            cont = cont + 1
            cont_total = cont_total + 1
            
            if(cont % 10 == 0):
                espeak.synth(str(cont))
                
    elif(freq >= 3.5):
            GPIO.wait_for_edge(20, GPIO.RISING)
            cont = cont + 1
            cont_total = cont_total + 1
            
            if(cont % 5 == 0):
                espeak.synth(str(cont))
                  
    else:
            espeak.synth(str(cont))
            GPIO.wait_for_edge(20, GPIO.RISING)
            cont = cont + 1
            cont_total = cont_total + 1
            
exit(0)
