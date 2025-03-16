To assist beginner students in understanding AES decryption on a Raspberry Pi Pico, I’ve created a separate Pico decrypter for the offline encrypter from the GitHub repository [https://github.com/XORBKPT/Encryption-AES-R-Pi-Pico](https://github.com/XORBKPT/Encryption-AES-R-Pi-Pico). Below, I provide the full decrypter code, list its dependencies, and include an extensive README tailored for beginners. Since the encrypter is offline, I’ve assumed it uses AES-256-CBC (a common mode) with a 32-byte key and a 16-byte IV, encrypts padded plaintext, and saves the IV and ciphertext to a file named `encrypted.bin`. The decrypter reverses this process; reading the file, prompting for the key, and displaying the decrypted message.

---

### Decrypter Code (`decrypter.py`)

This MicroPython script runs on a Raspberry Pi Pico, decrypts data encrypted by the encrypter, and is beginner-friendly with detailed comments.

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

### Dependencies

The decrypter relies on the following MicroPython modules, which are included in the standard MicroPython firmware for the Raspberry Pi Pico:

- **`ucryptolib`**: Provides AES encryption and decryption functions. Used for the `aes` object to decrypt data in CBC mode.
- **Built-in functions**: No additional imports are needed for file I/O (`open`, `read`) or string handling (`input`, `bytes.fromhex`), as these are part of MicroPython’s core.

No external libraries are required beyond the default MicroPython installation.

---

### README for Beginner Students

```markdown
# Pico AES Decrypter

Welcome to the Pico AES Decrypter project. This guide will help you decrypt messages on a Raspberry Pi Pico that were encrypted using the AES-256-CBC algorithm by an offline encrypter from [this repository](https://github.com/XORBKPT/Encryption-AES-R-Pi-Pico). This is a beginner-friendly project to learn about encryption and decryption and how to implement it. There are about 10 other repos here, this is level 1.

## What You’ll Learn
- How to use a Raspberry Pi Pico with MicroPython.
- What AES encryption is and how it works with CBC mode.
- How to decrypt a secret message using a key.

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
- If you don’t have `encrypted.bin`, you’ll need to run the encrypter first. Since it’s offline, get the encrypted file / encrypter code first.
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
Here’s what the code does:
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
   - The encrypter added padding (extra bytes) to make the message fit AES’s block size (16 bytes). The `unpad` function removes it. In further versions consider sources of true hardware randomness to mix in (see Crowd Supply RNG generator) and later use TPM to store and pin certificates (see Microchip ATECC608B or Infineon for exmaples)
6. **Shows the Result**:
   - Prints the original message if everything worked!
## Dependencies
- **`ucryptolib`**: Built into MicroPython for AES functions.
- No extra downloads needed—just use the standard MicroPython firmware.
## Troubleshooting
- **“encrypted.bin not found”**: Make sure the encrypter ran and saved the file. Check with Thonny’s file explorer (View > Files).
- **“Invalid key”**: Double-check your key is 64 hex characters long (0-9, a-f) hex format.
- **“Decryption failed”**: The key might be wrong, or the encrypted data is corrupted. Try the example key above if provided by your instructor.
- **No output?**: Ensure your Pico is connected and Thonny is set to the right interpreter (see Thonny Notes)
## Fun Facts
- **AES**: Advanced Encryption Standard, used worldwide to keep data safe.
- **CBC**: Cipher Block Chaining, a mode that mixes blocks with the IV for extra security.
- **IV**: A random value to make each encryption unique, even with the same key.
## Next Steps
- Try encrypting your own message with the encrypter (if you have it) and decrypt it.
- Discuss how to safely share keys in real life (hint: not hardcoded in CLR TEXT, see above ideas).
Happy decrypting!
```

---
