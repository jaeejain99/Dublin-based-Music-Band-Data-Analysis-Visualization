import pandas as pd
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QHBoxLayout,
    QDateEdit,
    QListWidget,
    QListWidgetItem,
    QCheckBox,
    QTabWidget,
)
from PyQt6.QtCore import Qt, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class DataQueryPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        ###################### TAB 1 ##############################
        tab1 = QWidget()
        tab_layout1 = QVBoxLayout(tab1)
        # UI Elements
        self.filter_layout = QHBoxLayout()
        self.filter_boxes = (
            {}
        )
        apply_filter_button1 = QPushButton("APPLY FILTER")
        apply_filter_button1.setFixedWidth(150)
        # Column selection widget
        column_selector_label = QLabel("Select Columns To Display:")
        self.column_selector = QListWidget()
        self.column_selector.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.column_selector.setFixedHeight(100)
        # Sorting widgets
        sort_column_label = QLabel("Sort By Column:")
        self.sort_column_combo = QComboBox()
        self.sort_order_combo = QComboBox()
        self.sort_order_combo.addItems(["Ascending", "Descending"])
        # Layout for sorting controls
        self.sort_layout = QHBoxLayout()
        self.sort_layout.addWidget(sort_column_label)
        self.sort_layout.addWidget(self.sort_column_combo)
        self.sort_layout.addWidget(self.sort_order_combo)
        # Date range selection widgets for Song Played First Time
        date_range_layout1 = QHBoxLayout()
        self.start_date_edit1 = QDateEdit()
        self.start_date_edit1.setCalendarPopup(True)
        self.start_date_edit1.setDate(
            QDate.currentDate().addMonths(-60)
        )
        self.end_date_edit1 = QDateEdit()
        self.end_date_edit1.setCalendarPopup(True)
        self.end_date_edit1.setDate(QDate.currentDate())
        self.checkbox = QCheckBox("Apply Date Range On Below Table")
        date_range_layout1.addWidget(
            QLabel(
                "Select Date Range To Get Songs Played First Time: \tStart Date:\t\t"
            )
        )
        date_range_layout1.addWidget(self.start_date_edit1)
        date_range_layout1.addWidget(QLabel("\tEnd Date:"))
        date_range_layout1.addWidget(self.end_date_edit1)
        date_range_layout1.addWidget(self.checkbox)

        self.table_widget1 = QTableWidget()
        # Adding UI elements to layout of tab 1
        tab_layout1.addWidget(
            apply_filter_button1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        tab_layout1.addLayout(self.filter_layout)
        tab_layout1.addWidget(column_selector_label)
        tab_layout1.addWidget(self.column_selector)
        tab_layout1.addLayout(self.sort_layout)
        tab_layout1.addLayout(date_range_layout1)
        tab_layout1.addWidget(self.table_widget1)
        self.tab_widget.addTab(tab1, "TAB INFO")

        ###################### TAB 2 ###########################
        tab2 = QWidget()
        tab_layout2 = QVBoxLayout(tab2)
        # UI Elements
        apply_filter_button2 = QPushButton("APPLY FILTER")
        apply_filter_button2.setFixedWidth(150)
        # Date range selection widgets for Song Played That Day
        date_range_layout2 = QHBoxLayout()
        self.start_date_edit2 = QDateEdit()
        self.start_date_edit2.setCalendarPopup(True)
        self.start_date_edit2.setDate(
            QDate.currentDate().addMonths(-60)
        )
        self.end_date_edit2 = QDateEdit()
        self.end_date_edit2.setCalendarPopup(True)
        self.end_date_edit2.setDate(QDate.currentDate())
        date_range_layout2.addWidget(
            QLabel(
                "Select Date Range To Get Songs Played On Tuesdays: \t\tStart Date:\t\t"
            )
        )
        date_range_layout2.addWidget(self.start_date_edit2)
        date_range_layout2.addWidget(QLabel("\t\tEnd Date:"))
        date_range_layout2.addWidget(self.end_date_edit2)

        songs_played_label = QLabel("Songs Played On Selected Tuesdays:")
        self.table_widget2 = QTableWidget()
        # Adding UI elements to layout of tab 2
        tab_layout2.addWidget(
            apply_filter_button2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        tab_layout2.addLayout(date_range_layout2)
        tab_layout2.addWidget(songs_played_label)
        tab_layout2.addWidget(self.table_widget2)
        self.tab_widget.addTab(tab2, "SONGS PLAYED INFO")

        ############################# TAB 3 #########################
        tab3 = QWidget()
        self.tab_layout3 = QVBoxLayout(tab3)
        # UI Elements
        apply_filter_button3 = QPushButton("APPLY FILTER")
        apply_filter_button3.setFixedWidth(150)
        # Date range selection widgets for Song Played That Day
        date_range_layout3 = QHBoxLayout()
        self.start_date_edit3 = QDateEdit()
        self.start_date_edit3.setCalendarPopup(True)
        self.start_date_edit3.setDate(
            QDate.currentDate().addMonths(-60)
        )
        self.end_date_edit3 = QDateEdit()
        self.end_date_edit3.setCalendarPopup(True)
        self.end_date_edit3.setDate(QDate.currentDate())
        date_range_layout3.addWidget(
            QLabel(
                "Select Date Range To Get Songs Requested On Tuesdays: \t\tStart Date:\t\t"
            )
        )
        date_range_layout3.addWidget(self.start_date_edit3)
        date_range_layout3.addWidget(QLabel("\t\tEnd Date:"))
        date_range_layout3.addWidget(self.end_date_edit3)
        songs_requested_label = QLabel("Songs Requested On Selected Tuesdays:")
        # Adding UI elements to layout of tab 3
        self.tab_layout3.addWidget(
            apply_filter_button3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.tab_layout3.addLayout(date_range_layout3)
        self.tab_layout3.addWidget(songs_requested_label)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.clear()
        self.ax.axis('off')
        self.tab_layout3.addWidget(self.canvas)
        self.tab_widget.addTab(tab3, "SONGS REQUESTED INFO")

        next_button = QPushButton("NEXT")
        next_button.setFixedWidth(150)
        self.layout.addWidget(next_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Connecting buttons to actions
        apply_filter_button1.clicked.connect(self.apply_tabdf_filter)
        apply_filter_button2.clicked.connect(self.apply_playdf_filter)
        apply_filter_button3.clicked.connect(self.apply_requestdf_filter)
        next_button.clicked.connect(self.main_window.go_to_visualization_page)

        # Placeholder for the loaded data
        self.tab_df = pd.DataFrame()
        self.play_df = pd.DataFrame()
        self.request_df = pd.DataFrame()

    def get_data(self, tab_df, play_df, request_df):
        self.tab_df = tab_df
        self.play_df = play_df
        self.request_df = request_df
        self.modify_data()
        self.setup_filter_boxes()
        self.setup_column_selector()
        self.setup_sorting()
        self.display_data(self.tab_df)  # Showing the initial data

    def modify_data(self):
        self.tab_df["total_play_count"] = self.tab_df["song"].map(
            self.play_df.set_index("song").iloc[:, 1:].notna().sum(axis=1)
        ) # Adding the number of times each song was played
        self.tab_df = self.tab_df.drop("tabber", axis=1)
        self.tab_df["date"] = pd.to_datetime(
            self.tab_df["date"].dropna().astype(int).astype(str),
            format="%Y%m%d",
            errors="coerce",
        ).dt.date
        self.tab_df["duration_seconds"] = self.tab_df["duration"].dropna().apply(
            self.duration_to_seconds
        ) # Converting time format from minutes to seconds

    def duration_to_seconds(self, duration_str):
        try:
            h, m, s = map(int, duration_str.split(":"))
            return h * 3600 + m * 60 + s
        except ValueError:
            return None  # Handle invalid formats gracefully

    def setup_filter_boxes(self):
        # Creating a combo box for each column and populate with unique values
        for column in self.tab_df.columns:
            if self.tab_df[column].dtype == "object" and column not in [
                "duration",
                "date",
            ]:
                # Making all entries to camel case
                self.tab_df[column] = self.tab_df[column].str.title()
            if column not in ("date", "duration_seconds"):
                column_layout = QVBoxLayout()
                column_label = QLabel(column)
                column_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                column_layout.addWidget(column_label)
                combo_box = QComboBox()
                combo_box.addItem("All")
                if column == "year":
                    combo_box.addItems(
                        [
                            "2020-2030",
                            "2010-2020",
                            "2000-2010",
                            "1990-2000",
                            "1980-1990",
                            "1970-1980",
                            "1960-1970",
                            "1950-1960",
                            "1940-1950",
                            "1930-1940",
                            "1920-1930",
                            "1910-1920",
                            "1900-1910",
                            "Before 1900",
                        ]
                    )
                elif column == "difficulty":
                    combo_box.addItems(["0-1", "1-2", "2-3", "3-4", "4-5"])
                elif column == "total_play_count":
                    combo_box.addItems(
                        [
                            "0-10",
                            "10-20",
                            "20-30",
                            "30-40",
                            "40-50",
                            "50-60",
                            "60-70",
                            "70-80",
                            "80-90",
                            "90-100",
                            "Above 100",
                        ]
                    )
                elif column == "duration":
                    combo_box.addItems(
                        [
                            "0-1 min",
                            "1-2 min",
                            "2-3 min",
                            "3-4 min",
                            "4-5 min",
                            "Above 5 min",
                        ]
                    )
                else:
                    combo_box.addItems(
                        sorted(self.tab_df[column].dropna().unique().astype(str))
                    )
                column_layout.addWidget(combo_box)
                self.filter_layout.addLayout(column_layout)
                self.filter_boxes[column] = combo_box

    def setup_column_selector(self):
        self.column_selector.clear()
        for column in self.tab_df.columns:
            if column != "duration_seconds":
                item = QListWidgetItem(column)
                self.column_selector.addItem(item)

    def setup_sorting(self):
        for column in self.tab_df.columns:
            if column != "duration_seconds":
                self.sort_column_combo.addItem(column)

    def display_data(self, df):
        # Sorting the DataFrame according to sort selector
        sort_column = self.sort_column_combo.currentText()
        sort_order = self.sort_order_combo.currentText() == "Ascending"
        if sort_column:
            df = df.sort_values(by=sort_column, ascending=sort_order)
        # Fetching the selected columns from the column selector
        selected_columns = [
            item.text() for item in self.column_selector.selectedItems()
        ]
        if not selected_columns:
            selected_columns = (
                df.columns.tolist()
            )
        # Filtering the DataFrame to include only the selected columns
        df = df[selected_columns]
        self.table_widget1.clear()

        if "duration_seconds" in df.columns:
            df = df.drop("duration_seconds", axis=1)

        self.table_widget1.setRowCount(len(df))
        self.table_widget1.setColumnCount(len(df.columns))
        self.table_widget1.setHorizontalHeaderLabels(df.columns)

        # Populating the table with DataFrame values
        for i, row in enumerate(df.itertuples(index=False)):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                # Making values non-editable
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                self.table_widget1.setItem(i, j, item)
        self.table_widget1.resizeColumnsToContents()

    def apply_tabdf_filter(self):
        filtered_df = self.tab_df
        # Checking if date range check box is selected
        if self.checkbox.isChecked():
            start_date1 = self.start_date_edit1.date().toPyDate()
            end_date1 = self.end_date_edit1.date().toPyDate()
            filtered_df = filtered_df[
                (filtered_df["date"] >= start_date1)
                & (filtered_df["date"] <= end_date1)
            ]

        # Applying filters based on combo box selections
        for column, combo_box in self.filter_boxes.items():
            value = combo_box.currentText()
            if value != "All":
                if column == "year":
                    if value == "Before 1900":
                        filtered_df = filtered_df[(filtered_df[column] < 1900)]
                    else:
                        lower, upper = map(int, value.split("-"))
                        filtered_df = filtered_df[
                            (filtered_df[column] >= lower)
                            & (filtered_df[column] < upper)
                        ]
                elif column == "difficulty":
                    lower, upper = map(float, value.split("-"))
                    filtered_df = filtered_df[
                        (filtered_df[column] >= lower) & (filtered_df[column] < upper)
                    ]
                elif column == "total_play_count":
                    if value == "Above 100":
                        filtered_df = filtered_df[(filtered_df[column] > 100)]
                    else:
                        lower, upper = map(int, value.split("-"))
                        filtered_df = filtered_df[
                            (filtered_df[column] >= lower)
                            & (filtered_df[column] < upper)
                        ]
                elif column == "duration":
                    if value == "Above 5 min":
                        filtered_df = filtered_df[
                            (filtered_df["duration_seconds"] > 5 * 60)
                        ]
                    else:
                        value = value.split(" ")[0]
                        lower, upper = map(int, value.split("-"))
                        filtered_df = filtered_df[
                            (filtered_df["duration_seconds"] >= lower * 60)
                            & (filtered_df["duration_seconds"] < upper * 60)
                        ]
                else:
                    filtered_df = filtered_df[filtered_df[column].astype(str) == value]

        self.display_data(filtered_df)

    def apply_playdf_filter(self):
        start_date = self.start_date_edit2.date().toPyDate()
        end_date = self.end_date_edit2.date().toPyDate()
        
        play_df_copy = self.play_df.copy()
        transformed_columns = list(play_df_copy.columns[:2]) + list(
            pd.to_datetime(
                play_df_copy.columns[2:].astype(int).astype(str),
                format="%Y%m%d",
                errors="coerce",
            ).date
        )
        play_df_copy.columns = transformed_columns
        date_range_cols = [
            col for col in play_df_copy.columns[2:] if start_date <= col <= end_date
        ]
        songs_played_list = play_df_copy.loc[
            play_df_copy[date_range_cols].gt(0).any(axis=1), "song"
        ]

        play_counts = play_df_copy[date_range_cols].gt(0).sum(axis=1)

        df_combined = pd.DataFrame({
            'song': songs_played_list,
            'play_count': play_counts[songs_played_list.index]
        })
        df_combined = df_combined.dropna(subset=['song'])
        df_combined.reset_index(drop=True, inplace=True)

        self.table_widget2.clear()
        self.table_widget2.setColumnCount(len(df_combined.columns))
        self.table_widget2.setRowCount(len(df_combined))
        self.table_widget2.setHorizontalHeaderLabels(df_combined.columns)

        # Populating the table with DataFrame values
        for i, row in enumerate(df_combined.itertuples(index=False)):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                # Making values non-editable
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                self.table_widget2.setItem(i, j, item)
        self.table_widget2.resizeColumnsToContents()   


    def apply_requestdf_filter(self):
        start_date = self.start_date_edit3.date().toPyDate()
        end_date = self.end_date_edit3.date().toPyDate()
        
        request_df_copy = self.request_df.copy()
        request_df_copy.columns = list(request_df_copy.columns[:2]) + list(
            pd.to_datetime(
                request_df_copy.columns[2:].astype(int).astype(str),
                format="%Y%m%d",
                errors="coerce",
            ).date
        )
        date_range_cols = [
            col for col in request_df_copy.columns[2:] if start_date <= col <= end_date
        ]
        counts = self.get_request_count(request_df_copy[date_range_cols])
        self.plot_requested_song_pie_chart(counts)

    def get_request_count(self, request_data):
        return {
            "A = Audience": (request_data == "A").sum().sum(),
            "G = Group": (request_data == "G").sum().sum(),
            "? = Unknown": (request_data == "?").sum().sum(),
        }
    
    def plot_requested_song_pie_chart(self,counts):
        counts = {
            key: value for key, value in counts.items() 
            if value > 0
        }
        self.ax.clear()
        values = list(counts.values())
        labels = list(counts.keys())
        wedges, texts, autotexts = self.ax.pie(
            values,
            labels=labels,
            autopct=lambda x: self.pie_chart_labels(x, values),
            startangle=140,
            colors=["#707070", "#A3A3A3", "#C7C7C7"],
            pctdistance=0.85,
        )

        for text in texts:
            text.set_fontsize(8)
        for autotext in autotexts:
            autotext.set_fontsize(8)
        self.canvas.draw()

    def pie_chart_labels(self, x, allvals):
        absolute = int(
            x / 100.*sum(allvals)
        )
        return f"{absolute} ({x:.1f}%)"