import pandas as pd
import datetime
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

class DataLoaderPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setLayout(QVBoxLayout())

        # Adding UI Elements
        label = QLabel("UPLOAD YOUR FILES")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tabdb_button = QPushButton("Upload tabdb.csv")
        self.playdb_button = QPushButton("Upload playdb.csv")
        self.requestdb_button = QPushButton("Upload requestdb.csv")

        self.status_label = QLabel()
        self.next_button = QPushButton("NEXT")
        self.next_button.setEnabled(False)
        self.next_button.setFixedWidth(150)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.tabdb_button)
        button_layout.addWidget(self.playdb_button)
        button_layout.addWidget(self.requestdb_button)

        self.layout().addWidget(label)
        self.layout().addLayout(button_layout)
        self.layout().addWidget(self.status_label)
        self.layout().addWidget(
            self.next_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Adding button connections
        self.tabdb_button.clicked.connect(lambda: self.upload_file("tabdb"))
        self.playdb_button.clicked.connect(lambda: self.upload_file("playdb"))
        self.requestdb_button.clicked.connect(lambda: self.upload_file("requestdb"))
        self.next_button.clicked.connect(self.main_window.go_to_query_page)

        self.data_frames = {"tabdb": None, "playdb": None, "requestdb": None}
        self.update_status_message()

    def upload_file(self, file_type):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            try:
                user_df = pd.read_csv(file_path)
                if file_type == "tabdb" and self.validate_tab_df(user_df):
                    self.data_frames[file_type] = user_df
                elif file_type == "playdb" and self.validate_play_df(user_df):
                    self.data_frames[file_type] = user_df
                elif file_type == "requestdb" and self.validate_request_df(user_df):
                    self.data_frames[file_type] = user_df
                else:
                    self.data_frames[file_type] = None
                self.update_status_message()
                if all(df is not None for df in self.data_frames.values()):
                    self.status_label.setText(
                        "All files successfully loaded and validated!"
                    )
                    self.next_button.setEnabled(True)
                    self.tabdb_button.setEnabled(False)
                    self.playdb_button.setEnabled(False)
                    self.requestdb_button.setEnabled(False)
            except Exception as e:
                self.show_message(
                    "Error",
                    f"Error loading {file_type}.csv: {str(e)}",
                    QMessageBox.Icon.Critical,
                )
        else:
            self.show_message(
                "Error",
                f"{file_type}.csv not uploaded. Please try again.",
                QMessageBox.Icon.Warning,
            )

    def update_status_message(self):
        messages = []
        for file_type, df in self.data_frames.items():
            if df is not None:
                messages.append(f"{file_type}.csv: Uploaded successfully!")
            else:
                messages.append(f"{file_type}.csv: Not uploaded")

        self.status_label.setText("\n".join(messages))

    def show_validation_result(self, errors):
        if errors:
            numbered_errors = [f"{i + 1}. {error}" for i, error in enumerate(errors)]
            error_message = "\n".join(numbered_errors)
            self.show_message(
                "Validation Error", error_message, QMessageBox.Icon.Critical
            )
            return False
        return True

    def validate_tab_df(self, tab_df):
        required_columns = [
            "song",
            "artist",
            "year",
            "type",
            "gender",
            "duration",
            "language",
            "tabber",
            "source",
            "date",
            "difficulty",
            "specialbooks",
        ]

        # Validating columns and empty data
        errors = self.validate_columns_and_empty_data(tab_df, required_columns)
        if errors:
            return self.show_validation_result(errors)

        # Performing column-specific validations
        column_validations = {
            "year": lambda col: col[
                pd.to_numeric(col, errors="coerce").apply(
                    lambda x: not (
                        isinstance(x, (int, float)) 
                        and (isinstance(x, float) and x.is_integer() or isinstance(x, int))
                        and 1800 <= x <= datetime.datetime.now().year
                    )
                )
            ],
            "type": lambda col: col[
                ~col.str.strip().str.lower().isin({"group", "person"})
            ],
            "gender": lambda col: col[
                ~col.str.strip()
                .str.lower()
                .isin({"male", "female", "duet", "ensemble", "instrumental"})
            ],
            "duration": lambda col: col[~col.str.match(r"^\d{2}:\d{2}:\d{2}$")],
            "language": lambda col: col[
                col.apply(
                    lambda x: isinstance(x, int) or (isinstance(x, str) and x.isdigit())
                )
            ],
            "tabber": lambda col: col[
                col.apply(
                    lambda x: isinstance(x, int) or (isinstance(x, str) and x.isdigit())
                )
            ],
            "source": lambda col: col[
                ~col.str.strip().str.lower().isin({"new", "old", "off"})
            ],
            "date": lambda col: col[
                pd.to_datetime(col, format="%Y%m%d", errors="coerce").isna()
            ],
            "difficulty": lambda col: col[
                ~pd.to_numeric(col, errors="coerce").apply(
                    lambda x: isinstance(x, (int, float)) and 1 <= x <= 5
                )
            ],
        }
        errors += self.validate_data(tab_df, column_validations)
        # Showing all collected errors
        return self.show_validation_result(errors)

    def validate_play_df(self, play_df):
        required_columns = ["song", "artist"]
        errors = self.validate_columns_and_empty_data(play_df, required_columns)
        if errors:
            return self.show_validation_result(errors)
        date_columns = [col for col in play_df.columns if col not in required_columns]
        errors += self.validate_play_and_request(play_df, date_columns, "playdb")

        return self.show_validation_result(errors)

    def validate_request_df(self, request_df):
        required_columns = ["song", "artist"]
        errors = self.validate_columns_and_empty_data(request_df, required_columns)
        if errors:
            return self.show_validation_result(errors)
        date_columns = [
            col for col in request_df.columns if col not in required_columns
        ]
        errors += self.validate_play_and_request(request_df, date_columns, "requestdb")
        return self.show_validation_result(errors)
    
    def validate_columns_and_empty_data(self, df, required_columns):
        errors = []

        # Check for empty DataFrame
        if df.empty or df.dropna(how="all").empty:
            errors.append("Required data not available in the uploaded file.")
            return errors

        # Check for missing columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing columns: {', '.join(missing_columns)}")

        return errors
    
    def validate_data(self, df, column_validations):
        errors = []

        for column, validation in column_validations.items():
            if column in df.columns:
                column_data = df[column].dropna()
                try:
                    invalid_rows = validation(column_data)
                    if not invalid_rows.empty:
                        # Collecting only invalid values
                        invalid_values = ", ".join(invalid_rows.astype(str).unique())
                        errors.append(
                            f"Invalid values in '{column}' column: {invalid_values}"
                        )
                except Exception as e:
                    errors.append(f"Error validating column '{column}': {str(e)}")
        return errors
    
    def validate_play_and_request(self, df, date_columns, file_type):
        errors = []
        # Validating date column headers for YYYYMMDD format
        try:
            parsed_dates = pd.to_datetime(date_columns, format="%Y%m%d", errors="coerce")
            invalid_dates = [
                date_columns[i]
                for i, valid in enumerate(~parsed_dates.isnull())
                if not valid
            ]
            if invalid_dates:
                errors.append(
                    f"Invalid date columns in {file_type}: {', '.join(invalid_dates)}. Dates must be in YYYYMMDD format."
                )
        except Exception as e:
            errors.append(f"Error validating date columns in {file_type}: {str(e)}")

        # Applying value-specific validations
        if file_type == "playdb":
            for col in date_columns:
                numeric_col = pd.to_numeric(df[col], errors="coerce")
                invalid_values = df[col][numeric_col.isna() | (numeric_col <= 0)]
                filtered_invalid_values = invalid_values.dropna().unique()

                if len(filtered_invalid_values) > 0:
                    invalid_entries = ", ".join(map(str, filtered_invalid_values))
                    errors.append(
                        f"The column '{col}' in playdb contains invalid play order values: {invalid_entries}. Play order must be a positive number."
                    )        
        elif file_type == "requestdb":
            valid_statuses = {"G", "A", "?", ""}
            for col in date_columns:
                df[col] = df[col].fillna("").astype(str).str.strip()
                invalid_values = df[col][~df[col].isin(valid_statuses)]
                if not invalid_values.empty:
                    invalid_entries = ", ".join(map(str, invalid_values.unique()))
                    errors.append(
                        f"The column '{col}' in requestdb contains invalid request status values: {invalid_entries}. Allowed values are 'G', 'A', '?', or blank."
                    )
        return errors

    def show_message(self, title, message, icon):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec()