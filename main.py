import google.generativeai as genai
import os
import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit,
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt


class AiApp(QWidget):
    def __init__(self):
        super().__init__()

        # UI Elements
        self.chat_box = QTextEdit(self)
        self.chat_box.setReadOnly(True)

        self.user_input = QLineEdit(self)
        self.get_result_button = QPushButton("Ask", self)

        self.initUI()

        # API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.chat_box.setText("❌ API key not found. Set GOOGLE_API_KEY.")
            return

        genai.configure(api_key=api_key)

        
        self.model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

        self.chat = self.model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "You are a helpful assistant. Keep answers short, clear, and well formatted using bullet points when needed."
                    ]
                }
            ]
        )

    def initUI(self):
        self.setWindowTitle("KH AI")

        vbox = QVBoxLayout()
        vbox.addWidget(self.chat_box)

        hbox = QHBoxLayout()
        hbox.addWidget(self.user_input)
        hbox.addWidget(self.get_result_button)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.get_result_button.clicked.connect(self.get_the_ans)
        self.user_input.returnPressed.connect(self.get_the_ans)

        self.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                background-color: #f5f5f5;
            }
            QLineEdit {
                font-size: 16px;
                padding: 8px;
                border-radius: 10px;
            }
            QPushButton {
                font-size: 16px;
                padding: 8px;
                border-radius: 10px;
            }
        """)

    #  Chat bubble system
    def append_message(self, sender, message):
        formatted = message.replace("\n", "<br>")

        if sender == "You":
            bubble = f"""
            <div style='text-align:right; margin:10px;'>
                <span style='background:#DCF8C6; padding:8px; border-radius:10px;'>
                    {formatted}
                </span>
            </div>
            """
        else:
            bubble = f"""
            <div style='text-align:left; margin:10px;'>
                <span style='background:#EAEAEA; padding:8px; border-radius:10px;'>
                    {formatted}
                </span>
            </div>
            """

        self.chat_box.append(bubble)

        #  Auto-scroll
        self.chat_box.verticalScrollBar().setValue(
            self.chat_box.verticalScrollBar().maximum()
        )

    def get_the_ans(self):
        user_msg = self.user_input.text().strip()
        if not user_msg:
            return

        
        self.append_message("You", user_msg)

        
        self.get_result_button.setText("Thinking...")
        self.get_result_button.setEnabled(False)
        QApplication.processEvents()

        try:
            response = self.chat.send_message(user_msg)
            ai_text = response.text

        
            self.append_message("AI", ai_text)

        except Exception as e:
            self.append_message("Error", str(e))

        
        self.get_result_button.setText("Ask")
        self.get_result_button.setEnabled(True)
        self.user_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AiApp()
    window.resize(500, 600)
    window.show()
    sys.exit(app.exec_())