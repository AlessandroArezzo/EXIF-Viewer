from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QListView, QHBoxLayout, QVBoxLayout, QFileDialog, \
    QScrollArea, QDesktopWidget
from ExifWidgets import ImageList, ImageBox, DataTab


class ExifView(QWidget):
    """
    This class contains the only application window

    Attributes:
    controller   reference to an object of class ExifController
    image_box    reference to an object of class ImageBox
    image_list   reference to an object of class ImageList
    tab_data     reference to an object of class DataTab

    and other graphical elements
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_UI()
        self.center_on_screen()

    def init_UI(self):
        """Method that initialize the UI"""
        self.setWindowTitle("EXIF Viewer")

        self.path_current_image = QLabel()
        self.path_current_image.setText("")

        self.scroll_bar = QScrollArea()
        self.scroll_bar.setWidgetResizable(True)
        self.scroll_bar.setWidget(self.path_current_image)
        self.scroll_bar.setMaximumHeight(50)
        self.scroll_bar.setMinimumWidth(200)
        self.scroll_bar.setMaximumWidth(400)
        self.scroll_bar.setVisible(False)
        self.scroll_bar.setStyleSheet("border: 0")

        self.image_box = ImageBox(view=self, controller=self.controller)
        self.image_box.resize(500, 400)

        self.tab_data = DataTab(view=self, controller=self.controller)
        self.tab_data.resize(300, 400)

        self.geo_info = QLabel()
        self.geo_info.setText("")
        self.geo_info.setOpenExternalLinks(True)
        self.geo_info.setMaximumHeight(50)
        self.geo_info.setAlignment(Qt.AlignCenter)

        self.left_rotate = QPushButton()
        self.left_rotate.setVisible(False)
        self.left_rotate.setIcon(QIcon('IconImage/rotate_left.png'))
        self.left_rotate.setMaximumHeight(30)
        self.left_rotate.setIconSize(QSize(24, 24))
        self.left_rotate.clicked.connect(self.image_box.rotate_to_left)

        self.right_rotate = QPushButton()
        self.right_rotate.setVisible(False)
        self.right_rotate.setIcon(QIcon('IconImage/rotate_right.png'))
        self.right_rotate.setMaximumHeight(30)
        self.right_rotate.setIconSize(QSize(24, 24))
        self.right_rotate.clicked.connect(self.image_box.rotate_to_right)

        self.add_image_btn = QPushButton()
        self.add_image_btn.setText("Aggiungi immagine")
        self.add_image_btn.clicked.connect(self.insert_image)

        self.delete_image_btn = QPushButton()
        self.delete_image_btn.setEnabled(False)
        self.delete_image_btn.setText("Rimuovi immagine")

        self.empty_list_btn = QPushButton()
        self.empty_list_btn.setEnabled(False)
        self.empty_list_btn.setText("Svuota")

        self.image_list = ImageList(image_box=self.image_box, controller=self.controller, view=self)
        self.image_list.setFlow(QListView.LeftToRight)
        self.image_list.setMaximumHeight(120)

        up_image_box = QHBoxLayout()
        up_image_box.addWidget(self.scroll_bar)
        up_image_box.addStretch()
        up_image_box.addWidget(self.left_rotate)
        up_image_box.addWidget(self.right_rotate)

        image_layout = QVBoxLayout()
        image_layout.addLayout(up_image_box)
        image_layout.addWidget(self.image_box)
        image_layout.addWidget(self.geo_info)

        up_box = QHBoxLayout()
        up_box.addLayout(image_layout)
        up_box.addWidget(self.tab_data)

        list_button_box = QVBoxLayout()
        list_button_box.addWidget(self.add_image_btn)
        list_button_box.addWidget(self.delete_image_btn)
        list_button_box.addWidget(self.empty_list_btn)

        bottom_box = QHBoxLayout()
        bottom_box.addWidget(self.image_list)
        bottom_box.addLayout(list_button_box)

        layout = QVBoxLayout()
        layout.addLayout(up_box)
        layout.addLayout(bottom_box)

        self.image_box.register(self.update_control)
        self.image_box.register(self.update_current_path)
        self.image_box.register(self.update_current_geo)
        self.image_box.register(self.tab_data.update_tab_value)

        self.setLayout(layout)

        self.setMinimumSize(800, 600)
        self.show()

    def resizeEvent(self, ev):
        """
        Method for window resize event
        :return:
        """
        self.image_box.show_image()
        super().resizeEvent(ev)

    def center_on_screen(self):
        """
        Method that center the window on the screen
        :return:
        """
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def insert_image(self):
        """
        Method that handles adding an image
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Images (*.jpg *.jpeg *.png *.JPG *.PNG)",
                                                  options=options)
        if filename:
            result_op = self.controller.insert_image(filename)
            if result_op:
                self.image_list.add_image()

    def update_control(self):
        """
        Method that updates the visibility of controls based on whether or not an image is represented in the image box.
        It is invoked every time the image is represented in the ImageBox changes.
        :return:
        """
        visibility_control = True if self.controller.get_current_image() is not None else False
        self.left_rotate.setVisible(visibility_control)
        self.right_rotate.setVisible(visibility_control)
        self.tab_data.setVisible(visibility_control)
        self.scroll_bar.setVisible(visibility_control)

    def update_current_geo(self):
        """
        Method that updates the geo link of the current image.
        It is invoked every time the image is represented in the ImageBox changes.
        :return:
        """
        geo = self.controller.get_current_geo()
        if geo == None:
            self.geo_info.setText("")
        else:
            latitude = geo['GPSLatitude']
            longitude = geo['GPSLongitude']
            latitude_coord = float(latitude[0] + latitude[1] / 60 +latitude[2] / 3600)
            longitude_coord = float(longitude[0] + longitude[1] / 60 + longitude[2] / 3600)
            url_geo = "https://www.google.it/maps?q="+str(latitude_coord)+","+ str(longitude_coord)
            url_link = "<a href=\""+url_geo+"\">Apri posizione in Google Maps</a>"
            self.geo_info.setText(url_link)

    def update_current_path(self):
        """
        Method that updates the path label of the current image.
        It is invoked every time the image is represented in the ImageBox changes.
        :return:
        """
        path = self.controller.get_current_image()
        if path is not None:
            self.path_current_image.setText(path)
        else:
            self.path_current_image.setText("")

