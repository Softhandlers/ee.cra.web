from DAO import *
import config as WebConfig 
import xlsxwriter
import json

class Report:
    def DownloadReport(BiceId,FromDate,ToDate,path):
        response=DataAccess.DownloadReport(BiceId,FromDate,ToDate)
        print(path)
        FileName=Report.CeateExcel(response,path)
        return FileName
    def CeateExcel(data,path):
        filename=''
        col=['Candidate_Id', 'Salutation', 'First_Name', 'Middle_Name', 'Last_Name', 'Bice_Name', 'Door_No_Street', 'City_Name', 'State_Name', 'Country_Name', 'Pincode', 'Dob', 'Mobile_Number', 'Max_Edu', 'Edu_Others', 'Id_Proof', 'Id_Number', 'Id_Others', 'Has_Bank', 'Bank_Name', 'Bank_Acc_Number', 'Created_By', 'Created_On', 'Bank_Image', 'Id_Proof_Image', 'Candidate_Image']
        ImagePath=WebConfig.FilePath
        try:
            workbook = xlsxwriter.Workbook(path)

            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'align': 'top',
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})

            write_format = workbook.add_format({
                'border': 1,
                'align': 'top',
                'valign': 'top'})

            url_format = workbook.add_format({
                'border': 1,
                'align': 'top',
                'valign': 'top',
                'font_color': 'blue',
                'underline': 1})
            worksheet = workbook.add_worksheet('Candidate Report')
            for i in range(len(col)):
                worksheet.write(0,i ,col[i], header_format)   
            for j in range(len(data)) : 
                for k in range(len(col)-3):
                    worksheet.write(j+1,k ,data.iloc[j,k],write_format)                  
                for l in range(k+1,len(col)):
                    if data.iloc[j,l]==None or data.iloc[j,l]=='':
                        worksheet.write(j+1,l ,'NA',write_format)
                    else:
                        worksheet.write_url(j+1,l,ImagePath+data.iloc[j,l], url_format, string='Image', tip='Click to open image')
            
            
            workbook.close()
        except Exception as e:
            #filename='Error creating excel '+ str(e)
            print(str(e))
            
        return filename

