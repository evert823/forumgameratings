import random
from datetime import datetime, timedelta

def surnames():
    return ["Smittoniaya", "Johnsonessuh", "Williamzz", "Joneysah", "Brownows",
            "McQuirklebee", "VonWobbleton", "Fizzlebottom", "Snickerdoodle", "Bumblethorpe",
            "Twistlepuff", "Crankleford", "Zigglewitz",
            "Kern", "van , Peter", "Leia", "Atreides", "X"]

def first_names():
    return ["Columbo", "Mickey", "Butlerella", "Godfather", "Avrana", "Hobbit", "Fish",
            "Wanda", 'Pjotr , not "Iljitsj"', "Casper", "Mefisto", "Arthur",
            "Harold", "Fellow", "Wally", "Pubby"]

def full_names():
    return [f"{first} {surname}" for first in first_names() for surname in surnames()]

def tournament_names():
    return ["Mother of all tournaments", "classic_blunders", "not for the faint of pawn",
            "Final Duel", "The Patzers strike back", "Rook disconnecT", 'The inheritage of "Magnaly Carlssov"',
            "Clash of the pawnthrowers", "Almost-galactical championship", "This Is Not A Variant",
            "Terraform64 winner's bracket", "Terraform64 looser's bracket", "Terraform64 draw-ish non-heroes bracket"]

def random_date():
    start_date = datetime(1995, 1, 1)
    end_date = datetime(2025, 7, 1)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def add_text_qualifier(mystring):
    if ',' in mystring or '"' in mystring:
        mystring = '"' + mystring.replace('"', '') + '"'
    return mystring

def gamelist_headers():
    return "Date of game,White player,Black player,Game result,\"Game, or Tournament description\"\n"

def ratinglist_headers():
    return "Full name of player,Rating\n"

def random_result(player01, player02):
    mytoken = random.randint(0, 99)
    if player01 == player02:
        return '0.5-0.5'
    elif player01[:1] == player02[:1]:
        if mytoken < 60:
            return '0.5-0.5'
        elif mytoken < 82:
            return '1-0'
        else:
            return '0-1'
    elif player01 > player02:
        if mytoken < 60:
            return '1-0'
        elif mytoken < 85:
            return '0.5-0.5'
        else:
            return '0-1'
    else:
        if mytoken < 60:
            return '0-1'
        elif mytoken < 85:
            return '0.5-0.5'
        else:
            return '1-0'

def random_game():
    player01 = random.choice(full_names_list)
    player02 = player01
    while player02 == player01:
        player02 = random.choice(full_names_list)
    mydate = random_date()
    tournament = random.choice(tournament_names())
    myresult = random_result(player01, player02)
    player01 = add_text_qualifier(player01)
    player02 = add_text_qualifier(player02)
    tournament = add_text_qualifier(tournament)
    s = f"{mydate.strftime('%Y-%m-%d')},{player01},{player02},{myresult},{tournament}"
    return s

def create_testfile_gamelist():
    file1 = open('./inputdata/gamelist_01.csv', 'w', encoding='utf-8')
    file1.write(gamelist_headers())
    for i in range(10000):
        s = random_game()
        file1.write(s + '\n')
    file1.close()
    sort_file('./inputdata/gamelist_01.csv')

def create_testfile_ratinglist():
    file1 = open('./inputdata/ratinglist_initial.csv', 'w', encoding='utf-8')
    file1.write(ratinglist_headers())

    for name in full_names_list:
        mytoken = random.randrange(0, 99)
        if mytoken < 83:
            myrating = random.randrange(1150, 3499)
            myname = add_text_qualifier(name)
            file1.write(f"{myname},{myrating}\n")
    file1.close()

def sort_file(path_and_name):
    file1 = open(path_and_name, 'r', encoding='utf-8')
    lines = file1.readlines()
    file1.close()
    header = lines[0]
    sorted_lines = sorted(lines[1:])
    file2 = open(path_and_name, 'w', encoding='utf-8')
    file2.write(header)
    file2.writelines(sorted_lines)
    file2.close()

full_names_list = full_names()
full_names_list.sort()
create_testfile_gamelist()
create_testfile_ratinglist()
