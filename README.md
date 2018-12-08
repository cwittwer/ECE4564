# ECE4564

## Assignment 1 Overview: Twitter Based Question and Answer System
>	Assignment 1 is a text-based question and answer system using WolframAlpha’scomputational knowledge engine.  Questions to your Q&A system are expressed as Twitter Tweets.  The question and resulting answer are “spoken” using text-to-speech (TTS) translation API.The system uses three Rpi’sfollowing the client/server model discussed in class.  The server is iterative and connection-oriented.  Communication among client, bridge and server is handled via stream-oriented sockets.The client Rpicaptures the Tweet containing the question text.  The client extracts, builds and sends a question “payload” to the bridge Rpivia sockets.  The bridge Rpispeaks the question/answer, and sends the payloads to server/client Rpi.The server  sends the question to the WolframAlphaengine and receives the answer.  The server builds and sends an answer “payload” back to the bridge Rpi. The client displays the answer on the attached monitor.

## Assignment 2 Overview: Book Inventory System
>	•  Client Rpi (client.py) 
		•  Uses RabbitMQ RPC to send and receive messages from Processor RPi
		•  Allows user to control storage info by proper CMDs (ADD/BUY/SELL/COUNT/LIST/DELETE)
	•  Processor RPi (processor.py) 
		•  Setup RabbitMQ RPC server receives and sends message to Client Rpi.
		•  Uses Bluetooth Serial over RFCOMM to send and receive messages to Storage RPi
	•  Storage Rpi (storage.py, MongoDB.py, LED.py)
		•  Service that manages 
			•  Messages sent from processor RPi
			•  Message requests to processor RPi
		•  Indicates # of book varieties in storage using RGB LED
		•  Setup Bluetooth server to receive and sent msgs to Processor Rpi. 
		•  Maintains all book info in local NoSQL database (MongoDB).

## Assignment 3 Overview:
>	Demonstrate web service interactions using REST
	•Build Requirements 
		•Flask Microframework 
		•Python Requests Library 
		•HTTP Basic Authentication 
		•Auth data maintained in MongoDB datastore 
		•Service Advertisement
		•Zeroconf
	•Supported Services 
		•RGB LED Controller 
		•Storage Server Controller 
