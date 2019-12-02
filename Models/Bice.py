from DAO import *

class Bice:
    def GetAllCountries():
        countries={"Countries":DataAccess.GetAllCountries()}
        return countries
    def AllStatesOnCountry(country_id):
        states_for_country={"States":DataAccess.GetStatesBasedOnCountry(country_id)}
        return states_for_country
    def AllCitiesOnState(state_id):
        cities_for_state={"Cities":DataAccess.GetCitiesBasedOnStates(state_id)}
        return cities_for_state
    def add_bice(BiceName,door_no,user_id,country_id,state_id,city_id,pincode,BiceId):
        popupMessage = {"PopupMessage": DataAccess.add_bice_details(BiceName,door_no,user_id,country_id,state_id,city_id,pincode,BiceId)}
        return popupMessage
    def bice_list(bice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        bice=DataAccess.bice_list(bice_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
        return bice
    def BiceDetails(BiceId):
        bice={"BiceDetail":DataAccess.BiceDetails(BiceId)}
        return bice
    