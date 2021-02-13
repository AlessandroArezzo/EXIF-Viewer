from PyQt5.QtCore import pyqtSignal, QSize, QFileInfo
from PyQt5.QtGui import QPixmap, QTransform, QImage, QIcon
from PyQt5.QtWidgets import QLabel, QSizePolicy, QListWidget, QListWidgetItem, QTabWidget, QVBoxLayout, QWidget, \
    QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PIL import Image

class ImageBox(QLabel):
    """
    This class contains the object for the representation of the current image

    Attributes:
    view           reference to an object of class ExifView
    controller     reference to an object of class ExifController


    """
    image_changed = pyqtSignal()

    def __init__(self, view, controller):
        QLabel.__init__(self, view)
        self.view = view
        self.controller = controller
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setAcceptDrops(True)
        self.rotation = 0

    def register(self, slot):
        """
        Method that attach a slot to call when signal is emitted.
        :param slot: function that must be called when the signal on image_changed is emitted
        :return:
        """
        self.image_changed.connect(slot)

    def show_image(self):
        """
        Method that show the current image. If no image is selected, clear the empty box.
        At the end it emits a signal on the image_changed object
        :return:
        """
        image_to_show = self.controller.get_current_image()
        if image_to_show and self.rotation == 0:
            self.qpix = QPixmap(image_to_show)
            self.setPixmap(self.qpix.scaled(QSize(min(self.size().width(), 512), min(self.size().height(), 512)),
                                            Qt.KeepAspectRatio, Qt.FastTransformation))
        elif image_to_show and self.rotation != 0:
            self.setPixmap(self.qpix.scaled(QSize(min(self.size().width(), 512), min(self.size().height(), 512)),
                                            Qt.KeepAspectRatio, Qt.FastTransformation))
        elif not image_to_show:
            self.qpix = QPixmap()
            self.setPixmap(self.qpix)
        self.rotation = 0
        self.image_changed.emit()

    def rotate_to_left(self):
        """
        Method that rotate the image represented in the box to the left 90 degrees and update the box view
        :return:
        """
        self.rotation -= 90
        transform = QTransform().rotate(self.rotation)
        self.qpix = self.qpix.transformed(transform, Qt.SmoothTransformation)
        self.show_image()

    def rotate_to_right(self):
        """
        Method that rotate the image represented in the box to the right 90 degrees and update the box view
        :return:
        """
        self.rotation += 90
        transform = QTransform().rotate(self.rotation)
        self.qpix = self.qpix.transformed(transform, Qt.SmoothTransformation)
        self.show_image()

    def dragEnterEvent(self, e):
        """
        Event fot the drag files directly onto the widget
        :param e: event
        :return:
        """
        if len(e.mimeData().urls()) > 0 and e.mimeData().urls()[0].isLocalFile():
            qi = QFileInfo(e.mimeData().urls()[0].toLocalFile())
            ext = qi.suffix()
            if ext == 'png' or ext == 'JPG' or ext == 'PNG' or ext == 'jpg' or ext == 'jpeg':
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Event for the drop files directly onto the widget
        :param e: event
        :return:
        """
        self.rotation = 0
        if e.mimeData().hasUrls:
            e.setDropAction(Qt.CopyAction)
            e.accept()
            result_op = False
            for url in e.mimeData().urls():
                fname = str(url.toLocalFile())
                current_result = self.controller.insert_image(fname)
                if not result_op and current_result:
                    result_op = True
            if result_op:
                self.view.image_list.add_image()
        else:
            e.ignore()

class ImageList(QListWidget):
    """
    This class contains the list for the representation of all the images inserted in the model

    Attributes:
    view                        reference to an object of class ExifView
    controller                  reference to an object of class ExifController
    image_box                   reference to an object of class ImageBox
    current_image_selected      image currently selected on the image list
    current_image_shown         image currently displayed on the image box

    """

    def __init__(self, image_box, view, controller):
        QListWidget.__init__(self, view)
        self.setIconSize(QSize(100, 100))
        self.image_box = image_box
        self.view = view
        self.controller = controller
        self.current_image_selected = None
        self.current_image_shown = None
        self.view.empty_list_btn.clicked.connect(self.empty_list)
        self.view.delete_image_btn.clicked.connect(self.delete_image)
        self.itemDoubleClicked.connect(self.load_image)
        self.itemClicked.connect(self.click_on_image)

    def load_image(self):
        """
        Method that select a new image to the list.
        :return:
        """
        if self.current_image_shown != self.currentRow():
            self.current_image_shown = self.currentRow()
            if self.image_box.rotation > 0:
                self.image_box.rotate = 0
            self.controller.select_image(self.current_image_shown)
            self.image_box.show_image()

    def empty_list(self):
        """
        Method that clears the list
        :return:
        """
        self.controller.empty_list()
        self.populate()
        self.current_image_selected = 0
        self.current_image_shown = 0

    def click_on_image(self):
        """
        Method that manages the click on an element of the list
        :return:
        """
        self.view.delete_image_btn.setEnabled(True)
        self.current_image_selected = self.currentRow()

    def delete_image(self):
        """
        Method that removes an element from the list
        :return:
        """
        self.controller.remove_image(self.current_image_selected)
        if self.current_image_shown == self.current_image_selected:
            self.current_image_shown = None
        if self.count() > 2:
            self.current_image_selected = self.current_image_selected-1
        elif self.count() == 2:
            self.current_image_selected = 0
        else:
            self.current_image_selected = None
        self.populate()
        self.setCurrentRow(self.current_image_selected)

    def add_image(self):
        """
        Method that adds an element to the list
        :return:
        """
        self.populate()
        self.image_box.rotation = 0
        self.current_image_shown = self.count() - 1
        self.current_image_selected = self.count() - 1
        self.setCurrentRow(self.count() - 1)

    def populate(self):
        """
        Method that updates the list with the controller contents
        :return:
        """
        self.clear()
        images = self.controller.get_images()
        for image in images:
            picture = Image.open(image)
            picture.thumbnail((72, 72), Image.ANTIALIAS)
            icon = QIcon(QPixmap.fromImage(QImage(picture.filename)))
            item = QListWidgetItem(self)
            item.setToolTip(image)
            item.setIcon(icon)
        if len(images) and (not self.view.empty_list_btn.isEnabled() or not self.view.delete_image_btn.isEnabled()):
            self.view.empty_list_btn.setEnabled(True)
            self.view.delete_image_btn.setEnabled(True)
        elif not len(images):
            self.current_image_shown = 0
            self.current_image_selected = 0
            self.view.delete_image_btn.setEnabled(False)
            self.view.empty_list_btn.setEnabled(False)
        self.image_box.show_image()

class DataTab(QTabWidget):
    """
    This class contains the tab for displaying info and exif of an image selected in the ImageList

    Attributes:
    view                        reference to an object of class ExifView
    controller                  reference to an object of class ExifController

    and other graphical elements
    """

    def __init__(self, view, controller):
        super(DataTab, self).__init__(view)
        self.setMinimumSize(300, 400)
        self.view = view
        self.controller = controller

    def init_data_tab(self):
        """
        Method that initialize the tab
        :return:
        """
        self.clear()

        self.tab_info = QWidget()
        self.tab_exif = QWidget()

        self.addTab(self.tab_info, "Info")
        self.addTab(self.tab_exif, "EXIF")

    def update_tab_value(self):
        """
        Method that update the data tab with the selected image data
        :return:
        """
        self.init_data_tab()
        info, exif = self.controller.get_current_data()
        self.__update_info(info)
        self.__update_exif(exif)

    def __update_info(self, info):
        """
        Method that update the info tab
        :param info: info of the image selected
        :return:
        """
        if info is not None:
            layout = QVBoxLayout()
            if len(info):
                info_tree = QTreeWidget()
                self.fill_widget(info_tree, info)
                info_tree.setHeaderLabel("Data")
            else:
                info_tree = QLabel()
                info_tree.setAlignment(Qt.AlignCenter)
                info_tree.setText("Nessuna informazione disponibile per questo file")

            layout.addWidget(info_tree)

            self.setTabText(0, "Info")
            self.tab_info.setLayout(layout)

    def __update_exif(self, exif):
        """
        Method that update the exif tab
        :exif info: exif of the image selected
        :return:
        """
        if exif is not None:
            layout = QVBoxLayout()
            if len(exif):
                exif_tree = QTreeWidget()
                self.fill_widget(exif_tree, exif)
                exif_tree.setHeaderLabel("Data")
            else:
                exif_tree = QLabel()
                exif_tree.setAlignment(Qt.AlignCenter)
                exif_tree.setText("Nessun EXIF disponibile per questo file")

            layout.addWidget(exif_tree)

            self.setTabText(1, "EXIF")
            self.tab_exif.setLayout(layout)

    def fill_widget(self, widget, value):
        """
        Method that populate the single widget that compose the data tab
        :param widget: widget to update
        :param value: value to set for the widget
        :return:
        """
        self.widget = widget
        self.widget.clear()
        self.fill_item(self.widget.invisibleRootItem(), value)

    def fill_item(self, item, value):
        """
        Method that populate the single item that compose the data tab
        :param widget: item to update
        :param value: value to set for the item
        :return:
        """
        item.setExpanded(True)
        if type(value) is dict:
            for key, val in value.items():
                child = QTreeWidgetItem()
                child.setText(0, str(key))
                item.addChild(child)
                self.fill_item(child, val)
        elif type(value) is list:
            for val in value:
                child = QTreeWidgetItem()
                item.addChild(child)
                if type(val) is dict:
                    child.setText(0, '[dict]')
                    self.fill_item(child, val)
                elif type(val) is list:
                    child.setText(0, '[list]')
                    self.fill_item(child, val)
                else:
                    child.setText(0, str(val))
                    child.setExpanded(True)
        else:
            child = QTreeWidgetItem()
            child.setText(0, str(value))
            item.addChild(child)
