The file “weather_gen.py” contains the code that generates the IoT data. The code uses the help of weather API. This API requires a couple of parameters one being the API key and the other a valid city name.

The “weather_gen.py” file also contains a ‘config.json’. The input fields present in JSON are.

```api_key```: This key is used for the weather API app. Can be ignored

```topic```: The topic name under which the data will be generated

```broker```: Broker IP through which the communication will happen. You should update this value in accordance to your AWS service. 

The broker DNS can be found in under the “properties” tab inside “Broker Details”. You can use any one of the endpoint values.

```cities```: The list of cities we query via the weather API to get the info. Note the cities needs to be valid for the weather API to work. 

Also, multiple cities need to be ‘,’ separated. You can update the cities present in it as per your preference. I have used the top 10 most populated cities in America as an example.               

The “weather_gen.py” code uses each city in random.

With the help of the weather API, we get real-time data of any city that is present in the config file. 

### Steps to setup the code

1) Create a virtualenv using ```virtualenv env```
2) Install the packages using ```pip3 install -r requirements.txt```
