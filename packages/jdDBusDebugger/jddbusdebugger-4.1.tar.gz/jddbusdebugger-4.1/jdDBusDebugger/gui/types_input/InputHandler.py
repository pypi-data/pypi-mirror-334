from PyQt6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit, QLabel
from ...Constants import SPIN_BOX_MINIMUM, SPIN_BOX_MAXIMUM
from ...types.DBusType import DBusTypeEnum, DBusType
from PyQt6.QtCore import QCoreApplication
from ...types.DBusValue import DBusValue


class InputHandler:
    def __init__(self) -> None:
        from .VariantEdit import VariantEdit
        self._variant_edit = VariantEdit

        from .ArrayInput import EditArrayButton
        self._array_button = EditArrayButton

        from .DictInput import EditDictButton
        self._dict_button = EditDictButton

        from .StructInput import EditStructButton
        self._struct_button = EditStructButton

        from .BrowseButton import BrowseButton
        self._browse_button = BrowseButton

        from .BytearrayInput import BytearrayInput
        self._bytearray_input = BytearrayInput

    def generate_widget_for_type(self, parent: QWidget | None, dbus_type: DBusType) -> QWidget:
        match dbus_type.type_const:
            case DBusTypeEnum.INTEGER:
                spin_box = QSpinBox()
                spin_box.setMinimum(SPIN_BOX_MINIMUM)
                spin_box.setMaximum(SPIN_BOX_MAXIMUM)
                return spin_box
            case DBusTypeEnum.DOUBLE:
                spin_box = QDoubleSpinBox()
                spin_box.setMinimum(SPIN_BOX_MINIMUM)
                spin_box.setMaximum(SPIN_BOX_MAXIMUM)
                return spin_box
            case DBusTypeEnum.BOOLEAN:
                boolean_box = QComboBox()
                boolean_box.addItem(QCoreApplication.translate("InputHandler", "True"), True)
                boolean_box.addItem(QCoreApplication.translate("InputHandler", "False"), False)
                return boolean_box
            case DBusTypeEnum.STRING | DBusTypeEnum.OBJECT_PATH:
                return QLineEdit()
            case DBusTypeEnum.VARIANT:
                return self._variant_edit()
            case DBusTypeEnum.ARRAY:
                return self._array_button(parent, dbus_type)
            case DBusTypeEnum.DICT:
                return self._dict_button(None)
            case DBusTypeEnum.STRUCT:
                return self._struct_button()
            case DBusTypeEnum.FILE_HANDLE:
                return self._browse_button()
            case DBusTypeEnum.BYTE_ARRAY:
                return self._bytearray_input()
            case _:
                return QLabel(QCoreApplication.translate("InputHandler", "Unsupported type"))

    def set_widget_value(self, widget: QWidget, dbus_type: DBusType, value: DBusValue) -> None:
        match dbus_type.type_const:
            case DBusTypeEnum.INTEGER:
                widget.setValue(value.value)
            case DBusTypeEnum.BOOLEAN:
                if value.value is True:
                    widget.setCurrentIndex(0)
                elif value.value is False:
                    widget.setCurrentIndex(1)
            case DBusTypeEnum.STRING | DBusTypeEnum.OBJECT_PATH:
                widget.setText(value.value)

    def get_value_from_widget(self, widget: QWidget, dbus_type: DBusType) -> DBusValue:
        match dbus_type.type_const:
            case DBusTypeEnum.INTEGER:
                return DBusValue.create(dbus_type, widget.value())
            case DBusTypeEnum.DOUBLE:
                return DBusValue.create(dbus_type, widget.value())
            case DBusTypeEnum.BOOLEAN:
                return DBusValue.create(dbus_type, widget.currentData())
            case DBusTypeEnum.STRING | DBusTypeEnum.OBJECT_PATH:
                return DBusValue.create(dbus_type, widget.text())
            case DBusTypeEnum.VARIANT:
                return widget.get_value()
            case DBusTypeEnum.ARRAY:
                return widget.get_array()
            case DBusTypeEnum.DICT:
                return DBusValue.create(dbus_type, widget.get_dict())
            case DBusTypeEnum.STRUCT:
                return DBusValue.create(dbus_type, widget.get_struct())
            case DBusTypeEnum.FILE_HANDLE:
                return DBusValue.create(dbus_type, widget.get_file_path())
            case DBusTypeEnum.BYTE_ARRAY:
                return DBusValue.create(dbus_type, widget.get_bytearray_data())
            case _:
                raise NotImplementedError()

    def get_validation_error(self, widget: QWidget, dbus_type: DBusType) -> str | None:
        match dbus_type.type_const:
            case DBusTypeEnum.FILE_HANDLE:
                return widget.get_validation_error()
            case DBusTypeEnum.BYTE_ARRAY:
                return widget.get_validation_error()
            case _:
                return None
