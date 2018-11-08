import socket
import time
import pickle
import psutil
def formatar_titulo():
    titulo = '{:^7}'.format("PID")
    titulo = titulo + '{:^11}'.format("# Threads")
    titulo = titulo + '{:^26}'.format("Criação")
    titulo = titulo + '{:^9}'.format("T. Usu.")
    titulo = titulo + '{:^9}'.format("T. Sis.")
    titulo = titulo + '{:^12}'.format("Mem. (%)")
    titulo = titulo + '{:^12}'.format("RSS")
    titulo = titulo + '{:^12}'.format("VMS")
    titulo = titulo + " Executável"
    print(titulo)

def formatar_textopro():
    try:
        p = psutil.Process(pid)
        texto = '{:6}'.format(pid)
        texto = texto + '{:11}'.format(p.num_threads())
        texto = texto + " " + time.ctime(p.create_time()) + " "
        texto = texto + '{:8.2f}'.format(p.cpu_times().user)
        texto = texto + '{:8.2f}'.format(p.cpu_times().system)
        texto = texto + '{:10.2f}'.format(p.memory_percent()) + " MB"
        rss = p.memory_info().rss / 1024 / 1024
        texto = texto + '{:10.2f}'.format(rss) + " MB"
        vms = p.memory_info().vms / 1024 / 1024
        texto = texto + '{:10.2f}'.format(vms) + " MB"
        texto = texto + " " + p.exe()
        print(texto)
    except:
        pass

def redes_formatada(info_redes):
    titulo = '{:21}'.format("Ip")
    titulo = titulo + '{:27}'.format("Netmask")
    titulo = titulo + '{:27}'.format("MAC")
    print(titulo)
    print(info_redes,'\n')

def processador_formato():
    titulo = '{:11}'.format("Nucleos Fisicos")
    titulo = titulo + '{:11}'.format("Frequencia")
    titulo = titulo + '{:7}'.format("Nucleos Logicos")
    print('\n',titulo)

# criar socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#conectar a um processo/servidor
server.connect((socket.gethostname(),9999))

print("Conectado")

#informações que são carregadas para o menu
#MENU
print("\n ------------------MENU-------------------")
print("\n 1- Informações da Máquina ")
print("\n 2- Arquivos  Ativos ")
print("\n 3- Informações de Redes ")
print("\n 4- Sair ")
print("\n 5- Processos ativos ")
print("\n -----------------------------------------")

while True:
    #envia resposta
    #decodifica mensagem em utf-8/ recebe a mensagem
    menu = input('digite a opção desejada: ')
    server.send(menu.encode('utf-8'))
    if menu == '1':
        for i in range (1):
            server.send(menu.encode('UTF-8'))
            msg = ' '
            print('{:>8}'.format('%CPU')+'{:>8}'.format('%MEM'))
            # Envia mens1agem vazia apenas para indicar a requisição
            bytes = server.recv(8192)
            # Converte os bytes para lista
            lista1 = pickle.loads(bytes)
            #Memoria em Porcentagem
            print(lista1)
            #CPU
            info_cpu = server.recv(1024)
            info = pickle.loads(info_cpu)
            print(info['brand'])
            #Informacao do processador
            processador_formato()
            nucleos1 = server.recv(1024)
            nucleos2 = pickle.loads(nucleos1)
            frequencia = server.recv(1024)
            frequencia1 = pickle.loads(frequencia)
            nucleosf = server.recv(1024)
            nucleosf1 = pickle.loads(nucleosf)
            print(nucleos2,frequencia1,nucleosf1)#nº de núcleos e Threads
             #Disco usado
            recebe_disco = server.recv(1024)
            disco = pickle.loads(recebe_disco)
            print("Percentual de Disco Usado:", disco,'%')

    elif menu == '2':
        server.send(menu.encode("utf-8"))
        bytes = server.recv(2048)
        lista2 = pickle.loads(bytes)
        titulo = '{:11}'.format("Tamanho") # 10 caracteres + 1 de espaço
        titulo = titulo + '{:27}'.format("Data de Modificação")
        titulo = titulo + '{:27}'.format("Data de Criação")
        titulo = titulo + "Nome"
        print(titulo)
        for i in lista2:
            kb = lista2[i][0]/1000
            tamanho = '{:10}'.format(str('{:.2f}'.format(kb)+' KB'))
            print(tamanho, time.ctime(lista2[i][2]), " ", time.ctime(lista2[i][1]), " ", i)
        time.sleep(1)

    elif menu == '3':
        recv = server.recv(2048)
        redes_formatada(pickle.load(recv))

    elif menu == '4':
        server.send(menu.encode('utf-8'))
        bytes = server.recv(1024)
        server.shutdown(socket.SHUT_RDWR)
        server.close()
    elif menu == '5' :
        server.send(menu.encode('utf-8'))
        recv = server.recv(1024)
        dic = pickle.loads(recv)
        lista = psutil.pids()
        time.sleep(2)
    else:
        server.close()
