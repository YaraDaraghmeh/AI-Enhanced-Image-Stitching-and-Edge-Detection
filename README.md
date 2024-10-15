# AI-Enhanced Image Stitching and Edge Detection

## Project Overview

This application combines image stitching with multiple edge detection techniques, including an AI-based human figure detection. It allows users to create panoramic images from multiple input images and apply various edge detection methods to the result.

## Features

- Image stitching to create panoramic images
- Multiple edge detection techniques:
  - Canny Edge Detection
  - Difference of Gaussians (DoG) with adjustable morphological operations
  - AI-based edge detection for human figures (>50% confidence)
- Interactive user interface for parameter adjustment and result comparison

## Requirements

- Python 3.x
- OpenCV
-  TensorFlow (for AI-based detection)
-  tkinter for the GUI
- Additional dependencies (PIL,numpy,tensorflowhub)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/YaraDaraghmeh/Ai-Image-Stitching-and-Edge-Detection.git
   ```
2. Navigate to the project directory:
   ```
   cd Ai-Image-Stitching-and-Edge-Detection.git
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
- `Inputs Directotry ` Contains Example inputs
- `Outputs Directory` Contains Saved images from stitching 

## Contributing

Contributions to this project are welcome. Please ensure to follow the coding standards and document any changes or additions.

## License

[MIT License](LICENSE)

## Acknowledgements

- OpenCV for image processing capabilities
- TensorFlow for AI model implementation
- Tkinter , PIL, numpy 

## Contact

For any queries regarding this project, please contact [Yara Daraghmeh] at [yaradaraghmeh056@gmail.com]
