import serial

SERIAL_PORT = "/dev/serial0"
running = True

# In the NMEA message, the position gets transmitted as:
# DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
# the minutes. However, I want to convert this format to the following:
# DD.MMMM. This method converts a transmitted string to the desired format
def formatDegreesMinutes(coordinates, digits):
    
    parts = coordinates.split(".")

    if (len(parts) != 2):
        return coordinates

    if (digits > 3 or digits < 2):
        return coordinates
    
    left = parts[0]
    right = parts[1]
    degrees = str(left[:digits])
    minutes = str(right[:3])

    return degrees + "." + minutes

def getPositionData(gps):
    while True:
        data = gps.readline().decode().strip()
        message = data[0:6]
        if message == "$GPRMC":
            parts = data.split(",")
            if parts[2] == 'V':
                print("GPS receiver warning")
            else:
                longitude = formatDegreesMinutes(parts[5], 3)
                latitude = formatDegreesMinutes(parts[3], 2)
                print("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
                return longitude, latitude


gps = None
def init_gps():
    global gps
    print("Application started!")
    gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)

def stop_gps():
    global gps
    gps.close()
    print("Application closed!")

