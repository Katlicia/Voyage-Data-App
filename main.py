import tkinter
import sqlite3
import tkinter.messagebox
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from ship import Ship
from harbor import Harbor
from crew import Crew
from captain import Captain
from voyage import Voyage


shipTypeList = ["Passenger", "Oil", "Container"]

window = tkinter.Tk()

def dateValidation(date, format = '%Y-%m-%d'):
    try:
        datetime.strptime(date, format) 
        return True
    except ValueError:
        return False


def addShipData():
    noError = True
    shipId = ship_id_entry.get()
    shipName = ship_name_entry.get()
    shipWeight = int(ship_weight_spinbox.get())
    shipConstructionYear = ship_construction_year_entry.get()
    shipType = ship_type_combobox.get()
    shipPassengerCapacity = None
    shipOilCapacity = None
    shipContainerCapacity = None
    shipMaxWeight = None

    # Checks For Invalid Entries
    if shipId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Ship ID")
        noError = False

    elif shipName == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Ship Name")
        noError = False

    elif shipWeight < 10000:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Ship Weight")
        noError = False

    elif shipType not in shipTypeList:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Ship Type")
        noError = False

    elif not dateValidation(shipConstructionYear, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Construction Date")
        noError = False

    elif shipType == shipTypeList[0]:
        shipPassengerCapacity = int(ship_pscapacity_spinbox.get())
        if shipPassengerCapacity <= 0:
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid Passenger Capacity")
            noError = False

    elif shipType == shipTypeList[1]:
        shipOilCapacity = int(ship_oilcapacity_spinbox.get())
        if shipOilCapacity <= 0:
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid Oil Capacity")
            noError = False

    elif shipType == shipTypeList[2]:
        shipContainerCapacity = int(ship_crcapacity_spinbox.get())
        shipMaxWeight = int(ship_maxweight_spinbox.get())                                                                                                               
        if shipContainerCapacity <= 0:
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid Container Capacity")
            noError = False
        elif shipMaxWeight <= 0:
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid Max Weight")
            noError = False
    
    # If No Invalid Entries or Errors Adds Ship to Database
    if noError == True:
        shipObj = Ship(shipId, shipName, shipType, shipWeight, shipConstructionYear, shipPassengerCapacity, shipMaxWeight, shipContainerCapacity, shipOilCapacity)
        conn = sqlite3.connect("data.db")
        table_create_query = ''' CREATE TABLE IF NOT EXISTS SHIP_DATA
        (SHIP_ID TEXT NOT NULL UNIQUE, SHIP_NAME TEXT NOT NULL, SHIP_TYPE TEXT NOT NULL, SHIP_WEIGHT INT NOT NULL, SHIP_CONSTRUCTION_YEAR DATE NOT NULL,
        SHIP_PASSENGER_CAPACITY INT, SHIP_MAX_WEIGHT INT, SHIP_CONTAINER_CAPACITY INT, SHIP_OIL_CAPACITY INT, SHIP_ON_VOYAGE BIT DEFAULT 0, PRIMARY KEY (SHIP_ID)) '''
        conn.execute(table_create_query)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM SHIP_DATA WHERE SHIP_ID = '{shipId}'")
        row = cursor.fetchone()
        if row != None:
            # If ID Exist in Database Shows Warning
            tkinter.messagebox.showwarning(title = "Error", message = "SHIP ID NOT UNIQUE")
            conn.close()
            return
        conn.execute(table_create_query)

        data_insert_query = '''INSERT INTO SHIP_DATA (SHIP_ID, SHIP_NAME, SHIP_TYPE, SHIP_WEIGHT, SHIP_CONSTRUCTION_YEAR, SHIP_PASSENGER_CAPACITY,
        SHIP_MAX_WEIGHT, SHIP_CONTAINER_CAPACITY, SHIP_OIL_CAPACITY) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        data_insert_tuple = (shipObj.getShipId(), shipObj.getShipName(), shipObj.getShipType(), shipObj.getShipWeight(),shipObj.getShipConstructionYear(), 
        shipObj.getPassengerCapacity(), shipObj.getMaxWeight(), shipObj.getContainerCapacity(), shipObj.getOilCapacity())


        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo(title="Success", message=f"Ship {shipId} added to database successfully.")


def deleteShipData():
    shipId = ship_id_entry.get()

    # Checks Invalid ID Entry
    if shipId == "":
        tkinter.messagebox.showwarning(title="Error", message="Invalid ID")
        return  
    
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        # Checks If ID Exist
        cursor.execute(f"SELECT * FROM SHIP_DATA WHERE SHIP_ID = '{shipId}'")
        row = cursor.fetchone()
        if row is None:
            # If Doesn't Exist Show Error
            tkinter.messagebox.showwarning(title="Error", message="ID Not Found")
            conn.close()
            return

        # If ID Exist Deletes It
        table_delete_query = f"DELETE FROM SHIP_DATA WHERE SHIP_ID = '{shipId}'"
        conn.execute(table_delete_query)
        conn.commit()
        conn.close()
        
        # Informs The User About The Deleted Data
        tkinter.messagebox.showinfo(title="Success", message=f"Ship {shipId} deleted successfully.")
    except sqlite3.Error as e:
        tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))


def updateShipData():
    noError = True
    shipId = ship_id_entry.get()
    shipName = ship_name_entry.get()
    shipWeight = int(ship_weight_spinbox.get())
    shipConstructionYear = ship_construction_year_entry.get()
    shipType = ship_type_combobox.get()
    shipPassengerCapacity = None
    shipOilCapacity = None
    shipContainerCapacity = None
    shipMaxWeight = None

    if shipId == "":
        tkinter.messagebox.showwarning(title="Error", message="Invalid Ship ID")
        noError = False
    elif shipName == "":
        tkinter.messagebox.showwarning(title="Error", message="Invalid Ship Name")
        noError = False
    elif shipWeight < 10000:
        tkinter.messagebox.showwarning(title="Error", message="Invalid Ship Weight")
        noError = False
    elif shipType not in shipTypeList:
        tkinter.messagebox.showwarning(title="Error", message="Invalid Ship Type")
        noError = False
    elif not dateValidation(shipConstructionYear, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title="Error", message="Invalid Construction Date")
        noError = False
    elif shipType == shipTypeList[0]:
        shipPassengerCapacity = int(ship_pscapacity_spinbox.get())
        if shipPassengerCapacity <= 0:
            tkinter.messagebox.showwarning(title="Error", message="Invalid Passenger Capacity")
            noError = False
    elif shipType == shipTypeList[1]:
        shipOilCapacity = int(ship_oilcapacity_spinbox.get())
        if shipOilCapacity <= 0:
            tkinter.messagebox.showwarning(title="Error", message="Invalid Oil Capacity")
            noError = False
    elif shipType == shipTypeList[2]:
        shipContainerCapacity = int(ship_crcapacity_spinbox.get())
        shipMaxWeight = int(ship_maxweight_spinbox.get())
        if shipContainerCapacity <= 0:
            tkinter.messagebox.showwarning(title="Error", message="Invalid Container Capacity")
            noError = False
        elif shipMaxWeight <= 0:
            tkinter.messagebox.showwarning(title="Error", message="Invalid Max Weight")
            noError = False

    if noError:
        try:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            # Checks If ID Exist
            cursor.execute(f"SELECT * FROM SHIP_DATA WHERE SHIP_ID = '{shipId}'")
            row = cursor.fetchone()
            if row is None:
                # If Doesn't Exist Show Error
                tkinter.messagebox.showwarning(title="Error", message="ID Not Found")
            else:
                # If ID Exist Updates It
                cursor.execute(f"UPDATE SHIP_DATA SET SHIP_NAME = ?, SHIP_WEIGHT = ?, SHIP_CONSTRUCTION_YEAR = ?, SHIP_TYPE = ?, "
                               "SHIP_PASSENGER_CAPACITY = ?, SHIP_OIL_CAPACITY = ?, SHIP_CONTAINER_CAPACITY = ?, "
                               "SHIP_MAX_WEIGHT = ? WHERE SHIP_ID = ?",
                               (shipName, shipWeight, shipConstructionYear, shipType, shipPassengerCapacity,
                                shipOilCapacity, shipContainerCapacity, shipMaxWeight, shipId))
                conn.commit()
                # Informs The User About The Updated Data
                tkinter.messagebox.showinfo(title="Success", message=f"Ship {shipId} updated successfully.")
        except sqlite3.Error as e:
            tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))
        finally:
            conn.close()


def addHarborData():
    noError = True
    harborName = harbor_name_entry.get()
    harborCountry = harbor_country_entry.get()
    harborPopulation = harbor_population_entry.get()
    harborPassportRequired = harbor_passport_var.get()
    harborDockingFee = harbor_fee_entry.get()

    if harborName == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Harbor Name")
        noError = False

    elif harborCountry == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Country Name")
        noError = False

    try:
        harborPopulation = int(harbor_population_entry.get())
        if harborPopulation <= 0:
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid Population")
            noError = False
    except:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Population")
        noError = False

    try:
        harborDockingFee = int(harbor_fee_entry.get())
        if harborDockingFee <= 0:
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid Docking Fee")
            noError = False
    except:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Docking Fee")
        noError = False

    if noError == True:
        harborObj = Harbor(harborName, harborCountry, harborPopulation, harborPassportRequired, harborDockingFee)
        conn = sqlite3.connect("data.db")
        table_create_query = ''' CREATE TABLE IF NOT EXISTS HARBOR_DATA
        (HARBOR_NAME TEXT NOT NULL, HARBOR_COUNTRY TEXT NOT NULL, HARBOR_POPULATION INT NOT NULL, HARBOR_PASSPORT_REQUIRED BIT NOT NULL,
        HARBOR_DOCKING_FEE INT NOT NULL, PRIMARY KEY (HARBOR_NAME, HARBOR_COUNTRY))'''
        conn.execute(table_create_query)


        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM HARBOR_DATA WHERE HARBOR_NAME = '{harborName}' AND HARBOR_COUNTRY = '{harborCountry}'")
        row = cursor.fetchone()
        if row != None:
            # If Harbor Exist In Database Show Error
            tkinter.messagebox.showwarning(title="Error", message="Harbor Already in Database")
            conn.close()
            return

        conn.execute(table_create_query)

        data_insert_query = '''INSERT INTO HARBOR_DATA (HARBOR_NAME, HARBOR_COUNTRY, HARBOR_POPULATION, HARBOR_PASSPORT_REQUIRED,
        HARBOR_DOCKING_FEE) VALUES (?, ?, ?, ?, ?)'''

        data_insert_tuple = (harborObj.getHarborName(), harborObj.getHarborCountry() , harborObj.getHarborPopulation(), harborObj.getPassportRequire(), 
        harborObj.getDockingFee())

        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo(title = "Success", message = f"Harbor {harborName} added to database successfully.")


def deleteHarborData():
    harborName = harbor_name_entry.get()
    harborCountry = harbor_country_entry.get()

    if harborName == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Name")
    elif harborCountry == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Country")

    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        # Checks If Harbor Exist
        cursor.execute(f"SELECT * FROM HARBOR_DATA WHERE HARBOR_NAME = '{harborName}' AND HARBOR_COUNTRY = '{harborCountry}' ")
        row = cursor.fetchone()
        if row is None:
            # If Doesn't Exist Show Error
            tkinter.messagebox.showwarning(title="Error", message="Harbor Not Found")
            conn.close()
            return

        # If ID Exist Deletes It
        table_delete_query = f"DELETE FROM HARBOR_DATA WHERE HARBOR_NAME = '{harborName}' AND HARBOR_COUNTRY = '{harborCountry}'"
        conn.execute(table_delete_query)
        conn.commit()
        conn.close()
        
        # Informs The User About The Deleted Data
        tkinter.messagebox.showinfo(title="Success", message=f"Harbor {harborName} in {harborCountry} deleted successfully.")
    except sqlite3.Error as e:
        tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))


def updateHarborData():
    noError = True
    harborName = harbor_name_entry.get()
    harborCountry = harbor_country_entry.get()
    harborPopulation = harbor_population_entry.get()
    harborPassportRequired = harbor_passport_var.get()
    harborDockingFee = harbor_fee_entry.get()

    if harborName == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Harbor Name")
        noError = False

    elif harborCountry == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Country Name")
        noError = False

    try:
        harborPopulation = int(harbor_population_entry.get())
        if harborPopulation <= 0:
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid Population")
            noError = False
    except:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Population")
        noError = False

    try:
        harborDockingFee = int(harbor_fee_entry.get())
        if harborDockingFee <= 0:
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid Docking Fee")
            noError = False
    except:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Docking Fee")
        noError = False


    if noError:
        try:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            # Checks If Harbor Exist
            cursor.execute(f"SELECT * FROM HARBOR_DATA WHERE HARBOR_NAME = '{harborName}' AND HARBOR_COUNTRY = '{harborCountry}' ")
            row = cursor.fetchone()
            if row is None:
                # If Doesn't Exist Show Error
                tkinter.messagebox.showwarning(title="Error", message="Harbor Not Found")
            else:
                # If Name and Country Exist Updates It
                cursor.execute(f"UPDATE HARBOR_DATA SET HARBOR_POPULATION = ?, HARBOR_PASSPORT_REQUIRED = ?, "
                               "HARBOR_DOCKING_FEE = ?"
                               "WHERE HARBOR_NAME = ? AND HARBOR_COUNTRY = ?",
                               (harborPopulation, harborPassportRequired, harborDockingFee, harborName, harborCountry))
                conn.commit()
                # Informs The User About The Updated Data
                tkinter.messagebox.showinfo(title="Success", message=f"Harbor {harborName} updated successfully.")
        except sqlite3.Error as e:
            tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))
        finally:
            conn.close()


def addCrewData():
    noError = True
    crewId = crew_id_entry.get()
    crewName = crew_name_entry.get()
    crewLastName = crew_lastname_entry.get()
    crewAddress = crew_address_entry.get()
    crewNationality = crew_nationality_entry.get()
    crewBirthday = crew_birthday_entry.get()
    crewHireDate = crew_hiredate_entry.get()
    crewIsCaptain = crew_captain_var.get()
    crewCaptainLicense = crew_cptlicense_entry.get()
    crewRole = crew_role_combobox.get()

    if crewId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid ID")
        noError = False

    elif crewName == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Name")
        noError = False

    elif crewLastName == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Last Name")
        noError = False

    elif crewAddress == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Address")
        noError = False

    elif crewNationality == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Nationality")
        noError = False

    elif not dateValidation(crewBirthday, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Birthday")
        noError = False

    elif not dateValidation(crewHireDate, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Hire Date")
        noError = False

    if crewIsCaptain == True:
        if crewCaptainLicense == "":
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid License")
            noError = False
    else:
        if crewRole == "":
            tkinter.messagebox.showwarning(title = "Error", message = "Invalid Role")
            noError = False

    if noError == True and crewIsCaptain == False:
        crewObj = Crew(crewId, crewName, crewLastName, crewAddress, crewNationality, crewBirthday, crewHireDate, crewRole)
        conn = sqlite3.connect("data.db")
        table_create_query = ''' CREATE TABLE IF NOT EXISTS CREW_DATA
        (CREW_ID TEXT NOT NULL UNIQUE, CREW_NAME TEXT NOT NULL, CREW_LAST_NAME TEXT NOT NULL, CREW_ADDRESS TEXT NOT NULL,
        CREW_NATIONALITY TEXT NOT NULL, CREW_BIRTHDAY DATE NOT NULL, CREW_HIRE_DATE DATE NOT NULL, CREW_ROLE TEXT NOT NULL, 
        CREW_ON_VOYAGE BIT DEFAULT 0, PRIMARY KEY (CREW_ID))'''
        conn.execute(table_create_query)
  

        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM CREW_DATA WHERE CREW_ID = '{crewId}'")
        row = cursor.fetchone()
        if row != None:
            # If Crew Member Exist In Database Show Error
            tkinter.messagebox.showwarning(title="Error", message="CREW ID NOT UNIQUE")
            conn.close()
            return

        conn.execute(table_create_query)

        data_insert_query = '''INSERT INTO CREW_DATA (CREW_ID, CREW_NAME, CREW_LAST_NAME, CREW_ADDRESS, CREW_NATIONALITY,
        CREW_BIRTHDAY, CREW_HIRE_DATE, CREW_ROLE) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

        data_insert_tuple = (crewObj.getCrewId(), crewObj.getFirstName(), crewObj.getLastName(), crewObj.getAddress(), crewObj.getNationality(),
        crewObj.getBirthDate(), crewObj.getHireDate(), crewObj.getRole())

        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo(title = "Success", message = f"Crew Member {crewId} added to database successfully.")

    if noError == True and crewIsCaptain == True:
        captainObj = Captain(crewId, crewName, crewLastName, crewAddress, crewNationality, crewBirthday, crewHireDate, crewCaptainLicense)
        conn = sqlite3.connect("data.db")
        table_create_query = ''' CREATE TABLE IF NOT EXISTS CAPTAIN_DATA
        (CAPTAIN_ID TEXT NOT NULL UNIQUE, CAPTAIN_NAME TEXT NOT NULL, CAPTAIN_LAST_NAME TEXT NOT NULL, CAPTAIN_ADDRESS TEXT NOT NULL,
        CAPTAIN_NATIONALITY TEXT NOT NULL, CAPTAIN_BIRTHDAY DATE NOT NULL, CAPTAIN_HIRE_DATE DATE NOT NULL, CAPTAIN_LICENSE TEXT NOT NULL, 
        CAPTAIN_ON_VOYAGE BIT DEFAULT 0, PRIMARY KEY (CAPTAIN_ID))'''
        conn.execute(table_create_query)


        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM CAPTAIN_DATA WHERE CAPTAIN_ID = '{crewId}'")
        row = cursor.fetchone()
        if row != None:
            # If Captain Exist In Database Show Error
            tkinter.messagebox.showwarning(title="Error", message="CAPTAIN ID NOT UNIQUE")
            conn.close()
            return

        conn.execute(table_create_query)

        data_insert_query = '''INSERT INTO CAPTAIN_DATA (CAPTAIN_ID, CAPTAIN_NAME, CAPTAIN_LAST_NAME, CAPTAIN_ADDRESS, CAPTAIN_NATIONALITY,
        CAPTAIN_BIRTHDAY, CAPTAIN_HIRE_DATE, CAPTAIN_LICENSE) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

        data_insert_tuple = (captainObj.getCaptainID(), captainObj.getFirstName(), captainObj.getLastName(), captainObj.getAddress(), captainObj.getNationality(),
        captainObj.getBirthDate(), captainObj.getHireDate(), captainObj.getLicenseType())

        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo(title = "Success", message = f"Captain {crewId} added to database successfully.")


def deleteCrewData():
    crewId = crew_id_entry.get()
    crewIsCaptain = crew_captain_var.get()

    if crewId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid ID")

    if crewIsCaptain == False:
        try:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            # Checks If Crew Member Exist
            cursor.execute(f"SELECT * FROM CREW_DATA WHERE CREW_ID = '{crewId}' ")
            row = cursor.fetchone()
            if row is None:
                # If Doesn't Exist Show Error
                tkinter.messagebox.showwarning(title="Error", message="Crew Member Not Found")
                conn.close()
                return

            # If ID Exist Deletes It
            table_delete_query = f"DELETE FROM CREW_DATA WHERE CREW_ID = '{crewId}'"
            conn.execute(table_delete_query)
            conn.commit()
            conn.close()
            
            # Informs The User About The Deleted Data
            tkinter.messagebox.showinfo(title="Success", message=f"Crew Member {crewId} deleted successfully.")
        except sqlite3.Error as e:
            tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))

    if crewIsCaptain == True:
        try:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            # Checks If Captain Exist
            cursor.execute(f"SELECT * FROM CAPTAIN_DATA WHERE CAPTAIN_ID = '{crewId}' ")
            row = cursor.fetchone()
            if row is None:
                # If Doesn't Exist Show Error
                tkinter.messagebox.showwarning(title="Error", message="Captain Not Found")
                conn.close()
                return

            # If ID Exist Deletes It
            table_delete_query = f"DELETE FROM CAPTAIN_DATA WHERE CAPTAIN_ID = '{crewId}'"
            conn.execute(table_delete_query)
            conn.commit()
            conn.close()
            
            # Informs The User About The Deleted Data
            tkinter.messagebox.showinfo(title="Success", message=f"Captain {crewId} deleted successfully.")
        except sqlite3.Error as e:
            tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))


def updateCrewData():
    noError = True
    crewId = crew_id_entry.get()
    crewName = crew_name_entry.get()
    crewLastName = crew_lastname_entry.get()
    crewAddress = crew_address_entry.get()
    crewNationality = crew_nationality_entry.get()
    crewBirthday = crew_birthday_entry.get()
    crewHireDate = crew_hiredate_entry.get()
    crewIsCaptain = crew_captain_var.get()
    crewCaptainLicense = crew_cptlicense_entry.get()
    crewRole = crew_role_combobox.get()

    if crewId == "":
        tkinter.messagebox.showwarning(title="Error", message="Invalid ID")
        noError = False

    elif crewName == "":
        tkinter.messagebox.showwarning(title="Error", message="Invalid Name")
        noError = False

    elif crewLastName == "":
        tkinter.messagebox.showwarning(title="Error", message="Invalid Last Name")
        noError = False

    elif crewAddress == "":
        tkinter.messagebox.showwarning(title="Error", message="Invalid Address")
        noError = False

    elif crewNationality == "":
        tkinter.messagebox.showwarning(title="Error", message="Invalid Nationality")
        noError = False

    elif not dateValidation(crewBirthday, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title="Error", message="Invalid Birthday")
        noError = False

    elif not dateValidation(crewHireDate, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title="Error", message="Invalid Hire Date")
        noError = False

    if crewIsCaptain:
        if crewCaptainLicense == "":
            tkinter.messagebox.showwarning(title="Error", message="Invalid License")
            noError = False
    else:
        if crewRole == "":
            tkinter.messagebox.showwarning(title="Error", message="Invalid Role")
            noError = False

    if noError:
        try:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()

            if crewIsCaptain:
                # Checks If ID Exist in Captain
                cursor.execute(f"SELECT * FROM CAPTAIN_DATA WHERE CAPTAIN_ID = '{crewId}'")
                row = cursor.fetchone()
                if row is None:
                    # If Doesn't Exist Show Error
                    tkinter.messagebox.showwarning(title="Error", message="Captain Not Found")
                else:
                    # If ID Exist Updates It
                    cursor.execute("UPDATE CAPTAIN_DATA SET CAPTAIN_NAME = ?, CAPTAIN_LAST_NAME = ?, CAPTAIN_ADDRESS = ?, "
                                "CAPTAIN_NATIONALITY = ?, CAPTAIN_BIRTHDAY = ?, CAPTAIN_HIRE_DATE = ?, CAPTAIN_LICENSE = ? "
                                "WHERE CAPTAIN_ID = ?",
                                (crewName, crewLastName, crewAddress, crewNationality, crewBirthday, crewHireDate, crewCaptainLicense, crewId))
                    table_name = "Captain"
            else:
                # Checks If ID Exist in Crew
                cursor.execute(f"SELECT * FROM CREW_DATA WHERE CREW_ID = '{crewId}'")
                row = cursor.fetchone()
                if row is None:
                    # If Doesn't Exist Show Error
                    tkinter.messagebox.showwarning(title="Error", message="Crew Member Not Found")
                else:
                    # If ID Exist Updates It
                    cursor.execute("UPDATE CREW_DATA SET CREW_NAME = ?, CREW_LAST_NAME = ?, CREW_ADDRESS = ?, "
                                "CREW_NATIONALITY = ?, CREW_BIRTHDAY = ?, CREW_HIRE_DATE = ?, CREW_ROLE = ? "
                                "WHERE CREW_ID = ?",
                                (crewName, crewLastName, crewAddress, crewNationality, crewBirthday, crewHireDate, crewRole, crewId))
                    table_name = "Crew Member"

            conn.commit()
            conn.close()

            # Informs The User About The Updated Data
            tkinter.messagebox.showinfo(title="Success", message=f"{table_name} {crewId} updated successfully.")
        except sqlite3.Error as e:
            tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))


def addVoyageData():
    noError = True
    voyageId = voyage_id_entry.get()
    voyageDepartureDate = voyage_departuredate_entry.get()
    voyageReturnDate = voyage_returndate_entry.get()
    voyageDepartureHarbor = voyage_departureharbor_entry.get()

    if voyageId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid ID")
        noError = False

    elif not dateValidation(voyageDepartureDate, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Departure Date")
        noError = False

    elif not dateValidation(voyageReturnDate, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Return Date")
        noError = False

    elif voyageDepartureHarbor == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Departure Harbor")
        noError = False

    if noError == True:
        voyageObj = Voyage(voyageId, voyageDepartureDate, voyageReturnDate, voyageDepartureHarbor)
        conn = sqlite3.connect("data.db")
        table_create_query = ''' CREATE TABLE IF NOT EXISTS VOYAGE_DATA
        (VOYAGE_ID TEXT NOT NULL UNIQUE, VOYAGE_DEPARTURE_DATE DATE NOT NULL, VOYAGE_RETURN_DATE DATE NOT NULL,
        VOYAGE_DEPARTURE_HARBOR TEXT NOT NULL, PRIMARY KEY (VOYAGE_ID)) '''
        conn.execute(table_create_query)


        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM VOYAGE_DATA WHERE VOYAGE_ID = '{voyageId}'")
        row = cursor.fetchone()
        if row != None:
            # If Voyage Exist In Database Show Error
            tkinter.messagebox.showwarning(title="Error", message="VOYAGE ID NOT UNIQUE")
            conn.close()
            return

        conn.execute(table_create_query)

        data_insert_query = '''INSERT INTO VOYAGE_DATA (VOYAGE_ID, VOYAGE_DEPARTURE_DATE, VOYAGE_RETURN_DATE, VOYAGE_DEPARTURE_HARBOR) 
        VALUES (?, ?, ?, ?)'''

        data_insert_tuple = (voyageObj.getVoyageId(), voyageObj.getDepartureDate(), voyageObj.getReturnDate(), voyageObj.getDepartureHarbor())

        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo(title = "Success", message = f"Voyage {voyageId} added to database successfully.")


def deleteVoyageData():
    voyageId = voyage_id_entry.get()

    if voyageId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid ID")

    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        # Checks If Voyage Exist
        cursor.execute(f"SELECT * FROM VOYAGE_DATA WHERE VOYAGE_ID = '{voyageId}' ")
        row = cursor.fetchone()
        if row is None:
            # If Doesn't Exist Show Error
            tkinter.messagebox.showwarning(title="Error", message="Voyage Not Found")
            conn.close()
            return

        # If ID Exist Deletes It
        table_delete_query = f"DELETE FROM VOYAGE_DATA WHERE VOYAGE_ID = '{voyageId}'"
        conn.execute(table_delete_query)
        conn.commit()
        conn.close()
        
        # Informs The User About The Deleted Data
        tkinter.messagebox.showinfo(title="Success", message=f"Voyage {voyageId} deleted successfully.")
    except sqlite3.Error as e:
        tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))


def updateVoyageData():
    noError = True
    voyageId = voyage_id_entry.get()
    voyageDepartureDate = voyage_departuredate_entry.get()
    voyageReturnDate = voyage_returndate_entry.get()
    voyageDepartureHarbor = voyage_departureharbor_entry.get()

    if voyageId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid ID")
        noError = False

    elif not dateValidation(voyageDepartureDate, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Departure Date")
        noError = False

    elif not dateValidation(voyageReturnDate, '%Y-%m-%d'):
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Return Date")
        noError = False

    elif voyageDepartureHarbor == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Departure Harbor")
        noError = False

    if noError:
        try:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            # Checks If Voyage Exist
            cursor.execute(f"SELECT * FROM VOYAGE_DATA WHERE VOYAGE_ID = '{voyageId}' ")
            row = cursor.fetchone()
            if row is None:
                # If Doesn't Exist Show Error
                tkinter.messagebox.showwarning(title="Error", message="Voyage Not Found")
            else:
                # If ID Exist Updates It
                cursor.execute(f"UPDATE VOYAGE_DATA SET VOYAGE_DEPARTURE_DATE = ?, VOYAGE_RETURN_DATE = ?, "
                               "VOYAGE_DEPARTURE_HARBOR = ?"
                               "WHERE VOYAGE_ID = ?",
                               (voyageDepartureDate, voyageReturnDate, voyageDepartureHarbor, voyageId))
                conn.commit()
                # Informs The User About The Updated Data
                tkinter.messagebox.showinfo(title="Success", message=f"Voyage {voyageId} updated successfully.")
        except sqlite3.Error as e:
            tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))
        finally:
            conn.close()


def startCreateVoyage():
    noError = True
    voyageId = cvoyage_id_entry.get()
    shipId = cship_id_entry.get()
    captainNum = int(ccaptain_num_spinbox.get())
    captainId = ccaptain_id_entry.get()
    crewNum = int(ccrew_num_spinbox.get())
    crewId = ccrew_id_entry.get()

    if voyageId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Voyage ID")
        noError = False

    elif shipId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Ship ID")
        noError = False

    elif captainNum < 2:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Captain Number") 
        noError = False

    elif captainId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Captain ID")
        noError = False

    elif crewNum < 1:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Crew Number")
        noError = False

    elif crewId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Crew ID")
        noError = False

    
    if noError:
        noError2 = True
        captainIdList = captainId.split(",")
        crewIdList = crewId.split(",")
        if len(captainIdList) != captainNum:
            tkinter.messagebox.showwarning(title = "Error", message = "Captain Number Doesn't Match")
            noError2 = False
        if len(crewIdList) != crewNum:
            tkinter.messagebox.showwarning(title = "Error", message = "Crew Number Doesn't Match")
            noError2 = False

        try:
            conn = sqlite3.connect("data.db")   
            cursor = conn.cursor()
            # Checks If There is Ship On Voyage
            cursor.execute(f"SELECT SHIP_ID, SHIP_ON_VOYAGE FROM SHIP_DATA")
            rows = cursor.fetchall()
            for row in rows:
                tempShipId, tempShipVoyage = row
                if tempShipVoyage == 1:
                    tkinter.messagebox.showwarning(title = "Error", message = f"There is already 1 ship on voyage.")
                    noError2 = False
                    return


            # Checks If Voyage Exist
            cursor.execute(f"SELECT * FROM VOYAGE_DATA WHERE VOYAGE_ID = '{voyageId}' ")
            row = cursor.fetchone()
            if row is None:
                # If Doesn't Exist Show Error
                tkinter.messagebox.showwarning(title = "Error", message = "Voyage Not Found")
                noError2 = False


            # Checks If Ship Exist
            cursor.execute(f"SELECT * FROM SHIP_DATA WHERE SHIP_ID = '{shipId}' ")
            row = cursor.fetchone()
            if row is None:
                # If Doesn't Exist Show Error
                tkinter.messagebox.showwarning(title = "Error", message = "Ship Not Found")
                noError2 = False
            cursor.execute(f"SELECT SHIP_ON_VOYAGE FROM SHIP_DATA WHERE SHIP_ID = '{shipId}'")
            row = cursor.fetchone()
            if row is not None and row[0] == 1:    
                tkinter.messagebox.showwarning(title = "Error", message = "Ship On Voyage")

            # Checks If Captains Exist
            for i in range(len(captainIdList)):
                cursor.execute(f"SELECT * FROM CAPTAIN_DATA WHERE CAPTAIN_ID = '{captainIdList[i]}' ")
                row = cursor.fetchone()
                if row is None:
                    # If Doesn't Exist Show Error        
                    tkinter.messagebox.showwarning(title = "Error", message = f"Captain {captainIdList[i]} Not Found")
                    noError2 = False
                cursor.execute(f"SELECT CAPTAIN_ON_VOYAGE FROM CAPTAIN_DATA WHERE CAPTAIN_ID = '{captainIdList[i]}'")
                row = cursor.fetchone()
                if row is not None and row[0] == 1:
                    tkinter.messagebox.showwarning(title = "Error", message = f"Captain {captainIdList[i]} On Voyage")
                    noError2 = False


            # Checks if Crew Exist 
            for y in range(len(crewIdList)):
                cursor.execute(f"SELECT * FROM CREW_DATA WHERE CREW_ID = '{crewIdList[y]}' ")
                row = cursor.fetchone()
                if row is None:
                    # If Doesn't Exist Show Error        
                    tkinter.messagebox.showwarning(title = "Error", message = f"Crew Member '{crewIdList[y]}' Not Found")
                    noError2 = False
                cursor.execute(f"SELECT CREW_ON_VOYAGE FROM CREW_DATA WHERE CREW_ID = '{crewIdList[y]}'")
                row = cursor.fetchone()
                if row is not None and row[0] == 1:
                    tkinter.messagebox.showwarning(title = "Error", message = f"Crew Member {crewIdList[y]} On Voyage")
                    noError2 = False
                    

            if noError2 == True:
                # Update On_Voyage Data
                cursor.execute(f"UPDATE SHIP_DATA SET SHIP_ON_VOYAGE = 1 WHERE SHIP_ID = '{shipId}'")
                conn.commit()

                for i in range(len(captainIdList)):
                    cursor.execute(f"UPDATE CAPTAIN_DATA SET CAPTAIN_ON_VOYAGE = 1 WHERE CAPTAIN_ID = '{captainIdList[i]}'")
                    conn.commit()
                for y in range (len(crewIdList)):
                    cursor.execute(f"UPDATE CREW_DATA SET CREW_ON_VOYAGE = 1 WHERE CREW_ID = '{crewIdList[y]}'")
                    conn.commit()

                tkinter.messagebox.showinfo(title="Success", message=f"Voyage created successfully.")

        except sqlite3.Error as e:
            tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))
        finally:
            conn.close()


def endCreateVoyage():
    noError = True
    voyageId = cvoyage_id_entry.get()
    shipId = cship_id_entry.get()
    captainNum = int(ccaptain_num_spinbox.get())
    captainId = ccaptain_id_entry.get()
    crewNum = int(ccrew_num_spinbox.get())
    crewId = ccrew_id_entry.get()

    if voyageId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Voyage ID")
        noError = False

    elif shipId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Ship ID")
        noError = False

    elif captainNum < 2:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Captain Number") 
        noError = False

    elif captainId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Captain ID")
        noError = False

    elif crewNum < 1:
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Crew Number")
        noError = False

    elif crewId == "":
        tkinter.messagebox.showwarning(title = "Error", message = "Invalid Crew ID")
        noError = False

    if noError:
        captainIdList = captainId.split(",")
        crewIdList = crewId.split(",")
        if len(captainIdList) != captainNum:
            tkinter.messagebox.showwarning(title = "Error", message = "Captain Number Doesn't Match")
            return
        if len(crewIdList) != crewNum:
            tkinter.messagebox.showwarning(title = "Error", message = "Crew Number Doesn't Match")
            return 
        try:
            conn = sqlite3.connect("data.db")
            cursor = conn.cursor()
            # Checks If Voyage Exist
            cursor.execute(f"SELECT * FROM VOYAGE_DATA WHERE VOYAGE_ID = '{voyageId}' ")
            row = cursor.fetchone()
            if row is None:
                # If Doesn't Exist Show Error
                tkinter.messagebox.showwarning(title="Error", message="Voyage Not Found")
                return

            # Checks If Ship Exist
            cursor.execute(f"SELECT * FROM SHIP_DATA WHERE SHIP_ID = '{shipId}'")
            row = cursor.fetchone()
            if row is None:
                tkinter.messagebox.showwarning(title = "Error", message = "Ship Not Found")
                return
            else:
                # Changes On Voyage to 0
                table_change_query = f"UPDATE SHIP_DATA SET SHIP_ON_VOYAGE = 0 WHERE SHIP_ID = '{shipId}'"
                conn.execute(table_change_query)
                conn.commit()
            
            # Checks If Captains Exist
            for i in range(len(captainIdList)):
                cursor.execute(f"SELECT * FROM CAPTAIN_DATA WHERE CAPTAIN_ID = '{captainIdList[i]}' ")
                row = cursor.fetchone()
                if row is None:
                    # If Doesn't Exist Show Error        
                    tkinter.messagebox.showwarning(title = "Error", message = f"Captain {captainIdList[i]} Not Found")
                    return
                else:
                    # Changes On Voyage To 0
                    table_change_query = f"UPDATE CAPTAIN_DATA SET CAPTAIN_ON_VOYAGE = 0 WHERE CAPTAIN_ID = '{captainIdList[i]}'"
                    conn.execute(table_change_query)
                    conn.commit()

            # Checks if Crew Exist
            for y in range(len(crewIdList)):
                cursor.execute(f"SELECT * FROM CREW_DATA WHERE CREW_ID = '{crewIdList[y]}'")
                row = cursor.fetchone()
                if row is None:
                    # If Doesn't Exist Show Error
                    tkinter.messagebox.showwarning(title = "Error", message = f"Crew Member {crewIdList[y]} Not Found")
                    return
                else:
                    table_change_query = f"UPDATE CREW_DATA SET CREW_ON_VOYAGE = 0 WHERE CREW_ID = '{crewIdList[y]}'"
                    conn.execute(table_change_query)
                    conn.commit()



            # Informs The User About The Updated Data
            tkinter.messagebox.showinfo(title="Success", message=f"Voyage {voyageId} ended successfully.")
        except sqlite3.Error as e:
            tkinter.messagebox.showwarning(title="Error", message="Database Error: " + str(e))


window.title("Database Form")

frame = tkinter.Frame(window)
frame.pack()


# -----------------------Ship Info Section-----------------------


ship_info_frame = tkinter.LabelFrame(frame, text = "Ship Information")
ship_info_frame.grid(row = 0, column = 0, padx = 20, pady = 10)

ship_id_label = tkinter.Label(ship_info_frame, text = "ID")
ship_id_entry = tkinter.Entry(ship_info_frame)
ship_id_label.grid(row = 0, column = 0)
ship_id_entry.grid(row = 1, column = 0)

ship_name_label = tkinter.Label(ship_info_frame, text = "Name")
ship_name_entry = tkinter.Entry(ship_info_frame)
ship_name_label.grid(row = 0, column = 1)
ship_name_entry.grid(row = 1, column = 1)

ship_weight_label = tkinter.Label(ship_info_frame, text = "Weight")
ship_weight_spinbox = tkinter.Spinbox(ship_info_frame, from_ = 10000, to = "infinity")
ship_weight_label.grid(row = 0, column = 2)
ship_weight_spinbox.grid(row = 1, column = 2)

ship_construction_year_label = tkinter.Label(ship_info_frame, text = "Construction Year (yyyy-mm-dd)")
ship_construction_year_entry = tkinter.Entry(ship_info_frame)
ship_construction_year_label.grid(row = 2, column = 0)
ship_construction_year_entry.grid(row = 3, column = 0)

ship_type_label = tkinter.Label(ship_info_frame, text = "Type")
ship_type_combobox = ttk.Combobox(ship_info_frame, values = ["Passenger", "Oil", "Container"])
ship_type_label.grid(row = 2, column = 1)
ship_type_combobox.grid(row = 3, column = 1)

ship_pscapacity_label = tkinter.Label(ship_info_frame, text = "Passenger Capacity")
ship_pscapacity_spinbox = tkinter.Spinbox(ship_info_frame, from_ = 0, to = 10000)
ship_pscapacity_label.grid(row = 2, column = 2)
ship_pscapacity_spinbox.grid(row = 3, column = 2)

ship_oilcapacity_label = tkinter.Label(ship_info_frame, text = "Oil Capacity")
ship_oilcapacity_spinbox = tkinter.Spinbox(ship_info_frame, from_ = 0, to = 10000)
ship_oilcapacity_label.grid(row = 4, column = 0)
ship_oilcapacity_spinbox.grid(row = 5, column = 0)

ship_maxweight_label = tkinter.Label(ship_info_frame, text = "Max Weight")
ship_maxweight_spinbox = tkinter.Spinbox(ship_info_frame, from_ = 0, to = 10000)
ship_maxweight_label.grid(row = 4, column = 1)
ship_maxweight_spinbox.grid(row = 5, column = 1)

ship_crcapacity_label = tkinter.Label(ship_info_frame, text = "Container Capacity")
ship_crcapacity_spinbox = tkinter.Spinbox(ship_info_frame, from_ = 0, to = 100)
ship_crcapacity_label.grid(row = 4, column = 2)
ship_crcapacity_spinbox.grid(row = 5, column = 2)


ship_button_frame = tkinter.LabelFrame(ship_info_frame, border = 0)
ship_button_frame.grid(row = 6, column = 1)


ship_add_button = tkinter.Button(ship_button_frame, text = "Add", command = addShipData, border = 3, width = 5)
ship_add_button.grid(row = 0, column = 0)

ship_del_button = tkinter.Button(ship_button_frame, text = "Delete", command = deleteShipData, border = 3, width = 5)
ship_del_button.grid(row = 0, column = 1)

ship_edit_button = tkinter.Button(ship_button_frame, text = "Update", command = updateShipData, border = 3, width = 5)
ship_edit_button.grid(row = 0, column = 2)

# Editing Label Sizes
for widget in ship_info_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)

for widget in ship_button_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)


# -----------------------Harbor Info Section-----------------------

harbor_info_frame = tkinter.LabelFrame(frame, text = "Harbor Information")
harbor_info_frame.grid(row = 1, column = 0, padx = 20, pady = 10)

harbor_name_label = tkinter.Label(harbor_info_frame, text = "Name")
harbor_name_entry = tkinter.Entry(harbor_info_frame)
harbor_name_label.grid(row = 0, column = 0)
harbor_name_entry.grid(row = 1, column = 0)

harbor_country_label = tkinter.Label(harbor_info_frame, text = "Country")
harbor_country_entry = tkinter.Entry(harbor_info_frame)
harbor_country_label.grid(row = 0, column = 1)
harbor_country_entry.grid(row = 1, column = 1)

harbor_population_label = tkinter.Label(harbor_info_frame, text = "Population")
harbor_population_entry = tkinter.Entry(harbor_info_frame)
harbor_population_label.grid(row = 0, column = 2)
harbor_population_entry.grid(row = 1, column = 2)

harbor_passport_label = tkinter.Label(harbor_info_frame, text = "Passport Required")
harbor_passport_var = tkinter.BooleanVar()
harbor_passport_var.set(False)
harbor_passport_checkbutton = tkinter.Checkbutton(harbor_info_frame, text = "Required", variable = harbor_passport_var)
harbor_passport_label.grid(row = 2, column = 0)
harbor_passport_checkbutton.grid(row = 3, column = 0)

harbor_fee_label = tkinter.Label(harbor_info_frame, text = "Docking Fee")
harbor_fee_entry = tkinter.Entry(harbor_info_frame)
harbor_fee_label.grid(row = 2, column = 1)
harbor_fee_entry.grid(row = 3, column = 1)


harbor_button_frame = tkinter.LabelFrame(harbor_info_frame, border = 0)
harbor_button_frame.grid(row = 3, column = 2)

harbor_add_button = tkinter.Button(harbor_button_frame, text = "Add", command = addHarborData, border = 3, width = 5)
harbor_add_button.grid(row = 0, column = 0)

harbor_del_button = tkinter.Button(harbor_button_frame, text = "Delete", command = deleteHarborData, border = 3, width = 5)
harbor_del_button.grid(row = 0, column = 1)

harbor_edit_button = tkinter.Button(harbor_button_frame, text = "Update", command = updateHarborData, border = 3, width = 5)
harbor_edit_button.grid(row = 0, column = 2)

for widget in harbor_info_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)

for widget in harbor_button_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)


# -----------------------Crew Info Section-----------------------


crew_info_frame = tkinter.LabelFrame(frame, text = "Crew Information")
crew_info_frame.grid(row = 2, column = 0, padx = 20, pady = 10)

crew_id_label = tkinter.Label(crew_info_frame, text = "ID")
crew_id_entry = tkinter.Entry(crew_info_frame)
crew_id_label.grid(row = 0, column = 0)
crew_id_entry.grid(row = 1, column = 0)

crew_name_label = tkinter.Label(crew_info_frame, text = "Name")
crew_name_entry = tkinter.Entry(crew_info_frame)
crew_name_label.grid(row = 0, column = 1)
crew_name_entry.grid(row = 1, column = 1)

crew_lastname_label = tkinter.Label(crew_info_frame, text = "Last Name")
crew_lastname_entry = tkinter.Entry(crew_info_frame)
crew_lastname_label.grid(row = 0, column = 2)
crew_lastname_entry.grid(row = 1, column = 2)

crew_address_label = tkinter.Label(crew_info_frame, text = "Address")
crew_address_entry = tkinter.Entry(crew_info_frame)
crew_address_label.grid(row = 2, column = 0)
crew_address_entry.grid(row = 3, column = 0)

crew_nationality_label = tkinter.Label(crew_info_frame, text = "Nationality")
crew_nationality_entry = tkinter.Entry(crew_info_frame)
crew_nationality_label.grid(row = 2, column = 1)
crew_nationality_entry.grid(row = 3, column = 1)

crew_birthday_label = tkinter.Label(crew_info_frame, text = "Birthday (yyyy-mm-dd)")
crew_birthday_entry = tkinter.Entry(crew_info_frame)
crew_birthday_label.grid(row = 2, column = 2)
crew_birthday_entry.grid(row = 3, column = 2)

crew_hiredate_label = tkinter.Label(crew_info_frame, text = "Hire Date (yyyy-mm-dd)")
crew_hiredate_entry = tkinter.Entry(crew_info_frame)
crew_hiredate_label.grid(row = 4, column = 0)
crew_hiredate_entry.grid(row = 5, column = 0)

crew_iscaptain_label = tkinter.Label(crew_info_frame, text = "Is Captain")
crew_captain_var = tkinter.BooleanVar()
crew_captain_var.set(False)
crew_iscaptain_checkbutton = tkinter.Checkbutton(crew_info_frame, text = "Captain", variable = crew_captain_var)
crew_iscaptain_label.grid(row = 4, column = 1)
crew_iscaptain_checkbutton.grid(row = 5, column = 1)

crew_cptlicense_label = tkinter.Label(crew_info_frame, text = "Captain License")
crew_cptlicense_entry = tkinter.Entry(crew_info_frame)
crew_cptlicense_label.grid(row = 4, column = 2)
crew_cptlicense_entry.grid(row = 5, column = 2)

crew_role_label = tkinter.Label(crew_info_frame, text = "Crew Role")
crew_role_combobox = ttk.Combobox(crew_info_frame, values = ["2nd Captain", "Navigator", "Cook", "Engineer", "Carpenter"])
crew_role_label.grid(row = 6, column = 0)
crew_role_combobox.grid(row = 7, column = 0)

crew_button_frame = tkinter.LabelFrame(crew_info_frame, border = 0)
crew_button_frame.grid(row = 7, column = 1)

crew_add_button = tkinter.Button(crew_button_frame, text = "Add", command = addCrewData, border = 3, width = 5)
crew_add_button.grid(row = 0, column = 0)

crew_del_button = tkinter.Button(crew_button_frame, text = "Delete", border = 3, command = deleteCrewData, width = 5)
crew_del_button.grid(row = 0, column = 1)

crew_edit_button = tkinter.Button(crew_button_frame, text = "Update", command = updateCrewData, border = 3, width = 5)
crew_edit_button.grid(row = 0, column = 2)


for widget in crew_info_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)

for widget in crew_button_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)


# -----------------------Voyage Info Section-----------------------


voyage_info_frame = tkinter.LabelFrame(frame, text = "Voyage Information")
voyage_info_frame.grid(row = 3, column = 0, padx = 20, pady = 10)

voyage_id_label = tkinter.Label(voyage_info_frame, text = "ID")
voyage_id_entry = tkinter.Entry(voyage_info_frame)
voyage_id_label.grid(row = 0, column = 0)
voyage_id_entry.grid(row = 1, column = 0)

voyage_departuredate_label = tkinter.Label(voyage_info_frame, text = "Departure Date (yyyy-mm-dd)")
voyage_departuredate_entry = tkinter.Entry(voyage_info_frame)
voyage_departuredate_label.grid(row = 0, column = 1)
voyage_departuredate_entry.grid(row = 1, column = 1)

voyage_returndate_label = tkinter.Label(voyage_info_frame, text = "Return Date (yyyy-mm-dd)")
voyage_returndate_entry = tkinter.Entry(voyage_info_frame)
voyage_returndate_label.grid(row = 0, column = 2)
voyage_returndate_entry.grid(row = 1, column = 2)

voyage_departureharbor_label = tkinter.Label(voyage_info_frame, text = "Departure Harbor")
voyage_departureharbor_entry = tkinter.Entry(voyage_info_frame)
voyage_departureharbor_label.grid(row = 2, column = 0)
voyage_departureharbor_entry.grid(row = 3, column = 0)

voyage_button_frame = tkinter.LabelFrame(voyage_info_frame, border = 0)
voyage_button_frame.grid(row = 3, column = 1)

voyage_add_button = tkinter.Button(voyage_button_frame, text = "Add", command = addVoyageData, border = 3, width = 5)
voyage_add_button.grid(row = 0, column = 0)

voyage_del_button = tkinter.Button(voyage_button_frame, text = "Delete", command = deleteVoyageData, border = 3, width = 5)
voyage_del_button.grid(row = 0, column = 1)

voyage_edit_button = tkinter.Button(voyage_button_frame, text = "Update", command = updateVoyageData, border = 3, width = 5)
voyage_edit_button.grid(row = 0, column = 2)

for widget in voyage_info_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)

for widget in voyage_button_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)



# -----------------------Create Voyage Section-----------------------

create_info_frame = tkinter.LabelFrame(frame, text = "Start Voyage")
create_info_frame.grid(row = 0, column = 1, padx = 20, pady = 10)

cvoyage_id_label = tkinter.Label(create_info_frame, text = "Voyage ID")
cvoyage_id_entry = tkinter.Entry(create_info_frame)
cvoyage_id_label.grid(row = 0, column = 0)
cvoyage_id_entry.grid(row = 1, column = 0)

cship_id_label = tkinter.Label(create_info_frame, text = "Ship ID")
cship_id_entry = tkinter.Entry(create_info_frame)
cship_id_label.grid(row = 0, column = 1)
cship_id_entry.grid(row = 1, column = 1)

ccaptain_num_label = tkinter.Label(create_info_frame , text = "Number of Captains (At Least 2)") 
ccaptain_num_spinbox = tkinter.Spinbox(create_info_frame, from_ = 2, to = 10)
ccaptain_num_label.grid(row = 0, column = 2)
ccaptain_num_spinbox.grid(row = 1, column =2)

ccaptain_id_label = tkinter.Label(create_info_frame, text =  "Captain ID (',' Between ID's)")
ccaptain_id_entry = tkinter.Entry(create_info_frame)
ccaptain_id_label.grid(row = 3, column = 0)
ccaptain_id_entry.grid(row = 4, column = 0)

ccrew_num_label = tkinter.Label(create_info_frame, text = "Number of Crew Members (At Least 1)")
ccrew_num_spinbox = tkinter.Spinbox(create_info_frame, from_ = 1, to = 10)
ccrew_num_label.grid(row = 3, column = 1)
ccrew_num_spinbox.grid(row = 4, column = 1)

ccrew_id_label = tkinter.Label(create_info_frame, text = "Crew ID (',' Between ID's)")
ccrew_id_entry = tkinter.Entry(create_info_frame)
ccrew_id_label.grid(row = 3, column = 2)
ccrew_id_entry.grid(row = 4, column = 2)

create_button_frame = tkinter.Frame(create_info_frame)
create_button_frame.grid(row = 5, column = 1)

create_add_button = tkinter.Button(create_button_frame, text = "Start", command = startCreateVoyage, border = 3, width = 5)
create_add_button.grid(row = 0, column = 0)

create_del_button = tkinter.Button(create_button_frame, text = "End", command = endCreateVoyage, border = 3, width = 5)
create_del_button.grid(row = 0, column = 1)

for widget in create_info_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)

for widget in create_button_frame.winfo_children():
    widget.grid_configure(padx = 10, pady = 5)


window.mainloop()