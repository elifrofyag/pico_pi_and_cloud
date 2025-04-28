# pico_pi_and_cloud [still updating]
A detailed documentation of how to connect Raspberry Pi Pico RP2040 to the cloud through Serial communication between the microcontroller and the host computer.

## Requirements
### Hardware
1. [Raspberry Pi Pico RP2040](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#pico-1-family) (no wifi available)
2. Sensor (used in this project: Capacitive Soil Moisture Sensor v2.0)
3. Micro-USB wire
4. Your own PC with a Serial Port

### Dependencies

Set up virtual environment to install `requirements.txt`

```Bash
pip install -r requirements.txt
```

## Setup
### Azure IoT Hub in the cloud
#### 1. Create account
Check this out: [Create a cloud subscription](https://github.com/microsoft/IoT-For-Beginners/tree/main/2-farm/lessons/4-migrate-your-plant-to-the-cloud#create-a-cloud-subscription)

> [!note] 
> **For Students who cannot verify academic status** (these steps an be found in Microsoft Azure Support + Troubleshooting, no need to submit support request)
> 
> If you are unable to sign-up for Azure for student as your university does not have contract with Microsoft to signup for Azure, you can sign up with a GitHub account:
> 1. Make sure to apply for the GitHub Student Developer Pack
> 2. Use the Sign in with GitHub option on the Azure sign-in page.
> 3. **Sign in using your Github userID and not email address.**
> 4. Select your profile in the upper right hand corner select Settings.
> 5. Make sure the same Azure email address is listed under Emails and that it is chosen as the Primary email.
> Note: Use your personal email address whenever possible. If you choose to use your school email, ensure that it has been verified.
>
> Go to - https://signup.azure.com/studentverification?offerType=1.
> 
> 7. Select Sign in with your Github
> 8. Select the Github option.
> 9. Once you have the confirmation email from GitHub, go to the offers on their website and get the benefits by finding the Azure section of the offers provided with the pack. Select "Activate Now" or "Get Access/Benefit" button to generate a unique code to use.
> 10. Once you get a prompt to sign in, use your GitHub credentials, then select the dropdown icon and select Verification code, where you will input the code, you received from GitHub's website.
>

#### 2. Create IoT Service
Check this out: [Create IoT Service](https://github.com/microsoft/IoT-For-Beginners/tree/main/2-farm/lessons/4-migrate-your-plant-to-the-cloud#create-an-iot-service-in-the-cloud)
- Make sure to follow the link above and have **Resource Group** and **IoT Hub** ready.

### Set Up MicroPython on the Raspberry Pi Pico
1. **Install MicroPython Firmware:**
   
- Download the latest MicroPython firmware for the Raspberry Pi Pico from the official MicroPython website.
- Connect your Pico to your computer while holding the BOOTSEL button to enter bootloader mode.
- Drag and drop the .uf2 firmware file onto the Pico’s storage device (it will appear as a USB drive).
- The Pico will restart with MicroPython installed, and the machine module will be available.

2. **Set Up Visual Studio Code**

- Install the Pico Extension and MicroPico vREPL for debugging. Check out [Pico Python SDK](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf).
- Connect to the Pico via USB and verify it’s detected in MicroPico vREPL shell.

### Hardware Wiring
Soil Moisture Sensor:

- Connect a capacitive soil moisture sensor (recommended to avoid corrosion):
- VCC to 3.3V (Pico pin 36)
- GND to GND (Pico pin 38)
- Analog output to GP26 (ADC0, Pico pin 31)

Power: Power the Pico via USB from the host device. Ensure stable 3.3V for the sensor.

[picture]

## Communication Flow
[picture]

## Pico Code to Read and Send Sensor Data
The Pico will read soil moisture and send the data over the serial connection (USB) to the host device. The code `main.py` formats the data as JSON for easy parsing by the host.

Upload `main.py` to Pico and make sure to **close the VSCode window for `main.py`** to release the serial port being used.

Use PuTTy to read inputs from Pico through serial port (COM3)

## Host Device Code to Communicate with Azure IoT Hub
The host device (e.g., your computer) will:
- Read serial data from the Pico using the pyserial library.
- Send the data to Azure IoT Hub using the azure-iot-device SDK.
- Receive direct method requests from Azure IoT Hub and send commands back to the Pico.
### 1. Set Up the Host Environment
Make sure you have `azure-iot-device pyserial` installed in your virtual environment.

Otherwise,
```Bash
pip install azure-iot-device pyserial
```
Ensure your Azure IoT Hub is set up with the device registered by substituting your own connection strings into `<connection_string>`. Check [Connect your Device to IoT Service](https://github.com/microsoft/IoT-For-Beginners/tree/main/2-farm/lessons/4-migrate-your-plant-to-the-cloud#connect-your-device-to-the-iot-service) to get your connection string.

### 2. Host Python Code
Make sure you have `host.py` on your computer.

**Find the Serial Port:**
- On Windows: Open **Device Manager**, look under “Ports (COM & LPT)” for the Pico’s COM port (e.g., `COM3`).
- On Linux/Mac: Run ls /dev/tty* to find the port (e.g., /dev/ttyACM0).
- Update `SERIAL_PORT` in the code to match your port.

## Run

## Credits
1. For Azure account and Azure IoT service setup: [IoT-For-Beginners]((https://github.com/microsoft/IoT-For-Beginners/tree/main/)
2. Fix the blocking problem in serial communication between host device and microcontroller: [link]()
3.  


