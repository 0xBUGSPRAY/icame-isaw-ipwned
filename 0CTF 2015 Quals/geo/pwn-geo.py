#!/usr/bin/python


import socket
import sys
import requests


verbose = False
if len(sys.argv) > 1:
    flg = sys.argv[1]
    flg = flg.lower()
    if flg.find("verbose") > -1 or flg == "v" or flg == "-v":
        verbose = True



US_LIST = ['United States', 'Yellowstone National Park', 'New York', 'Chicago', 'Honolulu', 'San Francisco', 'Mount Rushmore', 'Washington', 'United States of America', 'Las Vegas', 'Atlanta', 'Los Angeles']



def submit_place(place, s):
        found = False
        code = "NIL"

        if place == "Melbourne": place = "Australia"
        if place == "Hyde Park": place = "England"
        if place == "Tanzania, United Republic of": place = "Tanzania"
        if place == "Naples": place = "Italy"
        if place == "Volga": place = "Russia"
        if place == "Rickshaw capital of the world": place = "Dhaka"
        if place == "Holy See": place = "Vatican City"
        if place == "Which countries does Mekong River run across?": place = "china"
        if place == "Mount Olympus": place = "Greece"
        if place == "Alexandria": place = "Egypt"
        if place == "Lego": place = "Denmark"
        if place.find("Norfolk Island") > -1: place = "Australia"


        if place == "Georgia":
            code = "GE"
            found = True
        if place == "Korea (Democratic People's Republic of)":
            code = "KP"
            found = True
        if place == "Antarctica":
            code = "AQ"
            found = True
        if place == "Macedonia (the former Yugoslav Republic of)":
            code = "MK"
            found = True
        if place == "Virgin Islands (British)":
            code = "VG"
            found = True
        if place.lower() == "vancouver":
            code = "CA"
            found = True
        if place == "Micronesia (Federated States of)":
            code = "FM"
            found = True
        if place == "Korea (Republic of)":
            code = "KR"
            found = True



        if not found:
            code = "NIL"
            cache=""
            with open("cache.db", "r") as fp:
                cache = fp.read()
                fp.close()
            if cache.find(":") > -1:
              cache = cache.split("\n")[:-1]
              for item in cache:
                  place_cache, code_cache = item.split(":")
                  if place_cache == place:
                      print "\n\n\t [i] Cache hit for ", place, "\n\n"
                      code = code_cache
                      found = True
                      break



        if not found:
            code = "NIL"
            url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + place
            print "\n\n\t [i] requesting ", url, "\n\n"
            res=requests.get(url)
            data = res.json()
            locs = data['results'][0]['address_components']
            for item in locs:
                if found: break
                for typ in item['types']:
                    if typ.lower() == "country":
                        found = True
                        code = item['short_name']
                        cache = str(place) + ":" + str(code) + "\n"
                        if cache.find("Next") < 0:
                            with open("cache.db", "a") as fp:
                                fp.write(cache)
                                fp.close()
                        break



        print "\n\t [i] code: " + code
        if code == "US" and (not place in US_LIST):
            msg = "\n\t[*]  " + place + " (US) [Mannual Override]: "
            code = raw_input(msg)


        if not code[-1] == "\n": code = code + "\n"
        s.send(code)





def main():
    print "\n\n\t [i] connecting...\n\n"
    s = socket.create_connection(("202.112.26.111", 29995))
    q = ""
    while q.find(":") < 0:
        q += s.recv(1024)



    while True:
        print "\n\n\n[~] ", q, "\n\n\n"
        place = q.split("\n")[-1]
        place = place[:place.find(":")]

        n=place.find(",")
        if n > -1: place = place[:n]


        if place.find("?") > -1:
            if place.find("Andes") > -1:
                lst = ["Ecuador", "Chile", "Colombia", "Peru", "Argentina", "Bolivia", "Venezuela"]


            elif place.find("Amazon") > -1:
                lst = ["Colombia", "Peru", "Brazil"]


            elif place.find("Mekong") > -1:
                lst = ["Thailand", "Cambodia", "Laos", "China", "Myanmar", "Vietnam"]


            elif place.find("Himalayas") > -1:
                lst = ["India", "China", "Pakistan", "Nepal", "Bhutan"]


            elif place.find("Parana River") > -1:
                lst = ["Paraguay", "Brazil", "Argentina"]


            elif place.find("Alps") > -1:
                lst = ["France", "Austria", "Slovenia", "Liechtenstein", "Italy", "Germany", "Switzerland", "Monaco"]


            elif place.find("Congo River") > -1:
                lst = ['Angola', 'Burundi', 'Cameroon', 'CentralAfricanRepublic', 'Congo-Kinshasa', 'Gabon', 'Congo-Brazzaville', 'Rwanda', 'Tanzania', 'Zambia']


            elif place.find("Danube") > -1:
                lst = ['Germany', 'Austria', 'Slovakia', 'Hungary', 'Croatia', 'Serbia', 'Bulgaria', 'Romania', 'Moldova', 'Ukraine']


            elif place.find("Rhine River") > -1:
                lst = ['France', 'Austria', 'Liechtenstein', 'Netherlands', 'Germany', 'Switzerland']


            elif place.find("Nile") > -1:
                lst = ['Ethiopia', 'Sudan', 'Egypt', 'Uganda', 'Congo-Kinshasa', 'Kenya', 'Tanzania', 'Rwanda', 'Burundi', 'SouthSudan', 'Eritrea']


            elif place.find("Greater Caucasus") > -1:
                lst = ['Azerbaijan', 'Georgia', 'Russia']


            elif place.find("Apennine Mountains") > -1:
                lst = ['Italy', 'San Marino']


            elif place.find("Mississippi River") > -1:
                lst = ['United States']


            elif place.find("Rocky Mountains") > -1:
                lst = ['Canada', 'United States']






            else:
                inp = raw_input("\n\t [*] country list (comma separated) > ")
                lst = []
                if inp[-1] == '\n' or inp[-1] == " ": lst = lst[:-1]
                lst = inp.split(",")
                


            frst = True
            for country in lst:
                prompt = ""
                if not frst:
                    while prompt.find(":") < 0:
                        prompt += s.recv(1024)
                        prompt = prompt[:prompt.find(":")+1]
                frst = False
                print prompt
                print "\n\t [i] sending ", country, "...\n"
                submit_place(country, s)
        else:
            submit_place(place, s)

        q = ""
        while q.find(":") < 0:
            tmp = s.recv(1024)
            q += tmp
            q.replace("Next:", "Next>")
            if tmp.find("0CTF") > -1:
                print "\n\n\n\t [i] Flag found: ", tmp, "\n\n\n"
                sys.exit(0)


if __name__ == "__main__":
    main()
