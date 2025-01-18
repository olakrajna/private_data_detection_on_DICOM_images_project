import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pydicom
import numpy as np
import shutil
import logging
# from utils import dicom_utils
import time

"""
DICOM Image Generator (CAISE)
Team: IMG
Group: GEN
Leader: Jacek Ruminski
"""

class DICOMImageGenerator:
    """
    Generates PNG images from DICOM files with text overlays.
    
    :param dicom_folder: str: Path to the folder containing DICOM files.
    :param output_folder: str: Path to the folder where output PNG images will be saved.
    :param font_folder: str: Path to the folder containing font files for text rendering.
    :param log_path: str: Path to the file where logging information should be stored.
    :param log_level: int: Logging level (default is logging.INFO).
    """

    def __init__(self, dicom_folder, output_folder, font_folder, log_path, log_level=logging.INFO):
        self.dicom_folder = dicom_folder
        self.output_folder = output_folder
        self.font_folder = font_folder
        self.fonts = self.load_fonts(font_folder)
        
        self.logging_level = log_level


    def load_fonts(self, font_folder):
        """
        Loads all fonts from the specified folder.

        :param font_folder: str: Path to the folder containing font files.
        :return: list: A list of full paths to all font files in the folder.
        """
        fonts = []
        try:
            for font_name in os.listdir(font_folder):
                if font_name.endswith(".ttf") or font_name.endswith(".otf"):
                    fonts.append(os.path.join(font_folder, font_name))
            logging.info("Loaded %d fonts from folder.", len(fonts))
        except Exception as e:
            logging.error("Error loading fonts from folder %s: %s", font_folder, str(e))
        return fonts

    def random_position(self, image_size, text_size):
        """
        Selects a random position on the image for placing the text.

        :param image_size: tuple: Size of the image (width, height).
        :param text_size: tuple: Size of the text area (width, height).
        :return: tuple: A randomly selected (x, y) position for the text on the image.
        """
        width, height = image_size
        text_width, text_height = text_size
        
        positions = [
            (10, 10),  # Top-left
            (width - text_width - 10, 10),  # Top-right
            (10, height - text_height - 10),  # Bottom-left
            (width - text_width - 10, height - text_height - 10),  # Bottom-right
        ]
        
        if random.random() < 0.2:  # 20% chance of center (top or bottom)
            positions.append(((width - text_width) // 2, 10))  # Top-center
            positions.append(((width - text_width) // 2, height - text_height - 10))  # Bottom-center
        
        position = random.choice(positions)
        logging.debug("Selected random position for text: %s", position)
        return position

    def get_max_font_size(self, text, font_path, max_width, max_height):
        """
        Determines the largest possible font size for the text to fit within the given dimensions.

        :param text: str: The text to be displayed.
        :param font_path: str: Path to the font file.
        :param max_width: int: Maximum allowable width for the text area.
        :param max_height: int: Maximum allowable height for the text area.
        :return: int: The largest possible font size that fits within the given dimensions.
        """
        font_size = 10
        max_font_size = min(max_width, max_height) // 20
        while True:
            font = ImageFont.truetype(font_path, font_size)
            bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            if text_width > max_width or text_height > max_height:
                break
            if font_size >= max_font_size:
                break
            font_size += 1
        max_size = font_size - 7
        logging.debug("Determined max font size: %d", max_size)
        return max_size

    def calculate_brightness(self, image, position, text_size):
        """
        Calculates the average brightness of the area where the text will be placed.

        :param image: PIL.Image: The image where text will be placed.
        :param position: tuple: The (x, y) coordinates of the top-left corner of the text.
        :param text_size: tuple: Size of the text area (width, height).
        :return: float: The average brightness (0-255) of the text area.
        """
        x, y = position
        text_width, text_height = text_size
        crop_area = image.crop((x, y, x + text_width, y + text_height))
        grayscale_image = crop_area.convert("L")  # Convert to grayscale
        histogram = grayscale_image.histogram()
        
        brightness = sum(i * histogram[i] for i in range(256)) / sum(histogram)
        logging.debug("Calculated brightness: %.2f", brightness)
        return brightness

    def get_contrasting_color(self, brightness):
        """
        Chooses a text color that contrasts with the given brightness.

        :param brightness: float: The average brightness of the background area (0-255).
        :return: str: A color ("white", "lightgray", "black", etc.) that contrasts with the background.
        """
        if brightness < 64:
            color = random.choice(["white", "lightgray"])  # Very dark background
        elif brightness < 128:
            color = random.choice(["white", "darkgray"])  # Dark background
        elif brightness < 192:
            color = random.choice(["black", "gray"])  # Light background
        else:
            color = "black"  # Very light background
        logging.debug("Selected text color: %s for brightness: %.2f", color, brightness)
        return color

    def apply_blur(self, text_image, blur_probability=0.33, max_blur_radius=1):
        """
        Applies a Gaussian blur to the text image with a given probability.

        :param text_image: PIL.Image: The image containing the text to be blurred.
        :param blur_probability: float: Probability (0-1) of applying blur to the text (default is 0.33).
        :param max_blur_radius: float: Maximum radius for the blur effect (default is 1).
        :return: PIL.Image: The text image, possibly blurred.
        """
        if random.random() < blur_probability:
            blur_radius = random.uniform(0, max_blur_radius)
            blurred_image = text_image.filter(ImageFilter.GaussianBlur(blur_radius))
            logging.debug("Applied Gaussian blur with radius: %.2f", blur_radius)
            return blurred_image
        return text_image

    def process_dicom_to_png(self, dicom_file, output_folder, fonts, unique_suffix):
        """
        Converts a DICOM file to a PNG image with added text overlay.

        :param dicom_file: str: Path to the DICOM file.
        :param output_folder: str: Directory to save the generated PNG file.
        :param fonts: list: List of font file paths for text rendering.
        :param unique_suffix: str: A unique suffix to append to the filename to avoid overwriting.

        Saves the generated PNG file in the output folder.
        """
        try:
            ds = pydicom.dcmread(dicom_file)
            pixel_array = ds.pixel_array

            # Apply rescaling if intercept and slope are available
            intercept = ds.RescaleIntercept if 'RescaleIntercept' in ds else 0
            slope = ds.RescaleSlope if 'RescaleSlope' in ds else 1
            pixel_array = pixel_array * slope + intercept

            # Normalize to the 1st and 99th percentile to improve contrast
            lower, upper = np.percentile(pixel_array, (1, 99))
            pixel_array = np.clip((pixel_array - lower) / (upper - lower) * 255, 0, 255).astype(np.uint8)

            img = Image.fromarray(pixel_array)
            
            # Prepare text overlay
            # text = f"Patient: {ds.PatientName}\nID: {ds.PatientID}\nStudyDate: {ds.StudyDate}"

            attributes = [
                ("Study Date", ds.StudyDate),
                ("Series Date", ds.SeriesDate),
                ("Acquisition Date", ds.AcquisitionDate),
                ("Content Date", ds.ContentDate),
                ("Study Time", ds.StudyTime),
                ("Acquisition Time", ds.AcquisitionTime),
                ("Content Time", ds.ContentTime),
                ("Accession Number", ds.AccessionNumber),
                ("Referring Physicians Name", ds.ReferringPhysicianName),
                ("Patient Name", ds.PatientName),
                ("Patient ID", ds.PatientID),
                ("Study ID", ds.StudyID),
            ]

            selected_attributes = random.sample(attributes, 3)

            text = "\n".join([f"{name}: {value}" for name, value in selected_attributes])

            print([f"{name}: {value}" for name, value in selected_attributes])

            font_path = random.choice(fonts)
            font_size_max = self.get_max_font_size(text, font_path, img.width, img.height)
            font_size = random.randint(7, font_size_max)
            font = ImageFont.truetype(font_path, font_size)
            
            # Create text image
            text_image = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(text_image)
            
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
            position = self.random_position(img.size, text_size)
            
            brightness = self.calculate_brightness(img, position, text_size)
            color = self.get_contrasting_color(brightness)
            
            draw.text(position, text, font=font, fill=color)
            
            text_image = self.apply_blur(text_image)
            
            # Combine text image with original image
            img = Image.alpha_composite(img.convert('RGBA'), text_image)
            img = img.convert('RGB')
            
            # Save PNG file
            base_filename = os.path.splitext(os.path.basename(dicom_file))[0]
            png_filename = f"{base_filename}_{unique_suffix}.png"
            png_filepath = os.path.join(output_folder, png_filename)
            img.save(png_filepath)
            
            logging.info("Saved PNG file: %s", png_filepath)
        except Exception as e:
            logging.error("Error processing DICOM file %s: %s", dicom_file, str(e))

    def clear_folder(self, folder_paths):
        """
        Clears the content of the specified list of folders.

        :param folder_path: str: Path to the folder to be cleared.
        """
        for folder_path in folder_paths:
            try:
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                    os.makedirs(folder_path)
                    logging.info("Cleared folder: %s", folder_path)
            except Exception as e:
                logging.error("Error clearing folder %s: %s", folder_path, str(e))

    def generate_images(self, num_images):
        """
        Generates a specified number of PNG images from DICOM files.

        :param num_images (int): Number of images to generate.
        """
        dicom_files = [os.path.join(self.dicom_folder, f) for f in os.listdir(self.dicom_folder) if f.endswith(".dcm")]
        if len(dicom_files) < num_images:
            logging.warning("Requested %d images, but only %d DICOM files are available.", num_images, len(dicom_files))
            num_images = len(dicom_files)
        
        unique_suffixes = [str(int(time.time() * 1000)) + str(i) for i in range(num_images)]
        
        for i in range(num_images):
            dicom_file = random.choice(dicom_files)
            self.process_dicom_to_png(dicom_file, self.output_folder, self.fonts, unique_suffixes[i])

dc = DICOMImageGenerator(r"C:\Users\olakr\OneDrive\Pulpit\WK_projekt\private_data_detection_on_DICOM_images\case2", r"C:\Users\olakr\OneDrive\Pulpit\WK_projekt\private_data_detection_on_DICOM_images\ouput2", r"C:\Users\olakr\OneDrive\Pulpit\WK_projekt\private_data_detection_on_DICOM_images\fonts", "logs")

dc.generate_images(50)