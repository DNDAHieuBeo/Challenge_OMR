import cv2

def show_images(titles, im, wait=True):
    """Display multiple images with one line of code"""
    for (titles, im) in zip(titles, im):
        cv2.imshow(titles, im)

    if wait:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

