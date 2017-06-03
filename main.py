from flask import Flask, url_for, render_template, request, flash, session, redirect, Response
import csv


'''# Galileo imports'''
from camera import VideoCamera
from galileo_gpio import GalileoDigital
from galileo_gpio import GalileoAnalog
''''''


app = Flask(__name__, static_url_path='')


dpins = {}  # Digital pins
apins = {}  # Analog pins

# GALILEO ONLY
feedstream = True

#feedstream = False


## Read setup pins ------------------


with open('pins.csv') as csv_file:
    pins_list = csv.reader(csv_file)
    pins_list = list(pins_list)

    for pin in pins_list:
        if 'analog' in pin[2]:
            apins[int(pin[0])] = {'name': pin[1], 'value': 0}
            Analog = GalileoAnalog(int(pin[0])) #GALILEO ONLY

        else:
            dpins[int(pin[0])] = {'name': pin[1], 'mode': pin[2], 'value': 0}
            GPIO = GalileoDigital(int(pin[0])) #GALILEO ONLY


## Main -----------------------------


@app.route('/')
def main():
    for pin in apins:
        print("updating Analog")
        apins[pin]['value'] = Analog.read(pin)
        if 'Temperatura' in apins[pin]['name']:
            apins[pin]['value'] = float(apins[pin]['value']) * 0.1075268817204301

    for pin in dpins:
        print("updating Digital")
        dpins[pin]['value'] = GPIO.read(pin)

    templateData = {
        'apins': apins,
        'dpins': dpins,
        'stream': feedstream
    }
    return render_template('index.html', **templateData)


@app.route("/api/<ptype>/<pin>/<action>")
def action(ptype, pin, action):
    pin = int(pin)
    if ptype == 'analog':
        deviceName = apins[pin]['name']

        '''
        if action == "read":
            state = Analog.read(pin)
            print(deviceName + " has value " + str(state))

        for pin in apins:
            print("updating Analog")
            apins[pin]['value'] = Analog.read(pins)
        '''

    elif ptype == 'digital':
        deviceName = dpins[pin]['name']

        if action == "on":
            GPIO.output(pin, GPIO.HIGH)
            print("Turned " + deviceName + " on")

        if action == "off":
            GPIO.output(pin, GPIO.LOW)
            print("Turned " + deviceName + " off")
        '''
        if action == "read":
            state = GPIO.read(pin)
            print(deviceName + " is " + str(state))
        '''

    for pin in apins:
        print("updating Analog")
        apins[pin]['value'] = Analog.read(pin)
        if 'Temperatura' in apins[pin]['name']:
            apins[pin]['value'] = apins[pin]['value'] * 0.1075268817204301

    for pin in dpins:
        print("updating Digital")
        dpins[pin]['value'] = GPIO.read(pin)

    templateData = {
        'apins': apins,
        'dpins': dpins,
        'stream': feedstream
    }
    return render_template('index.html', **templateData)


## Stream -------------------


@app.route('/stream')
def stream():
    return render_template('stream.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


## App run -------------------


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
