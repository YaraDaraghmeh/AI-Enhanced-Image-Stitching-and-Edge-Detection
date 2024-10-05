
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
class MainView:
    def __init__(self, master):
        self.master = master
        self.master.title("AI-Enhanced Image Processing")
        self.master.geometry("600x400")

        self.create_main_view()

    def create_main_view(self):
        self.main_frame = ttk.Frame(self.master, padding="30")
        self.main_frame.pack(expand=True, fill="both")

        ttk.Label(self.main_frame, text="AI-Enhanced Image Processing", font=("Arial",25 )).pack(pady=20)

        ttk.Button(self.main_frame ,text="Image Stitching", command=self.open_stitching).pack(fill="x", pady=10)
        ttk.Button(self.main_frame, text="Edge Detection", command=self.open_edge_detection).pack(fill="x", pady=10)
        ttk.Button(self.main_frame, text="AI-based Detection", command=self.open_ai_detection).pack(fill="x", pady=10)

    def open_stitching(self):
        self.master.geometry("800x700+0+0")
        self.open_new_frame(StitchingFrame)

    def open_edge_detection(self):
        self.open_new_frame(EdgeDetectionFrame)

    def open_ai_detection(self):
        self.open_new_frame(AIDetectionFrame)

    def open_new_frame(self, FrameClass):
        self.main_frame.pack_forget()
        new_frame = FrameClass(self.master, self.return_to_main)
        new_frame.pack(expand=True, fill="both")

    def return_to_main(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.create_main_view()

class StitchingFrame(ttk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master, padding="20")
        self.return_callback = return_callback
        self.selected_images = []
        self.stitched_image = None

        # Title for the Stitching Frame
        ttk.Label(self, text="Image Stitching", font=("Arial", 16)).pack(pady=20)

        # Button to select images
        self.select_button = ttk.Button(self, text="Select Images", command=self.select_images)
        self.select_button.pack(pady=10)

        # Frame for displaying selected images
        self.image_frame = ttk.Frame(self)
        self.image_frame.pack(pady=10, fill="x", expand=True)

        # Button to stitch images together
        self.stitch_button = ttk.Button(self, text="Stitch Images", command=self.stitch_images)
        self.stitch_button.pack(pady=10)

        # Frame for displaying the stitched image
        self.stitched_frame = ttk.Frame(self)
        self.stitched_frame.pack(pady=10, fill="both", expand=True)

        # Button to save the stitched image, initially disabled
        self.save_button = ttk.Button(self, text="Save Stitched Image", command=self.save_stitched_image,
                                      state='disabled')
        self.save_button.pack(pady=10)

        # Button to return to the main screen
        ttk.Button(self, text="Back to Main", command=self.return_to_main).pack(pady=10)

    def select_images(self):
        # Open a file dialog to select multiple images
        filetypes = [("Image files", "*.jpg *.jpeg *.png")]
        filenames = filedialog.askopenfilenames(title="Select images for stitching", filetypes=filetypes)

        if filenames:
            self.selected_images = list(filenames)
            self.display_selected_images()  # Update the UI with selected images
        else:
            messagebox.showinfo("Info", "No images selected")

    def display_selected_images(self):
        # Clear previous selected images if any
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Display thumbnails of the selected images
        for img_path in self.selected_images:
            img = Image.open(img_path)
            img.thumbnail((100, 100))  # Resize the image thumbnail
            photo = ImageTk.PhotoImage(img)

            label = ttk.Label(self.image_frame, image=photo)
            label.image = photo  # Keep a reference to avoid garbage collection
            label.pack(side=tk.LEFT, padx=2)

        # Display how many images are selected
        num_images = len(self.selected_images)
        ttk.Label(self.image_frame, text=f"{num_images} image{'s' if num_images != 1 else ''} selected").pack(side=tk.LEFT, padx=5)

    def stitch_images(self):
        # Ensure there are at least two images selected
        if len(self.selected_images) < 2:
            messagebox.showerror("Error", "Please select at least two images for stitching")
            return

        # Perform the image stitching process using OpenCV
        imgs = [cv2.imread(img) for img in self.selected_images]
        stitcher = cv2.Stitcher_create()
        status, self.stitched_image = stitcher.stitch(imgs)

        if status != cv2.Stitcher_OK:
            messagebox.showerror("Error", "Can't stitch the images. Please try with different images.")
            return

        # Display the stitched image after success
        self.display_stitched_image()

    def display_stitched_image(self):
        # Clear previous image if any
        for widget in self.stitched_frame.winfo_children():
            widget.destroy()

        # Convert the stitched image (OpenCV format) to a PIL image
        stitched_image_rgb = cv2.cvtColor(self.stitched_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(stitched_image_rgb)

        # Resize the stitched image to fit in the frame (maintain aspect ratio)
        pil_image.thumbnail((400, 300))

        photo = ImageTk.PhotoImage(pil_image)
        label = ttk.Label(self.stitched_frame, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

        # Enable the save button once the stitched image is displayed
        self.save_button['state'] = 'normal'

    def save_stitched_image(self):
        # Save the stitched image to a file
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
        # Destroy the current frame and go back to the main view
        self.destroy()
        self.return_callback()




class AIDetectionFrame(ttk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master, padding="20")
        self.return_callback = return_callback

        ttk.Label(self, text="AI-based Detection", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Back to Main", command=self.return_to_main).pack(pady=10)

        # Add your AI-based detection functionality here

    def return_to_main(self):
        self.destroy()
        self.return_callback()
class EdgeDetectionFrame(ttk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master, padding="20")
        self.return_callback = return_callback

        ttk.Label(self, text="Edge Detection", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Back to Main", command=self.return_to_main).pack(pady=10)

        # Add your edge detection functionality here

    def return_to_main(self):
        self.destroy()
        self.return_callback()
def main():
    root = tk.Tk()
    app = MainView(root)
    root.mainloop()

if __name__ == "__main__":
    main()