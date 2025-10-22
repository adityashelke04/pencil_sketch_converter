import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

images = {"original": None, "sketch": None}

def open_file():
    filepath = filedialog.askopenfilename()         #open the original image
    if not filepath:
        return
    img = cv2.imread(filepath)
    display_image(img, original = True)
    sketch_img = convert_to_sketch(img)
    display_image(sketch_img, original = False)

def convert_to_sketch(img):                         #convert it to sketch - gray + invert + guassian blur
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                    
    inverted_img = cv2.bitwise_not(gray_img)         
    blurred_img = cv2.GaussianBlur(inverted_img,(21,21), sigmaX=0,sigmaY = 0)
    inverted_blur_img = cv2.bitwise_not(blurred_img)
    sketch_img = cv2.divide(gray_img,inverted_blur_img, scale = 256.0)
    return sketch_img

def display_image(img,original):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if original else img
    img_pil = Image.fromarray(img_rgb)
    img_pil.thumbnail((400, 400), Image.LANCZOS)

    img_tk = ImageTk.PhotoImage(image = img_pil)

    if original:
        images["original"] = img_pil
    else:
        images["sketch"] = img_pil

    label = original_image_label if original else sketch_image_label 
    label.config(image = img_tk)
    label.image = img_tk

def save_sketch():                   #save the sketch
    if images["sketch"] is None:
        messagebox.showerror("Error", "No sketch to save.")
        return
    
    sketch_filpath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files","*.png")])
    if not sketch_filpath:
        return
    
    images["sketch"].save(sketch_filpath,"PNG")
    messagebox.showinfo("Saved","Sketch saved {}".format(sketch_filpath))

app = tk.Tk()                 #get the app ready
app.title('Pencil Sketch Converter') #app title
app.geometry('900x500')             #window size
app.resizable(False, False)

frame = tk.Frame(app)
frame.pack(pady = 10, padx = 10)

original_image_label = tk.Label(frame)
original_image_label.grid(row = 0, column = 0, padx = 5, pady = 5)
sketch_image_label = tk.Label(frame)
sketch_image_label.grid(row = 0,column = 1,padx = 5,pady = 5)

btn_frame = tk.Frame(app)
btn_frame.pack(pady = 10)

open_button = tk.Button(btn_frame, text = "Open Image", command = open_file)         #open button
open_button.grid(row = 0, column = 0, padx= 5)

save_button = tk.Button(btn_frame, text = "Save Sketch", command = save_sketch)        #save button
save_button.grid(row = 0, column = 1, padx = 5)

app.mainloop()