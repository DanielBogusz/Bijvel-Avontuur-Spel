import random
import linecache
import ast
import os
import time
import re
import sys
import msvcrt

def screen_clear(t):
      # wacht voor een bepaalde tijd en schoon het scherm
      time.sleep(t)
      _ = os.system('cls')

# functie: laat langzaam de tekst op het scherm worden getyped,
# met "escape" kun je dit overslaan,
# een '~' symbool in de tekst betekend een nieuwe regel.
def TypText(text):
    rust = True
    # herhaal het schrijven naar scherm, voor de duur van de lengte van de tekst
    for i in range(0, len(text)):
        write = str(text[i])
        # als '~' symbool in de tekst word gelezen een nieuwe regel schrijven
        if write == '~':
            print()
            sys.stdout.flush() # zorgt dat er niet gewacht word met schrijven
        # schrijf het letter of teken naar het scherm
        else:
            print(write, end='')
            sys.stdout.flush()
        # als rust nog steeds waar is, willekeurig pauze nemen
        if rust == True:
            a = random.uniform(0.01, 0.12)
            time.sleep(a)
        # als de "Esc" toets word ingedrukt, is rust niet meer waaar
        if msvcrt.kbhit(): # detecteert toets aanslag
            if ord(msvcrt.getch()) == 27: # vergelijkt de waarde van de aanslag
                rust = False
                continue

# functie: die de ingevoerde text uitleest en zoekt naar
# antwoorden en/of instructies
def readtext (input_string,anwsers):
    done = 0
    score = 0
    # zet alle losse worden zonder lees- of speciale-tekens in een lijst
    text_list = re.findall(r'\w+', input_string)
    # de lijst is te lang...
    if len(text_list) > 15:
        TypText('Sorry, maar je zegt meer dan nodig is...\n')
    # als er alleen 'help' wordt geschreven geef dan een hint
    elif 'help' in map(lambda x: x.lower(), text_list):
        TypText(lijst[1])
    # kijk naar elk individueel woord in de lijst en vergelijk met mogelijk antwoord
    else:
        for i in range(0,len(anwsers)):
            if anwsers[i] in map(lambda x: x.lower(), text_list):
                score = score + 1
                if score >= 1:
                    done = 1
    bringback = [done,score]
    return bringback

# setup en introductie van het spel
# Lees het spel bestand
filename = "spel.txt"
number_of_lines = len(open(filename).readlines())
score = 0
maxscore = 0

# leest de eerste regel van het bestand en schrijft die naar het scherm
line = linecache.getline(filename, 1)
introductie = str(ast.literal_eval(line))
TypText(introductie)

# leest de tweede regel van het bestand en voert de individuele instructies uit
line = linecache.getline(filename, 2)
instructies = str(ast.literal_eval(line))
exec(instructies)
for i in range(0, len(lijst)):
    exec(lijst[i])

# voert de spelrouting uit totdat alle regels uit het spelbestand doorlopen zijn
for line_number in range(3, number_of_lines + 1):
    done = 0
    screen_clear(3)
    line = linecache.getline(filename, line_number)
    instructies = str(ast.literal_eval(line))
    # maakt een lijst van instructies
    exec(instructies)
    # de antwoorden zijn alles vanaf positie 5
    anwsers = list(lijst[4:])
    # maximale score is het aantal mogelijke antwoorden
    maxscore = maxscore + len(lijst[4:])
    pagina = lijst[0]
    TypText(f'Kijk op pagina {pagina} van je Bijbel:\n')
    TypText(lijst[3])
    # er wordt om antwoord gevraagd zolang er geen punt gescoord is
    while done == 0:
        TypText('Wat is je antwoord: ')
        invoer = input()
        takeback = (readtext(invoer,anwsers))
        score = score + takeback[1]
        done = takeback[0]
print(f'Je score is: {score} van het maximale: {maxscore}.')
