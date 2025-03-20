import sys

import finesse
from finesse.analysis.actions import Xaxis
from finesse.components.general import ModelElement
from finesse.detectors import PowerDetector
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PySide6 import QtCore, QtGui, QtWidgets

from virgui.component import ModelElementRectItem
from virgui.parameter_table import ParameterTableModel
from virgui.parse_layout import LAYOUTS, parse_layout

finesse.init_plotting()


# https://www.pythonguis.com/tutorials/pyside6-qgraphics-vector-graphics/
class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.scene = QtWidgets.QGraphicsScene(
            0, 0, 600, 600, backgroundBrush=QtGui.QBrush(QtCore.Qt.white)
        )

        model, hitbox_mapping, svg_b_string = parse_layout(LAYOUTS / "cavity")
        self.model = model
        background_pixmap = QtGui.QPixmap()
        background_pixmap.loadFromData(svg_b_string)
        background = QtWidgets.QGraphicsPixmapItem(background_pixmap)
        self.scene.addItem(background)

        # add completely transparent rectangles as hitboxes, so users can select elements
        for comp_name, rect in hitbox_mapping.items():
            hitbox = ModelElementRectItem(
                rect.x, rect.y, rect.width, rect.height, model.get(comp_name)
            )
            self.scene.addItem(hitbox)

        self.scene.selectionChanged.connect(self.on_selection)

        for item in self.scene.items():
            if item is not background:
                item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        # Define our layout

        # info window
        self.info_vbox = QtWidgets.QVBoxLayout()
        self.table_title = QtWidgets.QLabel(
            textFormat=QtCore.Qt.TextFormat.MarkdownText,
            textInteractionFlags=QtCore.Qt.TextInteractionFlag.TextBrowserInteraction,
            openExternalLinks=True,
        )
        self.table_view = QtWidgets.QTableView()
        self.info_vbox.addWidget(self.table_title)
        self.info_vbox.addWidget(self.table_view)

        view = QtWidgets.QGraphicsView(self.scene)
        view.setRenderHint(QtGui.QPainter.Antialiasing)

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(view)
        hbox.addLayout(self.info_vbox)

        self.tabs = QtWidgets.QTabWidget()

        # layout tab
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setLayout(hbox)
        self.tabs.addTab(self.tab1, "Layout")

        # calculate tab
        self.tab2 = QtWidgets.QWidget()
        self.tabs.addTab(self.tab2, "Calculate")
        self.setup_calculate_tab()

        # # calculate tab
        # self.tab2 = QtWidgets.QWidget()
        # self.tabs.addTab(self.tab2, "KatScript")
        # self.setup_calculate_tab()

    # this should be a separate class
    def setup_calculate_tab(self):
        calculate_hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        calculate_hbox.addLayout(vbox)

        ## PLOTTING
        self.plot_layout = QtWidgets.QVBoxLayout()
        calculate_hbox.addLayout(self.plot_layout)

        from matplotlib.figure import Figure

        # TODO let user decide where to add powerdetector
        self.circ = self.model.add(PowerDetector("circ", self.model.m2.p1.o))
        self.trans = self.model.add(PowerDetector("trans", self.model.m2.p2.o))
        self.refl = self.model.add(PowerDetector("refl", self.model.m1.p1.o))

        self.static_canvas = FigureCanvas(Figure())
        self.plot_toolbar = NavigationToolbar(self.static_canvas)
        self.plot_layout.addWidget(self.plot_toolbar)
        self.plot_layout.addWidget(self.static_canvas)

        # sweep parameter
        self.parameter_dropdown = QtWidgets.QComboBox()
        self.parameter_dropdown.addItems(
            [p.full_name for p in self.model.all_parameters]
        )
        parameter_label = QtWidgets.QLabel("Sweep Parameter:")
        self.parameter_dropdown.currentTextChanged.connect(self.on_parameter_changed)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(parameter_label)
        hbox.addWidget(self.parameter_dropdown)
        vbox.addLayout(hbox)

        # sweep mode
        self.mode_dropdown = QtWidgets.QComboBox()
        self.mode_dropdown.addItems(["lin", "log"])

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel("Sweep mode:"))
        hbox.addWidget(self.mode_dropdown)
        vbox.addLayout(hbox)

        self.start_spinbox = QtWidgets.QDoubleSpinBox()
        self.start_spinbox.setRange(-1e6, 1e6)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel("Start:"))
        hbox.addWidget(self.start_spinbox)
        vbox.addLayout(hbox)

        self.end_spinbox = QtWidgets.QDoubleSpinBox()
        self.end_spinbox.setRange(-1e6, 1e6)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel("End:"))
        hbox.addWidget(self.end_spinbox)
        vbox.addLayout(hbox)

        self.steps_spinbox = QtWidgets.QSpinBox()
        self.steps_spinbox.setRange(0, int(1e6))

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel("Steps:"))
        hbox.addWidget(self.steps_spinbox)
        vbox.addLayout(hbox)

        self.run_button = QtWidgets.QPushButton()
        self.run_button.clicked.connect(self.run_xaxis)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel("Run sweep:"))
        hbox.addWidget(self.run_button)
        vbox.addLayout(hbox)

        self.tab2.setLayout(calculate_hbox)

        # list of detectors to measure power or so?

    def make_figure_canvas(self, fig):

        # from matplotlib.figure import Figure

        temp_static_canvas = FigureCanvas(fig)
        temp_toolbar = NavigationToolbar(self.static_canvas)

        self.plot_layout.replaceWidget(self.plot_toolbar, temp_toolbar)
        self.plot_layout.replaceWidget(self.static_canvas, temp_static_canvas)

        self.static_canvas = temp_static_canvas
        self.temp_toolbar = NavigationToolbar

    @QtCore.Slot()
    def run_xaxis(self):

        sol = self.model.run(
            Xaxis(
                self.parameter_dropdown.currentText(),
                mode=self.mode_dropdown.currentText(),
                start=self.start_spinbox.value(),
                stop=self.end_spinbox.value(),
                steps=self.steps_spinbox.value(),
            )
        )
        sol.plot(show=False)
        self.make_figure_canvas(plt.gcf())
        # print(fig)
        # self.static_canvas.figure.add_axes(fig.axes[0])
        # fig.canvas.draw_idle()
        print("ran xaxis")

    @QtCore.Slot()
    def on_parameter_changed(self):
        p = self.model.get(self.parameter_dropdown.currentText())
        for spinbox in (self.start_spinbox, self.end_spinbox):
            if p.units:
                spinbox.setSuffix(f" [{p.units}]")
            else:
                spinbox.setSuffix("")

    @QtCore.Slot()
    def on_selection(self):
        items = self.scene.selectedItems()
        if len(items) == 0:
            # TODO empty info table
            pass
        elif len(items) == 1:
            item = items[0]
            assert isinstance(item.element, ModelElement)
            el: ModelElement = item.element
            par_table = el.parameter_table(return_str=False)
            info_table = ParameterTableModel(par_table)
            self.table_view.setModel(info_table)
            self.table_view.resizeRowsToContents()
            modules = el.__class__.__module__.split(".")
            doc_url = f"https://finesse.ifosim.org/docs/latest/api/{modules[1]}/{modules[2]}/{el.__class__.__module__}.{el.__class__.__name__}.html#{el.__class__.__module__}.{el.__class__.__name__}"
            self.table_title.setText(
                f"# [{el.__class__.__name__}]({doc_url}): {el.name}"
            )
        else:
            raise


def main():
    app = QtWidgets.QApplication(sys.argv)

    w = Window()
    w.tabs.show()

    app.exec()


if __name__ == "__main__":
    main()
