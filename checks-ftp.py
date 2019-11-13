#!/usr/bin/python3
from sys import argv
import os
from ftplib import FTP_TLS

notification = []

def _args():
    if len(argv) != 4:
        print("Usage: python3 checks-ftp.py base-dir file ftp-password")
        exit(1)

    return argv[1], argv[2], argv[3]

def downFile(ftp, fileName, localName):
    """ Realiza o download do arquivo denominado fileName """

    localfile = open(localName, 'wb')    #Nome que recebera no local
    ftp.retrbinary('RETR ' + fileName, localfile.write)
    localfile.close()

def compareFile(ftp, fileName):
    """ Compara se dois arquivos sao iguais """

    nameFile = [fileName, 'NEW_' + fileName]
    file = []
    downFile(ftp, nameFile[0], nameFile[1])
    for i in range(2):
        arquive = open(nameFile[i], 'r')
        file.append(arquive.read())
        arquive.close()

    local = ftp.pwd()
    if file[0] != file[1]:
        print('Os textos são diferentes em: ', local)
        notification.append('Os textos são diferentes em: ' + local)

def main():
    base_dir, file, FTP_PASSWORD = _args()

    FTP_HOST = 'oplab9.parqtec.unicamp.br'
    USER = 'jr-santos'
    ftp = FTP_TLS(FTP_HOST)
    ftp.login(USER, FTP_PASSWORD)
    ftp.prot_p()    #Ativado proteção dos dados

    ftp.cwd(base_dir)
    for i in ftp.nlst():
        if i == file:
            downFile(ftp, file, file)
        else:
            ftp.cwd(i)
            content_dir = ftp.nlst()
            try:
                content_dir.index(file)  #Tentar encontrar arquivo
                #Comparar arquivos
                compareFile(ftp, file)
            except ValueError:
                #Disparar erro de arquivo não existe
                local = ftp.pwd()
                print('Arquivo não existe em: ', local)
                notification.append('Arquivo não existe em: ' + local)
            ftp.cwd('..')

    ftp.prot_c()    #Fechando proteção de dados
    ftp.close()

    print('O número de problemas encontrados foi: ', len(notification))

    if len(notification) >= 1:
        exit(22)
    else:
        print('O diretorio possui o arquivo atualizado em todas as pastas')

main()
