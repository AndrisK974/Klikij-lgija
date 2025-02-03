from pynput.mouse import Listener
import screeninfo
import time

# Tuvastame ekraani suuruse
ekraan = screeninfo.get_monitors()[0]
ekraan_pikkus = ekraan.width
ekraan_laius = ekraan.height

# Jagame ekraani neljaks kastiks
MIDDLE_X = ekraan_pikkus // 2
MIDDLE_Y = ekraan_laius // 2

# Defineerime 4 ala nimetuse järgi
alad = {
    "Vasak-Ülemine": (0, MIDDLE_X, 0, MIDDLE_Y),           # Vasak ülemine
    "Parem-Ülemine": (MIDDLE_X, ekraan_pikkus, 0, MIDDLE_Y),  # Parem ülemine
    "Parem-Alumine": (MIDDLE_X, ekraan_pikkus, MIDDLE_Y, ekraan_laius),  # Parem alumine
    "Vasak-Alumine": (0, MIDDLE_X, MIDDLE_Y, ekraan_laius)  # Vasak alumine
}

# Õige järjekord. Selles järjestuses klikkides teeb programm tegevuse
õige_järjekord = ["Vasak-Ülemine", "Parem-Ülemine", "Parem-Alumine", "Vasak-Alumine"]

# Salvestame klikid massiivi
clicks = []

# Seame ajapiirangu, mis aja jooksul tuleb klikid teha (praegu 5 sekundit)
ajapiirang = 5

# Taimer on 0
taimer = None

# Kontrollime, kas klikkide järjekord on õige
def kontrolli_järjekorda():
    global clicks
    if len(clicks) == len(õige_järjekord):
        klikitud_alad = [click[0] for click in clicks]
        if klikitud_alad == õige_järjekord:
            print("Õnnestus!")
            clicks = []  # Tühjendame massiivi

# Kontrollime, millises piirkonnas hiireklik toimus
def kuhu_klikkisin(x, y):
    for ala, (x1, x2, y1, y2) in alad.items():
        if x1 <= x < x2 and y1 <= y < y2:
            return ala
    return None

# Hiireklikkide jälgimine
def on_click(x, y, hiirenupp, vajutus):
    global taimer, clicks

    if vajutus:
        if taimer is None:
            taimer = time.time()  # Kui esimene klikk on tehtud, käivitame taimeri

        # Kontrollime, kas ajalimiit on täis
        if time.time() - taimer > ajapiirang:
            print("Aeg on läbi, alusta uuesti!")
            clicks.clear()  # Kui aeg saab otsa, tühjendame klikkide massiivi
            taimer = None  # Nullime taimeri

        ala = kuhu_klikkisin(x, y)
        if ala:
            # Kui klikid ei ole õiges järjekorras, tühjendame massiivi ja alustame uuesti
            if len(clicks) > 0 and ala != õige_järjekord[len(clicks)]:
                print("Vale järjekord! Alustame otsast peale.")
                clicks.clear()  # Tühjendame klikid
                taimer = None  # Nullime taimeri

            clicks.append((ala, time.time()))  # Salvestame klikitud ala ja aja
            print(f"Klikkisid: {ala}") # Prindime konsooli, kuhu klikiti
            kontrolli_järjekorda() # Käivitame järjekorra kontrollimise funktsiooni

# Hiireklikkide kuulaja
with Listener(on_click=on_click) as listener:
    listener.join()
