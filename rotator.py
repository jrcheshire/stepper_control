# Stepper motor rotation control
# James Cheshire 2017

import sys, serial, glob, time, csv, getopt, re

inputString = ""
angle = 0
speed = 0
numRotations = 0

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def main(argv):

    global inputString
    global angle
    global speed
    global numRotations
    
    try:
        opts, args = getopt.getopt(argv, "hr:",["rotate="])
    except getopt.GetoptError:
        print('Usage:\nrotator.py -r <angle> \nrotator.py -r <speed,# rotations>\nSpeed is measured in degrees/second')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage:\nrotator.py -r <angle> \nrotator.py -r <speed,# rotations>\nSpeed is measured in degrees/second')
            sys.exit()
        elif opt in ("-r", "--rotate"):
            if arg.isdigit():
                # angle rotation
                angle = int(arg)
                inputString = '0' + arg
            elif re.match("^\d+?\,\d+?$", arg):
                # speed, rots rotation
                temp = 0
                speed = ''
                numRotations = ''
                for i in range(len(arg)):
                    if arg[i] == ',':
                        temp = 1
                    elif not temp:
                        speed += arg[i]
                    elif temp:
                        numRotations += arg[i]
                speed = int(speed)
                numRotations = int(numRotations)
                if speed > 20 or speed <= 0:
                    sys.exit('Speed must be between 0 and 20 deg/s')
                inputString = '1' + str(speed) + ',' + str(numRotations)
            else:
                sys.exit("Error: argument must be integer or integers of the form \"angle\" or \"speed, # rotations\"")

if __name__ == "__main__":
    main(sys.argv[1:])
    
    # this is probably bad style but the logic below wouldn't communicate with the Arduino consistently when in the main function, I assume due to black magic

    if inputString == "":
        sys.exit('Usage:\nrotator.py -r <degrees>\nrotator.py -r <speed,# rotations>')

    try:
        ser = serial.Serial(port=serial_ports()[0], baudrate=115200, timeout=3)
    except:
        sys.exit('Failed to connect to serial port')

    print('Connected to serial port: ' + serial_ports()[0])
    print('Communicating with Arduino...')

    time.sleep(2) # this is necessary to prevent the Arduino initialization from blocking communication
    junk = ser.readline().strip()
    if not int(inputString[0]):
        print('\nRotating by ' + str(angle) + ' degrees')
        for i in range(len(inputString)):
            ser.write(chr(int(inputString[i])).encode('ascii'))
            time.sleep(0.5)
            ser.flush()
            time.sleep(0.5)
    else:
        print('\nRotating at ' + str(speed) + ' degrees/second for ' + str(numRotations) + ' rotations')
        for i in range(len(inputString)):
            try:
                ser.write(chr(int(inputString[i])).encode('ascii'))
                time.sleep(0.5)
                ser.flush()
                time.sleep(0.5)
            except:
                ser.write(inputString[i].encode('ascii'))
                time.sleep(0.5)
                ser.flush()
                time.sleep(0.5)
