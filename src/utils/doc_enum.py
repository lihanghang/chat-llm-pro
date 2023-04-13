"""
pdf属性枚举类
"""

from enum import Enum, unique


@unique
class DocField(Enum):
    ROOT = 'root'
    PARENT_PATH = 'parent_path'
    ID = 'id'
    TREE = 'tree'
    TEXTLINES = 'textlines'
    NUMBER = 'number'
    PAGE_NUMBER = 'page_number'
    HEADER = 'header'
    FOOTER = 'footer'
    DATA = 'data'
    CHILDREN = 'children'
    PAGES = 'pages'
    TABLES = 'tables'
    SPANS = 'spans'
    BBOX = 'bbox'
    BODY = 'body'
    BLOCK = 'blocks'
    PDF_INFO = 'pdf_info'
    FONTS = 'fonts'
    TYPE = 'type'
    # 类型值
    COVER = '<封面>'
    MAINTEXT = '<正文>'
    ROOTNODE = 'RootNode'
    TABLE = 'table'
    SECTION = 'section'
    TITLE = 'title'
    TEXT = 'text'
    FIGURE = 'figure'
    ITEMS = 'items'
