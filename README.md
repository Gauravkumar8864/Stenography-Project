# Image Steganography using LSB

## Overview
This project implements **Image Steganography** using **Least Significant Bit (LSB)** technique in Python. It allows users to hide secret messages inside images securely using a password-based approach.

## Features
- Encode a message into an image
- Password protection for decoding
- GUI interface using Tkinter
- Supports PNG, JPG, JPEG, and BMP image formats

## Dependencies
Ensure you have the following Python libraries installed:
```bash
pip install opencv-python numpy pillow
```

## How to Use
### Encoding a Message
1. Run the script:
   ```bash
   python steganography.py
   ```
2. Browse and select an image.
3. Enter the message you want to hide.
4. Enter a password for secure decoding.
5. Choose an output file location and save the new image.

### Decoding a Message
1. Run the script.
2. Browse and select the steganographic image.
3. Enter the correct password.
4. If the password is correct, the hidden message will be displayed.

## Technologies Used
- **Python** (Programming language)
- **OpenCV** (Image processing)
- **NumPy** (Array manipulations)
- **PIL (Pillow)** (Image handling)
- **Tkinter** (Graphical User Interface)

## Screenshots
(Screenshots can be added here to show the GUI)

## Limitations
- Image must be large enough to store the message.
- The password is embedded along with the message, so longer passwords reduce storage capacity.

## License
This project is open-source and free to use.

## Author
Developed by **Gaurav**

---
