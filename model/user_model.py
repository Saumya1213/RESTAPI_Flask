import mysql.connector
import json
import jwt
from flask import make_response
from datetime import datetime, timedelta
from config.config import dbconfig

class user_model():
    def __init__(self):
        # Connection establishment code
        try:
            self.con=mysql.connector.connect(host=dbconfig['hostname'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.cur=self.con.cursor(dictionary=True)
            self.con.autocommit=True
            print("Connection Successfully Established !!")
        except:
            print("Some Error!!")
        
        
    def user_getall_model(self): 
        # Query execution code
        self.cur.execute("SELECT*FROM users")
        res = self.cur.fetchall()
        #print(res)
        if len(res)>0:
            resp= make_response({"payload":res},200)
            resp.headers['Access-Control-Allow-Origin']="*"
            return resp
        else: 
            return make_response({"message":"No Data Found !!"},204)
        
    def user_addone_model(self, data): 
        # Query execution code
        self.cur.execute(f"Insert into users(name, email, role_id, password) values('{data['name']}', '{data['email']}', '{data['role_id']}', '{data['password']}')")
        return {"message":"User created successfully !!"}
    
    def user_update_model(self, data): 
        # Query execution code
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated Succeessfully!"},201)
        else:
            return make_response({"message":"Nothing To Update!"},202)
        
    def user_delete_model(self, id): 
        # Query execution code
        self.cur.execute(f"DELETE FROM users where id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Deleted Succeessfully!"},200)
        else:
            return make_response({"message":"Nothing To Delete!"},202)
    
    def user_patch_model(self, data, id): 
        # #Update users set col=val, col=val where id=(id)
        qry = "UPDATE users SET "
        #print(data)
        for key in data:
            qry += f"{key}='{data[key]}',"
        
        qry = qry[:-1] + f" WHERE id={id}"
        
        self.cur.execute(qry)
        
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated Succeessfully!"},201)
        else:
            return make_response({"message":"Nothing To Update!"},202)
        
    def user_pagination_model(self,limit,page):
        limit=int(limit)
        page=int(page)
        start = (page*limit)-limit 
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            resp= make_response({"payload":result, "page_no":page, "limit":limit},200)
            return resp
        else: 
            return make_response({"message":"No Data Found !!"},204)
    
    def user_upload_avatar_model(self, uid, filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' WHERE id={uid}")
        if self.cur.rowcount>0:
            return make_response({"message":"File uploaded Succeessfully!"},201)
        else:
            return make_response({"message":"Nothing To Upload!"},202)
    
    def user_login_model(self,data):
        self.cur.execute(f"SELECT id, name, email, phone, avatar, role_id FROM users WHERE email='{data['email']}' and password = '{data['password']}'")
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload":userdata,
            "exp":exp_epoch_time
        }
        token = jwt.encode(payload,"saumya", algorithm="HS256")
        return make_response({"token":token}, 200) 