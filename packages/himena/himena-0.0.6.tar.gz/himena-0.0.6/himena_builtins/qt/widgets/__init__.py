from himena.plugins import register_widget_class, register_previewer_class
from himena_builtins.qt.widgets.array import QArrayView
from himena_builtins.qt.widgets.text import QTextEdit, QRichTextEdit
from himena_builtins.qt.widgets.table import QSpreadsheet, SpreadsheetConfigs
from himena_builtins.qt.widgets.dataframe import (
    QDataFrameView,
    QDataFramePlotView,
    DataFrameConfigs,
)
from himena_builtins.qt.widgets.dict_subtypes import QDataFrameStack, QArrayStack
from himena_builtins.qt.widgets.image import (
    QImageView,
    QImageLabelView,
    ImageViewConfigs,
)
from himena_builtins.qt.widgets.image_rois import QImageRoiView
from himena_builtins.qt.widgets.excel import QExcelEdit
from himena_builtins.qt.widgets.ipynb import QIpynbEdit
from himena_builtins.qt.widgets.text_previews import QSvgPreview, QMarkdowPreview
from himena_builtins.qt.widgets.model_stack import QModelStack
from himena_builtins.qt.widgets.reader_not_found import QReaderNotFound
from himena_builtins.qt.widgets.function import QFunctionEdit
from himena_builtins.qt.widgets.workflow import QWorkflowView
from himena.consts import StandardType


def register_default_widget_types() -> None:
    """Register default widget types."""

    from himena_builtins.qt.widgets import _commands

    del _commands

    # text
    register_widget_class(StandardType.TEXT, QTextEdit, priority=50)
    register_widget_class(StandardType.HTML, QRichTextEdit, priority=50)
    register_widget_class(StandardType.IPYNB, QIpynbEdit, priority=50)

    # table
    register_widget_class(
        StandardType.TABLE,
        QSpreadsheet,
        priority=50,
        plugin_configs=SpreadsheetConfigs(),
    )

    # array
    register_widget_class(StandardType.ARRAY, QArrayView, priority=50)
    register_widget_class(StandardType.IMAGE_LABELS, QImageLabelView, priority=50)
    register_widget_class(
        StandardType.IMAGE,
        QImageView,
        priority=50,
        plugin_configs=ImageViewConfigs(),
    )

    # dataframe
    register_widget_class(
        StandardType.DATAFRAME,
        QDataFrameView,
        priority=50,
        plugin_configs=DataFrameConfigs(),
    )
    register_widget_class(StandardType.DATAFRAME_PLOT, QDataFramePlotView, priority=50)

    register_widget_class(StandardType.DATAFRAMES, QDataFrameStack, priority=50)
    register_widget_class(StandardType.ARRAYS, QArrayStack, priority=50)

    # others
    register_widget_class(StandardType.ROIS, QImageRoiView, priority=50)
    register_widget_class(StandardType.EXCEL, QExcelEdit, priority=50)
    register_widget_class(StandardType.MODELS, QModelStack, priority=50)
    register_widget_class(StandardType.READER_NOT_FOUND, QReaderNotFound, priority=0)
    register_widget_class(StandardType.FUNCTION, QFunctionEdit, priority=50)
    register_widget_class(StandardType.WORKFLOW, QWorkflowView, priority=50)

    register_previewer_class(StandardType.SVG, QSvgPreview)
    register_previewer_class(StandardType.MARKDOWN, QMarkdowPreview)


register_default_widget_types()
del register_default_widget_types
