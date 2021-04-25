import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Диалог открытия файлов (и папок)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
from PIL import ImageFilter

class ImageProcessor():
   def __init__(self):
      self.image = None
      self.filename = None
      self.save_dir='Mod/'
   def loadImage(self, filename):
      self.filename = filename
      image_path = os.path.join(workdir, filename)
      self.image = Image.open(image_path)
   def showImage(label, path):
      image.hide()
      pixmapinge = QPixmap(path)
      w, h = image.width(), image.height()
      pixmapinge = pixmapinge.scaled(w, h, Qt.KeepAspectRatio)
      image.setPixmap(pixmapinge)
      image.show()
   def do_bw(self):
      self.image = self.image.convert("L")
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def saveImage(self):
      path = os.path.join(workdir, self.save_dir)
      if not(os.path.exists(path) or os.path.isdir(path)):
         os.mkdir(path)
      image_path = os.path.join(path, self.filename)
      self.image.save(image_path)
   
   def do_flip(self):
      self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)
   
   def blur(self):
      self.image = self.image.filter(ImageFilter.BLUR)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)
   def up_left(self):
      self.image = self.image.filter(Image.ROTATE_180)
      self.saveImage()

   


def showChosenImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)


def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
   result = []
   for filename in files:
      for ext in extensions:
         if filename.endswith(ext):
            result.append(filename)
   return result

def showFilenamesList():
   extensions = ['png', 'jpg', 'jpeg']
   chooseWorkdir()
   result = filter(os.listdir(workdir),extensions)
   file_list.clear()
   for res in result:
      file_list.addItem(res)



app  = QApplication([])
window = QWidget()
window.resize(1150,650)
window.setWindowTitle('Easy Editor')

#Виджеты:
btn_file = QPushButton('Выбор папки')
btn_left = QPushButton('Повернуть в лево')
btn_right = QPushButton('Повернуть в право')
btn_mirror = QPushButton('Отобразить зеркально')
btn_gray = QPushButton('Черно-белое')
btn_blur = QPushButton('Размытие')

file_list = QListWidget()

image = QLabel('картинка')

#Направляющие линии:
main_line = QHBoxLayout()
left_line = QVBoxLayout()
right_line = QVBoxLayout()
btn_line = QHBoxLayout()

#Добавление на главное окно:
btn_line.addWidget(btn_left)
btn_line.addWidget(btn_right)
btn_line.addWidget(btn_mirror)
btn_line.addWidget(btn_blur)
btn_line.addWidget(btn_gray)

left_line.addWidget(btn_file)
left_line.addWidget(file_list)

right_line.addWidget(image)
right_line.addLayout(btn_line)

main_line.addLayout(left_line, 20)
main_line.addLayout(right_line, 80)
window.setLayout(main_line)

window.show()
workdir = ''
workimage = ImageProcessor()
file_list.currentRowChanged.connect (showChosenImage)
btn_file.clicked.connect(showFilenamesList)
btn_gray.clicked.connect(workimage.do_bw)
btn_mirror.clicked.connect(workimage.do_flip)
btn_blur.clicked.connect(workimage.blur)


app.exec()