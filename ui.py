import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import image_stitching
from tkinter import ttk

class ImageStitchingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Stitching")
        self.selected_images = []

        self.select_button = tk.Button(master, text="Select Images", command=self.select_images)
        self.select_button.pack(pady=10)

        self.stitch_button = tk.Button(master, text="Stitch Images", command=self.stitch_images)
        self.stitch_button.pack(pady=10)

        self.image_frame = tk.Frame(master)
        self.image_frame.pack(pady=10)

    def select_images(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png")]
        filenames = filedialog.askopenfilenames(title="Select images for stitching", filetypes=filetypes)

        if filenames:
            self.selected_images = list(filenames)
            self.display_selected_images()
        else:
            messagebox.showinfo("Info", "No images selected")

    def display_selected_images(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        for img_path in self.selected_images:
            img = Image.open(img_path)
            img.thumbnail((100, 100))  # Resize image for thumbnail
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(self.image_frame, image=photo)
            label.image = photo
            label.pack(side=tk.LEFT, padx=5)

        num_images = len(self.selected_images)
        tk.Label(self.image_frame, text=f"{num_images} image{'s' if num_images != 1 else ''} selected").pack(
            side=tk.LEFT, padx=10)

    def stitch_images(self):
        if len(self.selected_images) < 2:
            messagebox.showerror("Error", "Please select at least two images for stitching")
            return

        try:
            stitched_image = image_stitching.stitch_images(self.selected_images)
            self.display_stitched_image(stitched_image)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during image stitching: {str(e)}")

    def display_stitched_image(self, image):
        # Clear previous images
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Display stitched image
        image.thumbnail((400, 400))  # Resize image for display
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.image_frame, image=photo)
        label.image = photo
        label.pack()

def create_ui():
    root = tk.Tk()
    app = ImageStitchingApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_ui()