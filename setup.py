import csv
import sys

# Import pins from pins.csv
pins = {}
with open('pins.csv') as csv_file:
    pins_list = csv.reader(csv_file)
    pins_list = list(pins_list)
    for pin in pins_list:
        pins[int(pin[0])] = {'name': pin[1], 'state': pin[2]}


def terminate():
    print("Terminating Utilis Setup...")
    sys.exit()


# Main menu
menu = True
print("""
Utilis Alpha-0.1
""")
while menu:
    print("""
1 - Show pins
2 - Add a pin
3 - Remove a pin
4 - Quit
    """)
    menu = int(input(">> "))

    # 1 - Show pins dict
    if menu == 1:
        print("\nShowing all pins that are currently configured:\n")
        for pin in pins:
            print("Name:", pins[pin]['name'],
                  "\nState:", pins[pin]['state'], '\n')
        print("1 - Go back to main menu\n2 - Quit")
        menu = int(input(">> "))

    # 2 - Add pin - Appends new pin line to pins.csv
    elif menu == 2:
        csv_file = open('pins.csv', 'a')
        pin_number = input("\nPin number >> ")
        while not pin_number.isdigit():
            print("\That's not a valid input!")
            pin_number = input("\nPin number >> ")
        name = input("\nPin name >> ")
        while len(name) == 0:
            print("That's not a valid input!")
            name = input("\nPin name >> ")
        state = input("\nPin state (0 for GPIO.LOW - 1 for GPIO.HIGH) >> ")
        while state != '0' and state != '1':
            print("That's not a valid input!")
            state = input("\nPin state (0 for GPIO.LOW - 1 for GPIO.HIGH) >> ")
        if state == '0':
            state = 'GPIO.LOW'
        else:
            state = 'GPIO.HIGH'
        csv_file.write('\n' + ",".join([pin_number, name, state]))
        csv_file.close()

    # 3 - Remove pin - rewrite pins.csv without the desired option
    elif menu == 3:
        with open('pins.csv', 'w') as csv_file:
            pin_writer = csv.writer(csv_file)
            to_be_removed = int(input("\nPin number (If you want to go back insert 0) >> "))
            if to_be_removed >= 1 and to_be_removed <= 40:
                for pin in pins:
                    if pin != to_be_removed:
                        pin_writer.writerow(
                            [pin, pins[pin]['name'], pins[pin]['state']])
                if pins[to_be_removed]:
                    print("\nPin", to_be_removed, "has been deleted!\n")
                    del pins[to_be_removed]
            else:
                print("\nGoing back to main menu...\n")

    # 4 - Quit
    elif menu == 4:
        terminate()

    # Not a valid option
    else:
        print("That's not a valid option!")
