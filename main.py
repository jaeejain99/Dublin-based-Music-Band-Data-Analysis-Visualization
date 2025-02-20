import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from loader import DataLoaderPage
from query import DataQueryPage
from visualization import DataVisualizationPage


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ukulele Tuesday Data Analyzer")
        self.setGeometry(0, 0, 900, 500)

        # Stacked Widget to switch between pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create instances of each page
        self.data_loader_page = DataLoaderPage(self)
        self.data_query_page = DataQueryPage(self)
        self.data_visualization_page = DataVisualizationPage(self)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.data_loader_page)
        self.stacked_widget.addWidget(self.data_query_page)
        self.stacked_widget.addWidget(self.data_visualization_page)

        # Show the first page
        self.stacked_widget.setCurrentWidget(self.data_loader_page)

    def go_to_query_page(self):
        tab_df = self.data_loader_page.data_frames.get("tabdb")
        play_df = self.data_loader_page.data_frames.get("playdb")
        request_df = self.data_loader_page.data_frames.get("requestdb")
        self.data_query_page.get_data(tab_df, play_df, request_df)
        self.stacked_widget.setCurrentWidget(self.data_query_page)

    def go_to_visualization_page(self):
        tab_df = self.data_loader_page.data_frames.get("tabdb")
        play_df = self.data_loader_page.data_frames.get("playdb")
        if tab_df is not None:
            self.data_visualization_page.see_data(tab_df, play_df)
        self.stacked_widget.setCurrentWidget(self.data_visualization_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())
