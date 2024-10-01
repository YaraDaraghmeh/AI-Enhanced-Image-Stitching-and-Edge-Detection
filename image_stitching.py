import cv2
import numpy as np

def stitch_images(images):
    #images reading operation
    imgs = []
    for img_path in images:
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error reading image: {img_path}")
            continue
        imgs.append(img)

    if len(imgs) < 2:
        print("Need at least two images to stitch.")
        return None

    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch(imgs)

    if status != cv2.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
        return None

    return stitched

def save_result(result, output_path):
    cv2.imwrite(output_path, result)
    print(f"Stitched image saved to {output_path}")