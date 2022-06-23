import re

def decoder(file):
    with open(file, "r") as file:
        data = file.read()

    organizedData = re.split("\n |\n", data)
    organizedData = organizedData[1:len(organizedData)-1]

    #Creates dictionary that we want to return
    returnData = {
                    "61444.54": {
                        "time": [],
                        "data": []},

                    "65265.32": {
                        "time": [],
                        "data": []},

                    "65265.4.1": {
                        "time": [],
                        "data": []},

                    "65265.4.5": {
                        "time": [],
                        "data": []}
                    }
    

    #Declare lists
    time = []
    dataID = []
    byteData = []
    numOfBytes= []

    #Parses CAN data into different lists
    for i in range(0, len(organizedData)):
        split = re.split("   |  ", organizedData[i])
        time.append(split[0][1:len(split[0])-1])
        dataID.append(split[2])
        numOfBytes.append(split[3][1:2])
        byteData.append(split[4])
    
    #Analyze CAN data
    for i in range(0, len(dataID)):
        
        #Calculate PGN
        if(len(dataID[i]) < 8):
            continue

        pgn = dataID[i][2:6]
        if(int(pgn[0:2],16) < int("F0",16)):
            pgn = pgn[0:2] + "00"
        pgn = str(int(pgn, 16))
        
        #Case for PGN 61444
        if(pgn == "61444"):

            #Checks the amount of bytes of the data
            if(int(numOfBytes[i]) < 8):
                continue

            #Splits the byte data into a list and calculates rpm
            bytes = byteData[i].split(" ")
            
            rpm = int(bytes[4] + bytes[3], 16)*0.125
            if(rpm < 8031.875):
                #Adds in data and time into dictionary
                returnData["61444.54"]["time"].append(float(time[i]))
                returnData["61444.54"]["data"].append(rpm)
        
        #Case for PGN 65265
        elif(pgn == "65265"):

            #Checks the amount of bytes of the data
            if(int(numOfBytes[i]) < 8):
                continue

            #Splits the byte data into a list and calculates wheelbased speed
            bytes = byteData[i].split(" ")
            
            speed = int(bytes[2] + bytes[1], 16)*0.00390625
            if(speed < 250.99609375):
                returnData["65265.32"]["time"].append(float(time[i]))
                returnData["65265.32"]["data"].append(speed)

            #Cruise control calculation
            cruiseControl = bin(int(bytes[3], 16))[2:].zfill(8)[0]
            returnData["65265.4.1"]["time"].append(float(time[i]))
            returnData["65265.4.1"]["data"].append(int(cruiseControl))

            #Brake switch calculation
            brakeSwitch = bin(int(bytes[3], 16))[2:].zfill(8)[4]
            returnData["65265.4.5"]["time"].append(float(time[i]))
            returnData["65265.4.5"]["data"].append(int(brakeSwitch))
    
            
    return returnData
