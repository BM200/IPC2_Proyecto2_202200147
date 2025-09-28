# app/__init__.py
from flask import Flask

app = Flask(__name__)

# Asegúrate de que esta línea esté aquí y guardada
app.secret_key = 'mi_clave_secreta_del_proyecto'

from app import routes