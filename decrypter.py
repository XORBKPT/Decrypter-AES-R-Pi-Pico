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
