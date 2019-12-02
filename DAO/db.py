import psycopg2 as db
from .config import *
import pandas as pd
import json
import numpy as np
from flask import jsonify

class DataAccess:
    def Login(email,passw,device_model,android_version,app_version,imei):
        con=None
        tr =[]
        try:            
            con = db.connect(conn_str)
            cur = con.cursor()
            cur.callproc('users.user_authenticate',(email,passw,device_model,android_version,app_version,imei))
            #cur.execute("SELECT u.user_id,u.user_name,u.user_role_id FROM users.tbl_users AS u LEFT JOIN users.tbl_user_details AS ud ON ud.user_id=u.user_id where ud.email='"+email+"' AND u.password='"+passw+"';")
            for row in cur:
                tr.append(row)
            cur.close()  
            con.close()          
        except (Exception,db.DatabaseError) as e:
           print(e)
        #finally:
            #if con is not None:
        return tr

    def GetAllCountries():
        countries = []
        con = db.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM regions.tbl_countries")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            countries.append(h)
        cur2.close()
        con.close()
        return countries

    def GetStatesBasedOnCountry(country_id):
        states = []
        con = db.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM regions.tbl_states WHERE country_id="+country_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            states.append(h)
        cur2.close()
        con.close()
        return states

    def GetCitiesBasedOnStates(state_id):
        cities = []
        con = db.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM regions.tbl_cities WHERE state_id="+state_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            cities.append(h)
        cur2.close()
        con.close()
        return cities
    
    def add_bice_details(BiceName,door_no,user_id,country_id,state_id,city_id,pincode,BiceId):
        con = db.connect(conn_str)
        cur = con.cursor()
        cur.callproc('masters.add_edit_bice',(BiceName,door_no,country_id,state_id,city_id,pincode,BiceId,user_id))
        print(BiceName,door_no,user_id,country_id,state_id,city_id,pincode,BiceId)
        for row in cur:
            pop=row[1]
        con.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg

    def bice_list(bice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        Bice = {}
        d = []
        con = db.connect(conn_str)
        cur = con.cursor()
        cur.callproc('masters.fn_get_bice_list',(bice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[3]
            fil=row[4]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2]}
            d.append(h)
        Bice = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return Bice

    def GetMasterDate():
        Bice = []
        con = db.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT bice_id,bice_name  FROM masters.tbl_bices WHERE is_active=TRUE")
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            Bice.append(h)
        
        Bank=[]
        cur2.execute("SELECT bank_id,bank_name  FROM masters.tbl_banks")
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            Bank.append(h)
        
        Country=[]
        cur2.execute("SELECT country_id,country_name FROM   regions.tbl_countries ;")
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            Country.append(h)
        
        State=[]
        cur2.execute("SELECT state_id,state_name,country_id FROM   regions.tbl_states ;")
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2]}
            State.append(h)
        
        City=[]
        cur2.execute('''SELECT 
                                    c.city_id,
                                    c.city_name,
                                    c.state_id,
                                    s.country_id
                            FROM regions.tbl_cities c
                            LEFT JOIN	regions.tbl_states s on s.state_id=c.state_id;''')
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3]}
            City.append(h)
        
        cur2.close()
        con.close()
        return {"Bice": Bice, "Banks":Bank, "Country":Country,"State":State,"City":City}
    def BiceDetails(BiceId):
        con = db.connect(conn_str)
        cur = con.cursor()        
        cur.execute('SELECT * FROM masters.tbl_bices WHERE bice_id='+BiceId)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7]}
        cur.close()
        con.close()
        return h   
    def RegisterCandidate(BiceId,Salutation,FirstName,MiddleName,LastName,CountryId,StateId,CityID,DoorNoStreet,Pincode,DOB,Mobile,MaximumEducation,EduOthers,ID_Proof,ID_Number,IdOthers,BankId,BankAccountNumber,UserId,CandidateImageName,IdImage,BankImage,HasBank):
        success=''
        description=''
        try:
            con = db.connect(conn_str)
            cur = con.cursor()
            cur.callproc('candidates.fn_register_candidate',(BiceId,Salutation,FirstName,MiddleName,LastName,CountryId,StateId,CityID,DoorNoStreet,Pincode,DOB,Mobile,MaximumEducation,EduOthers,ID_Proof,ID_Number,IdOthers,BankId,BankAccountNumber,UserId,CandidateImageName,IdImage,BankImage,HasBank))
            for row in cur:
                pop=row[0]
            con.commit()
            cur.close()
            con.close()
            if pop > 0:
                success=True
                description='Candidate Registered Successfully.'
            else:    
                success=False
                description='Error occurred while registration.'
        except Exception as e:
            success=False
            description='Error ' + str(e)
        
        return {'Success':success,'Description':description}
    def GetCandidateList(BiceId,UserId,CandidateName):
        res=[]
        con = db.connect(conn_str)
        cur = con.cursor()        
        cur.callproc('candidates.fn_get_candidate_list',(BiceId,UserId,CandidateName,'',''))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[16]+"":row[16]}
            res.append(h)
        cur.close()
        con.close()
        return res
    def GetAllBice():
        res=[]
        con = db.connect(conn_str)
        cur = con.cursor()
        cur.execute('SELECT * FROM masters.tbl_bices WHERE is_active=TRUE')
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            res.append(h)
        cur.close()
        con.close()
        return res
    
    def DownloadReport(BiceId,FromDate,ToDate):
        columns=[]
        response={}
        con = db.connect(conn_str)
        cur = con.cursor()
        cur.callproc('candidates.fn_get_candidate_list',(BiceId,0,'',FromDate,ToDate))
        columns = [column[0].title() for column in cur.description]
        for col in columns:
            col.replace('_',' ')
        data=cur.fetchall()        
        col=['Candidate_Id', 'Salutation', 'First_Name', 'Middle_Name', 'Last_Name', 'Bice_Name', 'Door_No_Street', 'City_Name', 'State_Name', 'Country_Name', 'Pincode', 'Dob', 'Mobile_Number', 'Max_Edu', 'Edu_Others', 'Id_Proof', 'Id_Number', 'Id_Others', 'Has_Bank', 'Bank_Name', 'Bank_Acc_Number', 'Created_By', 'Created_On', 'Bank_Image', 'Id_Proof_Image', 'Candidate_Image']
        #print(col)
        df=pd.DataFrame(data,columns=columns)
        df=df[col]
        #print(df)
        cur.close()
        con.close()
        response
        return df
