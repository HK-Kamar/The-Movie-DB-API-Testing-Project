"""
Created on Mon Aug  2 13:08:28 2021

@author: HK
"""
import requests
import json
import mysql.connector
import flask

def get_json_data(query):
    response =  requests.get(query)
    if (response.status_code == 200): 
        array = response.json()
        text = json.dumps(array)
        return (text)
    else:
        return ("Error")
        
def provider_checker(series_ID,API_key):
    query = 'https://api.themoviedb.org/3/tv/'
    query += str(series_ID) + '/watch/providers?'
    query += 'api_key=' + API_key
    #query += '&locale=TR'
    
    text = get_json_data(query)
    if text != 'Error':
        dataset = json.loads(text)
        try:
            provider = dataset['results']['TR']['flatrate'][0]['provider_name']
            if provider == 'Amazon Prime Video':
                return True
        except:
            return False      

#Making the database connection
def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="themoviedb"
    )
    return mydb
    
def insert_series_to_db(series_id, name, overview, number_of_seasons, number_of_episodes, 
                popularity, vote_average,vote_count, first_air_date, last_air_date, status):
    mycursor = mydb.cursor()

    sql = "INSERT IGNORE INTO TV_SERIES (ID,Name,Overview,Number_of_Seasons,Number_of_Episodes,Popularity,Vote_Average,Vote_Count,First_Air_Date,Last_Air_Date,Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (series_id, name, overview, number_of_seasons, number_of_episodes, 
            popularity, vote_average,vote_count, first_air_date, last_air_date, status)
    mycursor.execute(sql, val)

    mydb.commit()
    
def insert_person_to_db(cast_id, name, gender, known_for_department, popularity):
    mycursor = mydb.cursor()

    sql = "INSERT IGNORE INTO PERSON (ID,Name,Gender,Known_For_Department,Popularity) VALUES (%s, %s, %s, %s, %s)"
    val = (cast_id, name, gender, known_for_department, popularity)
    mycursor.execute(sql, val)

    mydb.commit()
    
def insert_cast_to_db(series_id,person_id,character):
    mycursor = mydb.cursor()

    sql = "INSERT IGNORE INTO CAST (Series_ID,Person_ID,Type,Character_Name) VALUES (%s, %s, %s, %s)"
    val = (series_id,person_id,'Cast',character)
    mycursor.execute(sql, val)
    
    mydb.commit()    
    
def insert_crew_to_db(series_id,person_id):
    mycursor = mydb.cursor()

    sql = "INSERT IGNORE INTO CAST (Series_ID,Person_ID,Type) VALUES (%s, %s, %s)"
    val = (series_id,person_id,'Crew')
    mycursor.execute(sql, val)

    mydb.commit()    
    
# Get every series from database
def get_every_series_from_db(mydb):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM TV_SERIES")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)
        print('')    
    
# Get every person from database
def get_every_person_from_db(mydb):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM PERSON")

    myresult = mycursor.fetchall()

    print("Number of results: ", len(myresult))

    for x in myresult:
        print(x)    
    
# Get every cast from database
def get_every_cast_from_db(mydb):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM CAST")

    myresult = mycursor.fetchall()

    print(len(myresult))

    for x in myresult:
        print(x)    
    
# Execute any query
def query_executer(query):
    mycursor = mydb.cursor()

    mycursor.execute(query)

    myresult = mycursor.fetchall()

    print("Number of results: ", len(myresult))

    for x in myresult:
        print(x)    
    
mydb = connect_to_db()

#Setting the filtering query

prefix = 'https://api.themoviedb.org/3/discover/tv?'
API_key = 'b8f5ea4374a732cdb90a9457176f7034'
minimum_vote_count = '750'
minimum_vote_average = '8.3'
provider_name = 'Amazon%20Prime%20Video'
watch_region = 'TR'
sort_by = 'first_air_date.asc'
page = 1

query = prefix
query += 'api_key=' + API_key
query += '&vote_count.gte=' + minimum_vote_count 
query += '&vote_average.gte=' + minimum_vote_average 
query += '&provider_name=' + provider_name 
query += '&watch_region=' + watch_region 
query += '&page=' + str(page)
query += '&sort_by=' + sort_by

#Getting series ids according to filter
text = get_json_data(query)
list_series_ids = [] # list of the series ids
if text != 'Error':
    dataset = json.loads(text)
    count = 0
    i = 0;
    while(count < 3):
        if(provider_checker(dataset['results'][i]['id'],API_key)):
            list_series_ids.append(dataset['results'][i]['id'])
            count += 1
        i += 1
        if(i == 20):
            page +=1
            query = 'https://api.themoviedb.org/3/discover/tv?'
            query += 'api_key=' + API_key
            query += '&vote_count.gte=' + minimum_vote_count 
            query += '&vote_average.gte=' + minimum_vote_average 
            query += '&provider_name=' + provider_name 
            query += '&watch_region=' + watch_region 
            query += '&page=' + str(page)
            query += '&sort_by=' + sort_by
            text = get_json_data(query)
            dataset = json.loads(text)
            i=0
            
#Getting the asked information of the first 3 series
list_series_details = []
print("Related Links:")
for i in range (3):
    query = 'https://api.themoviedb.org/3/tv/'
    query += str(list_series_ids[i])
    query += '?api_key=' + API_key
    print(query)
    text = get_json_data(query)
    if text != 'Error':
        dataset = json.loads(text)
        series_id = dataset['id']
        name = dataset['name'] 
        overview = dataset['overview'] 
        number_of_seasons = dataset['number_of_seasons'] 
        number_of_episodes = dataset['number_of_episodes'] 
        popularity = dataset['popularity'] 
        vote_average = dataset['vote_average'] 
        vote_count = dataset['vote_count'] 
        first_air_date = dataset['first_air_date'] 
        last_air_date = dataset['last_air_date'] 
        status = dataset['status']
        
        insert_series_to_db(series_id, name, overview, number_of_seasons, number_of_episodes, 
                popularity, vote_average,vote_count, first_air_date, last_air_date, status)
        
        
        result = [series_id, name, overview, number_of_seasons, number_of_episodes, 
                  popularity, vote_average,vote_count, first_air_date, last_air_date, status]
        
        list_series_details.append(result)
        
        
get_every_series_from_db(mydb)

#Getting the cast information of the first 3 series
list_casts = []
list_crews = []
print("Related Links:")
for j in range (3):
    query = 'https://api.themoviedb.org/3/tv/'
    query += str(list_series_ids[j]) + '/credits'
    query += '?api_key=' + API_key
    print(query)
    text = get_json_data(query)
    if text != 'Error':
        list_cast = []
        list_casts.append(list_cast)
        list_crew = []
        list_crews.append(list_crew)
        dataset = json.loads(text)
        i=0
        while(1):
            try:
                cast_id = dataset['cast'][i]['id']
                name = dataset['cast'][i]['name'] 
                gender = dataset['cast'][i]['gender'] 
                known_for_department = dataset['cast'][i]['known_for_department'] 
                popularity = dataset['cast'][i]['popularity']
                character = dataset['cast'][i]['character']
                
                insert_person_to_db(cast_id, name, gender, known_for_department, popularity)
                insert_cast_to_db(list_series_ids[j],cast_id,character)
                    
                result = [cast_id, name, gender, known_for_department, popularity]
                list_casts[j].append(result)
                i+=1
            except:
                break
        i=0
        while(1):
            try:
                crew_id = dataset['crew'][i]['id']
                name = dataset['crew'][i]['name'] 
                gender = dataset['crew'][i]['gender'] 
                known_for_department = dataset['crew'][i]['known_for_department'] 
                popularity = dataset['crew'][i]['popularity']
                
                insert_person_to_db(crew_id, name, gender, known_for_department, popularity)
                insert_crew_to_db(list_series_ids[j],crew_id)
                
                result = [crew_id, name, gender, known_for_department, popularity]
                list_crews[j].append(result)
                i+=1
            except:
                break
                
get_every_person_from_db(mydb)

get_every_cast_from_db(mydb)


# Author: Huveyscan Kamar