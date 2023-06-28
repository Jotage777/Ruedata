from flask import jsonify, g, Blueprint, request, send_file
from ..arquivos.functions.functions import is_valid_sequence, read_text_file, read_text_file_link
import mimetypes


file = Blueprint('file',__name__)

# Rota para trocar o arquivo txt e validar o codigo de verificação
@file.route('/upload', methods=["POST"])
def uploadFile():
    """Rota para realizar o upload de um arquivo e fornecer o codigo de validação, o arquivo pode ser atraves de link ou de forma direta
    ---
    tags:
        - FILE
    parameters:
      - in: body
        description: Request body - FORM-DATA
        schema:
          type: object
          properties:
            code:
              type: string
              required: true
              example: "12458765213"
            file:
              type: string
              required: false
              example: arquivo.txt
            file_link:
              type: string
              required: false
              example: "https://rue-platform-dev.s3.amazonaws.com/keylog.txt"
    responses:
      200:
        description: Codigo valido
        examples:
          application/json:
            {
              "message": "Código {code} encontrado na mesma sequência {sequence}"
            }
      400:
        description: Faltando informações
        examples:
          application/json:
            {
              "message": "É preciso fornecer o código de acesso e o arquivo.txt"
            }
      400(2):
        description: Forneceu dois arquivos .txt
        examples:
          application/json:
            {
              "message": "Forneça apenas um arquivo .txt"
            }
      400(3):
        description: O arquivo fornecido não é um .txt
        examples:
          application/json:
            {
              "message": "O arquivo fornecido não é um arquivo de texto (.txt)"
            }
      404:
        description: Não existe codigo valido
        examples:
          application/json:
            {
              "message": "Nenhum código encontrado na mesma sequência"
            }
    """
    #Informações fornecidas
    #Codigo de validação
    code = request.form.get('code')

    #Arquivo via link
    file_link = request.form.get('file_link')

    #Arquivo sem ser link
    file = request.files.get('file')

    #Verificando se todas as informações foram fornecidas
    if not ((file or file_link) and code):
        return jsonify({"message": "É preciso fornecer o código de acesso e o arquivo.txt"}), 400
    
    #Verificando se foi fornecido apenas 1 arquivo
    if file and file_link:
        return jsonify({"message": "Forneça apenas um arquivo .txt"}), 400

    #Verificando se o arquivo fornecido é um .txt
    if file:
        if not file.filename.endswith('.txt') :
            return jsonify({"message": "O arquivo fornecido não é um arquivo de texto (.txt)"}), 400
        
        #Lendo as informações do arquivo
        code_valid = read_text_file(file)
    
    #Verificando se o arquivo link fornecido é um .txt
    elif file_link:
        file_type, _ = mimetypes.guess_type(file_link)
        if file_type != 'text/plain':
            return jsonify({"message": "O arquivo fornecido não é um arquivo de texto (.txt)"}), 400

         #Lendo as informações do arquivo
        code_valid = read_text_file_link(file_link)
    

    # Separa os números do código em uma lista
    code_list = code_valid.strip().split('\n')

    #Verificando se existe algum codigo valido
    for sequence in code_list:
        #Se existir a função para e retorna como verdadeira
        if is_valid_sequence(code, sequence):
            return jsonify({"message": f"Código {code} encontrado na mesma sequência {sequence}"}), 200

    #Caso não exista codigo valido
    return jsonify({"message": "Nenhum código encontrado na mesma sequência"}), 404


#Rota com o arquivo de sequncias validas já definido e com a função de valida o código de acesso fornecido
@file.route('/code_validation', methods=["POST"])
def validadeCode():
    """Rota para realizar fornecer o codigo de validação, e validar com um arquivo txt que já estar dentro da rota
    ---
    tags:
        - FILE
    parameters:
      - in: body
        description: Request body 
        schema:
          type: object
          properties:
            code:
              type: string
              required: true
              example: "12458765213"
            
    responses:
      200:
        description: Codigo valido
        examples:
          application/json:
            {
              "message": "Código {code} encontrado na mesma sequência {sequence}"
            }
      400:
        description: Faltando informações
        examples:
          application/json:
            {
              "message": "É preciso fornecer o código de acesso "
            }
      
      400(2):
        description: O arquivo fornecido não é um .txt
        examples:
          application/json:
            {
              "message": "O arquivo fornecido não é um arquivo de texto (.txt)"
            }
      404:
        description: Não existe codigo valido
        examples:
          application/json:
            {
              "message": "Nenhum código encontrado na mesma sequência"
            }
    """

    #Informações fornecidas
    #Codigo de validação
    request_data = request.get_json()
    code = request_data.get('code')
    
    #Verificando se todas as informações foram fornecidas
    if not  code:
        return jsonify({"message": "É preciso fornecer o código de acesso"}), 400

    #link do arquivo 
    file_link = 'https://rue-platform-dev.s3.amazonaws.com/keylog.txt'

    #Verificando se o arquivo é um .txt
    file_type, _ = mimetypes.guess_type(file_link)
    if file_type != 'text/plain':
        return jsonify({"message": "O arquivo fornecido não é um arquivo de texto (.txt)"}), 400
    
    #Lendo arquivo
    code_valid = read_text_file_link(file_link)
    

    # Separa os números do código em uma lista
    code_list = code_valid.strip().split('\n')
    
    #Verificando se existe algum codigo valido
    for sequence in code_list:
        #Se existir a função para e retorna como verdadeira
        if is_valid_sequence(code, sequence):
            return jsonify({"message": f"Código {code} encontrado na mesma sequência {sequence}"}), 200

    #Caso não exista codigo valido
    return jsonify({"message": "Nenhum código encontrado na mesma sequência"}), 404