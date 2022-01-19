import os
import ipinfo
import gmplot
import sys

import config

latitude = []
longitude = []


def find_between(s):
    try:
        start = s.index( "(" ) + len( "(" )
        end = s.index( ")", start )
        return s[start:end]
    except ValueError:
        return ""

def main(argv):
    stream = os.popen('traceroute -m 15 -q 2 -w 2 ' + argv[0])
    output = stream.readlines()

    # output[0]
    for out in output:
        ip_address = find_between(out)
        print(ip_address)
        handler = ipinfo.getHandler(config.access_token)
        details = handler.getDetails(ip_address)
        if(hasattr(details, 'latitude')):
            if(details.latitude != None):
                latitude.append(float(details.latitude))
                longitude.append(float(details.longitude))
    print(latitude)
    print(longitude)
    gmap = gmplot.GoogleMapPlotter(latitude[0], longitude[0], 10, apikey= config.mapsAPIkey)

    gmap.scatter( latitude, longitude, c = "black", size = 250, marker = False)
    gmap.marker( latitude[0], longitude[0], c = "red", size = 250, marker = False, title='start')
    gmap.plot(latitude, longitude, 'black', edge_width = 2.5)

    gmap.draw( "./samplemaps/" + argv[0] + ".html" )

if __name__ == "__main__":
   main(sys.argv[1:])