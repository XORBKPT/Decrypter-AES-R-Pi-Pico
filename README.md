The decrypter is designed to work with the offline encrypter [https://github.com/XORBKPT/Encryption-AES-R-Pi-Pico](https://github.com/XORBKPT/Encryption-AES-R-Pi-Pico) 
---
## Decrypter Code (`decrypter.py`)

```python
# decrypter.py
import ucryptolib  # Library for AES encryption/decryption in MicroPython

def unpad(data):
    """
    Remove PKCS7 padding from decrypted data.
    PKCS7 padding adds bytes equal to the padding length, so we check and remove them.
    """
    padding_length = data[-1]  # Last byte indicates number of padding bytes
    if padding_length < 1 or padding_length > 16:
        raise ValueError("Invalid padding")
    # Verify all padding bytes match the padding length
    for i in range(1, padding_length + 1):
        if data[-i] != padding_length:
            raise ValueError("Invalid padding")
    return data[:-padding_length]  # Return data without padding

# Read the encrypted data from the file created by the encrypter
print("Reading encrypted data from encrypted.bin...")
try:
    with open('encrypted.bin', 'rb') as f:  # Open file in binary read mode
        data = f.read()
except OSError:
    print("Error: encrypted.bin not found. Run the encrypter first.")
    raise SystemExit  # Exit if file is missing

# Check if data is long enough (IV is 16 bytes, plus ciphertext)
if len(data) < 16:
    print("Error: Encrypted data is too short.")
    raise SystemExit

# Extract IV and ciphertext from the data
iv = data[:16]  # First 16 bytes are the Initialization Vector
ciphertext = data[16:]  # Rest is the encrypted message

# Prompt user to enter the key via serial console
print("Enter the 64-character hex key used for encryption:")
print("Example: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")
key_hex = input()  # Read key as a hex string from the terminal

# Convert hex key to bytes and validate length
try:
    key = bytes.fromhex(key_hex)  # Convert hex string to bytes
    if len(key) != 32:  # AES-256 requires a 32-byte key
        raise ValueError
except ValueError:
    print("Invalid key. Must be 64 hex characters (32 bytes).")
    raise SystemExit

# Decrypt the ciphertext using AES-256-CBC
print("Decrypting the message...")
try:
    aes = ucryptolib.aes(key, 2, iv)  # Mode 2 is CBC in ucryptolib
    padded_plaintext = aes.decrypt(ciphertext)  # Decrypt the data
    plaintext = unpad(padded_plaintext)  # Remove padding
    print("Decrypted message:", plaintext.decode('utf-8'))  # Display as text
except ValueError as e:
    print("Decryption failed:", e)  # Likely wrong key if padding is invalid
```
---
## Dependencies

The decrypter uses only the following, which are included in the standard MicroPython firmware for the Pico:

- **`ucryptolib`**: Handles AES decryption (built into MicroPython).
- **Core MicroPython functions**: No extra imports needed for file handling or input.

No additional libraries are required—just the default MicroPython setup.
---
## README for Students
```markdown
# Pico AES Decrypter

Welcome to the Pico AES Decrypter project! This guide will help you decrypt messages on your Raspberry Pi Pico that were encrypted using the AES-256-CBC algorithm by an offline encrypter from [this repository](https://github.com/XORBKPT/Encryption-AES-R-Pi-Pico). It’s a fun way to learn about encryption!

## What You’ll Learn
- How to program your Raspberry Pi Pico with MicroPython.
- Basics of AES encryption and CBC mode.
- How to decrypt a secret message with a key.

## What You Need
- **Raspberry Pi Pico** with MicroPython installed.
- **A computer** and USB cable to connect to the Pico.
- **Thonny** (a free program to talk to your Pico—download at [thonny.org](https://thonny.org)).

## Setup Instructions

### Step 1: Install MicroPython on Your Pico
1. Download the MicroPython `.uf2` file from [micropython.org/download/rp2-pico/](https://micropython.org/download/rp2-pico/).
2. Hold the BOOTSEL button on your Pico and plug it into your computer via USB.
3. Drag the `.uf2` file onto the Pico (it’ll show up as a USB drive).
4. The Pico will restart with MicroPython ready! See the [official guide](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) if you’re stuck.

### Step 2: Upload the Decrypter Code
1. Open Thonny on your computer.
2. Connect your Pico via USB.
3. Copy the `decrypter.py` code (above) into a new file in Thonny.
4. Save it to your Pico as `decrypter.py` (choose “Raspberry Pi Pico” when saving).

### Step 3: Get the Encrypted File
- The offline encrypter should have created a file called `encrypted.bin` on your Pico.
- If you don’t have it, ask your instructor for the encrypted file or run the encrypter first.

## How to Decrypt a Message

1. **Connect to Your Pico**:
   - In Thonny, go to “Run” > “Select interpreter” and pick “MicroPython (Raspberry Pi Pico)”.
   - Look at the REPL (bottom panel) to see messages.

2. **Run the Code**:
   - Open `decrypter.py` in Thonny and click the green “Run” button (or press F5).
   - You’ll see: `Reading encrypted data from encrypted.bin...`

3. **Enter the Key**:
   - It’ll ask: `Enter the 64-character hex key used for encryption:`.
   - Type the key used by the encrypter (ask your instructor if unsure). Example:
     ```
     0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
     ```
   - Press Enter.

4. **See the Message**:
   - If the key is right, you’ll get:
     ```
     Decrypting the message...
     Decrypted message: Hello, this is a secret message!
     ```
   - If it’s wrong, you might see: `Decryption failed: Invalid padding`.

## How It Works
1. **Loads the Encrypted File**: Reads `encrypted.bin` (IV + encrypted message).
2. **Splits the Data**: Takes the first 16 bytes as the IV, the rest as the ciphertext.
3. **Gets Your Key**: Converts your 64-character hex key to 32 bytes.
4. **Decrypts**: Uses AES-256-CBC to unlock the message.
5. **Cleans Up**: Removes padding added by the encrypter.
6. **Shows the Result**: Prints your secret message!

## Troubleshooting
- **“encrypted.bin not found”**: Check if the file is on your Pico (View > Files in Thonny).
- **“Invalid key”**: Ensure your key is exactly 64 hex characters (0-9, a-f).
- **“Decryption failed”**: Wrong key—double-check with your instructor.
- **No output?**: Confirm Thonny is set to the Pico interpreter.

## Cool Encryption Facts
- **AES**: A super-secure standard used everywhere (banks, phones, etc.).
- **CBC**: Mixes each block with the previous one for extra safety.
- **IV**: A random starter to keep things unique.

####More details for first starters:####
---
The decrypter relies on the following MicroPython modules, which are included in the standard MicroPython firmware for the Raspberry Pi Pico:
- **`ucryptolib`**: Provides AES encryption and decryption functions. Used for the `aes` object to decrypt data in CBC mode.
- **Built-in functions**: No additional imports are needed for file I/O (`open`, `read`) or string handling (`input`, `bytes.fromhex`), as these are part of MicroPython’s core.
---

## Prerequisites
- **Raspberry Pi Pico** with MicroPython installed.
- **A computer** with a USB cable to connect to the Pico.
- **A terminal program** like Thonny (recommended) or PuTTY to talk to the Pico.
## Setup Instructions
### Step 1: Install MicroPython on Your Pico
1. Download the MicroPython firmware from the [official website](https://micropython.org/download/rp2-pico/).
2. Connect your Pico to your computer while holding the BOOTSEL button.
3. Drag the `.uf2` file onto the Pico (it’ll appear as a USB drive).
4. The Pico will restart with MicroPython ready! Check the [official guide](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) if you need help.
### Step 2: Upload the Decrypter Code
1. Open Thonny (download it from [thonny.org](https://thonny.org) if you don’t have it).
2. Connect your Pico via USB.
3. Copy the `decrypter.py` code from above into a new file in Thonny.
4. Save it to your Pico as `decrypter.py` (select “Raspberry Pi Pico” as the save location).
### Step 3: Prepare the Encrypted Data
- The encrypter (from the offline repository) should have already run on your Pico and created a file called `encrypted.bin`. This file contains the encrypted message and a random IV (Initialization Vector).
- If you don’t have `encrypted.bin`, you’ll need to run the encrypter first. Since it’s offline, ask your instructor for the encrypted file or the encrypter code.
## How to Use the Decrypter
1. **Connect to the Pico**:
   - In Thonny, go to “Run” > “Select interpreter” and choose “MicroPython (Raspberry Pi Pico)”.
   - Open the REPL (bottom panel) to see messages from the Pico.
2. **Run the Decrypter**:
   - With `decrypter.py` open in Thonny, click the green “Run” button (or press F5).
   - You’ll see: `Reading encrypted data from encrypted.bin...`
3. **Enter the Key**:
   - The Pico will ask: `Enter the 64-character hex key used for encryption:`.
   - Type the key used by the encrypter. For example, if the encrypter used:
     ```
     0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
     ```
     enter that exact key (64 characters, representing 32 bytes in hex).
   - Press Enter in the REPL.
4. **See the Decrypted Message**:
   - If the key is correct, you’ll see something like:
     ```
     Decrypting the message...
     Decrypted message: Hello, this is a secret message!
     ```
   - If the key is wrong, you might see: `Decryption failed: Invalid padding`.
## How the Decrypter Works
Here’s what the code does, step by step:

1. **Reads the Encrypted File**:
   - Opens `encrypted.bin` and loads the data (IV + ciphertext).

2. **Splits the Data**:
   - Takes the first 16 bytes as the IV (used for CBC mode).
   - The rest is the ciphertext (encrypted message).

3. **Gets the Key**:
   - Asks you to type a 64-character hex key (like `0123...cdef`).
   - Converts it to 32 bytes for AES-256.

4. **Decrypts the Message**:
   - Uses AES-256-CBC with your key and the IV to decrypt the ciphertext.

5. **Removes Padding**:
   - The encrypter added padding (extra bytes) to make the message fit AES’s block size (16 bytes). The `unpad` function removes it.

6. **Shows the Result**:
   - Prints the original message if everything worked!

## Dependencies
- **`ucryptolib`**: Built into MicroPython for AES functions.
- No extra downloads needed—just use the standard MicroPython firmware!

## Troubleshooting
- **“encrypted.bin not found”**: Make sure the encrypter ran and saved the file. Check with Thonny’s file explorer (View > Files).
- **“Invalid key”**: Double-check your key is 64 hex characters long (0-9, a-f).
- **“Decryption failed”**: The key might be wrong, or the encrypted data is corrupted. Try the example key above if provided by your instructor.
- **No output?**: Ensure your Pico is connected and Thonny is set to the right interpreter.

## Fun Facts
- **AES**: Advanced Encryption Standard, used worldwide to keep data safe.
- **CBC**: Cipher Block Chaining, a mode that mixes blocks with the IV for extra security.
- **IV**: A random value to make each encryption unique, even with the same key.

## Next Steps
- Try encrypting your own message with the encrypter (if you have it) and decrypt it.
- Discuss how to safely share keys in real life (hint: not hardcoded).

```

