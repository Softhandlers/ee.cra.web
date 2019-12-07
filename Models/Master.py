from DAO import DataAccess

class Master:
    def GetMasterDate():
        #Bice={"Bice": DataAccess.GetBiceDetails()}
        return DataAccess.GetMasterDate()
    def GetBankDetails():
        BankDetails={"BankDetails": DataAccess.GetBankDetails()}
        return BankDetails
    def RegisterCandidate(BiceId,Salutation,FirstName,MiddleName,LastName,CountryId,StateId,CityID,DoorNoStreet,Pincode,DOB,Mobile,MaximumEducation,EduOthers,ID_Proof,ID_Number,IdOthers,BankId,BankAccountNumber,UserId,CandidateImageName,IdImage,BankImage,HasBank,FatherName,MotherName,Religion,Caste):
        response=DataAccess.RegisterCandidate(BiceId,Salutation,FirstName,MiddleName,LastName,CountryId,StateId,CityID,DoorNoStreet,Pincode,DOB,Mobile,MaximumEducation,EduOthers,ID_Proof,ID_Number,IdOthers,BankId,BankAccountNumber,UserId,CandidateImageName,IdImage,BankImage,HasBank,FatherName,MotherName,Religion,Caste)
        return response
    def GetCandidateList(BiceId,UserId,CandidateName):
        response=DataAccess.GetCandidateList(BiceId,UserId,CandidateName)
        return response
