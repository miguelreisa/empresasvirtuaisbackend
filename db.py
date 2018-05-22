from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #objecto que se vai ligar à flask app e procurar pelos objectos que queremos para nos deixar mapear esses objectos a rows da DB. Ou seja, passar objecto pa db

#SQLALCHEMY faz as connetion() por nos e ao contrario do sqlite, nao nos devolve rows mas sim objectos, o que facilita
