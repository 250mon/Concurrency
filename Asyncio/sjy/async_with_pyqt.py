import asyncio
import sys
import functools

import asyncpg
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTableWidget
)
import qasync
from qasync import asyncSlot, asyncClose, QApplication
from util import connect_pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

    @asyncSlot()
    async def connect_to_database(self):
        # self.db_conn = await asyncpg.connect(user='user', password='password', database='database', host='localhost')
        self.db_conn = await connect_pg()

    @ asyncSlot()
    async def submit_name(self):
        color_name = self.name_input.text()

        # Connect to database
        await self.connect_to_database()

        # Execute query
        query = f"SELECT * FROM sku WHERE product_color_id='{color_name}'"
        result = await self.db_conn.fetch(query)

        # Display result
        if row_count := len(result) == 0:
            self.result_label.setText("No result found.")
        else:
            self.show_in_qtable(result)
            # for record in result:
                # print(record['sku_id'])
                # self.result_label.setText(str(result))

        # Close database connection
        await self.db_conn.close()

    def show_in_qtable(self, records):
        row_count = len(records)
        col_count = len(records[0])
        table = QTableWidget(row_count, col_count)

        headers = list(records[0].keys())
        table.setHorizontalHeaderLabels(headers)
        def record_to_row(table, row_num, record):
            setItemCol = functools.partial(table.setItem, row_num)
            map(setItemCol, zip(range(col_count), record.values()))
        record_to_table_row = functools.partial(record_to_row, table)
        [map(record_to_table_row, zip(range(row_count), records))]



async def main():
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            functools.partial(close_future, future, loop)
        )

    mainWindow = MainWindow()
    mainWindow.show()

    await future
    return True


if __name__ == '__main__':
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)
