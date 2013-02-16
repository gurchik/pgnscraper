#!/usr/bin/env python

USERNAME = "derekmaciel"
PASSWORD = ""
PGNPATH  = "/Volumes/Data/pgn"

import urllib2
from bs4 import BeautifulSoup
import re
from os.path import exists
from os import mkdir

def main():
    # If credentials supplied:
        # Sign in

    # For each game type
    #types = ['echess', 'live_bullet', 'live_blitz', 'live_standard']
    types = ['echess']
    for gametype in types:
        
        html = get_html("http://www.chess.com/home/game_archive?show={0}&member={1}".format(gametype, USERNAME))
        soup = BeautifulSoup(html)
        
        # If no games are found of this type, go to the next type
        if soup.find("table", id="c14") == None: 
            print "No games found of type {0}".format(gametype)
            continue
            
        else:
            row = 0
            saved = 0
            
            # For every game listed:
            while True:
                game = {}
            
                # If the row does not exist, go to the next game type 
                if soup.find("td", id=re.compile("c14_row{0}".format(row))) == None:
                    break
                    
                # Cells are in the format "c14_row{ROW}_{COL}"
                # where {ROW} starts from 0 but {COL} starts from 1
                
                game['type'] = gametype
                
                # White player
                cell = soup.find("td", id=re.compile("c14_row{0}_1".format(row)))
                game['white'] = cell.find_all("a")[1].get_text() #Player's name is the second link in the cell
        
                # Black player
                cell = soup.find("td", id=re.compile("c14_row{0}_2".format(row)))
                game['black'] = cell.find_all("a")[1].get_text() #Player's name is the second link in the cell
        
                # Number of moves
                cell = soup.find("td", id=re.compile("c14_row{0}_5".format(row)))
                game['moves'] = cell.get_text()
        
                # Game ID
                cell = soup.find("td", id=re.compile("c14_row{0}_7".format(row)))
                link = cell.find("a")['href'] # the ID is part of the URL of the link in the cell
                game['id'] = link.replace("/echess/game?id=", "") # /echess/ for corresp., /livechess/ otherwise
                
                # Date
                cell = soup.find("td", id=re.compile("c14_row{0}_6".format(row)))
                date_str = cell.get_text() # the date is in mm/dd/yy and must be converted to yyyy_mm_dd
                year = "20" + date_str.split("/")[2]
                month = "%02d" % int(date_str.split("/")[0]) # Add leading zero if needed
                day = "%02d" % int(date_str.split("/")[1]) # Add leading zero if needed
                game['date'] = "{0}_{1}_{2}".format(year, month, day)
                
                
                pgnroot = PGNPATH + "/correspondence"
                if not exists(pgnroot):
                    mkdir(pgnroot)
                    
                path = pgnroot + "/" + year
                if not exists(path):
                    mkdir(path)
                
                path = path + "/" + month
                if not exists(path):
                    mkdir(path)
                    
                # If the pgn does not exist, download it
                filename = "{0}_vs_{1}_{2}_{3}_{4}.pgn".format(game['white'], game['black'], year, month, day)
                if not exists(path + "/" + filename):
                    print "Downloading {0}".format(filename)
                    output = open(path + "/" + filename, "wb")
                    output.write(get_html("http://www.chess.com/echess/download_pgn?id={0}".format(game['id'])))
                    output.close()
                    saved += 1
                    
                
                row += 1
                
    print "Saved {0} files".format(saved)
                    
        
        
def get_html(url):
    response = urllib2.urlopen(url)
    return response.read()

if __name__ == '__main__':
    main()

