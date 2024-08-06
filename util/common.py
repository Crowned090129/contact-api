import os
import json
import psycopg2
from string import Template
from dotenv import load_dotenv

class ENVIRONMENT:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ENVIRONMENT, cls).__new__(cls)
            project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
            dotenv_path = os.path.join(project_dir, '.env')
            load_dotenv(dotenv_path)
            cls._instance.domain = os.getenv("DOMAIN")
            cls._instance.port = os.getenv("PORT")
            cls._instance.prefix = os.getenv("PREFIX")
            cls._instance.database = os.getenv("DB_DATABASE")
            cls._instance.dbhost = os.getenv("DB_HOST")
            cls._instance.dbuser = os.getenv("DB_USER")
            cls._instance.dbpassword = os.getenv("DB_PASSWORD")
            cls._instance.dbport = os.getenv("DB_PORT")
        return cls._instance
    def get_domain(self):
        return self.domain
    def get_port(self):
        return self.port
    def get_prefix(self):
        return self.prefix
    def get_db_info(self):
        return {
            "dbhost": self.dbhost,
            "dbport": self.dbport,
            "db": self.database,
            "dbuser": self.dbuser,
            "dbpassword": self.dbpassword
        }

def build_swagger_config_json():
    config_file_path = 'static/swagger/config.json'
    try:
        with open(config_file_path, 'r') as file:
            config_data = json.load(file)
        config_data['servers'] = [
            {"url": f"http://localhost:{ENVIRONMENT().get_port()}{ENVIRONMENT().get_prefix()}"},
            {"url": f"http://{ENVIRONMENT().get_domain()}:{ENVIRONMENT().get_port()}{ENVIRONMENT().get_prefix()}"}
        ]
        with open(config_file_path, 'w') as new_file:
            json.dump(config_data, new_file, indent=2)
    except Exception as e:
        print(f"Error updating swagger config: {e}")

def get_conn_obj():
    try:
        conn_info = ENVIRONMENT().get_db_info()
        conn = psycopg2.connect(
            database=conn_info["db"],
            host=conn_info["dbhost"],
            user=conn_info["dbuser"],
            password=conn_info["dbpassword"],
            port=conn_info["dbport"]
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None