from AnyQt.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QHBoxLayout, QTextEdit
)
from AnyQt.QtGui import QFont, QTextCursor
from AnyQt.QtCore import Qt
import sys


class ChatbotUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chatbot")
        self.setGeometry(200, 200, 500, 600)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Chat display (Read-only)
        self.chat_display = QTextBrowser()
        self.chat_display.setFont(QFont("Arial", 12))
        self.chat_display.setStyleSheet(
            "background-color: #F5F5F5; border-radius: 8px; padding: 10px;"
        )
        layout.addWidget(self.chat_display)

        # Input area
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.input_box = QLineEdit()
        self.input_box.setFont(QFont("Arial", 12))
        self.input_box.setStyleSheet(
            "border: 2px solid #CCCCCC; border-radius: 6px; padding: 6px;"
        )
        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.send_button.setStyleSheet(
            "background-color: #007BFF; color: white; border-radius: 6px; padding: 6px;"
            "border: none;"
        )
        self.send_button.setFixedWidth(80)

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        # Connect button click
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)  # Press Enter to send

    def send_message(self):
        user_text = self.input_box.text().strip()
        if user_text:
            self.append_message(user_text, "user")
            self.input_box.clear()  # Clear input field

            # Simulate a bot response
            bot_response = "This is a bot response!"
            self.append_message(bot_response, "bot")

    def append_message(self, text, sender):
        """Formats and appends a message to the chat display."""
        if sender == "user":
            color = "#007BFF"
            align = "right"
            bg_color = "rgba(0, 123, 255, 0.2)"  # Semi-transparent blue
        else:
            color = "#28A745"
            align = "left"
            bg_color = "rgba(40, 167, 69, 0.2)"  # Semi-transparent green

        # Create a styled HTML message bubble
        message_html = f"""
        <div style="
            background-color: {bg_color};
            color: {color};
            padding: 8px 12px;
            border-radius: 12px;
            max-width: 70%;
            margin: 5px 10px;
            text-align: left;
            display: inline-block;">
            {text}
        </div>
        """

        # Align messages properly
        if align == "right":
            message_html = f'<div style="text-align: right;">{message_html}</div>'
        else:
            message_html = f'<div style="text-align: left;">{message_html}</div>'

        self.chat_display.append(message_html)
        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)  # Auto-scroll down


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotUI()
    window.show()
    sys.exit(app.exec())
