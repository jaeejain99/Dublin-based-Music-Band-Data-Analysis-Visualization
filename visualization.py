import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton, QFileDialog
from PyQt6.QtCore import Qt
import pandas as pd
import os


class DataVisualizationPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.download_button = QPushButton("DOWNLOAD ALL GRAPHS(PDF)")
        self.download_button.setFixedWidth(200)
        layout.addWidget(self.download_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.download_button.clicked.connect(self.download_graphs)
        self.setLayout(layout)

        # Placeholder attributes for data
        self.tab_df = None
        self.play_df = None
        self.graphs = []

    def see_data(self, tab_df, play_df):
        # Load data and generate plots
        self.tab_df = tab_df
        self.play_df = play_df
        self.generate_all_plots()

    def generate_all_plots(self):
        # Plot 1: Histogram of songs by difficulty level
        self.plot_histogram(
            "difficulty",
            "Songs by Difficulty Level (The graph is based on the entire data uploaded)",
            "Difficulty Level",
            "Number of Songs"
        )

        # Plot 2: Histogram of songs by duration
        self.tab_df["duration_seconds"] = self.tab_df["duration"].apply(
            self.duration_to_seconds
        )
        self.plot_histogram(
            "duration_seconds",
            "Songs by Duration (The graph is based on the entire data uploaded)",
            "Duration (sec)",
            "Number of Songs"
        )

        # Plot 3: Bar chart of songs by language
        self.plot_bar_chart(
            "language", "Songs by Language (The graph is based on the entire data uploaded)", "Language", "Number of Songs"
        )

        # Plot 4: Bar chart of songs by source
        self.plot_bar_chart(
            "source", "Songs by Source (The graph is based on the entire data uploaded)", "Source", "Number of Songs"
        )

        # Plot 5: Bar chart of songs by decade
        self.plot_decade_chart()

        # Plot 6: Cumulative line chart of songs played
        cumulative_df = self.get_cumulative_song_count()
        self.plot_line_chart(
            cumulative_df,
            "count",
            "Songs Played Over Time (The graph is based on the entire data uploaded)",
            "Date",
            "Number of Songs"
        )

        # Plot 7: Pie chart of songs by gender
        self.plot_pie_chart("gender", "Songs by Gender (The graph is based on the entire data uploaded)")

    def duration_to_seconds(self, duration_str):
        try:
            h, m, s = map(int, duration_str.split(":"))
            return h * 3600 + m * 60 + s
        except ValueError:
            return None

    def get_cumulative_song_count(self):
        date_columns = [col for col in self.play_df.columns if col.isdigit()]
        dates = pd.to_datetime(date_columns, format="%Y%m%d", errors="coerce")
        songs_played_counts = [
            self.play_df[date].notna().sum() for date in date_columns
        ]

        cumulative_df = (
            pd.DataFrame({"Date": dates, "Songs Played": songs_played_counts})
            .sort_values(by="Date")
            .reset_index(drop=True)
        )

        cumulative_df["count"] = cumulative_df["Songs Played"].cumsum()
        return cumulative_df

    def plot_histogram(self, column, title, xlabel, ylabel):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        fig, ax = plt.subplots()

        self.tab_df[column].dropna().plot(
            kind="hist", bins=10, color="grey", edgecolor="black", linewidth=0.1, ax=ax
        )
        ax.set_title(title, fontsize=10, color="black")
        ax.set_xlabel(xlabel, fontsize=8, color="black")
        ax.set_ylabel(ylabel, fontsize=8, color="black")

        ax.tick_params(axis="both", which="both", length=2, width=2)
        ax.tick_params(axis="both", which="major", labelsize=8)
        ax.tick_params(axis="both", which="minor", labelsize=8)

        self.add_bar_label(ax)

        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()

        canvas = FigureCanvas(fig)
        tab_layout.addWidget(canvas)
        self.tab_widget.addTab(tab, title.split("(")[0])
        self.graphs.append(fig)

    def plot_bar_chart(self, column, title, xlabel, ylabel):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        fig, ax = plt.subplots()

        ax.clear()
        value_counts = self.tab_df[column].value_counts().dropna().sort_index()
        value_counts.plot(kind="bar", color="grey", ax=ax)
        ax.set_title(title, fontsize=10, color="black")
        ax.set_xlabel(xlabel, fontsize=8, color="black")
        ax.set_ylabel(ylabel, fontsize=8, color="black")

        ax.tick_params(axis="both", which="both", length=2, width=2)
        ax.tick_params(axis="both", which="major", labelsize=8)
        ax.tick_params(axis="both", which="minor", labelsize=8)

        self.add_bar_label(ax)

        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()

        canvas = FigureCanvas(fig)
        tab_layout.addWidget(canvas)
        self.tab_widget.addTab(tab, title.split("(")[0])
        self.graphs.append(fig)

    def plot_decade_chart(self):
        self.tab_df["decade"] = (self.tab_df["year"] // 10) * 10

        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        fig, ax = plt.subplots()

        ax.clear()
        self.tab_df["decade"].value_counts().sort_index().plot(
            kind="bar", color="grey", ax=ax
        )
        ax.set_xticklabels(
            [f"{int(float(label.get_text()))}s" for label in ax.get_xticklabels()]
        )
        ax.set_title("Songs by Decade (The graph is based on the entire data uploaded)", fontsize=10, color="black")
        ax.set_xlabel("Decade", fontsize=8, color="black")
        ax.set_ylabel("Number of Songs", fontsize=8, color="black")

        ax.tick_params(axis="both", which="both", length=2, width=2)
        ax.tick_params(axis="both", which="major", labelsize=8)
        ax.tick_params(axis="both", which="minor", labelsize=8)

        self.add_bar_label(ax)

        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()

        canvas = FigureCanvas(fig)
        tab_layout.addWidget(canvas)
        self.tab_widget.addTab(tab, "Songs by Decade")
        self.graphs.append(fig)

    def plot_line_chart(self, df, column, title, xlabel, ylabel):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        fig, ax = plt.subplots()

        ax.clear()
        df.plot(
            x="Date",
            y=column,
            kind="line",
            marker=".",
            color="grey",
            markersize=0.2,
            ax=ax,
            legend=False,
        )
        ax.set_title(title, fontsize=10, color="black")
        ax.set_xlabel(xlabel, fontsize=8, color="black")
        ax.set_ylabel(ylabel, fontsize=8, color="black")

        ax.tick_params(axis="both", which="both", length=2, width=2)
        ax.tick_params(axis="both", which="major", labelsize=8)
        ax.tick_params(axis="both", which="minor", labelsize=8)

        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()

        canvas = FigureCanvas(fig)
        tab_layout.addWidget(canvas)
        self.tab_widget.addTab(tab, title.split("(")[0])
        self.graphs.append(fig)

    def plot_pie_chart(self, column, title):
        self.tab_df[column] = self.tab_df[column].str.title()

        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        fig, ax = plt.subplots()

        ax.clear()
        gender_counts = (
            self.tab_df[column].value_counts().dropna()
        )
        wedges, texts, autotexts = ax.pie(
            gender_counts,
            labels=gender_counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=["#707070", "#A3A3A3", "#C7C7C7", "#E0E0E0", "#F2F2F2"],
            pctdistance=0.85,
        )
        ax.set_title(title)

        for text in texts:
            text.set_fontsize(8)
        for autotext in autotexts:
            autotext.set_fontsize(8)

        canvas = FigureCanvas(fig)
        tab_layout.addWidget(canvas)
        self.tab_widget.addTab(tab, title.split("(")[0])
        self.graphs.append(fig)

    # Displaying the count label on top of each bar
    def add_bar_label(self, ax):
        for bar in ax.patches:
            ax.annotate(
                format(bar.get_height(), ".0f"),
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center",
                va="bottom",
                fontsize=8,
            )

    def download_graphs(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Save Graphs")
        if folder:
            for i, figure in enumerate(self.graphs):
                file_path = os.path.join(
                    folder, f"Graph - {figure.gca().get_title()}.pdf"
                )
                figure.savefig(file_path)
