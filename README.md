pgnscraper
==========

Downloads your PGN files from chess.com

How do I use it?
========

pgnscraper depends on Beautiful Soup 4, a tarball of which can be downloaded [here](http://www.crummy.com/software/BeautifulSoup/bs4/download/). The `bs4` folder must be extracted to the same directory as `pgnscraper.py`. Your folder structure therefore would look like this:

    pgnscraper/
        pgnscraper.py
        bs4/
            ...
            
pgnscraper is written in Python so of course you will need that too. If you are running Mac OS X or Linux, chances are you already have it installed.

Open `pgnscraper.py` in a text editor and edit your `username`, `password` (optional), and `pgndir`.

You can run the script by simply executing `python “path/to/pgnscraper.py”`.

How does it work?
=========

You supply your chess.com username and the directory you want to save your PGNs to, and every time the script is run, it will download any PGNs you do not have into the directory. The script is limited to your games from the past 6 weeks and your past 50 games of each type.

The PGNs are organized by type (correspondence or live), then by subtype (standard/chess960) if a correspondence game, or by time control (standard/blitz/bullet) if a live game, and then by year and then month.

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
            standard/
                2013/
                    ...
            blitz/
                ...
            bullet/
                ...
            
PGNs are saved in the format `white_vs_black_yyyy_mm_dd.pgn`, where `white` is the name of the white player, `black` is the black player, `yyyy` is the year, `mm` is the month, and `dd` is the day. Keep in mind that the date is given by the date the game *completed*, which differs from downloading the PGN in the browser, which is dated by the date you *started* the game. It is done this way because that is the date given in the Game Archive, and it is quicker to use this date than to load a second page to get the starting date.

What is my password used for?
===================

Entering in your password is optional. The script will work without it. In the future, you will be able to enter your password to download the PGNs of the analyses you submitted. Also, premium users will be able to download games that are older than 6 weeks.