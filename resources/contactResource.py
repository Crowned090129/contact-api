from flask_restful import Resource
from flask import request, jsonify
from util.common import get_conn_obj
import json

class ContactsGETResource(Resource):
    def get(self):
        try:
            with get_conn_obj() as dbConn:
                with dbConn.cursor() as cursor:
                    cursor.execute("SELECT id_, name_, lastname_, mail_, phone_ FROM NPE_CONTACT_TBL WHERE CTRL_DELETED_ = '0'")
                    contacts = cursor.fetchall()
            return jsonify(contacts)
        except Exception as e:
            return {'error': str(e)}, 500

class ContactGETResource(Resource):
    def get(self, id):
        try:
            with get_conn_obj() as dbConn:
                with dbConn.cursor() as cursor:
                    cursor.execute("SELECT id_, name_, lastname_, mail_, phone_ FROM NPE_CONTACT_TBL WHERE CTRL_DELETED_ = '0' AND id_ = %s", ([id]))
                    contact = cursor.fetchall()
            return jsonify(contact)
        except Exception as e:
            return {'error': str(e)}, 500

class ContactPOSTResource(Resource):
    def post(self):
        try:
            contact = json.loads(request.data)
            with get_conn_obj() as dbConn:
                with dbConn.cursor() as cursor:
                    cursor.execute("INSERT INTO NPE_CONTACT_TBL (id_, name_, lastname_, mail_, phone_) VALUES (%s, %s, %s, %s, %s)", 
                                   (contact["id"], contact["name"], contact["lastname"], contact["mail"], contact["phone"]))
                    dbConn.commit()
            return jsonify(contact)
        except Exception as e:
            return {'error': str(e)}, 500

class ContactPUTResource(Resource):
    def put(self, id):
        try:
            contact = json.loads(request.data)
            with get_conn_obj() as dbConn:
                with dbConn.cursor() as cursor:
                    cursor.execute("UPDATE NPE_CONTACT_TBL SET name_ = %s, lastname_ = %s, mail_ = %s, phone_ = %s WHERE id_ = %s AND CTRL_DELETED_ = '0'", 
                                   (contact["name"], contact["lastname"], contact["mail"], contact["phone"], id))
                    dbConn.commit()
            return {'status': 'success'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

class ContactDELETEResource(Resource):
    def delete(self, id):
        try:
            with get_conn_obj() as dbConn:
                with dbConn.cursor() as cursor:
                    cursor.execute("UPDATE NPE_CONTACT_TBL SET CTRL_DELETED_ = '1' WHERE id_ = %s", ([id]))
                    dbConn.commit()
            return {'status': 'success'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
