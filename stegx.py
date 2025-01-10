import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QFileDialog, QProgressDialog, 
                             QTextEdit, QTabWidget, QMessageBox,)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pydub import AudioSegment
import cv2
import numpy as np

class SteganographyApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('STEGX')
        self.setWindowIcon(QIcon('icon.png'))  # Optional
        self.setGeometry(100, 100, 985, 800)
        
        # Set up layout with no margins or spacing
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create a tab widget to hold different tabs for Image, Text, Audio steganography
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(""" 
            QTabBar::tab {
                font-size: 20px;
                font-weight: bold;
                font-family: Monaco;
                padding: 15px 20px;
                margin: 2px;
                min-width: 275px;
                min-height: 50px;
                align: center;
            }
            QTabBar::tab:selected {
                background-color:  #148f77;  /* Selected tab color */
                color: white;
            }
            QTabBar::tab:hover{
                background-color:  #99e6d6; /* Tab color on hover */
            }
            QTabBar::tab:selected:hover{
                background-color:  #148f77; /* Selected tab color on hover */
            }
        """)

        self.img_tab = QWidget()
        self.txt_tab = QWidget()
        self.aud_tab = QWidget()

        # Initialize each tab's UI
        self.imageTabUI()
        self.textTabUI()
        self.audioTabUI()

        # Add tabs to widget
        self.tabs.addTab(self.img_tab, "IMAGE STEGANOGRAPHY")
        self.tabs.addTab(self.txt_tab, "TEXT STEGANOGRAPHY")
        self.tabs.addTab(self.aud_tab, "AUDIO STEGANOGRAPHY")
        
        # Set layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # Apply general stylesheet
        self.setStyleSheet(""" 
            QWidget {
                background-color: #212f3d;  /* Background */
                border: none;               /* Remove any border */
            }

            QLabel {
                font-size: 18px;            /* Adjust the font size as needed */
                font-weight: bold;          /* Make the font bold */
                color: #d1f2eb;             /* Text color */
                padding: 5px;               /* Optional: Add padding */
            }

            QTabWidget::pane {
                border: none;               /* Remove the border around the tab pane */
                margin: 0px;                /* Remove any margin */
                padding: 0px;               /* Remove padding */
            }

            QTabBar::tab {
                background-color: #d1f2eb;  /* Background for unselected tabs */
                border: none;               /* Remove any border */
                margin: 0px;                /* Remove margin */
                padding: 10px;
            }

            QTabBar::tab:selected {
                background-color: #0e6251;  
                color: white;
                border: none;               
            }

            QPushButton {
                font-size: 18px;
                font-weight: bold;
                background-color: #148f77; 
                color: white;
                border-radius: 5px;
                border: none;               
                padding: 10px 15px;
            }

            QPushButton:hover {
                background-color: #0e6251; 
            }

            QLineEdit, QTextEdit {
                background-color: #d1f2eb; 
                border: 2px solid #0e6251;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }

            QLineEdit:focus, QTextEdit:focus {
                border-color: #0e6251;  
            }
        """)

    def refreshTab(self):
        current_tab = self.tabs.currentWidget()
        if current_tab == self.img_tab:
            self.img_file_path.clear()
            self.img_message.clear()
        elif current_tab == self.txt_tab:
            self.txt_file_path.clear()
            self.txt_message.clear()
        elif current_tab == self.aud_tab:
            self.aud_file_path.clear()
            self.aud_message.clear()
        QMessageBox.information(self, "Success", "Tab refreshed successfully!")

    # Image Tab UI
    def imageTabUI(self):
        layout = QVBoxLayout()
        
        self.img_encode_btn = QPushButton("ENCODE")
        self.img_decode_btn = QPushButton("DECODE")
        self.img_refresh_btn = QPushButton("REFRESH")  # Created new refresh button
        self.img_file_path = QLineEdit()
        self.img_file_path.setPlaceholderText("Image File Path")
        self.img_select_btn = QPushButton("SELECT IMAGE")
        self.img_message = QTextEdit()
        self.img_message.setPlaceholderText("Enter The Message To Be Encoded")

        self.img_select_btn.clicked.connect(self.selectImageFile)
        self.img_encode_btn.clicked.connect(self.encodeImage)
        self.img_decode_btn.clicked.connect(self.decodeImage)
        self.img_refresh_btn.clicked.connect(self.refreshTab)  # Connected refresh button

        layout.addWidget(QLabel("IMAGE STEGANOGRAPHY"))
        layout.addWidget(self.img_file_path)
        layout.addWidget(self.img_select_btn)
        layout.addWidget(QLabel("MESSAGE TO ENCODE"))
        layout.addWidget(self.img_message)
        layout.addWidget(self.img_encode_btn)
        layout.addWidget(self.img_decode_btn)
        layout.addWidget(self.img_refresh_btn)  # Added refresh button below decode

        self.img_tab.setLayout(layout)

    # Text Tab UI
    def textTabUI(self):
        layout = QVBoxLayout()
        
        self.txt_encode_btn = QPushButton("ENCODE")
        self.txt_decode_btn = QPushButton("DECODE")
        self.txt_refresh_btn = QPushButton("REFRESH")  # Created new refresh button
        self.txt_file_path = QLineEdit()
        self.txt_file_path.setPlaceholderText("Text File Path")
        self.txt_select_btn = QPushButton("SELECT TEXT FILE")
        self.txt_message = QTextEdit()
        self.txt_message.setPlaceholderText("Enter The Message To Be Encoded")

        self.txt_select_btn.clicked.connect(self.selectTextFile)
        self.txt_encode_btn.clicked.connect(self.encodeText)
        self.txt_decode_btn.clicked.connect(self.decodeText)
        self.txt_refresh_btn.clicked.connect(self.refreshTab)  # Connected refresh button

        layout.addWidget(QLabel("TEXT STEGANOGRAPHY"))
        layout.addWidget(self.txt_file_path)
        layout.addWidget(self.txt_select_btn)
        layout.addWidget(QLabel("MESSAGE TO ENCODE"))
        layout.addWidget(self.txt_message)
        layout.addWidget(self.txt_encode_btn)
        layout.addWidget(self.txt_decode_btn)
        layout.addWidget(self.txt_refresh_btn)  # Added refresh button below decode

        self.txt_tab.setLayout(layout)

    # Audio Tab UI
    def audioTabUI(self):
        layout = QVBoxLayout()
        
        self.aud_encode_btn = QPushButton("ENCODE")
        self.aud_decode_btn = QPushButton("DECODE")
        self.aud_refresh_btn = QPushButton("REFRESH")  # Created new refresh button
        self.aud_file_path = QLineEdit()
        self.aud_file_path.setPlaceholderText("Audio File Path")
        self.aud_select_btn = QPushButton("SELECT AUDIO FILE")
        self.aud_message = QTextEdit()
        self.aud_message.setPlaceholderText("Enter The Message To Be Encoded")

        self.aud_select_btn.clicked.connect(self.selectAudioFile)
        self.aud_encode_btn.clicked.connect(self.encodeAudio)
        self.aud_decode_btn.clicked.connect(self.decodeAudio)
        self.aud_refresh_btn.clicked.connect(self.refreshTab)  # Connected refresh button

        layout.addWidget(QLabel("AUDIO STEGANOGRAPHY"))
        layout.addWidget(self.aud_file_path)
        layout.addWidget(self.aud_select_btn)
        layout.addWidget(QLabel("MESSAGE TO ENCODE"))
        layout.addWidget(self.aud_message)
        layout.addWidget(self.aud_encode_btn)
        layout.addWidget(self.aud_decode_btn)
        layout.addWidget(self.aud_refresh_btn)  # Added refresh button below decode

        self.aud_tab.setLayout(layout)

    # File Selection Functions
    def selectImageFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Image Files (*.png *.jpg *.bmp)')
        if filename:
            self.img_file_path.setText(filename)

    def selectTextFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Text File', '', 'Text Files (*.txt)')
        if filename:
            self.txt_file_path.setText(filename)

    def selectAudioFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Audio File', '', 'Audio Files (*.wav *.mp3)')
        if filename:
            self.aud_file_path.setText(filename)

    # Image Steganography Functions
    def encodeImage(self):
        img_path = self.img_file_path.text()
        message = self.img_message.toPlainText()
        if not img_path or not message:
            QMessageBox.warning(self, "Error", "Please select an image and enter a message to encode.")
            return

        try:
            img = cv2.imread(img_path)
            encoded_img = self.hide_message_in_image(img, message)
            save_path, _ = QFileDialog.getSaveFileName(self, 'Save Encoded Image', '', 'PNG Files (*.png);;All Files (*)')
            if save_path:
                cv2.imwrite(save_path, encoded_img)
                QMessageBox.information(self, "Success", "Message encoded and saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to encode message: {str(e)}")

    def decodeImage(self):
        img_path = self.img_file_path.text()
        if not img_path:
            QMessageBox.warning(self, "Error", "Please select an image to decode.")
            return

        try:
            img = cv2.imread(img_path)
            message = self.extract_message_from_image(img)
            QMessageBox.information(self, "Decoded Message", f"Decoded message: {message}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to decode message: {str(e)}")

    def hide_message_in_image(self, img, message):
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        binary_message += '1111111111111110'  # End of message delimiter

        data_index = 0
        binary_message_length = len(binary_message)

        for row in img:
            for pixel in row:
                for i in range(3):  # For each RGB channel
                    if data_index < binary_message_length:
                        pixel[i] = int(format(pixel[i], '08b')[:-1] + binary_message[data_index], 2)
                        data_index += 1
        return img

    def extract_message_from_image(self, img):
        binary_message = ''
        for row in img:
            for pixel in row:
                for i in range(3):  # For each RGB channel
                    binary_message += format(pixel[i], '08b')[-1]

        # Split binary message into 8-bit segments
        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte == '11111111':
                break
            message += chr(int(byte, 2))
        return message

    # Text Steganography Functions
    def encodeText(self):
        txt_path = self.txt_file_path.text()
        message = self.txt_message.toPlainText()
        if not txt_path or not message:
            QMessageBox.warning(self, "Error", "Please select a text file and enter a message to encode.")
            return

        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Add delimiter to mark the end of the message
            message += "§EOF§"
            
            # Convert message to a format that preserves special characters
            encoded_chars = []
            content_chars = list(content)
            
            # Calculate required space for the message
            if len(content) < len(message) * 2:
                QMessageBox.warning(self, "Error", "Cover text is too short to hide the message safely.")
                return
                
            # Insert message characters between content characters with variable spacing
            message_index = 0
            spacing = max(3, len(content) // (len(message) * 2))  # Dynamic spacing based on content length
            
            for i in range(len(content)):
                encoded_chars.append(content[i])
                
                # Insert message character after variable spacing
                if message_index < len(message) and i % spacing == 0:
                    # Insert a special marker followed by the message character
                    encoded_chars.append('​')  # Zero-width space as marker
                    encoded_chars.append(message[message_index])
                    message_index += 1

            encoded_content = ''.join(encoded_chars)

            save_path, _ = QFileDialog.getSaveFileName(self, 'Save Encoded Text File', '', 
                                                     'Text Files (*.txt);;All Files (*)')
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as file:
                    file.write(encoded_content)
                QMessageBox.information(self, "Success", "Message encoded and saved successfully!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to encode message: {str(e)}")

    def decodeText(self):
        txt_path = self.txt_file_path.text()
        if not txt_path:
            QMessageBox.warning(self, "Error", "Please select a text file to decode.")
            return

        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Extract the hidden message using the zero-width space marker
            hidden_chars = []
            i = 0
            
            while i < len(content):
                if content[i] == '​':  # Zero-width space marker
                    if i + 1 < len(content):
                        hidden_chars.append(content[i + 1])
                        i += 2
                i += 1

            hidden_message = ''.join(hidden_chars)
            
            # Remove the EOF marker
            if "§EOF§" in hidden_message:
                hidden_message = hidden_message.split("§EOF§")[0]
            
            if hidden_message:
                QMessageBox.information(self, "Decoded Message", f"Decoded message: {hidden_message}")
            else:
                QMessageBox.warning(self, "No Message Found", "No hidden message was detected in this file.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to decode message: {str(e)}")

    # Encode/Decode Functions for Audio Steganography
    def encodeAudio(self):
        aud_path = self.aud_file_path.text()
        message = self.aud_message.toPlainText()
        if not aud_path or not message:
            QMessageBox.warning(self, "Error", "Please select an audio file and enter a message to encode.")
            return

        try:
            audio = AudioSegment.from_file(aud_path)
            encoded_audio = self.hide_message_in_audio(audio, message)
            save_path, _ = QFileDialog.getSaveFileName(self, 'Save Encoded Audio File', '', 'Audio Files (*.wav *.mp3)')
            if save_path:
                encoded_audio.export(save_path, format="wav" if save_path.endswith(".wav") else "mp3")
                QMessageBox.information(self, "Success", "Message encoded and saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to encode message: {str(e)}")

    def decodeAudio(self):
        aud_path = self.aud_file_path.text()
        if not aud_path:
            QMessageBox.warning(self, "Error", "Please select an audio file to decode.")
            return

        try:
            audio = AudioSegment.from_file(aud_path)
            message = self.extract_message_from_audio(audio)
            QMessageBox.information(self, "Decoded Message", f"Decoded message: {message}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to decode message: {str(e)}")

    def hide_message_in_audio(self, audio, message):
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        binary_message += '1111111111111110'  # End of message delimiter

        audio_samples = np.array(audio.get_array_of_samples())
        data_index = 0
        binary_message_length = len(binary_message)

        for i in range(len(audio_samples)):
            if data_index < binary_message_length:
                audio_samples[i] = (audio_samples[i] & ~1) | int(binary_message[data_index])
                data_index += 1

        # Create a new audio segment with the modified samples
        encoded_audio = audio._spawn(audio_samples.tobytes())
        return encoded_audio

    def extract_message_from_audio(self, audio):
        binary_message = ''
        audio_samples = np.array(audio.get_array_of_samples())

        for sample in audio_samples:
            binary_message += str(sample & 1)  # Get the least significant bit

        # Split binary message into 8-bit segments
        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte == '11111111':
                break
            message += chr(int(byte, 2))
        return message

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SteganographyApp()
    ex.show()
    sys.exit(app.exec_())