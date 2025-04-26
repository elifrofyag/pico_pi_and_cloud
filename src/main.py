from machine import Pin, ADC
import sys
import ujson
import utime
import select

led = Pin("LED", Pin.OUT)


SOIL_MOISTURE_PIN = 26


soil = ADC(Pin(SOIL_MOISTURE_PIN))
def read_soil_moisture():
    adc_value = soil.read_u16() >> 4 
    return adc_value


selpoll = select.poll()
selpoll.register(sys.stdin, select.POLLIN)

stop = False
command = ""

try:
    while not stop:
        # send telemetry
        soil_moisture = read_soil_moisture()
        telemetry = {"soil_moisture": soil_moisture}
        print(ujson.dumps(telemetry))

        # check for incoming commands (non-blocking) (in this case: led_on/led_off)
        if selpoll.poll(0):
            try:
                line = sys.stdin.readline().strip()
                if line:
                    if line == "led_on":
                        led.on()
                        response = {"status": "success", "led_state": led.value()}
                    elif line == "led_off":
                        led.off()
                        response = {"status": "success", "led_state": led.value()}
                    elif line == "exit":
                        response = {"status": "success", "message": "Exiting"}
                        stop = True
                    else:
                        response = {"status": "error", "message": "Unknown command"}
                    print(ujson.dumps(response))
            except Exception as e:
                print(ujson.dumps({"status": "error", "message": str(e)}))

        utime.sleep(2)

except KeyboardInterrupt:
    led.off()
    


