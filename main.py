import pyautogui
import questionary
import time
import numpy as np
import threading
import pyaudio

morseCodeDictionary = {
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....",
    "i": "..", "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---", "p": ".--.",
    "q": "--.-", "r": ".-.", "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-",
    "y": "-.--", "z": "--..",

    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.",

    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.", "!": "-.-.--", "/": "-..-.",
    "(": "-.--.", ")": "-.--.-", "&": ".-...", ":": "---...", ";": "-.-.-.", "=": "-...-",
    "+": ".-.-.", "-": "-....-", "_": "..--.-", "$": "...-..-", "@": ".--.-.",
    "à": ".--.-", "è": ".-..-", "é": "..-..", "ù": "..--", "ò": "---.", "ì": "..--..",
    "ç": "-.-..-", "é": "..-..", "ñ": "--.--", "°": ".-.-.-"
}


def ask(prompt):
    try:
        answer = questionary.text(prompt).ask()
        if answer is None:
            print("Exiting...")
            exit(0)
        return answer
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        exit(0)


def askWPM():
    while True:
        wpm = ask("Insert Words Per Minute:")

        try:
            wpmI = int(wpm)
            if (wpmI < 1 or wpmI > 100):
                print("Error: WPM must be greater than 0 and lower than 101")
                continue
            return wpmI
        except ValueError:
            print("Error: WPM has to be an integer")


def askText():
    while True:
        text = ask("Insert text to convert to morse code:")

        if (not text):
            print('Error: text cannot be empty')
            continue
        return text


def askSound():
    while True:
        sound = str(ask("Activate sound? (yes(Y) or no(n)) [Leave blank for no]")).lower()

        if(sound):
            if (sound[0] not in ['y', 'n']):
                print('Error: activate sound can only be yes(Y) or no(n)')
                continue
            sound = True if sound[0] == 'y' else False
        else: sound = False
        return sound

def askAllKeys():
    while True:
        allKeys = str(ask("Also use Num Lock and Scroll Lock? (yes(Y) or no(n)) [Leave blank for no]")).lower()

        if(allKeys):
            if(allKeys[0] not in ['y', 'n']):
                print('Error: Use all keys can only be yes(Y) or no(n)')
                continue

            allKeys = True if allKeys[0] == 'y' else False
        else: allKeys = False
        return allKeys

# This function (beep) is derived from PySine (https://github.com/lneuhaus/pysine) and is licensed under the MIT license.
def beep(duration):
    PyAudio = pyaudio.PyAudio

    bitrate = 96000
    frequency = 550.0
    length = duration

    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1), channels=1, rate=bitrate, output=True)  

    grain = round(bitrate / frequency)
    points = grain * round(bitrate * duration / grain)
    duration = points / bitrate

    data = np.zeros(int(bitrate * max(duration, 1.0)))

    times = np.linspace(0, duration, points, endpoint=False)
    data[:points] = np.sin(times * frequency * 2 * np.pi)
    data = np.array((data + 1.0) * 127.5, dtype=np.int8).tobytes()

    stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

def toMorse(text):
    text = text.lower()
    return " ".join(morseCodeDictionary.get(char, "") for char in text if char in morseCodeDictionary)


def timings(wpm):
    point = 60 / (wpm * 50)
    dash = point * 3
    word = point * 7

    return point, dash, word


def main(wpm, text, sound, allKeys):
    point, dash, word = timings(wpm)
    keysToPress = ['numlock', 'capslock', 'scrolllock'] if allKeys else 'capslock'

    print(f"== Timings ==\nPoint: {point} seconds\nDash: {dash} seconds\nBetween letters: {point} seconds\nBetween words: {word} seconds\n== Timings ==\n")

    start = time.time()
    for i, char in enumerate(text):
        print(char)
        notEnd = i != len(text) - 1
        for morseChar in toMorse(char):
            if morseChar == '.':
                if (sound):
                    threading.Thread(target=beep, args=(point,)).start()

                pyautogui.press('capslock')
                time.sleep(point)
                pyautogui.press('capslock')
                if notEnd:
                    time.sleep(point)
            elif morseChar == '-':
                if (sound):
                    threading.Thread(target=beep, args=(dash,)).start()

                pyautogui.press(keysToPress)
                time.sleep(dash)
                pyautogui.press(keysToPress)

                if notEnd:
                    time.sleep(point)
            else:
                print('Error\nExiting...')
                exit(0)
        if (char == ' ' and notEnd):
            print('word pause')
            time.sleep(word)
        elif (notEnd):
            print('letter pause')
            time.sleep(dash)
    end = time.time()

    print(f"\nFinished in {round(end - start, 3)} seconds!\nExiting...")
    exit(0)


if __name__ == "__main__":
    try:
        print('== Welcome to MorseKB ==')

        wpm = askWPM()
        text = askText()
        sound = askSound()
        allKeys = askAllKeys()
        if allKeys:
            ask("Please check that Caps Lock, Scroll Lock and Num Lock are off and then press ENTER")
        else:
            ask("Please check that Caps Lock is off and then press ENTER")
        main(wpm, text, sound, allKeys)
    except KeyboardInterrupt:
        print("Cancelled by user\nExiting...")
        exit(0)