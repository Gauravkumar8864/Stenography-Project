import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary_data):
    chars = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    try:
        return ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)
    except ValueError:
        return ""

def encode_image(image_path, message, password, output_path):
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Invalid image path!")
        return

    binary_message = text_to_bin(password + message) + '1111111111111110'
    h, w, _ = img.shape
    total_pixels = h * w * 3

    if len(binary_message) > total_pixels:
        messagebox.showerror("Error", "Message is too large for the image!")
        return

    data_index = 0
    for i in range(h):
        for j in range(w):
            for color in range(3):
                if data_index < len(binary_message):
                    img[i, j, color] = (img[i, j, color] & 254) | int(binary_message[data_index])
                    data_index += 1

    cv2.imwrite(output_path, img)
    messagebox.showinfo("Success", f"Message encoded successfully in '{output_path}'")
    os.system(f"start {output_path}")

def decode_image(image_path, password):
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Invalid image path!")
        return "Decoding Failed!"

    binary_data = ""
    h, w, _ = img.shape

    for i in range(h):
        for j in range(w):
            for color in range(3):
                binary_data += str(img[i, j, color] & 1)

    if '1111111111111110' not in binary_data:
        messagebox.showerror("Error", "EOF marker not found! Message may be corrupted.")
        return "Decoding Failed!"

    extracted_bin = binary_data.split('1111111111111110')[0]
    extracted_text = bin_to_text(extracted_bin).strip()

    if not extracted_text.startswith(password):
        messagebox.showerror("Error", "Incorrect password!")
        return "Decoding Failed!"

    return extracted_text[len(password):]

def browse_image():
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if filepath:
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(0, filepath)

def encode_message():
    image_path = image_path_entry.get()
    message = message_text.get("1.0", tk.END).strip()
    password = password_entry.get()
    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if output_path:
        encode_image(image_path, message, password, output_path)

def decode_message():
    image_path = image_path_entry.get()
    password = simpledialog.askstring("Password", "Enter decryption password:")

    if password:
        decoded_message = decode_image(image_path, password)
        if decoded_message != "Decoding Failed!":
            messagebox.showinfo("Decoded Message", f"Decoded Message:\n{decoded_message}")
            if os.name == "nt":
                os.system(f'start {image_path}')
            elif os.name == "posix":
                os.system(f'open {image_path}' if "darwin" in os.sys.platform else f'xdg-open {image_path}')

# GUI Setup
root = tk.Tk()
root.title("Image Steganography")

# Image Path
tk.Label(root, text="Image Path:").grid(row=0, column=0, sticky="w")
image_path_entry = tk.Entry(root, width=50)
image_path_entry.grid(row=0, column=1)
browse_button = tk.Button(root, text="Browse", command=browse_image)
browse_button.grid(row=0, column=2)

# Message
tk.Label(root, text="Message:").grid(row=1, column=0, sticky="w")
message_text = tk.Text(root, width=50, height=5)
message_text.grid(row=1, column=1)

# Password
tk.Label(root, text="Password:").grid(row=2, column=0, sticky="w")
password_entry = tk.Entry(root, width=50, show="*")
password_entry.grid(row=2, column=1)

# Encode Button
encode_button = tk.Button(root, text="Encode", command=encode_message)
encode_button.grid(row=3, column=1, pady=10)

# Decode Button
decode_button = tk.Button(root, text="Decode", command=decode_message)
decode_button.grid(row=4, column=1, pady=10)

root.mainloop()
