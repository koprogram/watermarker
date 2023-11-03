import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            img = Image.open(file_path)
            img.thumbnail((500, 500))  # Resize for GUI display
            tk_image = ImageTk.PhotoImage(img)
            panel.config(image=tk_image)
            panel.image = tk_image
            panel.img = img  # Keep a reference to the full image
            status_var.set("Image loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open this file: {e}")

def add_watermark():
    text = watermark_entry.get()
    position = watermark_pos.get()
    if not panel.img:
        messagebox.showwarning("Warning", "Please select an image first.")
        return
    if not text:
        messagebox.showwarning("Warning", "Please enter a watermark text.")
        return

    watermark_img = panel.img.copy()
    draw = ImageDraw.Draw(watermark_img)
    width, height = watermark_img.size
    font_size = 30
    font = ImageFont.truetype("arial.ttf", font_size)
    text_width, text_height = draw.textsize(text, font)

    pos = calculate_position(position, width, height, text_width, text_height)

    draw.text(pos, text, font=font, fill=(255, 255, 255, 128))

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if output_path:
        watermark_img.save(output_path)
        status_var.set("Watermark added and image saved successfully.")
    else:
        status_var.set("Save operation cancelled.")

def calculate_position(position, width, height, text_width, text_height):
    positions = {
        "bottom-right": (width - text_width - 10, height - text_height - 10),
        "top-right": (width - text_width - 10, 10),
        "top-left": (10, 10),
        "bottom-left": (10, height - text_height - 10)
    }
    return positions[position]

# GUI Layout
root = tk.Tk()
root.title("Image Watermarker")
root.resizable(True, True)

main_frame = ttk.Frame(root, padding="30")
main_frame.pack(expand=False, fill=tk.BOTH)

# Panel for displaying the image
panel = ttk.Label(main_frame)
panel.img = None
panel.pack()

# Entry for watermark text
watermark_label = ttk.Label(main_frame, text="Watermark Text:")
watermark_label.pack(pady=(10, 10))
watermark_entry = ttk.Entry(main_frame, width=50)
watermark_entry.pack()

# Dropdown for watermark position
position_label = ttk.Label(main_frame, text="Watermark Position:")
position_label.pack(pady=(10, 10))
positions = ["bottom-right", "bottom-left", "top-right", "top-left"]
watermark_pos = tk.StringVar(root)
watermark_pos.set(positions[0])
pos_menu = ttk.OptionMenu(main_frame, watermark_pos, *positions)
pos_menu.pack()

# Button frame
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=(10, 10), expand=True)

btn_open = ttk.Button(button_frame, text="Open Image", command=open_image)
btn_open.pack(side=tk.LEFT, padx=(0, 5))

btn_watermark = ttk.Button(button_frame, text="Add Watermark", command=add_watermark)
btn_watermark.pack(side=tk.LEFT)

# Status bar
status_var = tk.StringVar()
status_var.set("Ready.")
status_bar = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Start the GUI loop
root.mainloop()
