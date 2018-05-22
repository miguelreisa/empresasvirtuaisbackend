from app import app
from db import db

db.init_app(app)

#nao precisamos de criar as tabelas antes
@app.before_first_request #antes do prmeiro request, corre db.create_all() a menos que ja exista o ficheiro data.db
def create_tables():
	db.create_all() #cria as tables apenas que vê (nos imports). #sempre que criarmos uma nova tabela eliminar ficheiro data.db para isto correr e criar todas incluindo as novas
