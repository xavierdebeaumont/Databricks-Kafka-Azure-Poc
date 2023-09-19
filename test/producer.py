import datetime
from datetime import datetime, timedelta
import json
from time import sleep
import requests

# importing KafkaProducer
from kafka import KafkaProducer

def send_near_objects(objects_json, start_date_str, end_date_str, producer):
    
    start_date_dt = datetime.strptime(start_date_str,"%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date_str,"%Y-%m-%d")
    
    delta = (end_date_dt - start_date_dt).days
    
    index = 1
    
    for i in range(0,delta+1):
        
        current_date_dt = start_date_dt + timedelta(days=i)
        current_date_str = current_date_dt.strftime("%Y-%m-%d")
        
        asteroids = objects_json[current_date_str]
        
        for asteroid in asteroids:
            
            asteroid['current_date'] = current_date_str
            
            print(f"Sending element {index} to Kafka")
            
            data_asteroid = json.dumps(asteroid)
            
            #sending element to Kafka
            producer.send("neowstopic",data_asteroid.encode())
            
            sleep(10)
            
            index += 1

#The API request needs to have 2 parameteres: start_date and end_date, this will obtain all the information captured between those dates.
start_date_str = '2022-11-18'
end_date_str = '2022-11-19'

#calling the API
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date_str}&end_date={end_date_str}&api_key=DEMO_KEY"

response = requests.request("GET",url)
response = response.text
response_json = json.loads(response)

producer = KafkaProducer(bootstrap_servers="localhost:9092")

objects_elements = response_json["near_earth_objects"]

send_near_objects(objects_elements, start_date_str, end_date_str, producer)

producer.flush()