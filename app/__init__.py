from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pyodbc
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SECRET_KEY'] = 'c5c146f9af44e21a607187560ea61ee5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.db'
#  Connect SQL Server
sql_server_engine = create_engine(
    'mssql+pyodbc://sa:Z@gros@PB@172.25.10.16/ZAGROSDW',
    connect_args={'driver': 'SQL Server'}
)
db = SQLAlchemy(app)

# ایجاد context برای اپلیکیشن
app.app_context().push()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'برای مشاهده این قسمت ابتدا وارد شوید'
login_manager.login_message_category = 'error'
sql_server_conn_str = 'DRIVER={SQL Server};SERVER=172.25.10.16;DATABASE=ZAGROSDW;UID=sa;PWD=Z@gros@PB'
sql_server_conn = pyodbc.connect(sql_server_conn_str)
sql_server_cursor = sql_server_conn.cursor()

from app import routes

migrate = Migrate(app, db)
