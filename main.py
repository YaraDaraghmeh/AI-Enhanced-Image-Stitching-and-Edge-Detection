
import tkinter as tk
from tkinter import ttk

from image_stitching import StitchingFrame
from edge_detection import EnhancedImageProcessingFrame
from ai_detection import AIDetectionFrame
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
        self.master.geometry("900x800+0+0")
        self.open_new_frame(StitchingFrame)

    def open_edge_detection(self):

        self.open_new_frame(EnhancedImageProcessingFrame)

    def open_ai_detection(self):
        self.master.geometry("900x800+0+0")
        self.open_new_frame(AIDetectionFrame)

    def open_new_frame(self, FrameClass):
        self.main_frame.pack_forget()
        new_frame = FrameClass(self.master, self.return_to_main)
        new_frame.pack(expand=True, fill="both")

    def return_to_main(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.create_main_view()





def main():
    root = tk.Tk()
    app = MainView(root)
    root.mainloop()

if __name__ == "__main__":
    main()