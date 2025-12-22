from datetime import datetime,timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

#launch url
newUrl = 'https://www.flightstatus.co.il/'

def getFlights():
    tomorrow_date = (datetime.now() + timedelta(days=1)).isoformat()[:10]

    options = Options()
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # The URL of your remote webdriver
    executor_url = 'https://flight-management-system-scrapper.onrender.com'

    driver = None

    max_retries = 12
    for i in range(max_retries):
        try:
            print(f"Attempting to connect (Try {i+1}/{max_retries})...")
            driver = webdriver.Remote(
                command_executor=executor_url,
                options=options
            )
            print("Success! Connected to the driver.")
            break
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Service might be sleeping. Waiting 10 seconds...")
            time.sleep(10)

    if driver:
        driver.get(newUrl)
        flightsList = driver.page_source
        driver.quit()

    else:
        print("Could not connect after multiple attempts.")


    aeroCompanies = ["UX","IB","AI","B2","WZ","QS","EY","5F","3F","J2","HY","CY","A9","ET","FB","VY","FX","I2","XZ"]
    flights = {"flights":[]}

    try:
        fltListSoup = BeautifulSoup(flightsList,features="html.parser")
        
        arrivalFlightsDiv = fltListSoup.find(id="tab_container_0") #ARRIVALS
        arvlFlts = arrivalFlightsDiv.findAll(attrs={"class": f"date_{tomorrow_date}"})
        counter = 0
        for flightRow in arvlFlts:
            details = flightRow.findAll('td')
            if(details[1].getText()[:2] in aeroCompanies):
                number = details[1].getText()
                dest = details[2].getText()
                time = details[3].getText()
                fTime = datetime(year=int(tomorrow_date[:4]),month=int(tomorrow_date[5:7]),day=int(tomorrow_date[8:]),hour=int(time[:2]),minute=int(time[3:]))
                for i in flights["flights"]:
                    if i["flightNum"] == number:
                        counter += 1
                if counter == 0:
                    flights["flights"].append({"flightNum":number,"dest":dest,"stdLocal":f"{fTime.year}-{fTime.month}-{fTime.day}T{fTime.timetz()}.000000+02:00","type":"A","aircraftType":"TBA","aircraftReg":"TBA","gate":"TBA","pit":"TBA"})


        deptFlightsDiv = fltListSoup.find(id="tab_container_1") #DEPARTURES
        deptFlts = deptFlightsDiv.findAll(attrs={"class": f"date_{tomorrow_date}"})
        counter = 0
        for flightRow in deptFlts:
            items = flightRow.findAll('td')
            if(items[1].getText()[:2] in aeroCompanies):
                number = items[1].getText()
                dest = items[2].getText()
                time = items[3].getText()
                fTime = datetime(year=int(tomorrow_date[:4]),month=int(tomorrow_date[5:7]),day=int(tomorrow_date[8:]),hour=int(time[:2]),minute=int(time[3:]))
                for i in flights["flights"]:
                    if i["flightNum"] == number:
                        counter += 1
                if counter == 0:
                    flights["flights"].append({"flightNum":number,"dest":dest,"stdLocal":f"{fTime.year}-{fTime.month}-{fTime.day}T{fTime.timetz()}.000000+02:00","type":"D","aircraftType":"TBA","aircraftReg":"TBA","gate":"TBA","pit":"TBA"})
    except:
        print("bs failed")
    # print(flights)
    return flights