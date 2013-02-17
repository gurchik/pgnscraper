#!/usr/bin/env python

# Your chess.com username (or, in other words, the user you want to download the 
# games for).
#
# Example:
#     USERNAME = "myusername"
USERNAME = "derekmaciel"

# Optional: Your chess.com password. You only need to supply this if you are a
# premium user and you wish to download games older than 6 weeks.
#
# Leave blank if you do not wish to take advantage of that
#
# Example with password:
#     PASSWORD = "mypassword"
# Example without password:
#     PASSWORD = ""
PASSWORD = ""

# The path you wish to save your PGNs to. If on Windows and using forward
# slashes, you must escape them. Do not add a trailing slash afterward
#
# Example on Windows:
#     USERNAME = "C:\\Users\\Me\\pgns"
# Example on Mac/Linux/Unix
#     USERNAME = "/home/me/pgns"
# Bad example with trailing slash
#    USERNAME = "/home/me/pgns/"
PGNPATH  = "/Volumes/Data/pgn"

import urllib2
from bs4 import BeautifulSoup
import re
from os.path import exists
from os import makedirs

def main():
    # If credentials supplied:
        # Sign in

    # For each game type
    types = ['echess', 'live_bullet', 'live_blitz', 'live_standard']
    
    saved = 0
    
    for gametype in types:
        
        html = get_file("http://www.chess.com/home/game_archive?show={0}&member={1}".format(gametype, USERNAME))
        soup = BeautifulSoup(html)
        
        # If no games are found of this type, go to the next type
        if soup.find("table", id="c14") == None: 
            print "No games found of type {0}".format(gametype)
            continue
            
        else:
            row = 0
            
            # For every game listed:
            while True:
                game = {}
            
                # If the row 's first column does not exist, the row must not exist
                # Go to the next game type
                if get_table_cell(soup, row, 1) == None:
                    break
                    
                info = get_game_info(soup, row, gametype)
                
                # Figure out where the PGN will go
                if gametype == 'echess':
                    if info["is960"] == True:
                        pgnroot = PGNPATH + "/correspondence/" + "chess960"
                    else:
                        pgnroot = PGNPATH + "/correspondence/" + "standard"
                elif gametype == 'live_bullet':
                    pgnroot = PGNPATH + "/live/" + "bullet"
                elif gametype == 'live_blitz':
                    pgnroot = PGNPATH + "/live/" + "blitz"
                elif gametype == 'live_standard':
                    pgnroot = PGNPATH + "/live/" + "standard"
                    
                path = pgnroot + "/" + info['year'] + "/" + info['month'] 
                if not exists(path):
                    makedirs(path)
                    
                # If the pgn does not exist, download it
                filename = "{0}_vs_{1}_{2}_{3}_{4}.pgn".format(info['white'], info['black'], info['year'], info['month'], info['day'])
                destination = path + "/" + filename
                if not exists(destination):
                    print "Downloading {0}".format(filename)
                    url = "http://www.chess.com/echess/download_pgn?id={0}".format(info['id'])
                    save_file(url, destination)
                    saved += 1
                
                row += 1
                
    print "Saved {0} files".format(saved)
                    
        
def get_file(url):
    response = urllib2.urlopen(url)
    return response.read()
    
def save_file(url, path):
    data = get_file(url)
    output = open(path, "wb")
    output.write(data)
    output.close
    
def get_table_cell(soup, row, col):
    # All cells in the table have an id of "c14_row{row number}_{col number}"
    expr = "c14_row{0}_{1}".format(row, col)
    tag = soup.find("td", id=re.compile(expr))
    return tag
    
def get_game_info(soup, row, gametype):
    # Cells are in the format "c14_row{ROW}_{COL}"
    
    info = {}
    
    # Check the images in the 0th column.
    cell = get_table_cell(soup, row, 0)
    for tags in cell.find_all("span"):
        info["is960"] = "c960" in tags["class"] # One of the span's classes would be "c960"
        info["analyzed"] = "computer" in tags["class"] # Would only show if signed in
                
    # White player
    cell = get_table_cell(soup, row, 1)
    info['white'] = cell.find_all("a")[1].get_text() #Player's name is the second link in the cell
        
    # Black player
    cell = get_table_cell(soup, row, 2)
    info['black'] = cell.find_all("a")[1].get_text() #Player's name is the second link in the cell
        
    # Number of moves
    cell = get_table_cell(soup, row, 5)
    info['moves'] = cell.get_text()
        
    # Game ID
    cell = get_table_cell(soup, row, 7)
    link = cell.find("a")['href'] # the ID is part of the URL of the link in the cell
    # /echess/ for corresp., /livechess/ otherwise
    if gametype == 'echess':
        info['id'] = link.replace("/echess/game?id=", "")
    else:
        info['id'] = link.replace("/livechess/game?id=", "")
                
    # Date
    cell = get_table_cell(soup, row, 6)
    date_str = cell.get_text() # the date is in mm/dd/yy and must be converted to yyyy, mm, and dd
    info['year'] = "20" + date_str.split("/")[2]
    info['month'] = "%02d" % int(date_str.split("/")[0]) # Add leading zero if needed
    info['day'] = "%02d" % int(date_str.split("/")[1]) # Add leading zero if needed
    
    return info

if __name__ == '__main__':
    main()

