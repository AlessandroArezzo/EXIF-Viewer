class ExifController:
    """
    This class contains the controller

    Attributes:
    model   reference to an object of class ExifModel
    """

    def __init__(self, model):
        self.model = model

    def insert_image(self, image_name):
        """
        Method that insert an image to the model if it is not already present
        :param image_name: name of the image to insert into the model
        :return: True if the image was not already present in the list, False otherwise
        """
        if not self.model.check_image(image_name):
            self.model.add_image(image_name)
            self.model.select_image(image_name)
            return True
        return False

    def select_image(self, index):
        """
        Method that select an image contained into the model by his index
        :param index: index of the image to select
        :return:
        """
        if index is not None:
            image_selected = self.model.get_image_by_idx(index)
        else:
            image_selected = None
        self.model.select_image(image_selected)

    def remove_image(self, index):
        """
        Method that remove an image contained into the model by his index
        :param index: index of the image to remove
        :return:
        """
        image_selected = self.model.get_image_by_idx(index)
        if image_selected == self.model.get_current_image():
            self.model.select_image(None)
        self.model.remove_image(image_selected)

    def empty_list(self):
        """
        Method that clear the list into the model
        :return:
        """
        self.model.empty_list()
        self.model.select_image(None)

    def get_current_image(self):
        """
        Method that return image currently selected in the model
        :return: currently selected image
        """
        return self.model.get_current_image()

    def get_current_data(self):
        """
        Method that return info end exif of the image currently selected in the model
        :return: info and exif of the currently selected image
        """
        current_info = self.model.get_current_info()
        current_exif = self.model.get_current_exif()
        return current_info, current_exif

    def get_current_geo(self):
        """
        Method that return geolocalization info of the image currently selected in the model
        :return: geolocalization info of the currently selected image into the model
        """
        return self.model.get_current_geo()

    def get_images(self):
        """
        Method that return all images contained in the model
        :return: all images contained in the model
        """
        return self.model.get_all_images()