from PyQt6.QtCore import QMetaType
from .EnumHelper import EnumHelper
from typing import Any
import re


class DBusTypeEnum(EnumHelper):
    UNKNOWN = 0
    INTEGER = 1
    DOUBLE = 2
    BYTE = 3
    BOOLEAN = 4
    STRING = 5
    VARIANT = 6
    OBJECT_PATH = 7
    FILE_HANDLE = 8
    ARRAY = 9
    STRUCT = 10
    DICT = 11
    BYTE_ARRAY = 12


class DBusSignatureTypeEnum(EnumHelper):
    UNKNOWN = 0
    INT = 0
    UINT = 1


class DBusType:
    def __init__(self) -> None:
        self.type_text = ""
        self.type_const = DBusTypeEnum.UNKNOWN
        self.signature_type_const = DBusSignatureTypeEnum.UNKNOWN

        self.array_type: "DBusType" | None = None

    @classmethod
    def from_type_text(cls: type["DBusType"], type_text: str) -> "DBusType":
        dbus_type = cls()

        dbus_type.type_text = type_text

        if len(type_text) == 1:
            match type_text:
                case "n" | "q" | "i" | "x" | "t":
                    dbus_type.type_const = DBusTypeEnum.INTEGER
                    dbus_type.signature_type_const = DBusSignatureTypeEnum.INT
                case "u":
                    dbus_type.type_const = DBusTypeEnum.INTEGER
                    dbus_type.signature_type_const = DBusSignatureTypeEnum.UINT
                case "d":
                    dbus_type.type_const = DBusTypeEnum.DOUBLE
                case "y":
                    dbus_type.type_const = DBusTypeEnum.BYTE
                case "b":
                    dbus_type.type_const = DBusTypeEnum.BOOLEAN
                case "s":
                    dbus_type.type_const = DBusTypeEnum.STRING
                case "v":
                    dbus_type.type_const = DBusTypeEnum.VARIANT
                case "o":
                    dbus_type.type_const = DBusTypeEnum.OBJECT_PATH
                case "h":
                    dbus_type.type_const = DBusTypeEnum.FILE_HANDLE
                case _:
                    dbus_type.type_const = DBusTypeEnum.UNKNOWN
        else:
            if re.match(r"a{[a-z]{2,}}", type_text) is not None:
                dbus_type.type_const = DBusTypeEnum.DICT
                #dbus_type.dict_key = DBusType(dbus_type.type_text[2])
                #dbus_type.dict_value = DBusType(dbus_type.type_text[3:-1])
            elif type_text.startswith("a"):
                dbus_type.type_const = DBusTypeEnum.ARRAY
                dbus_type.array_type = cls.from_type_text(type_text[1:])
                if dbus_type.array_type.type_const == DBusTypeEnum.BYTE:
                    dbus_type.type_const = DBusTypeEnum.BYTE_ARRAY
            else:
                dbus_type.type_const = DBusTypeEnum.UNKNOWN

        return dbus_type

    @classmethod
    def from_type_const(cls: type["DBusType"], type_const: int) -> "DBusType":
        dbus_type = cls()

        dbus_type.type_const = type_const

        return dbus_type

    @classmethod
    def from_type_const_with_signature(cls: type["DBusType"], type_const: int, signature_type_const: int) -> "DBusType":
        dbus_type = cls()

        dbus_type.type_const = type_const
        dbus_type.signature_type_const = signature_type_const

        return dbus_type

    @classmethod
    def from_display_name(cls: type["DBusType"], name: str) -> "DBusType":
        for current_type in cls.get_available_types():
            if current_type.get_display_name() == name:
                return current_type

    @classmethod
    def from_json_data(cls: type["DBusType"], json_data: dict[str, Any]) -> "DBusType":
        dbus_type = cls()

        dbus_type.type_text = json_data["type_text"]
        dbus_type.type_const = DBusTypeEnum.get_enum_value_by_name(json_data["type_const"])
        dbus_type.signature_type_const = DBusTypeEnum.get_enum_value_by_name(json_data["signature_type_const"])

        match dbus_type.type_const:
            case DBusTypeEnum.ARRAY:
                dbus_type.array_type = cls.from_json_data("array_type")

        return dbus_type

    def get_json_data(self) -> dict[str, Any]:
        json_data = {
            "type_text": self.type_text,
            "type_const": DBusTypeEnum.get_enum_name_by_value(self.type_const),
            "signature_type_const": DBusSignatureTypeEnum.get_enum_name_by_value(self.signature_type_const)
        }

        match self.type_const:
            case DBusTypeEnum.ARRAY:
                json_data["array_type"] = self.array_type.get_json_data()

        return json_data

    def get_display_name(self) -> str:
        match self.type_const:
            case DBusTypeEnum.INTEGER:
                return "Integer"
            case DBusTypeEnum.DOUBLE:
                return "Double"
            case DBusTypeEnum.BYTE:
                return "Byte"
            case DBusTypeEnum.BOOLEAN:
                return "Boolean"
            case DBusTypeEnum.STRING:
                return "String"
            case DBusTypeEnum.VARIANT:
                return "Variant"
            case DBusTypeEnum.OBJECT_PATH:
                return "Object Path"
            case DBusTypeEnum.FILE_HANDLE:
                return "File Handle"
            case DBusTypeEnum.ARRAY:
                return "Array"
            case DBusTypeEnum.STRUCT:
                return "Struct"
            case DBusTypeEnum.DICT:
                return "Dict"
            case DBusTypeEnum.BYTE_ARRAY:
                return "Bytearray"
            case _:
                return "Unknown"

    def get_qmeta_type(self) -> QMetaType:
        match self.type_const:
            case DBusTypeEnum.INTEGER:
                match self.signature_type_const:
                    case DBusSignatureTypeEnum.UINT:
                        return QMetaType(QMetaType.Type.UInt.value)
                    case _:
                        return QMetaType(QMetaType.Type.Int.value)
            case DBusTypeEnum.DOUBLE:
                return QMetaType(QMetaType.Type.Double.value)
            case DBusTypeEnum.BOOLEAN:
                return QMetaType(QMetaType.Type.Bool.value)
            case DBusTypeEnum.STRING:
                return QMetaType(QMetaType.Type.QString.value)

    def is_simple_type(self) -> bool:
        return self.type_const in (DBusTypeEnum.INTEGER, DBusTypeEnum.DOUBLE, DBusTypeEnum.BOOLEAN, DBusTypeEnum.STRING)

    def __repr__(self) -> str:
        return f"DBusType(type_text: '{self.type_text}' type_const: {DBusTypeEnum.get_enum_name_by_value(self.type_const)}, signature_type_const: {DBusSignatureTypeEnum.get_enum_name_by_value(self.signature_type_const)}, array_type: {self.array_type})"

    @classmethod
    def get_available_types(cls: type["DBusType"]) -> list["DBusType"]:
        return [
            cls.from_type_const_with_signature(DBusTypeEnum.INTEGER, DBusSignatureTypeEnum.INT),
            cls.from_type_const_with_signature(DBusTypeEnum.INTEGER, DBusSignatureTypeEnum.UINT),
            cls.from_type_const(DBusTypeEnum.DOUBLE),
            cls.from_type_const(DBusTypeEnum.BYTE),
            cls.from_type_const(DBusTypeEnum.BOOLEAN),
            cls.from_type_const(DBusTypeEnum.STRING),
            cls.from_type_const(DBusTypeEnum.VARIANT),
            cls.from_type_const(DBusTypeEnum.OBJECT_PATH),
            cls.from_type_const(DBusTypeEnum.FILE_HANDLE),
            cls.from_type_const(DBusTypeEnum.ARRAY),
            cls.from_type_const(DBusTypeEnum.STRUCT),
            cls.from_type_const(DBusTypeEnum.DICT),
            cls.from_type_const(DBusTypeEnum.BYTE_ARRAY),
        ]
