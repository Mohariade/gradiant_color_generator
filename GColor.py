import os
import sys
from PyQt5.QtCore import Qt, QPoint, QEasingCurve, QVariantAnimation, QPropertyAnimation, QRect, QSize
from PyQt5.QtWidgets import (
    QApplication, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QSlider,
    QLineEdit, QLabel, QPushButton, QDialog, QFileDialog, QGroupBox, QFrame, QGraphicsOpacityEffect
)
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QGuiApplication




class MainWindow(QStackedWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        
        with open('style.css', 'r') as f:
            self.stylesheet=f.read()
            
        self.color1, self.color2= "#C33764", "#1D2671"
        
        self.setWindowTitle("ColorsApp")
        self.setStyleSheet(self.stylesheet)

        self.LabelStyle={
            "QPushButton": {
                "background-color": "#FFFFFF"
            },
            "QPushButton:hover": {
                "border": "2px solid #FFFFFF"
            },
            "QPushButton:pressed": {
                "background-color": "#FFFFFF"
            }

        }

        layout0=QHBoxLayout()
        conatainer=QWidget()
        conatainer.setLayout(layout0)
        conatainer.setObjectName("container")
        conatainer.setStyleSheet(self.stylesheet)
        
        
        
        self.MainWidget=QWidget()
        self.setGeometry(800, 200, 1000, 550)
        self.addWidget(self.MainWidget)

        
        
        self.layout=QVBoxLayout()
        self.layout.addSpacing(40)
        
        

        layout1=QHBoxLayout()
        layout1.addStretch()
        self.layout2=QHBoxLayout()

        self.layout.setAlignment(Qt.AlignCenter)
        
        self.SwitchBtn=SwitchButton()
        self.SwitchBtn.valueChanged.connect(self.update_screen)
        self.HexInput=QLineEdit()
        self.HexInput.setPlaceholderText("#FFFFFF")
        self.HexInput.editingFinished.connect(self.show_colors)
        self.btn=QPushButton("Add")
        self.btn.setStyleSheet(self.stylesheet)
        self.btn.clicked.connect(self.show_colors)

        layout1.addSpacing(20)
        
        
        layout1.addWidget(self.SwitchBtn)
        layout1.addStretch()
        layout1.addWidget(self.HexInput)
        layout1.addWidget(self.btn)
        
        layout1.addStretch()

        
        
        self.layout.addLayout(layout1)
        
        
       
        self.layout.addSpacing(40)
        self.layout.addLayout(self.layout2)
        
        self.layout2.addSpacing(20)
        layout1.addSpacing(20)

        colors=self.generate_graduated_colors("#0000FF", 12, self.SwitchBtn.value())
        self.labels=[]
        for i in range(10):
            self.label=QPushButton()
            self.label.setFixedHeight(300)
            color=colors[i]
            self.update_style(self.LabelStyle,"QPushButton", "background-color", color)
            self.set_style_from_json(self.label, self.LabelStyle)
            self.label.clicked.connect(self.show_copied)
            self.labels.append(self.label)
            self.layout2.addWidget(self.label)
            self.layout2.setSpacing(0)

        self.layout2.addSpacing(20)

        self.layout3=QHBoxLayout()
        self.layout3.setAlignment(Qt.AlignCenter)
        
        self.layout.addStretch()
        self.layout.addLayout(self.layout3)
        self.layout.addStretch()
        self.MainWidget.setLayout(self.layout)

    def paintEvent(self, event):
        # Override the paintEvent to draw the left to right gradient background
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), 0)  # Left to right gradient
        gradient.setColorAt(0, QColor(self.color1))  # Start color (#12c2e9)
        gradient.setColorAt(1, QColor(self.color2))  # End color (#f64f59)
        painter.fillRect(self.rect(), gradient)

    
    def convert_json_to_stylesheet(self, json_style):
        style_str = ""
        style_str+="QPushButton{"
        v=json_style["QPushButton"]
        for key, value in v.items():
            style_str += f"{key}: {value}; "
        style_str+="}"
        style_str+="QPushButton:hover{"
        v=json_style["QPushButton:hover"]
        for key, value in v.items():
            style_str += f"{key}: {value}; "
        style_str+="}"
        style_str+="QPushButton:pressed{"
        v=json_style["QPushButton:pressed"]
        for key, value in v.items():
            style_str += f"{key}: {value}; "
        style_str+="}"
        return style_str.strip()
    
    def set_style_from_json(self, widget, style_json):
        style_str = self.convert_json_to_stylesheet(style_json)
        widget.setStyleSheet(style_str)
    
    def update_style(self, json_style, selector, property, value):
        json_style[selector][property]=value
        
    def update_colors(self):
        if not self.SwitchBtn.value():
            self.color1, self.color2= "#04619F", "#000000"
        else:
            self.color1, self.color2= "#C33764", "#1D2671"
            

    def move_top(self):
        button=self.MainWidget.sender()
        TargetPos=QPoint(button.geometry().x(), button.geometry().y()-20)
        self.animation = QPropertyAnimation(button, b'pos')
        self.animation.setDuration(20)  # Animation duration in milliseconds
        self.animation.setEndValue(TargetPos)  # Final size
        self.animation.start()
        self.AnimatedButton=button
       
       

    def move_buttom(self):
        button=self.AnimatedButton
        TargetPos=QPoint(button.geometry().x(), button.geometry().y()+20)
        self.anim = QPropertyAnimation(button, b'pos')
        self.anim.setDuration(20)  # Animation duration in milliseconds
        self.anim.setEndValue(TargetPos)  # Final size
        self.anim.start()
        print("inversed_animation")
    
    def expand_animation(self):
        button=self.MainWidget.sender()
        TargetSize=QSize(button.geometry().width()+40, button.geometry().height())
        self.expand_anim=QPropertyAnimation(button, b'size')
        self.expand_anim.setDuration(20)
        self.expand_anim.setEndValue(TargetSize)
        self.expand_anim.start()
        
    def retreive_text(self):
        text=self.HexInput.text()
        if text:
            if text[0]=="#":
                return text[1:]
            else:
                return text
        else:
            return None

    
    def show_colors(self):
        try:
            BaseColor="#"+self.HexInput.text()
            colors=self.generate_graduated_colors(BaseColor, 10, self.SwitchBtn.value())
            print(BaseColor)
            for i in range(10):
                label=self.labels[i]
                color=colors[i]
                self.update_style(self.LabelStyle,"QPushButton", "background-color", color)
                
                self.set_style_from_json(label, self.LabelStyle)
        except:
            BaseColor="#0000FF"
            colors=self.generate_graduated_colors(BaseColor, 10, self.SwitchBtn.value())
            print(BaseColor)
            for i in range(10):
                label=self.labels[i]
                color=colors[i]
                self.update_style(self.LabelStyle,"QPushButton", "background-color", color)
                
                self.set_style_from_json(label, self.LabelStyle)
            
               

    def darken_color(self, color, factor):
        # Convert the hex color to RGB
        r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

        # Darken the RGB components
        r = max(0, r - factor)
        g = max(0, g - factor)
        b = max(0, b - factor)

        # Convert the darkened RGB back to hex
        darkened_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        return darkened_color
    
    def whiten_color(self, color, factor):
        # Convert the hex color to RGB
        r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

        # Lighten the RGB components
        r = min(255, r + factor)
        g = min(255, g + factor)
        b = min(255, b + factor)

        # Convert the lightened RGB back to hex
        lightened_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        return lightened_color

    def generate_graduated_colors(self, original_color, n, mode):
        colors = []
        colors.append(original_color)

        # Calculate the factor to darken the color in each step
        factor = int(255 / (n - 1)) if n > 1 else 0

        # Generate the graduated colors by darkening the original color
        for i in range(n - 1):
            if mode:
                original_color = self.darken_color(original_color, factor)
            else:
                original_color = self.whiten_color(original_color, factor)
            colors.append(original_color)

        return colors


    def validate_hex(self):
        pass

    def show_copied(self):
        self.MsgLab=QLabel("Copied ")
        self.layout3.addWidget(self.MsgLab)
        self.MsgLab.setStyleSheet(self.stylesheet)
        
        self.animation = QVariantAnimation()
        self.animation.setDuration(800)  # Animation duration in milliseconds
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.MsgLab.setGraphicsEffect(self.opacity_effect)
        self.animation.valueChanged.connect(self.update_opacity)
        self.animation.finished.connect(self.MsgLab.deleteLater)
        self.animation.start()
        
        self.copy_to_clipbord()
    
    def update_opacity(self, value):
        self.opacity_effect.setOpacity(value)
    
    
        
    def retreive_hex(self):
        button=self.sender()
        style=str(button.styleSheet())
        index=style.index("#")
        return style[index: index+7]
        
    def copy_to_clipbord(self):
        clipboard=QGuiApplication.clipboard()
        clipboard.setText(self.retreive_hex())
        print("copied", clipboard.text())
        
    def update_screen(self):
        self.update_colors()
        self.show_colors()
        self.update()
        
class SwitchButton(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setRange(0, 1)
        self.setFixedHeight(60)
        self.setFixedWidth(120)
        self.setValue(1)
        self.setStyleSheet("""
            QSlider {
                background-color: white;
                
                border-radius: 30px;
            }
            QSlider::groove:horizontal {
                width: 100px;
                height: 20px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                width: 40px;
                height: 40px;
                border-radius: 20px;
                background-color: #EC6EAD;
                margin: -10px 0;
            }
        """)
        self.valueChanged.connect(self.on_slider_value_changed)

    def on_slider_value_changed(self, value):
        # The slider will only have 0 or 1 values for our switch button
        self.setValue(value) # Ensure the slider snaps to the closest valid position
        if value:
            self.setStyleSheet("""
                QSlider {
                    background-color: white;
                    
                    border-radius: 30px;
                }
                QSlider::groove:horizontal {
                    width: 100px;
                    height: 20px;
                    border-radius: 5px;
                }
                QSlider::handle:horizontal {
                    width: 40px;
                    height: 40px;
                    border-radius: 20px;
                    background-color: #EC6EAD;
                    margin: -10px 0;
                }
            """)
        else:
            self.setStyleSheet("""
            QSlider {
                background-color: white;
                
                border-radius: 30px;
            }
            QSlider::groove:horizontal {
                width: 100px;
                height: 20px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                width: 40px;
                height: 40px;
                border-radius: 20px;
                background-color: #000000;
                margin: -10px 0;
            }
        """)
            
        

def main():
    app = QApplication(sys.argv)
    home=MainWindow()
    home.show()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    main()



