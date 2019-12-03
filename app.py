from flask import Flask,render_template,request,redirect,url_for,session,g,jsonify,send_file
from flask_restful import Resource
from flask_restful import Api
import os
from flask import jsonify
import json
from datetime import datetime
import pandas as pd
import config as WebConfig
from DAO import config
from DAO import DataAccess
from Models import Bice
from Models import Master
from Models import Report
import xlsxwriter

app = Flask(__name__)

api = Api(app)

app.config["SESSION_PERMANENT"] = True
app.secret_key=WebConfig.secret_key
#app.config['SQLALCHEMY_DATABASE_URI']=config.ConnectionString

@app.route("/")
def index():
    if g.user:        
        return render_template("home.html",values=g.User_detail_with_ids,html="")
    else:
        return render_template("login.html",error=config.displaymsg)

@app.before_request
def before_request():     
    g.user = None
    g.user_id = None
    g.user_role_id = None
    #g.web_user_id = None
    g.User_detail_with_ids = []
    g.session_data = None
    g.bice_id = None
    if 'user_name' in session.keys():
        g.user = session['user_name']
        g.user_id = session['user_id']
        g.user_role_id = session['user_role_id']
        # print(g.user,g.user_id,g.user_role)
        g.User_detail_with_ids.append(g.user)
        g.User_detail_with_ids.append(g.user_id)
        g.User_detail_with_ids.append(g.user_role_id)
        g.User_detail_with_ids.append(WebConfig.WebUrl)
    if 'bice_id' in session.keys():
        g.bice_id = session['bice_id']
    '''
    if 'web_user_role_id' in session.keys():
        g.user_role_id = session['web_user_role_id']
    if 'web_user_id' in session.keys():
        g.web_user_id = session['web_user_id']
    '''

@app.route("/home")
def home():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="")
    else:        
        return redirect(url_for('index'))
        
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        tr = []
        email = request.form['username']
        password = request.form['userpassword']
        print(email,password)
        device_model=''
        android_version=''
        app_version=''
        imei=''
        if 'device_model' in request.form:
            device_model=request.form['device_model']
        if 'android_version' in request.form:
            android_version=request.form['android_version']
        if 'app_version' in request.form:
            app_version=request.form['app_version']
        if 'imei' in request.form:
            imei=request.form['imei']
        
        tr = DataAccess.Login(email,password,device_model,android_version,app_version,imei)
        #print(DataAccess.Login(email,password))
        if tr != []:
            session['user_name'] = tr[0][1]            
            session['user_id'] = tr[0][0]
            session['user_role_id'] = tr[0][2]            
            config.displaymsg=""
            return redirect(url_for('home'))
            #assign_sessions()
            
        else:
            config.displaymsg="wrong"
            return redirect(url_for('index'))

@app.route('/log_out',methods=['GET', 'POST'])
def report_log_out():
    if g.user:
        session.pop('user_name', None)
        session.pop('user_id', None)
        return redirect('/')
        #return render_template("login.html",error=config.displaymsg)
    else:
        return render_template("login.html",error="Already logged out")

@app.route("/EraseDisplayMsg")
def EraseDisplayMsg():
    config.displaymsg=""
    return redirect(url_for('index'))
    
@app.route("/bice_list_page")
def bice_list_page():
    if g.user:
        return render_template("Bice/bice-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/bice")
def bice():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="bice_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/bice_add_edit")
def bice_add_edit():
    if g.user:
        return render_template("Bice/bice-add-edit.html",bice_id=g.bice_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_bice_add_edit_to_home", methods=['GET','POST'])
def assign_bice_add_edit_to_home():
    session['bice_id']=request.form['hdn_bice_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="bice_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_bice")
def after_popup_center():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="bice")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/report_page")
def report_page():
    if g.user:
        return render_template("Report/report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/report")
def report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetAllBice(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response={'Bice':DataAccess.GetAllBice()}
            return response
class get_all_countries(Resource):
    @staticmethod
    def get():
        if request.method== 'GET':
            return Bice.GetAllCountries()
         
class get_all_states_based_on_country(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            country_id=request.form['country_id']
            return Bice.AllStatesOnCountry(country_id)

class get_all_cities_based_on_state(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            state_id=request.form['state_id']
            return Bice.AllCitiesOnState(state_id)

class add_bice_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            bice_name=request.form['BiceName']
            door_no=request.form['DoorNo']
            user_id=g.user_id
            country_id=request.form['Country']
            state_id=request.form['State']
            city_id=request.form['City']
            pincode=request.form['Pincode']
            print(pincode)
            BiceId=request.form['BiceId']
            print(bice_name,door_no,user_id)
            return Bice.add_bice(bice_name,door_no,user_id,country_id,state_id,city_id,pincode,BiceId)

class get_master_data(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            Bice=Master.GetMasterDate()
            return Bice

class bice_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            bice_id = request.form['bice_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Bice.bice_list(bice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class get_bice_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            print(jsonify(Bice.BiceDetails(g.bice_id)))
            return jsonify(Bice.BiceDetails(g.bice_id))


class RegisterCandidate(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            response=''
            try:
                details={}                
                BiceId=request.form['bice_id']
                Salutation=request.form['salutation']
                FirstName=request.form['first_name']
                MiddleName=request.form['middle_name']
                LastName=request.form['last_name']
                CountryId=request.form['country_id']
                StateId=request.form['state_id']
                CityID=request.form['city_id']
                DoorNoStreet=request.form['door_no_street']
                Pincode=request.form['pincode']
                DOB=request.form['dob']
                Mobile=request.form['mobile_number']
                MaximumEducation=request.form['maximum_education']
                EduOthers=request.form['edu_others']
                ID_Proof=request.form['id_proof']
                ID_Number=request.form['id_number']
                IdOthers=request.form['id_others']
                BankId=request.form['bank_id']
                BankAccountNumber=request.form['bank_account_number']
                UserId=request.form['user_id']
                CandidateImageName=request.form['candidate_image']
                IdImage=request.form['id_image']
                BankImage=request.form['bank_image']
                HasBank=request.form['has_bank']
                
                response=Master.RegisterCandidate(BiceId,Salutation,FirstName,MiddleName,LastName,CountryId,StateId,CityID,DoorNoStreet,Pincode,DOB,Mobile,MaximumEducation,EduOthers,ID_Proof,ID_Number,IdOthers,BankId,BankAccountNumber,UserId,CandidateImageName,IdImage,BankImage,HasBank)

            except Exception as e:
                response={'Success':False,'Description':'Error '+str(e)}
            return response

class upload_images(Resource):
    upload_path = WebConfig.FileUploadPath
    @staticmethod
    def post():
        if request.method=='POST':
            response=''
            count=request.form['count']
            try:
                files=request.files.getlist('files')
            except Exception as e:
                response={'Success':False,'Description':'Error reading files '+ str(e)}
                return jsonify(response)
            print(count,len(files))
            if int(count)==len(files):
                for file in files:
                    try:
                        name = file.filename
                        file.save(upload_images.upload_path + name)
                    except Exception as e:
                        res = {'Success': False, 'Description': "uploaded failed " + str(e)}
                        return jsonify(res)
                response={'Success':True,'Description':'Files uploaded successfully.'}
            else:
                response={'Success':False,'Description':'Error uploading files '}
                return jsonify(response)
            return jsonify(response)

class AppLogin(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            tr = []
            res=''
            email = request.form['username']
            password = request.form['userpassword']
            print(email,password)
            device_model=''
            android_version=''
            app_version=''
            imei=''
            if 'device_model' in request.form:
                device_model=request.form['device_model']
            if 'android_version' in request.form:
                android_version=request.form['android_version']
            if 'app_version' in request.form:
                app_version=request.form['app_version']
            if 'imei' in request.form:
                imei=request.form['imei']
            
            tr = DataAccess.Login(email,password,device_model,android_version,app_version,imei)
            #print(DataAccess.Login(email,password))
            if tr != []:
                res={'Success':True,'Description':'Successfully logged in.' ,'user_name':tr[0][1],'user_id':tr[0][0],'user_role_id':tr[0][2]}
            else:
                res={'Success':False,'Description':'Invalid username or password'}
            return jsonify(res)

class GetCandidateList(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            response=''
            BiceId=request.form['bice_id']
            UserId=request.form['user_id']
            CandidateName=request.form['candidate_name']
            res=Master.GetCandidateList(BiceId,UserId,CandidateName)
            if res==[]:
                response={'Success':False,'Description':'No candidates found'}
            else:
                response={'Success':True,'Description':'Candidate List','candidates':res}
            return jsonify(response)


@app.route("/download_report",methods=['GET', 'POST'])
def download_report():
               
    FromDate=request.form['FromDate']
    ToDate=request.form['ToDate']
    BiceId=int(request.form['ddlBice']) 
    print(BiceId,FromDate,ToDate)
    df={}
    
    #for i in os.listdir(DownloadReport.DownloadPath)[1:]:
    #    os.remove( DownloadReport.DownloadPath + i)
    FileName = DownloadReport.report_name
    #df.to_excel('{}{}.xlsx'.format(DownloadReport.DownloadPath,FileName),encoding='utf-8',index = None)
    path = '{}{}.xlsx'.format(DownloadReport.DownloadPath,FileName)
    df=Report.DownloadReport(BiceId,FromDate,ToDate,path)
    return send_file(path, as_attachment=True)
    return 'Hi'


class DownloadReport(Resource):
    DownloadPath=WebConfig.ReportDownloadPath
    report_name = "Candidate_Report_"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            BiceId=int(request.form['BiceId'])            
            FromDate=request.form['FromDate']
            ToDate=request.form['ToDate']
            print(BiceId,FromDate,ToDate)
            df=[]
            df=DataAccess.DownloadReport(BiceId,FromDate,ToDate)
            #for i in os.listdir(DownloadReport.DownloadPath)[1:]:
            #    os.remove( DownloadReport.DownloadPath + i)
            FileName = DownloadReport.report_name
            df.to_excel('{}{}.xlsx'.format(DownloadReport.DownloadPath,FileName),encoding='utf-8',index = None)
            path = '{}{}.xlsx'.format(DownloadReport.DownloadPath,FileName)
            send_file(path, as_attachment=True)
            return {'Path':path,'FileName':FileName}
            

api.add_resource(bice_list, '/bice_list')

api.add_resource(get_all_countries, '/GetAllCountries')
api.add_resource(get_all_states_based_on_country, '/AllStatesBasedOnCountry')
api.add_resource(get_all_cities_based_on_state, '/AllCitiesBasedOnState')

api.add_resource(add_bice_details, '/add_bice_details')
api.add_resource(get_bice_details, '/GetBiceDetails')
api.add_resource(GetAllBice,'/GetAllBice')
api.add_resource(DownloadReport,'/DownloadReport')
# APP API's
api.add_resource(AppLogin,'/AppLogin')
api.add_resource(get_master_data,'/get_master_data')
api.add_resource(upload_images,'/UploadImages')
api.add_resource(RegisterCandidate,'/RegisterCandidate')
api.add_resource(GetCandidateList,'/GetCandidateList')

if __name__ == '__main__':    
    app.run(debug=True)
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    #app.run(host='127.0.0.1',port='4000',debug=True)
    
