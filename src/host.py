import serial
import json
import time
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

# serial port config
SERIAL_PORT = "COM1" #usually COM3, but i change mine to COM1
BAUD_RATE = 115200 #speed of data transmission to match the Pico's baud rate

# Azure IoT Hub connection string
CONNECTION_STRING = "<connection_string>"

def connect_azure():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    print("Connecting to Azure IoT Hub...")
    client.connect()
    print("Connected")
    return client

def handle_method_request(request, client, ser):
    print(f"Direct method received: {request.name}, Payload: {request.payload}")
    ser.write((request.name.strip() + "\n").encode())
    
    # read response from Pico
    start_time = time.time()
    response = None
    while time.time() - start_time < 15:  # 15-second timeout
        line = ser.readline().decode("utf-8").strip()
        if line:
            try:
                data = json.loads(line)
                if "status" in data:  # check if it's a response
                    response = data
                    break
            except json.JSONDecodeError:
                pass  # ignore telemetry data
        time.sleep(0.1)

    # send response to Azure IoT Hub
    if response:
        method_response = MethodResponse.create_from_method_request(request, 200, response)
    else:
        method_response = MethodResponse.create_from_method_request(request, 408, {"status": "Timeout"})
    client.send_method_response(method_response)

def main():
    # init serial connection
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) 
  
    # connect to Azure IoT Hub
    client = connect_azure()

    # register method request handler - call the handle_method_request function when a direct method is called
    client.on_method_request_received = lambda request: handle_method_request(request, client, ser)

    while True:
        try:
            # read JSON data from Pico
            line = ser.readline().decode("utf-8").strip()
            if line:
                try:
                    data = json.loads(line)
                    print(f"Received from Pico: {data}")
                    # send to Azure IoT Hub
                    message = Message(json.dumps(data))
                    client.send_message(message)
                    print("Telemetry sent to Azure IoT Hub")
                except json.JSONDecodeError:
                    print("Invalid JSON:", line)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1) 

if __name__ == "__main__":
    main()


