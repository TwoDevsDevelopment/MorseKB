![The MorseKB Logo](/images/Logo.png)

MorseKB is a program that uses the Num Lock, Caps Lock and Scroll Lock LEDs on your keyboard to display morse code + Optional sound

# Installation
> [!CAUTION]
> MorseKB has not been tested on Linux or MacOS and may not function correctly on these platforms. Use at your own risk.

Prerequisites:
- Git
- Python 3
- Pip

## Windows
```bash
git clone https://github.com/TwoDevsDevelopment/MorseKB.git
cd MorseKB
pip install -r requirements.txt
```

# Running
## Windows
```bash
python main.py
```

# Third-Party Code
[PySine](https://github.com/lneuhaus/pysine) for the `beep` function (lines 87-110 of `main.py`)