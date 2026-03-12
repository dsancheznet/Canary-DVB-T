import os, datetime, requests, bs4

def get_channel_array():
    """ Function to pair the channel page, filename and geographic region of the dataset """
    return [
            [ "https://www.muxtdt.com/canales-santa-cruz-tenerife/arona", 
              "es-Arona",
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-santa-cruz-tenerife/hierro", 
              "es-Hierro",
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-santa-cruz-tenerife/gomera", 
              "es-Gomera",
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-santa-cruz-tenerife/orotava", 
              "es-Orotava",
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-santa-cruz-tenerife/la-palma", 
              "es-La Palma",
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-santa-cruz-tenerife", 
              "es-Santa Cruz",
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-santa-cruz-tenerife/tenerife", 
              "es-Tenerife",
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-las-palmas/fuerteventura", 
              "es-Fuerteventura", 
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-las-palmas/gran-canaria", 
              "es-Gran Canaria", 
              "Canary Islands, Spain (🇮🇨 🇪🇸)" ],
            [ "https://www.muxtdt.com/canales-las-palmas/lanzarote", 
              "es-Lanzarote", 
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-las-palmas", 
              "es-Las Palmas", 
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-las-palmas/mogan", 
              "es-Mogan", 
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ],
            [ "https://www.muxtdt.com/canales-las-palmas/telde", 
              "es-Telde",
              "Canary Islands, Spain (🇮🇨 🇪🇸)" 
            ]
           ]

def get_name_array( tmpCHANNELS ):
    """ Extract the TV and RADIO channel list from the document and create an array """
    tmpRETURNARRAY = [ ] # create am empty array to hold the data
    for tmpCHANNEL in tmpCHANNELS: # iterate over all channels
        tmpRETURNARRAY.append( [ 
                                tmpCHANNEL.select_one( "td.channel-mux>span" ).text,
                                tmpCHANNEL.select_one( "td.channel-name" ).text,
                                tmpCHANNEL.select_one( "td.channel-hd, td.channel-4k, td.channel-audio" ).text,
                                ] ) # append data to the array
    return( tmpRETURNARRAY ) # return array

def extract_streams( tmpCHANNEL, tmpCHANNELARRAY, tmpFile ):
    """ Format the name_array as comments for the header of each channel """
    tmpINSERTCOMMA = False # variable to control the insertion of commas ( cosmetic use )
    print("# TV      : ", end="", file=tmpFile ) # wite string to file
    for CHN in tmpCHANNELARRAY: # iterate over channels
        if CHN[0]==tmpCHANNEL and CHN[2].upper( )!="RADIO": # is the actual channel NOT a radio channel?
            # YES
            if tmpINSERTCOMMA: # Is this the first channel?
                # NO
                print( f", {CHN[1]}", end="", file=tmpFile ) # write to file
            else:
                # YES
                tmpINSERTCOMMA = True # see above
                print( f"{CHN[1]}", end="", file=tmpFile ) # write to file
    tmpINSERTCOMMA = False # reset the variable for the next loop
    print("\n# RADIO   : ", end="", file=tmpFile ) # write to file
    for CHN in tmpCHANNELARRAY: # iterate over channels
        if CHN[0]==tmpCHANNEL and CHN[2].upper( )=="RADIO": # is the actual channel a radio channel?
            if tmpINSERTCOMMA: # is this the first channel?
                # NO
                print( f", {CHN[1]}", end="", file=tmpFile ) # print to file
            else:
                # YES
                tmpINSERTCOMMA = True # see above
                print( f"{CHN[1]}", end="", file=tmpFile ) # insert into file
    print( "", file=tmpFile ) # write to file

def get_data_from( tmpExtractFrom, tmpFilename, tmpNameString ):
    """ Main function to compose an TVHeadend scan file for the selected regions """
    print(f"Creating file {tmpFilename}...", end="") # print progress information
    tmpFile = open( tmpFilename, 'w') # get a filehandle
    tmpCurrentDate = datetime.datetime.now() # get current date 
    tmpDateString  = tmpCurrentDate.strftime( "%d %b %Y" ).upper() # format the date string
    tmpBANDWIDTH   = "8" # Bandwidth in MHz since the HTML site does not specify
    tmpURL         = tmpExtractFrom # Locally store URL to scrape
    tmpHTML        = requests.get( tmpURL ) # Scrape the page data
    tmpSOUP        = bs4.BeautifulSoup( tmpHTML.content, "html.parser") # extract data with bs4
    print( "# ✂----------- Author Info ----------", file=tmpFile )
    print("# ", file=tmpFile )
    print("# Edited by D.Sánchez", file=tmpFile )
    print(f"# Updated             : {tmpDateString}", file=tmpFile ) # insert tmpDateString variable
    print("# Github              : https://github.com/dsancheznet", file=tmpFile )
    print("# Homepage            : https://www.dsanchez.net/", file=tmpFile )
    print(f"# Region              : {tmpNameString}", file=tmpFile) # insert tmpNAmeString variable
    print(f"# {tmpSOUP.select_one("div.cobertura").text.replace("cobertura:", "cobertura :") }", file=tmpFile ) # insert "ámbito de cobertura"
    print("# ", file=tmpFile )
    print("# ✂----------- Channel List ----------", file=tmpFile )
    print(" ", file=tmpFile )
    for tmpCHNDATA in tmpSOUP.select("table.frequency" ): # loop over frequency table
        tmpCHNARRAY = tmpCHNDATA.select("td") # select td subset
        if len( tmpCHNARRAY )>3: # do we actually have anyh data?
            # YES
            tmpCHANNEL        = tmpCHNARRAY[1].text[0:2] # channel number and frequency
            tmpFREQUENCY      = str( int( tmpCHANNEL ) * int( tmpBANDWIDTH ) + 306 ) # calculate frequency
            tmpMODULATION     = f"{tmpCHNARRAY[3].text[2:]}/{tmpCHNARRAY[3].text[0:2]}" 
            tmpCODE_RATE_HP   = f"{tmpCHNARRAY[4].text[0:3]}"
            tmpGUARD_INTERVAL = f"{tmpCHNARRAY[4].text[4:]}"
            print(f"# Channel : {tmpCHANNEL}", file=tmpFile ) # insert tmpCHANNEL variable
            extract_streams( tmpCHANNEL, get_name_array( tmpSOUP.select("table.channels tr") ), tmpFile ) 
            print(f"[CHANNEL {tmpCHANNEL}]", file=tmpFile ) # insert tmpCHANNEL variable ( again )
            print(f"    DELIVERY_SYSTEM = DVBT2", file=tmpFile )
            print(f"    FREQUENCY = {tmpFREQUENCY}000000", file=tmpFile )
            print(f"    BANDWIDTH_HZ = {tmpBANDWIDTH}000000", file=tmpFile )
            print(f"    CODE_RATE_HP = {tmpCODE_RATE_HP}", file=tmpFile )
            print(f"    CODE_RATE_LP = NONE", file=tmpFile )
            print(f"    MODULATION = {tmpMODULATION}", file=tmpFile )
            print(f"    TRANSMISSION_MODE = 8K", file=tmpFile )
            print(f"    GUARD_INTERVAL = {tmpGUARD_INTERVAL}", file=tmpFile )
            print(f"    HIERARCHY = NONE", file=tmpFile )
            print(f"    INVERSION = AUTO", file=tmpFile )
            print("", file=tmpFile )
    print("Done.")

if __name__ == '__main__':
    CHANNEL_INFO = get_channel_array( )

    for channel in CHANNEL_INFO:
        print( "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=" )
        print( f"→  Analyzing \033[33m{channel[0]}\033[0m Filename \033[36m{channel[1]}\033[0m" )
        print( "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=" )
        if os.access( channel[1], os.F_OK ): # Does the file already exist and is writeable?
            print(f"Found an old copy of {channel[1]}" )
            print("Deleting...", end="")
            #YES
            os.remove( channel[1] ) # Delete file
            print("Done.")
        get_data_from( channel[0], channel[1], channel[2] )
    print( "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=" )
