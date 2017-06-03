from os import system as call
from os import popen as get
import csv

I2C_MUX = '29'  # gpio29


with open('galileo_gpio_mapping.csv') as csv_file:
    table = csv.reader(csv_file)
    table = list(table)
    dgpio = [x for x in table if 'd' in x[0]]  # Digital GPIO ports
    agpio = [x for x in table if 'a' in x[0]]  # Analog GPIO ports
    for pin in dgpio:
        dgpio[int(pin[0].split("d")[-1])] = int(pin[1].split("gpio")[-1])
    for pin in agpio:
        agpio[int(pin[0].split("a")[-1])] = int(pin[1].split("gpio")[-1])


class GalileoDigital:
    IN = "in"
    OUT = "out"
    LOW = 0
    HIGH = 1

    def __init__(self, pin):
        print("setup pin " + str(pin) + " as gpio " + str(dgpio[pin]))
        self.unexport(pin)
        self.export(pin)
        self.setup(pin, 'out')

    def export(self, pin):
	print("EXPORTING PIN " + str(pin) + " AS " + str(dgpio[pin]))
        call("echo -n " + str(dgpio[pin]) + " > /sys/class/gpio/export")

    def unexport(self, pin):
        call("echo -n " + str(dgpio[pin]) + " > /sys/class/gpio/unexport")

    def setup(self, pin, mode):
        print("SETTING UP PIN " + str(pin) + " AS " + str(dgpio[pin]))
        call("echo -n " + mode + " > /sys/class/gpio/gpio" + str(dgpio[pin]) + "/direction")

    def output(self, pin, value):
        print("OUTPUTING PIN " + str(pin) + " AS " + str(dgpio[pin]))
        call("echo -n " + str(value) + " > /sys/class/gpio/gpio" + str(dgpio[pin]) + "/value")

    def read(self, pin):
        command = "cat /sys/class/gpio/gpio" + str(dgpio[int(pin)]) + "/value"
        return int(get(command).readlines()[0].split()[0])


class GalileoAnalog:
    def __init__(self, pin):
        if pin == 4 or pin == 5:
            call("echo -n " + IC2_MUX + " > /sys/class/gpio/uneport")
            call("echo -n " + I2C_MUX + " > /sys/class/gpio/export")
            call("echo -n out > /sys/class/gpio/gpio" + I2C_MUX + "/direction")
            call("echo -n 0 > /sys/class/gpio/gpio" + I2C_MUX + "/value")

        call("echo -n " + str(agpio[int(pin)]) + " > /sys/class/gpio/unexport")
        call("echo -n " + str(agpio[int(pin)]) + " > /sys/class/gpio/export")
        call("echo -n out > /sys/class/gpio/gpio" + str(agpio[pin]) + "/direction")
        call("echo -n 0 > /sys/class/gpio/gpio" + str(agpio[pin]) + "/value")


    def read(self, pin):
        command = "cat /sys/bus/iio/devices/iio\:device0/in_voltage" + str(pin) + "_raw"
        return int(get(command).readlines()[0])
