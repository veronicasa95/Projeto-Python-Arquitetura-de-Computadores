import socket, pickle, psutil, cpuinfo, os

def mostra_ram():

    # Gera a lista de resposta
    resposta = []
    resposta.append(psutil.cpu_percent())
    mem = psutil.virtual_memory()
    mem_percent = mem.used/mem.total
    resposta.append(mem_percent)
    # Prepara a lista para o envio
    socket_cliente.send(pickle.dumps(resposta))

def info_cpu():
    info = cpuinfo.get_cpu_info()
    bytes_resp = pickle.dumps(info)
    socket_cliente.send(bytes_resp)

def info_processador():
    #Porcentagem de cpu por nucleos
    cpu_nucleos_fisicos = psutil.cpu_count()
    #Frequencia
    cpu_freq =psutil.cpu_freq().current
    #Numero de nucleos e threads
    cpu_nucleos = psutil.cpu_count(logical=False)
    #Prepara para o envio
    bytes_resp1= pickle.dumps(cpu_nucleos_fisicos)
    bytes_resp2 = pickle.dumps(cpu_freq)
    bytes_resp3 = pickle.dumps(cpu_nucleos)
    #Envia os dados
    socket_cliente.send(bytes_resp1)
    socket_cliente.send(bytes_resp2)
    socket_cliente.send(bytes_resp3)

def info_disk():
    disco = psutil.disk_usage(os.getcwd()).percent
    print(disco)
    #Prepara para o envio
    bytes_resp_disco = pickle.dumps(disco)
    #envia os dados
    socket_cliente.send(bytes_resp_disco)

def arquivos_diretorios():

    #obtém lista de arquivos e diretórios
    lista = os.listdir()
    arquivos_formatado()
    #Cria um dicionário
    dic = {}
    for i in lista:
        #verifica se é um arquivo
        if os.path.isfile(i):
            dic[i] = []
            #tamanho do arquivo
            dic[i].append(os.stat(i).st_size)
            #data de criação
            dic[i].append(os.stat(i).st_atime)
            #data de modificação
            dic[i].append(os.stat(i).st_mtime)
    #Envia os dados
    bytes_rep=pickle.dumps(dic)
    #Envia a mensagem
    socket_cliente.send(bytes_rep)
    print(mensagem2)

def processos():
    dic = psutil.pids()
    resposta = pickle.dumps(dic)
    socket_cliente.send(resposta)

def info_redes():
    interfaces_dic = psutil.net_if_addrs()
    resposta = pickle.dumps(interfaces_dic)
    socket_cliente.send(resposta)
    # ip = interfaces_dic['Ethernet'][1].address
    # netmask = interfaces_dic['Ethernet'][1].netmask
    # mac = interfaces_dic['Ethernet'][0].address
    # print(ip,'      ', netmask,'              ', mac)
    # # Envia mensagem

def sair():
    mensagem4=('Fim da conexão')
    socket_cliente.send(mensagem4.encode('utf-8'))
    print ("Fim da conexão com",str(address))
    socket_cliente.shutdown(socket.SHUT_RDWR)
    socket_cliente.close()

def arquivos_formatado():
    titulo = '{:11}'.format("Tamanho") # 10 caracteres + 1 de espaço
    # Concatenar com 25 caracteres + 2 de espaços
    titulo = titulo + '{:27}'.format("Data de Modificação")
    # Concatenar com 25 caracteres + 2 de espaços
    titulo = titulo + '{:27}'.format("Data de Criação")
    titulo = titulo + "Nome"
    print(titulo)

#criar socket
s_servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host= socket.gethostname()
porta=9999
address=(host,porta)
#associar endereço e porta a um socket
s_servidor.bind(address)
#Escutando
s_servidor.listen()
print("Servidor", host, "esperando conexão na porta", porta)
(socket_cliente,addr) = s_servidor.accept()
print("Conectado a:", str(addr))

# Envia mensagem codificada em bytes ao servidor
msg = socket_cliente.recv(1024).decode('utf-8')

while True:
    if msg == '1':
        print('Informações de uso de Memória')
        mostra_ram()
        info_cpu()
        info_processador()
        info_disk()

    elif msg == '2':
        mensagem2 = ('\nInformações sobre arquivos ativos')
        arquivos_diretorios()

    elif msg == '3':
        print('Informações da rede')
        info_redes()
    elif msg == '4':
        print('Sair')
        sair()
    elif msg == '5':
        print('Informações dos processos')
        processos()
    else:
        print('Opções invalidas.')

#fechar conexão
# s_servidor.close()