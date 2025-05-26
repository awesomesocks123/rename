import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# 1. Choose folder with images
folder_path = os.path.join(os.path.dirname(__file__), 'pictures')
image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")

# 2. Load images
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]
current_index = 0

# 3. Set up GUI
root = tk.Tk()
root.title("Image Renamer")

img_label = tk.Label(root)
img_label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack()

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

def show_image():
    if current_index >= len(image_files):
        status_label.config(text="✅ All files renamed.")
        img_label.config(image="")
        entry.delete(0, tk.END)
        entry.config(state='disabled')
        save_btn.config(state='disabled')
        return

    filename = image_files[current_index]
    path = os.path.join(folder_path, filename)

    try:
        img = Image.open(path)
        img.thumbnail((400, 400))
        tk_img = ImageTk.PhotoImage(img)

        img_label.img = tk_img
        img_label.config(image=tk_img)

        entry.config(state='normal')
        entry.delete(0, tk.END)
        entry.insert(0, os.path.splitext(filename)[0])
        status_label.config(text=f"Renaming file {current_index + 1} of {len(image_files)}")
        save_btn.config(state='normal')
    except Exception as e:
        status_label.config(text=f"❌ Error loading image: {e}")


def save_and_next():
    global current_index
    if current_index >= len(image_files):
        return

    old_name = image_files[current_index]
    new_name = entry.get().strip()

    if new_name:
        old_path = os.path.join(folder_path, old_name)
        ext = os.path.splitext(old_name)[1]
        new_path = os.path.join(folder_path, new_name + ext)

        os.rename(old_path, new_path)
        image_files[current_index] = new_name + ext

    current_index += 1
    show_image()


save_btn = tk.Button(root, text="Save & Next", command=save_and_next)
save_btn.pack(pady=10)

show_image()
root.mainloop()
