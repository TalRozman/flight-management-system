from datetime import datetime,timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

#launch url
newUrl = 'https://www.flightstatus.co.il/'

def getFlights():
    # create a new Edge session
    options = Options()
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    try:
        driver = webdriver.Remote(command_executor='https://finalproj-aerohandling-scrapper.onrender.com',options=options)
    except:
        print("connection failed")

    driver.get(newUrl)
    arvlDiv = driver.find_element(by=By.ID,value='tab_container_0') #ARRIVALS
    datesList = arvlDiv.find_elements(by=By.CLASS_NAME, value='flight_table_date_row')
    tomorrow = datesList[2]
    date = tomorrow.find_element(by=By.TAG_NAME,value='th').text

    flightsList = driver.page_source

    driver.quit()    

    aeroCompanies = ["UX","IB","AI","B2","WZ","QS","EY","5F","3F","J2","HY","CY","A9","ET","FB","VY","FX","I2","XZ"]
    flights = {"flights":[]}

    try:
        fltListSoup = BeautifulSoup(flightsList,features="html.parser")
        
        arrivalFlightsDiv = fltListSoup.find(id="tab_container_0") #ARRIVALS
        arvlFlts = arrivalFlightsDiv.findAll(attrs={"class": f"date_{date}"})
        counter = 0
        for flightRow in arvlFlts:
            details = flightRow.findAll('td')
            if(details[1].getText()[:2] in aeroCompanies):
                number = details[1].getText()
                dest = details[2].getText()
                time = details[3].getText()
                fTime = datetime(year=int(date[:4]),month=int(date[5:7]),day=int(date[8:]),hour=int(time[:2]),minute=int(time[3:]))
                for i in flights["flights"]:
                    if i["flightNum"] == number:
                        counter += 1
                if counter == 0:
                    flights["flights"].append({"flightNum":number,"dest":dest,"stdLocal":f"{fTime.year}-{fTime.month}-{fTime.day}T{fTime.timetz()}.000000+02:00","type":"A","aircraftType":"TBA","aircraftReg":"TBA","gate":"TBA","pit":"TBA"})


        deptFlightsDiv = fltListSoup.find(id="tab_container_1") #DEPARTURES
        deptFlts = deptFlightsDiv.findAll(attrs={"class": f"date_{date}"})
        counter = 0
        for flightRow in deptFlts:
            items = flightRow.findAll('td')
            if(items[1].getText()[:2] in aeroCompanies):
                number = items[1].getText()
                dest = items[2].getText()
                time = items[3].getText()
                fTime = datetime(year=int(date[:4]),month=int(date[5:7]),day=int(date[8:]),hour=int(time[:2]),minute=int(time[3:]))
                for i in flights["flights"]:
                    if i["flightNum"] == number:
                        counter += 1
                if counter == 0:
                    flights["flights"].append({"flightNum":number,"dest":dest,"stdLocal":f"{fTime.year}-{fTime.month}-{fTime.day}T{fTime.timetz()}.000000+02:00","type":"D","aircraftType":"TBA","aircraftReg":"TBA","gate":"TBA","pit":"TBA"})
    except:
        print("bs failed")
    return flights