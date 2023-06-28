import requests

#Função para ler o conteudo do arquivo .txt
def read_text_file(file):
    try:
        # Ler o conteúdo do arquivo
        content = file.read().decode('utf-8')
        return content

    except UnicodeDecodeError:
        return None

 
#Função para baixar o conteudo do link informado
def read_text_file_link(file_link):
    try:
        #baixar o arquivo atraves do link
        file = requests.get(file_link)
        return file.content.decode('utf-8')

    except UnicodeDecodeError:
        return None
    

#Função para confirmar uma sequencia valida
#Complexidade O(n*m)
def is_valid_sequence(code, sequence):
    j = 0
    #For para procurar o codigo valido dentro da sequencia fornecida
    for digit in code:
        #Procurando o numero da sequencia
        if digit == sequence[j]:
            j += 1
            #Se encontrar todos os numeros da sequencia
            if j == 3:
                return True

    return False