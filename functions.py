import random 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dateutil import parser 
#from cred import dataMallAPIKEY as DMkey
from datetime import datetime 
import pytz 

def randomQuote():
    try:
        quotes=[]
        category=['motivational','inspiration','positive','funny','alone','love','friendship','humor']
        category=['romantic','valentines-day','love']
        ranCat=random.choice(category)
        print(ranCat)
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
                    }
        # Make a request to the website
        url = "https://www.brainyquote.com/topics/funny-quotes"
        url=f'https://www.brainyquote.com/topics/{ranCat}-quotes'
        try:
            response = requests.get(url, headers=headers)
        except:
            print('requests not allowed here')
            raise

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")
        print (soup)

        #* Find all elements with the container class
        elements = soup.find_all("div", {"class": "bqQt"})

    #* for each element found above, find its child element that contains the actual quote
        for element in elements:
            quote=element.find("div")
            #print(quote.text)
            #* the text contains the \n as well so replace it with blank
            quotes.append(quote.text.replace("\n",''))
    #* remove all the quotes from the list that doesnt contain anything after removing \n
        for quote in quotes:
            if quote==' ':
                quotes.remove(quote)
        # Print the extracted texts

        #print("-----------------------------------------start----------------------------")
        print(quotes)

        #* pick a random quote from the list of quotes
        randomQuote=random.choice(quotes)
    except Exception as e:
        print (e) 
        randomQuote='This function cant be used right now, sorry babe!'
    return randomQuote

#**************************************************************************************************************

#* activities/Dates and places to go
def DataAdder(data,authorizedUser):
    itemstoremove=[]
    #* start the data string from the actual data, removing the /addDates at the front
    data=data[9:]
    #* turning the data into a list separated by commas
    data=data.split(',')

    #* check if function was called by authorized user
    if authorizedUser:
        filename = 'dates.csv'
    else:
        filename = 'suggestedDates.csv'

    #* to validate if user input anything
    for item in data:
        #*append it to itemstoremove if it is blank
        if item.strip()=='':
            itemstoremove.append(item)
    #* remove the item from the original datalist if it is found in itemstoremove
    for item in itemstoremove:
        if item in data:
            data.remove(item)

    if len(data)==0:
        return 'You didnt input anything!'
    
    #* Use a for loop with strip method to remove leading whitespace from each item
    for i in range(len(data)):
        data[i] = data[i].strip()


    try:
        oldDF=pd.read_csv(filename)
        print('file can be found, proceeding to concat new df with existing df')
        combineDF=True
    except:
        combineDF=False
        print('df doesnt exist, creating new df')


    
    df=pd.DataFrame(columns=['Dates'])
    #* append every item in the list to the df 
    for item in data:
        print(len(df))
        df.loc[len(df)] = item
    #* if old df exist, concat them then save it
    if(combineDF):
        df=pd.concat([df,oldDF])

    df.to_csv(filename,index=0)
    print(df)
    return 'data added!'

def RandomDates():

    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv('dates.csv')
    except:
        return 'You didnt store any dates in me beforehand to tell you!'
    # Sample a random row from the DataFrame
    random_row = df.sample(n=1).iloc[0,0]

    # Print the random row
    print(random_row)

    return random_row

#--------------------------------------------------------------------

def get_unique_filename(target_dir, filename):
    # If the filename doesn't exist in the target directory, return it as is
    if not os.path.exists(os.path.join(target_dir, filename)):
        return filename

    # If the filename already exists, append a number to the file name until we find a unique filename
    base_filename, extension = os.path.splitext(filename)
    index = 1
    while True:
        new_filename = f"{base_filename}_{index}{extension}"
        if not os.path.exists(os.path.join(target_dir, new_filename)):
            return new_filename
        index += 1



def getBusTiming():
    #nested Dict to store the bus stop code and the buses to enquire
    #! only if its my id, if its jq, 912 and 912a from woodlands

    enquiredPlaces = {'Clementi Bus Int': [17009,['175','282','285']], 'Clementi Exit A':[17171,['78']],'Clementi Exit B':[17179,['201']], 'Woodlands Bus Int':[46009,['912','912A']]}
    baseURL = 'https://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2'
    busesDict = {} 
    DMkey = os.environ.get('dataMallAPIKey')
    for key,value in enquiredPlaces.items():
        busesDict[key] = {}

        busStopCode = value[0]
        param = {'BusStopCode' : busStopCode}

        res = requests.get(baseURL, headers={'AccountKey': DMkey}, params=param) 
        res.raise_for_status() 
        # indent 4 


        for bus in res.json()['Services']:
            if bus['ServiceNo'] in enquiredPlaces[key][1]:
                #busesDict[bus['ServiceNo']] = bus['NextBus']['EstimatedArrival']
                busesDict[key][bus['ServiceNo']] = bus['NextBus']['EstimatedArrival']
        print (busesDict) 

    
    currentTime = datetime.now(pytz.timezone('Asia/Singapore'))

    for busStopName, arrivalTimingDict in busesDict.items():
        for busNumber, arrivalTime in arrivalTimingDict.items():
            print (f"bus {busNumber}")
            parsed = parser.parse(arrivalTime) 
            print (parsed) 
            print ((parsed - currentTime).total_seconds()/60)   
            
            timeDiff = int((parsed - currentTime).total_seconds()/60)
            
            #convert it to how many minutes left by subtracting the current time from the estimated arrival time 
            busesDict[busStopName][busNumber] = f'{timeDiff} mins' if timeDiff > 0 else 'Arriving' 
            print ("==========")

        

    
    print (busesDict) 
    return busesDict 







