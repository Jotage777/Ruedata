from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

# Configurando o aplicativo Flask
app = Flask(__name__)

# Ativando o CORS
CORS(app)

# Configurando o swagger
swagger = Swagger(app)

# Registrando os blueprints
from blueprints.arquivos.file import file
app.register_blueprint(file, url_prefix='/file')

# Inicializando a aplicação
if __name__ == '__main__':
    app.run(debug=True)


