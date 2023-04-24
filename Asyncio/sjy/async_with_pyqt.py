import asyncio
import asyncpg
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from ch05.ch05_util import connect_pg


class MainWindow(QMainWindow):
    def __init__(self, loop):
        super().__init__()
        self.loop = loop
        self.db_conn = None
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label = QLabel("Enter name:")
        self.name_input = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.result_label = QLabel()

        # Create layouts
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.label)
        input_layout.addWidget(self.name_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.result_label)

        # Set layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Connect signals
        self.submit_button.clicked.connect(self.submit_name)

    async def connect_to_database(self):
        # self.db_conn = await asyncpg.connect(user='user', password='password', database='database', host='localhost')
        self.db_conn = await connect_pg()

    async def submit_name(self):
        color_name = self.name_input.text()

        # Connect to database
        await self.connect_to_database()

        # Execute query
        query = f"SELECT * FROM table WHERE product_color='{color_name}'"
        result = await self.db_conn.fetch(query)

        # Display result
        if len(result) == 0:
            self.result_label.setText("No result found.")
        else:
            self.result_label.setText(str(result))

        # Close database connection
        await self.db_conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = QApplication([])
    main_window = MainWindow(loop)
    main_window.show()
    app.exec_()
