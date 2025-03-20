# coding: utf-8


import os
import PIL
from PIL import Image
import numpy as np
import base64
import io
from ksupk import get_current_function_name, gen_random_string, mkdir_with_p

from KanvasObjectKlick.assets import create_black_image


# def numpy_to_html_base64(image_array: np.ndarray):
#     _, buffer = cv2.imencode(".png", image_array)
#     base64_str = base64.b64encode(buffer).decode("utf-8")
#     return f"data:image/png;base64,{base64_str}"


def pillow_to_html_base64(image: PIL.Image.Image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffer = buffered.getvalue()
    base64_str = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/png;base64,{base64_str}"


def convert_cv2_to_pillow(image_bgr: np.ndarray):
    """
    Converts an image from BGR format to Pillow format (RGB).

    :param image_bgr: NumPy array of the image in BGR format
    :return: Pillow Image object
    """
    if image_bgr.ndim == 2:  # Single-channel image (grayscale)
        return Image.fromarray(image_bgr, mode='L')
    elif image_bgr.ndim == 3:
        if image_bgr.shape[2] == 3:  # BGR image
            # Convert BGR to RGB by reversing the channel order
            rgb_image = image_bgr[..., ::-1]
            return Image.fromarray(rgb_image, mode='RGB')
        elif image_bgr.shape[2] == 4:  # BGRA image
            # Convert BGRA to RGBA by reversing the channel order
            rgba_image = image_bgr[..., ::-1]
            return Image.fromarray(rgba_image, mode='RGBA')
        else:
            raise ValueError("Unsupported number of channels: {}".format(image_bgr.shape[2]))
    else:
        raise ValueError("Unsupported array shape: {}".format(image_bgr.shape))


class KOKEntity:

    def __init__(self, name: str, coords: tuple[float, float], color: tuple[int, int, int],
                 img: np.ndarray | PIL.Image.Image | os.PathLike | None):
        self.name = name
        self.coords = coords
        self.color = color
        if img is None:
            img = convert_cv2_to_pillow(create_black_image())
        elif isinstance(img, os.PathLike):
            img = Image.open(img)
        elif isinstance(img, PIL.Image.Image):
            img = img
        elif isinstance(img, np.ndarray):
            img = convert_cv2_to_pillow(img)
        else:
            raise ValueError(f"({get_current_function_name()}) img must be np.ndarray (opencv), Pillow image, path to image or None. ")
        self.img: PIL.Image.Image = img

    def get_dict_str(self, path_to_work_dir_if_mode_b: os.PathLike | None = None) -> str:
        IMAGE_FOLDER_NAME = "images"

        # mode a:
        # {"name": "Точка 1", "x": 10.5, "y": 20.3, "color": [255, 0, 0], "image": "data:image/png;base64,..."}
        # mode b:
        # {"name": "Точка 1", "x": 10.5, "y": 20.3, "color": [255, 0, 0], "image": "images/img1.jpg"}

        res = (f"\"name\": \"{self.name}\", \"x\": {self.coords[0]}, \"y\": {self.coords[1]}, "
               f"\"color\": [{self.color[0]}, {self.color[1]}, {self.color[2]}], \"image\": ")
        if path_to_work_dir_if_mode_b is None:
            res += f"\"{pillow_to_html_base64(self.img)}\""
        else:
            image_out_dir_path = os.path.join(path_to_work_dir_if_mode_b, IMAGE_FOLDER_NAME)
            if not os.path.isdir(image_out_dir_path):
                mkdir_with_p(image_out_dir_path)

            img_name = f"{self.name}_{gen_random_string()}.png"
            img_path = os.path.join(image_out_dir_path, img_name)
            self.img.save(img_path, "PNG")

            res += f"\"{IMAGE_FOLDER_NAME}/{img_name}\""
        return "{" + res + "}"
