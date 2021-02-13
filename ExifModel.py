import os
import time
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class ExifModel:
    """
    This class contains the model

    Attributes:
    current_image   currently image selected
    images_list     list of images
    current_info    dict of info of the current image
    current_exif    dict of exif of the current image
    current_geo     latitude and longitude of the current image
    """

    def __init__(self):
        self.current_image = None
        self.current_info = {}
        self.current_exif = {}
        self.current_geo = None
        self.images_list = []

    def add_image(self, image_name):
        """
        Method that insert an image to the list
        :param image_name: name of the image to insert into the model
        :return:
        """
        self.images_list.append(image_name)

    def remove_image(self, image_name):
        """
        Method that remove an image contained into the list by his name
        :param index: name of the image to remove
        :return:
        """
        self.images_list.remove(image_name)

    def empty_list(self):
        """
        Method that remove all element from the list
        :return:
        """
        self.images_list.clear()

    def select_image(self, image_name):
        """
        Method that select an image contained into the list by his name if it is present
        :param image_name: name of the image to select
        :return:
        """
        if self.check_image(image_name) or image_name == None:
            self.current_image = image_name
            self.extract_current_data()

    def check_image(self, image_name):
        """
        Method that check if an image is present in the list
        :param image_name: name of the image to search
        :return: True if the image is present in the list, False otherwise
        """
        if image_name in self.images_list:
            return True
        return False

    def get_image_by_idx(self, index):
        """
        Method that return an image by his index
        :param index: index of the image
        :return: image at the indicated index
        """
        return self.images_list[index]

    def get_all_images(self):
        """
        Method that return all images contained in the list
        :return: all images contained in the list
        """
        return self.images_list

    def extract_current_data(self):
        """
        Method that extract info end exif of the image currently selected
        :return:
        """
        self.__extract_current_info()
        self.__extract_current_exif()

    def __extract_current_info(self):
        """
        Method that extract info of the image currently selected
        :return:
        """
        self.current_info = {}
        if self.current_image != None:
            image = Image.open(self.current_image)
            self.current_info['Name file'] = os.path.basename(image.filename)
            self.current_info['Extension'] = image.format
            self.current_info['Image size'] = image.size
            self.current_info['Creation date'] = time.ctime(os.path.getctime(image.filename))
            self.current_info['Modification date'] = time.ctime(os.path.getmtime(image.filename))
            # self.current_info['file_size'] = size(os.stat(image.filename).st_size) + " (%5d bytes)" % os.stat(image.filename).st_size

    def __extract_current_exif(self):
        """
        Method that extract exif of the image currently selected
        :return:
        """
        self.current_exif = {}
        self.current_geo = None
        try:
            if self.current_image != None:
                image = Image.open(self.current_image)
                if image.format == 'PNG':
                    exif_data = image.info
                else:
                    exif_data = image.getexif()
                for tag, value in exif_data.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == "GPSInfo":
                        gps_data = {}
                        for v in value:
                            sub_decoded = GPSTAGS.get(v, v)
                            gps_data[sub_decoded] = value[v]
                        self.current_geo = gps_data
                    else:
                        self.current_exif[decoded] = value
        except UnicodeDecodeError:
            print("Error of extraction for this image")

    def get_current_info(self):
        """
        Method that return the current info
        :return: info of the image currently selected
        """
        if self.current_image:
            return self.current_info
        return None

    def get_current_exif(self):
        """
        Method that return the current exif
        :return: exif of the image currently selected
        """
        if self.current_image:
            return self.current_exif
        return None

    def get_current_geo(self):
        """
        Method that return the current geolocalization info
        :return: geolocalization info of the image currently selected
        """
        return self.current_geo

    def get_current_image(self):
        """
        Method that return the image currently selected
        :return: image currently selected
        """
        return self.current_image