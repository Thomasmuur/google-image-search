# Import onze dependencies

# pip install python-tk
from tkinter import *

# pip install Pillow
from PIL import Image, ImageTk
import requests
import json
import io
from io import BytesIO
import urllib
import random

# Je google token, hierdoor weet google wie de request maakt.
# Hoe vraag je er eentje aan? Dit leer je op https://developers.google.com/places/web-service/get-api-key
google_token = 'AIzaSyA3WWo7gBxUpkhCBt4WfWpZ7Xrc6-Mo2Ac'

# In deze list worden alle labels gezet die momenteel op het scherm staan.
selected_labels = []

# Hier maken wij de functie search aan,
# hier kan een parameter debug (met als default None) gestuurd worden
# Dit gebruiken wij nergens voor, maar het Enter event geeft een parameter door
# anders krijg je een error
def search(debug = None):
    # Als eerst willen we de hele lijst weghalen, (we gaan namelijk nieuwe afbeeldingen laten zien)
    # Met een for loop, gaan wij door de list heen. We kunnen dan een item uit de lijst selecteren met selected_label
    for selected_label in selected_labels:
        # met de destroy functie halen wij de afbeelding van het scherm
        selected_label.destroy()

    # door get() op onze input te gebruiken halen wij de ingevulde data er uit.
    search_value = input.get()
    # We maken een HTTP request naar de google api
    # Hierbij geven wij onze unieke google token door, de zoektermen en watvoor zoekterm het is, een textquery dus.
    # met de .json() functie zetten wij dit op in een JSON.
    search = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key=' + google_token + '&input=' + search_value + '&inputtype=textquery').json()
    # Controleer hoeveel resultaten er zijn in de candidates list.
    # als dit er 0 zijn, dan plaatsen wij een error
    if len(search['candidates']) == 0:
        # We maken een label aan, dit is simpelweg tekst
        # Wij storen dit in de variable "error"
        error = Label(app, text='Die plaats is niet gevonden!')
        # We maken een plekje klaar voor de tekst.
        error.grid()
        # Wij stoppen de text in de "selected_labels" tekst
        # zodat wij deze later weer kunnen verwijderen bij het volgende zoekresultaat
        selected_labels.append(error)
        # Wij plaatsen de error text op het scherm.
        root.mainloop()
        # Wij stoppen de code.
        return

    # Wij kunnen in de array dingen selecteren door het "toegangs punt" tussen [] te zetten.
    # Dus: Wij gaan de list "candidates" in > met de 0 pakken wij de eerst uit de list > in deze list zit een dictionary, we willen de "place_id" hier uit halen.
    # simpelweg, we pakken het eerste resultaat pakken
    place_id = search['candidates'][0]['place_id']

    # Met dit place id kunnen wij een nieuwe HTTP request maken naar google
    # Hierbij geven wij weer onze unieke google token door
    # Ook geven wij nu de place ID door, deze hebben wij bij de vorige request verkregen.
    image_id = requests.get('https://maps.googleapis.com/maps/api/place/details/json?key=' + google_token + '&placeid=' + place_id).json()
    # Hier krijgen wij een dictionary terug genaamd "result"
    # Deze gaan wij in, hierin zit een list genaamd "photos", wij willen weten hoeveel foto's hierin zitten, dit doen we met de len functie.
    images_amount = len(image_id['result']['photos'])
    # Met random.randint maken wij een willekeurig getal aan tussen de 0 en het aantal afbeeldingen.
    # Omdat je geen file kan geven in een JSON, werkt google met een "reference"
    # Wij gaan de "result" dictionary in, dan de "photos" list, hier pakken wij vervolgens een random dictionary uit, in deze dictionary staat een photoreference, deze pakken wij.
    reference = image_id['result']['photos'][random.randint(0, images_amount - 1)]['photo_reference']

    # Met deze reference kunnen wij een URL naar de afbeelding maken
    # Wij geven onze token door, de reference die wij zonet kregen, een maximale breedte en maximale hoogte.
    image_url = 'https://maps.googleapis.com/maps/api/place/photo?key=' + google_token + '&photoreference=' + reference + '&maxheight=600&maxwidth=800'

    # Met urllib openen wij de file die op de url staat in de variable "image_url"
    u = urllib.request.urlopen(image_url)
    # Vervolgens lezen wij de data die we ontvangen
    raw_data = u.read()
    # en sluiten wij de request.
    u.close()

    # We converten dit naar Bytes en openen deze afbeelding vervolgens als een afbeelding.
    im = Image.open(BytesIO(raw_data))
    # Met imageTK.PhotoImage converten wij dit naar een type dat wij kunnen inladen met Tkinter(Ons applicatie systeem)
    image = ImageTk.PhotoImage(im)
    # Wij laden de afbeelding in als een label, aangezien dit de enige optie is die Tkinter ons geeft.
    label = Label(image=image)
    # Wij stoppen de afbeelding in de list "selecte_labels" zodat wij deze later weer kunnen weghalen.
    selected_labels.append(label)
    # Wij maken het plekje klaar voor de afbeelding
    label.grid()

    # We renderen alles op het scherm van de gebruiker
    root.mainloop()

# Hier maken we de root variable aan
# dit is een instantie van de Tkinter dependency
# Tkinter zorgt ervoor dat wij een interface kunnen laten zien aan de gebruiker.
root = Tk()

# Hier geven we de applicatie een titel.
root.title('Places Locator')
# Hier bepalen wij hoeveel pixels bij hoeveel pixels het programma moet openen.
root.geometry('800x600')

# Hier maken wij het frame aan, hierbij geven wij ons root element door aan de functie.
app = Frame(root)
# Met grid maken wij het plekje klaar voor het frame
app.grid()

# Hier maken wij een text input, hier kan de gebruiker iets invullen
# Bij deze functie geven wij onze app door aan de functie.
input = Entry(app)
# Met grid maken wij weer het plekje klaar.
input.grid()

# Wij zorgen ervoor dat als de gebruiker Enter (<Return>) drukt, er ook word gezocht.
input.bind('<Return>', search)

# Wij maken een button aan, hierbij geven wij onze app door
# Daarnaast geven wij de tekst voor op de knop door
# En wij geven door welke functie er moet worden uitgevoerd wanneer op de knop word gedrukt.
button = Button(app, text = 'Search', command=search)
# Met grid maken wij weer het plekje klaar
button.grid()

# door de mainloop functie op root te gebruiken zet je alles in het venster.
root.mainloop()
