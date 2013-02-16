pgnscraper
==========

Downloads your PGN files from chess.com

How to use it
========

pgnscraper depends on Beautiful Soup 4, a tarball of which can be downloaded [here](http://www.crummy.com/software/BeautifulSoup/bs4/download/). The `bs4` folder must be extracted to the same directory as `pgnscraper.py`. Your folder structure therefore would look like this:

    pgnscraper/
        pgnscraper.py
        bs4/
            ...
            
pgnscraper is written in Python so of course you will need that too. If you are running Mac OS X or Linux, chances are you already have it installed.

Open `pgnscraper.py` in a text editor and edit your `username`, `password`, and `pgnpath`.

You can run the script by simply executing `python “path/to/pgnscraper.py”`.

How it works
=========

You supply your chess.com username and the directory you want to save your PGNs to, and every time the script is run, it will download any PGNs you do not have into the directory. The script is limited to your games from the past 6 weeks.

The PGNs are organized by time controls (coorespondence, standard, blitz, bullet), and then by year and then month.

    /pgns/  
        correspondence/  
            chess960/  
                2013/
                    01/
                        ....  
                    02/  
                    ...  
                2012/
                ...  
            standard/
                ....  
        live/
            ...
            
PGNs are saved in the format `white_vs_black_yyyy_mm_dd.pgn`, where `white` is the name of the white player, `black` is the black player, `yyyy` is the year, `mm` is the month, and `dd` is the day. Keep in mind that the date is given by the date the game *completed*, which differs from downloading the PGN in the browser, which is dated by the date you *started* the game. I chose to save it the way I did because that is the date that is given in the Game Archive on Chess.com and having to load the game to get the starting date would significant increase the bandwidth used.