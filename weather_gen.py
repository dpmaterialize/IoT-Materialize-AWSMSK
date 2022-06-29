import requests
import json
import signal
import sys
import boto3
from time import sleep
import random
from faker import Faker
from kafka import KafkaProducer


def signal_handler(signal, frame):
    index = read_index()
    write_index(index + 2)
    sys.exit(0)


def write_index(index):
    with open('counter', 'w+') as val:
        val.write(str(index))
    return


def read_index(): 
    try:
        with open('counter', 'r+') as val:
            index = int(val.readline())
    except FileNotFoundError as e:
            index = 0
    return index


def send_to_producer(producer, topic, data):
    producer.send(topic, data)
    return


def main():
    with open('config.json', 'r') as config_file:
        config_json = json.load(config_file)
    g_index = read_index()
    producer = KafkaProducer(bootstrap_servers=config_json['broker'])
    signal.signal(signal.SIGINT, signal_handler)
    fake = Faker()
    while True:
        data = {}
        api_key = config_json['api_key']
        base_url = "http://api.weatherapi.com/v1"
        city_list = config_json['cities'].split(',')
        rand_index = random.randint(0, len(city_list) - 1)
        city = city_list[rand_index]

        parameters = {"key":api_key, "q":city}         # URL parameters
        r = requests.get(f"{base_url}/current.json", params=parameters)
        r = r.json()
        data['index'] = g_index
        data['date'] = str(fake.date_this_year(True, True))
        data['city'] = city
        data['latitude'] = r['location']['lat']
        data['longitude'] = r['location']['lon']
        data['temp_celcius'] = round(r['current']['temp_c'] - fake.pyfloat(left_digits=1, right_digits=2), 2)
        data['condition'] = r['current']['condition']['text']
        data['wind_kmph'] = round(r['current']['wind_kph'] + fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)
        data['wind_degree'] = r['current']['wind_degree'] + fake.pyint(min_value=0, max_value=56)
        data['pressure'] = round(r['current']['pressure_mb'] + fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)
        data_json = json.dumps(data)
        data_json = bytes(str(data_json), 'utf-8')
        send_to_producer(producer, config_json['topic'], data_json)
        print(f"Inserted entry {g_index} to topic {config_json['topic']}")
        g_index += 1
        write_index(g_index)
        sleep(5)
    return


main()
