from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, getfqdn, gethostbyname
from os import system
from time import sleep
server = None
para = False
def voltar ():
    for i in range(5, 0, -1):
        print(f"\rVoltando em: {i}", end="")
        sleep(1)
    opcao()
def opcao ():
    system("cls")
    for i in "--- SimpleTSC ---\n":
        print(i, end="", flush= True)
        sleep(0.025)
    resposta = input("\nCriar chat (1)\nConectar a um chat (2)\n")
    if resposta == "1": criar()
    elif resposta == "2": conectar()
    else:
        print("\nErro: Esta opção não existe", "\n", flush=True)
        voltar()
def criar ():
    try:
        global server
        server = socket(AF_INET, SOCK_STREAM)
        system("cls")
        porta = int(input("Digite a porta: "))
        server.bind((gethostbyname(getfqdn()), porta))
        server.listen(5)
        system("cls")
        print(f"Chat estabelecido: {gethostbyname(getfqdn())}: {porta}.\n\n\n\n\n         [Aguardando conexão...]", end="")
        sanandreas, endereco = server.accept()
        print (f"\r              [CONECTADO]       ")
        sleep (0.7)
        system ("cls")
        print(f"Conexão estabelecida com {endereco} (Para fechar o chat, digite: -Sair).\n")
        sistema(sanandreas)
    except Exception as e:
        print("Erro: ", e, "\n", flush=True)
        voltar()
def conectar ():
    system ("cls")
    endereco = input ("Digite o endereço: ")
    porta = int (input ("Digite a porta: "))
    sanandreas = socket(AF_INET, SOCK_STREAM)
    try:
        sanandreas.connect ((endereco, porta))
        system ("cls")
        print ("Conexão estabelecida (Para fechar o chat, digite: -Sair).\n")
        sistema (sanandreas)
    except Exception as e:
        print ("Erro: ", e, "\n", flush=True)
        voltar()
def sistema (sla): 
    global server
    def mensagem():
        while True:
            msg = input ("")
            try:
                sla.send (msg.encode())
                if msg == "-Sair":
                    print("\nConexão finalizada.")
                    sla.close()
                    if server: server.close()
                    voltar()
                    break
            except ConnectionAbortedError:
                print("\nConexão finalizada.")
                sla.close()
                if server: server.close()
                voltar()
                break
            except: continue
    def receber ():
        global para
        global server
        para = False
        while not para:
            try:
                info = sla.recv(1024)
                if info.decode() == "-Sair":
                    print("\nConexão finalizada do outro lado.")
                    sla.close()
                    if server: server.close()
                    para = True
                    voltar()
                    break
                else: print(f"{getfqdn()}: {info.decode()}")
            except ConnectionResetError:
                print("\nConexão finalizada do outro lado.")
                sla.close()
                if server:
                    server.close()
                para = True
                voltar()
                break
            except: continue
    Thread(target=receber).start()
    mensagem()
opcao()