# AI-Enhanced Image Stitching and Edge Detection

## Project Overview
This application combines image stitching with multiple edge detection techniques, including an AI-based human figure detection. It allows users to create panoramic images from multiple input images and apply various edge detection methods to the result.

## Gaza Sky Geeks
Computer Vision Bootcamp 2024

## Features
- Image stitching to create panoramic images
- Multiple edge detection techniques:
  - Canny Edge Detection
  - Difference of Gaussians (DoG) with adjustable morphological operations
  - AI-based edge detection for human figures (>50% confidence)
- Interactive user interface for parameter adjustment and result comparison

## Design Decisions
### Image Stitching
- OpenCV for image stitching
- The user can browse files and select multiple images to stitch

### Edge Detection
- OpenCV for Canny Edge Detection and NumPy to calculate the lower and upper thresholds
- DoG edge detection followed by morphological close operation for noise reduction
- A slider for adjusting the kernel size

### AI-based Human Edge Detection
- Filtered and displayed human figure detections with confidence levels above 50%
- TensorFlow used for implementation to gain familiarity with the framework

## Challenges
- Time constraints
- GUI: Building a good GUI using tkinter was challenging
  Solution: Used software that assists in building GUIs with tkinter

## Code Quality and Documentation
While writing the code, I aimed to follow programming principles to achieve high-quality code that is readable, usable, clean, and maintainable.

## Future Enhancements
- Enhancing the GUI
- Applying different edge detection techniques and algorithms
- Exploring the use of PyTorch as an alternative to TensorFlow

## Requirements
- Python 3.x
- OpenCV
- TensorFlow (for AI-based detection)
- tkinter for the GUI
- Additional dependencies (PIL, numpy, tensorflowhub)

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/YaraDaraghmeh/Ai-Image-Stitching-and-Edge-Detection.git
   ```
2. Navigate to the project directory:
   ```
   cd Ai-Image-Stitching-and-Edge-Detection
   ```

## Usage
1. Run the main application:
   ```
   python main.py
   ```
2. Use the interface to select and upload images for stitching.
3. View the stitched panoramic image in the first window.
4. Adjust parameters for edge detection in the second window.
5. View AI-based human figure detection results in the third window.

## Project Structure
- `main.py`: Entry point of the application
- `image_stitching.py`: Contains functions for image stitching
- `edge_detection.py`: Implements various edge detection techniques
- `ai_detection.py`: Handles AI-based human figure detection
- `Inputs Directory`: Contains example inputs
- `Outputs Directory`: Contains saved images from stitching 

## License
[MIT License](LICENSE)

## Acknowledgements
- OpenCV for image processing capabilities
- TensorFlow for AI model implementation
- tkinter, PIL, numpy for additional functionality

## Contact
For any queries regarding this project, please contact [Yara Daraghmeh] at [yaradaraghmeh056@gmail.com]
