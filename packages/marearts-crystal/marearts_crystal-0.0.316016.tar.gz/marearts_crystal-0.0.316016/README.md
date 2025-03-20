# MareArts Crystal

MareArts Crystal is a Python package for encryption, decryption, and serial key management. It provides a simple interface for generating and validating serial keys, encrypting and decrypting strings and files, and performing date-based operations.

## Installation

Install MareArts Crystal using pip:

```bash
pip install marearts-crystal
```

## Usage

Here's a comprehensive guide on how to use MareArts Crystal:

```python
from marearts_crystal import ma_crystal

# Initialize with a secret key
secret_key = "your_secret_key_here"
skm = ma_crystal(secret_key)

# Generate a serial key
username = "john_doe"
start_date = "2023-07-01"
end_date = "2023-12-31"
serial_key = skm.generate_serial_key(username, start_date, end_date)
print(f"Generated Serial Key: {serial_key}")

# Validate the serial key
validated_start, validated_end = skm.validate_serial_key(username, serial_key)
print(f"Validated Start Date: {validated_start}")
print(f"Validated End Date: {validated_end}")

# Date validation
if skm.validate_date("2024-07-01", "2024-12-31"):
    print("Date range is valid")
else:
    print("Date range is invalid")

# Get today's date
print("Today's date:", skm.get_today_date())

# Generate end dates
print("Tomorrow:", skm.generate_end_date(0, 0, 1))
print("Next month:", skm.generate_end_date(0, 1, 0))
print("Next year:", skm.generate_end_date(1, 0, 0))

# Try with an invalid key
invalid_result = skm.validate_serial_key(username, "invalid_key")
print(f"Invalid Key Result: {invalid_result}")

invalid_result = skm.validate_serial_key("wrong_name", serial_key)
print(f"Invalid Key Result: {invalid_result}")

# String encryption and decryption
original_string = "Hello, MareArts Crystal!"
encrypted = skm.encrypt_string(original_string)
print(f"Encrypted: {encrypted}")

decrypted = skm.decrypt_string(encrypted)
print(f"Decrypted: {decrypted}")

# Decryption with wrong key
wrong_key = "wrong_secret_key"
wrong_skm = ma_crystal(wrong_key)
wrong_decryption = wrong_skm.decrypt_string(encrypted)
print(f"Decryption with wrong key: {wrong_decryption}")

# File encryption and decryption
input_filename = "example.bin"  # This can be any file, binary or text
output_encrypted_filename = "example_encrypted.bin"

# Read and encrypt the file
with open(input_filename, "rb") as file:
    file_content = file.read()
encrypted_content = skm.encrypt_data(file_content)

# Save the encrypted content
with open(output_encrypted_filename, "wb") as file:
    file.write(encrypted_content)
print(f"File '{input_filename}' has been encrypted and saved as '{output_encrypted_filename}'")

# Decrypt the file
input_encrypted_filename = output_encrypted_filename
output_decrypted_filename = "example_decrypted.bin"

# Read and decrypt the file
with open(input_encrypted_filename, "rb") as file:
    encrypted_content = file.read()
decrypted_content = skm.decrypt_data(encrypted_content)

if decrypted_content:
    # Save the decrypted content
    with open(output_decrypted_filename, "wb") as file:
        file.write(decrypted_content)
    print(f"File '{input_encrypted_filename}' has been decrypted and saved as '{output_decrypted_filename}'")
else:
    print("Decryption failed. The file might be corrupted or the wrong key was used.")
```

## Features

- Serial key generation and validation
- Date validation and manipulation
- String encryption and decryption
- File encryption and decryption
- Secure key management

## License

This project is licensed under the MIT License


## Support

www.marearts.com