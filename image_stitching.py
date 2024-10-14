import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

class StitchingFrame(ttk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master, padding="20")
        self.return_callback = return_callback
        self.selected_images = []
        self.stitched_image = None


        ttk.Label(self, text="Image Stitching", font=("Arial", 16)).pack(pady=20)


        self.select_button = ttk.Button(self, text="Select Images", command=self.select_images)
        self.select_button.pack(pady=10)


        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(pady=10, fill="x", expand=True)


        self.stitch_button = ttk.Button(self, text="Stitch Images", command=self.stitch_images)
        self.stitch_button.pack(pady=10)


        self.stitched_frame = ttk.Frame(self)
        self.stitched_frame.pack(pady=10, fill="both", expand=True)


        self.save_button = ttk.Button(self, text="Save Stitched Image", command=self.save_stitched_image,
                                      state='disabled')
        self.save_button.pack(pady=5)


        ttk.Button(self, text="Back to Main", command=self.return_to_main).pack(pady=5)

    def select_images(self):
        # file dialog to select multiple images
        filetypes = [("Image files", "*.jpg *.jpeg *.png")]
        filenames = filedialog.askopenfilenames(title="Select images for stitching", filetypes=filetypes)

        if filenames:
            self.selected_images = list(filenames)
            self.display_selected_images()  # Update the UI with selected images
        else:
            messagebox.showinfo("Info", "No images selected")

    def display_selected_images(self):
        # Clear previous selected
        for widget in self.image_frame.winfo_children():
            widget.destroy()


        for img_path in self.selected_images:
            img = Image.open(img_path)
            img.thumbnail((100, 100))  # Resize the image thumbnail
            photo = ImageTk.PhotoImage(img)

            label = ttk.Label(self.image_frame, image=photo)
            label.image = photo  # Keep a reference to avoid garbage collection
            label.pack(side=tk.LEFT, padx=2)


        num_images = len(self.selected_images)
        ttk.Label(self.image_frame, text=f"{num_images} image{'s' if num_images != 1 else ''} selected").pack(side=tk.LEFT, padx=5)

    def stitch_images(self):
        # check that there are at least two images selected
        if len(self.selected_images) < 2:
            messagebox.showerror("Error", "Please select at least two images for stitching")
            return

        # Perform  stitching process using OpenCV
        imgs = [cv2.imread(img) for img in self.selected_images]
        stitcher = cv2.Stitcher_create()
        status, self.stitched_image = stitcher.stitch(imgs)

        if status != cv2.Stitcher_OK:
            messagebox.showerror("Error", "Can't stitch the images. Please try with different images.")
            return

        # Display the stitched image after success
        self.display_stitched_image()

    def display_stitched_image(self):
        # clear previous if any
        for widget in self.stitched_frame.winfo_children():
            widget.destroy()

        # convert  stitched  to a PIL image
        stitched_image_rgb = cv2.cvtColor(self.stitched_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(stitched_image_rgb)


        pil_image.thumbnail((400, 300))

        photo = ImageTk.PhotoImage(pil_image)
        label = ttk.Label(self.stitched_frame, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()


        self.save_button['state'] = 'normal'

    def save_stitched_image(self):

        if self.stitched_image is None:
            messagebox.showerror("Error", "No stitched image to save")
            return

        # Open a file dialog to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, self.stitched_image)  # Save the image using OpenCV
            messagebox.showinfo("Success", f"Stitched image saved to {file_path}")

    def return_to_main(self):

        self.destroy()
        self.return_callback()