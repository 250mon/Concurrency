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
    QTableWidget,
    QTableWidgetItem
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
        self.result_table = QTableWidget()

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
        main_layout.addWidget(self.result_table)

        # Set layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setGeometry(20, 20, 1000, 500)

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
            self.result_table.clear()
        else:
            self.result_label.setText(f"{len(result)} records found.")
            self.show_in_qtable(result)
            # for record in result:
            #     print(record['sku_id'])
                # self.result_label.setText(str(result))

        # Close database connection
        await self.db_conn.close()

    def show_in_qtable(self, records):
        row_count = len(records)
        col_count = len(records[0])
        self.result_table.setRowCount(row_count)
        self.result_table.setColumnCount(col_count)

        headers = list(records[0].keys())
        self.result_table.setHorizontalHeaderLabels(headers)

        for row_num in range(row_count):
            for col_num, val in zip(range(col_count), records[row_num].values()):
                self.result_table.setItem(row_num, col_num, QTableWidgetItem(str(val)))

        # def record_to_row(row_num, record):
        #     for c, val in zip(range(col_count), record.values()):
        #         self.result_table.setItem(row_num, c, QTableWidgetItem(str(val)))
        #
        # list(map(record_to_row, range(row_count), records))


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
