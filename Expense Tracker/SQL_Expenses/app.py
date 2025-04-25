from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QDate, Qt
from database import fetch_expenses, add_expense_to_db, delete_expense_from_db

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_table_data()

    def init_ui(self):
        self.setWindowTitle("Expense Tracker 2.0")
        self.resize(550, 500)

        # Initialize Widgets
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Id", "Date", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Connect Buttons to Methods
        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)

        # Setup Layouts
        self.setup_layout()

        # Populate Dropdown Categories
        self.populate_dropdown()

        # Apply Styling
        self.apply_styles()

    def setup_layout(self):
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        # Row 1
        row1.addWidget(QLabel("Date:"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category:"))
        row1.addWidget(self.dropdown)

        # Row 2
        row2.addWidget(QLabel("Amount:"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description:"))
        row2.addWidget(self.description)

        # Row 3 (Buttons)
        row3.addWidget(self.add_button)
        row3.addWidget(self.delete_button)

        # Add rows to main layout
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def populate_dropdown(self):
        categories = ["Food", "Transportation", "Rent", "Shopping", "Entertainment", "Bills", "Other"]
        self.dropdown.addItems(categories)

    def apply_styles(self):
        self.setStyleSheet("""
        /* Base styling */
        QWidget {
            background-color: #f0f4f8;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
            color: #333;
        }

        /* Headings for labels */
        QLabel {
            font-size: 16px;
            color: #34495e;
            font-weight: bold;
            padding: 10px;
        }

        /* Styling for input fields */
        QLineEdit, QComboBox, QDateEdit {
            background-color: #ffffff;
            font-size: 14px;
            color: #34495e;
            border: 2px solid #2980b9;
            border-radius: 8px;
            padding: 8px;
        }
        QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
            border: 2px solid #3498db;
        }
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
            border: 2px solid #1abc9c;
            background-color: #ecf9fb;
        }

        /* Table styling */
        QTableWidget {
            background-color: #ffffff;
            alternate-background-color: #f8f9fa;
            gridline-color: #d1d8e0;
            selection-background-color: #3498db;
            selection-color: white;
            font-size: 14px;
            border: 1px solid #bdc3c7;
        }
        QHeaderView::section {
            background-color: #2980b9;
            color: white;
            font-weight: bold;
            padding: 6px;
            border: 1px solid #bdc3c7;
        }

        /* Scroll bar styling */
        QScrollBar:vertical {
            width: 12px;
            background-color: #f0f4f8;
            border: none;
        }
        QScrollBar::handle:vertical {
            background-color: #2980b9;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
        }

        /* Buttons */
        QPushButton {
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        /* Add Expense Button */
        QPushButton#add_button {
            background-color: #28a745; /* Green */
        }
        QPushButton#add_button:hover {
            background-color: #218838; /* Darker Green */
        }
        QPushButton#add_button:pressed {
            background-color: #1e7e34; /* Even Darker Green */
        }
        
        /* Delete Expense Button */
        QPushButton#delete_button {
            background-color: #dc3545; /* Red */
        }
        QPushButton#delete_button:hover {
            background-color: #c82333; /* Darker Red */
        }
        QPushButton#delete_button:pressed {
            background-color: #bd2130; /* Even Darker Red */
        }

        /* Disabled button's style */
        QPushButton:disabled {
            background-color: #bdc3c7;
            color: #6e6e6e;
        }

        /* Tooltip styling */
        QToolTip {
            background-color: #34495e;
            color: #ffffff;
            # color : #0a0a0a;
            border: 1px solid #333;
            font-size: 12px;
            padding: 6px;
            border-radius: 4px;
        }
        """)

        # Set object names for buttons to apply specific styles
        self.add_button.setObjectName("add_button")
        self.delete_button.setObjectName("delete_button")

    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(expense):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description cannot be empty!")
            return

        if add_expense_to_db(date, category, amount, description):
            self.load_table_data()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add expense")

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select an expense to delete.")
            return

        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to delete this expense?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes and delete_expense_from_db(expense_id):
            self.load_table_data()

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()