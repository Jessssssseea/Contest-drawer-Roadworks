import sys
import os
import random
import winreg
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QTextEdit, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsPixmapItem
)
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QFont, QBrush, QPixmap, QImage, QIcon
)
from PyQt5.QtCore import Qt, QRectF

import base64
# 创建图标缓存
base64_ico_data = b'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'
ico_data = base64.b64decode(base64_ico_data)
ico_path = 'temp_icon.ico'
with open(ico_path, 'wb') as f:
    f.write(ico_data)
import atexit

# ==================== 可配置的坐标常量（基于原始地图图片像素坐标） ====================
PROJECT_POS = {
    1: (1300*1.5, 3900*1.5),   # 工程1
    2: (1140*1.5, 640*1.5),    # 工程2
    3: (1840*1.5, 5800*1.5),   # 工程3
    4: (3560*1.5, 780*1.5),    # 工程4
    5: (3860*1.5, 6400*1.5),   # 工程5
    6: (6285*1.5, 6400*1.5),   # 工程6
    7: (5090*1.5, 3915*1.5),   # 工程7
    8: (5291*1.5, 770*1.5),    # 工程8
    9: (7870*1.5, 820*1.5),    # 工程9
    "隧道": (3590*1.5, 4020*1.5),
    "重力闸口": (8020*1.5, 3890*1.5),
    "充电区": (7980*1.5, 6520*1.5)
}

BACKGROUND_IMG_PATH = "工程道路.bmp"

TASK_COLORS = {
    "物料回收": QColor(33, 150, 243),
    "建设服务区": QColor(139, 195, 74),
    "搭建桥梁": QColor(255, 152, 0),
    "建设加油站": QColor(233, 30, 99),
    "隧道挖掘": QColor(96, 125, 139),
    "重力闸口": QColor(156, 39, 176),
    "自动充电": QColor(0, 188, 212)
}

def delete_file_at_exit():
    file_to_delete = ico_path
    try:
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
    except Exception as e:
        print(f"删除文件失败: {e}")

# ==================== 地图视图类 ====================
class MapGraphicsView(QGraphicsView):
    BOX_WIDTH = 1000*1.5
    BOX_HEIGHT = 600*1.5
    SMALL_SQUARE_SIZE = 250*1.5
    FIXED_CIRCLE_SIZE = 240*1.5          # 增大固定任务圆点
    MARKER_SIZE = 240*1.5                # 增大动态标记圆点
    SMALL_MARKER_SIZE = 230*1.5          # 增大叠放区域小圆点

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.bg_item = None
        self.bg_width = 0
        self.bg_height = 0
        self.load_background()

        self.dynamic_items = []
        self.calculate_zone_offsets()
        self.draw_static_elements()

    def calculate_zone_offsets(self):
        """根据矩形尺寸和小方格尺寸，计算四个小方格中心相对于工程点中心的偏移量，使其在底部水平排列"""
        half_small = self.SMALL_SQUARE_SIZE / 2
        # 矩形底部 Y 坐标 = cy + BOX_HEIGHT/2
        # 小方格中心 Y = 矩形底部 - half_small
        center_y = self.BOX_HEIGHT / 2 - half_small
        # 四个小方格中心 X 偏移（水平均匀分布，总宽度为 BOX_WIDTH）
        # 每个方格宽 SMALL_SQUARE_SIZE，四个方格紧贴排列，总宽正好等于 BOX_WIDTH
        start_x = -self.BOX_WIDTH / 2 + half_small
        self.ZONE_OFFSETS = [
            (start_x + 0 * self.SMALL_SQUARE_SIZE, center_y),  # 第1个
            (start_x + 1 * self.SMALL_SQUARE_SIZE, center_y),  # 第2个
            (start_x + 2 * self.SMALL_SQUARE_SIZE, center_y),  # 第3个
            (start_x + 3 * self.SMALL_SQUARE_SIZE, center_y)  # 第4个
        ]

    def load_background(self):
        if os.path.exists(BACKGROUND_IMG_PATH):
            pixmap = QPixmap(BACKGROUND_IMG_PATH)
            if not pixmap.isNull():
                self.bg_item = QGraphicsPixmapItem(pixmap)
                self.scene.addItem(self.bg_item)
                self.bg_width = pixmap.width()
                self.bg_height = pixmap.height()
                self.scene.setSceneRect(QRectF(0, 0, self.bg_width, self.bg_height))
                return
        self.bg_width, self.bg_height = 1200, 1000
        self.scene.setSceneRect(0, 0, self.bg_width, self.bg_height)
        QMessageBox.warning(self, "提示", f"无法加载地图文件：{BACKGROUND_IMG_PATH}\n将显示空白背景。")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.scene.sceneRect().isNull():
            self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.scene.sceneRect().isNull():
            self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def clear_dynamic_items(self):
        for item in self.dynamic_items:
            self.scene.removeItem(item)
        self.dynamic_items.clear()

    def add_dynamic_item(self, item, z=10):
        item.setZValue(z)
        self.scene.addItem(item)
        self.dynamic_items.append(item)

    def draw_static_elements(self):
        # 清除除背景外的所有静态项
        items_to_remove = []
        for item in self.scene.items():
            if item != self.bg_item and item not in self.dynamic_items:
                items_to_remove.append(item)
        for item in items_to_remove:
            self.scene.removeItem(item)

        pen = QPen(QColor(80, 80, 80), 2)
        font_size = max(12, int(self.BOX_HEIGHT * 0.15))
        font = QFont("微软雅黑", font_size, QFont.Bold)

        for pid in range(1, 10):
            if pid not in PROJECT_POS:
                continue
            cx, cy = PROJECT_POS[pid]

            # 大矩形
            rect = QRectF(cx - self.BOX_WIDTH/2, cy - self.BOX_HEIGHT/2,
                          self.BOX_WIDTH, self.BOX_HEIGHT)
            rect_item = QGraphicsRectItem(rect)
            rect_item.setPen(pen)
            rect_item.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            rect_item.setZValue(0)
            self.scene.addItem(rect_item)

            # 工程编号（放在矩形顶部）
            text_item = QGraphicsTextItem(f"工程{pid}")
            text_item.setFont(font)
            text_item.setDefaultTextColor(Qt.black)
            text_rect = text_item.boundingRect()
            # 矩形顶部 Y 坐标 = cy - BOX_HEIGHT/2，文字顶部距离矩形顶部 10 像素
            top_y = cy - self.BOX_HEIGHT / 2 + 10
            text_item.setPos(cx - text_rect.width() / 2, top_y)
            text_item.setZValue(0)
            self.scene.addItem(text_item)

            # 四个小方格
            small_pen = QPen(QColor(150, 150, 150), 1)
            half_small = self.SMALL_SQUARE_SIZE / 2
            for i, (dx, dy) in enumerate(self.ZONE_OFFSETS):
                x = cx + dx - half_small
                y = cy + dy - half_small
                small_rect = QRectF(x, y, self.SMALL_SQUARE_SIZE, self.SMALL_SQUARE_SIZE)
                rect_item = QGraphicsRectItem(small_rect)
                rect_item.setPen(small_pen)
                rect_item.setBrush(QBrush(QColor(240, 240, 240)))
                rect_item.setZValue(0)
                self.scene.addItem(rect_item)

                # 区域数字
                num_text = QGraphicsTextItem(str(i + 1))
                num_font_size = int(self.SMALL_SQUARE_SIZE * 0.2)
                num_text.setFont(QFont("Arial", num_font_size, QFont.Bold))
                num_text.setDefaultTextColor(QColor(80, 80, 80))
                num_rect = num_text.boundingRect()
                num_text.setPos(x + (self.SMALL_SQUARE_SIZE - num_rect.width())/2,
                                y + (self.SMALL_SQUARE_SIZE - num_rect.height())/2)
                num_text.setZValue(0)
                self.scene.addItem(num_text)

        # 固定任务
        fixed = [
            ("隧道挖掘", "隧道", "🚇"),
            ("重力闸口", "重力闸口", "🚧"),
            ("自动充电", "充电区", "🔌")
        ]
        for task, key, icon in fixed:
            if key not in PROJECT_POS:
                continue
            x, y = PROJECT_POS[key]
            r = self.FIXED_CIRCLE_SIZE / 2
            circle = QGraphicsEllipseItem(x - r, y - r, self.FIXED_CIRCLE_SIZE, self.FIXED_CIRCLE_SIZE)
            circle.setBrush(QBrush(TASK_COLORS[task]))
            circle.setPen(QPen(Qt.black, 1))
            circle.setZValue(0)
            self.scene.addItem(circle)
            text = QGraphicsTextItem(icon)
            icon_font_size = max(14, int(self.FIXED_CIRCLE_SIZE * 1.5))
            text.setFont(QFont("Segoe UI Emoji", icon_font_size))
            text.setDefaultTextColor(Qt.white)
            text_rect = text.boundingRect()
            text.setPos(x - text_rect.width()/2, y - text_rect.height()/2)
            text.setZValue(0)
            self.scene.addItem(text)

    def update_dynamic_items(self, draw_data):
        self.clear_dynamic_items()
        if not draw_data:
            return

        # 物料回收
        if "物料回收" in draw_data:
            data = draw_data["物料回收"]
            pid = data["工程点"]
            zone = data["区域"]
            if pid in PROJECT_POS:
                cx, cy = PROJECT_POS[pid]
                dx, dy = self.ZONE_OFFSETS[zone - 1]
                x = cx + dx - self.MARKER_SIZE/2
                y = cy + dy - self.MARKER_SIZE/2
                circle = QGraphicsEllipseItem(x, y, self.MARKER_SIZE, self.MARKER_SIZE)
                circle.setBrush(QBrush(TASK_COLORS["物料回收"]))
                circle.setPen(QPen(Qt.black, 1))
                self.add_dynamic_item(circle)
                text = QGraphicsTextItem("回")
                text_font_size = max(12, int(self.MARKER_SIZE * 0.4))
                text.setFont(QFont("微软雅黑", text_font_size, QFont.Bold))
                text.setDefaultTextColor(Qt.white)
                text_rect = text.boundingRect()
                text.setPos(x + (self.MARKER_SIZE - text_rect.width())/2,
                            y + (self.MARKER_SIZE - text_rect.height())/2)
                self.add_dynamic_item(text)

        # 建设服务区
        if "建设服务区" in draw_data:
            svc = draw_data["建设服务区"]
            four_pid = svc["工程点_4杯"]
            three_pid = svc["工程点_3杯"]
            if four_pid in PROJECT_POS:
                cx, cy = PROJECT_POS[four_pid]
                circle = QGraphicsEllipseItem(cx - self.MARKER_SIZE/2, cy - self.MARKER_SIZE/2,
                                              self.MARKER_SIZE, self.MARKER_SIZE)
                circle.setBrush(QBrush(TASK_COLORS["建设服务区"]))
                circle.setPen(QPen(Qt.black, 1))
                self.add_dynamic_item(circle)
                text = QGraphicsTextItem("服")
                text_font_size = max(12, int(self.MARKER_SIZE * 0.4))
                text.setFont(QFont("微软雅黑", text_font_size, QFont.Bold))
                text.setDefaultTextColor(Qt.white)
                text_rect = text.boundingRect()
                text.setPos(cx - text_rect.width()/2, cy - text_rect.height()/2)
                self.add_dynamic_item(text)
            if three_pid in PROJECT_POS:
                cx, cy = PROJECT_POS[three_pid]
                circle = QGraphicsEllipseItem(cx - self.MARKER_SIZE/2, cy - self.MARKER_SIZE/2,
                                              self.MARKER_SIZE, self.MARKER_SIZE)
                circle.setBrush(QBrush(QColor(100, 100, 100)))
                circle.setPen(QPen(Qt.black, 1))
                self.add_dynamic_item(circle)
                text = QGraphicsTextItem("叠")
                text_font_size = max(12, int(self.MARKER_SIZE * 0.4))
                text.setFont(QFont("微软雅黑", text_font_size, QFont.Bold))
                text.setDefaultTextColor(Qt.white)
                text_rect = text.boundingRect()
                text.setPos(cx - text_rect.width()/2, cy - text_rect.height()/2)
                self.add_dynamic_item(text)
            # 叠放区域标记（带颜色的小圆点 + "杯1","杯2","杯3"文字）
            zones = svc["叠放区域"]
            colors = svc["区域颜色"]  # 获取颜色列表
            if three_pid in PROJECT_POS:
                cx, cy = PROJECT_POS[three_pid]
                for idx, (zone, color) in enumerate(zip(zones, colors)):
                    dx, dy = self.ZONE_OFFSETS[zone - 1]
                    x = cx + dx - self.SMALL_MARKER_SIZE / 2
                    y = cy + dy - self.SMALL_MARKER_SIZE / 2
                    # 根据颜色设置圆点填充色
                    if color == "红":
                        fill_color = QColor(255, 0, 0)  # 红色
                        text_color = Qt.white
                    else:  # 绿
                        fill_color = QColor(0, 255, 0)  # 绿色
                        text_color = Qt.black
                    circle = QGraphicsEllipseItem(x, y, self.SMALL_MARKER_SIZE, self.SMALL_MARKER_SIZE)
                    circle.setBrush(QBrush(fill_color))
                    circle.setPen(QPen(Qt.black, 1))
                    self.add_dynamic_item(circle)
                    text = QGraphicsTextItem(f"杯")
                    text_font_size = max(10, int(self.SMALL_MARKER_SIZE * 0.4))
                    text.setFont(QFont("微软雅黑", text_font_size, QFont.Bold))
                    text.setDefaultTextColor(text_color)
                    text_rect = text.boundingRect()
                    text.setPos(x + (self.SMALL_MARKER_SIZE - text_rect.width()) / 2,
                                y + (self.SMALL_MARKER_SIZE - text_rect.height()) / 2)
                    self.add_dynamic_item(text)
                    self.add_dynamic_item(text)

        # 搭建桥梁
        if "搭建桥梁" in draw_data:
            data = draw_data["搭建桥梁"]
            pid = data["工程点"]
            if pid in PROJECT_POS:
                cx, cy = PROJECT_POS[pid]
                circle = QGraphicsEllipseItem(cx - self.MARKER_SIZE/2, cy - self.MARKER_SIZE/2,
                                              self.MARKER_SIZE, self.MARKER_SIZE)
                circle.setBrush(QBrush(TASK_COLORS["搭建桥梁"]))
                circle.setPen(QPen(Qt.black, 1))
                self.add_dynamic_item(circle)
                text = QGraphicsTextItem("桥")
                text_font_size = max(12, int(self.MARKER_SIZE * 0.4))
                text.setFont(QFont("微软雅黑", text_font_size, QFont.Bold))
                text.setDefaultTextColor(Qt.white)
                text_rect = text.boundingRect()
                text.setPos(cx - text_rect.width()/2, cy - text_rect.height()/2)
                self.add_dynamic_item(text)

                # 颜色顺序方块
                colors = data["颜色顺序"]
                color_map = {
                    "红": QColor(255, 0, 0),
                    "蓝": QColor(135, 206, 235),
                    "绿": QColor(0, 255, 0)
                }
                block_width = 250*1.5
                block_height = 250*1.5
                start_x = cx + self.BOX_WIDTH/2 + 110*1.5
                start_y = cy - self.BOX_HEIGHT/2 + (self.BOX_HEIGHT - len(colors)*block_height) / 2
                for i, col in enumerate(colors):
                    y = start_y + i * block_height
                    rect = QGraphicsRectItem(start_x, y, block_width, block_height)
                    rect.setBrush(QBrush(color_map[col]))
                    rect.setPen(QPen(Qt.black, 1))
                    rect.setZValue(10)
                    self.scene.addItem(rect)
                    self.dynamic_items.append(rect)
                    text = QGraphicsTextItem(col)
                    text_font_size = max(9, int(self.MARKER_SIZE * 0.35))  # 圆点直径的35%
                    text.setFont(QFont("微软雅黑", text_font_size, QFont.Bold))
                    text.setDefaultTextColor(Qt.white)
                    text_rect = text.boundingRect()
                    text.setPos(start_x + (block_width - text_rect.width())/2,
                                y + (block_height - text_rect.height())/2)
                    text.setZValue(10)
                    self.scene.addItem(text)
                    self.dynamic_items.append(text)

        # 建设加油站
        if "建设加油站" in draw_data:
            station = draw_data["建设加油站"]
            pid = station["工程点"]
            cup_zone = station["纸杯区域"]
            ball_zone = station["泡沫球区域"]
            if pid in PROJECT_POS:
                cx, cy = PROJECT_POS[pid]
                circle = QGraphicsEllipseItem(cx - self.MARKER_SIZE / 2, cy - self.MARKER_SIZE / 2,
                                              self.MARKER_SIZE, self.MARKER_SIZE)
                circle.setBrush(QBrush(TASK_COLORS["建设加油站"]))
                circle.setPen(QPen(Qt.black, 1))
                self.add_dynamic_item(circle)
                text = QGraphicsTextItem("加")
                text_font_size = max(12, int(self.MARKER_SIZE * 0.4))
                text.setFont(QFont("微软雅黑", text_font_size, QFont.Bold))
                text.setDefaultTextColor(Qt.white)
                text_rect = text.boundingRect()
                text.setPos(cx - text_rect.width() / 2, cy - text_rect.height() / 2)
                self.add_dynamic_item(text)
                # 纸杯标记
                dx, dy = self.ZONE_OFFSETS[cup_zone - 1]
                x = cx + dx - self.MARKER_SIZE/2
                y = cy + dy - self.MARKER_SIZE/2
                circle = QGraphicsEllipseItem(x, y, self.MARKER_SIZE, self.MARKER_SIZE)
                circle.setBrush(QBrush(TASK_COLORS["建设加油站"]))
                circle.setPen(QPen(Qt.black, 40))
                self.add_dynamic_item(circle)
                text = QGraphicsTextItem("杯")
                text_font_size = max(12, int(self.MARKER_SIZE * 0.4))
                text.setFont(QFont("微软雅黑", text_font_size, QFont.Bold))
                text.setDefaultTextColor(Qt.white)
                text_rect = text.boundingRect()
                text.setPos(x + (self.MARKER_SIZE - text_rect.width())/2,
                            y + (self.MARKER_SIZE - text_rect.height())/2)
                self.add_dynamic_item(text)
                # 球标记
                dx, dy = self.ZONE_OFFSETS[ball_zone - 1]
                x = cx + dx - self.MARKER_SIZE/2
                y = cy + dy - self.MARKER_SIZE/2
                circle = QGraphicsEllipseItem(x, y, self.MARKER_SIZE, self.MARKER_SIZE)
                circle.setBrush(QBrush(QColor(255, 213, 79)))
                circle.setPen(QPen(Qt.black, 40))
                self.add_dynamic_item(circle)
                text = QGraphicsTextItem("球")
                text_font_size = max(12, int(self.MARKER_SIZE * 0.4))
                text.setFont(QFont("微软雅黑", text_font_size, QFont.Bold))
                text.setDefaultTextColor(Qt.black)
                text_rect = text.boundingRect()
                text.setPos(x + (self.MARKER_SIZE - text_rect.width())/2,
                            y + (self.MARKER_SIZE - text_rect.height())/2)
                self.add_dynamic_item(text)

# ==================== 主窗口（不变） ====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("道路工程比赛抽签系统")
        self.setWindowIcon(QIcon('temp_icon.ico'))
        self.current_group = "高中"
        self.lottery_data = {}

        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        win_width = max(1000, int(screen_width * 0.85))
        win_height = max(700, int(screen_height * 0.8))
        self.resize(win_width, win_height)
        self.move((screen_width - win_width) // 2, (screen_height - win_height) // 2)

        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.map_view = MapGraphicsView()
        main_layout.addWidget(self.map_view, 3)

        right_widget = QWidget()
        right_widget.setFixedWidth(400)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(10)

        control_bar = QHBoxLayout()
        control_bar.addWidget(QLabel("组别："))
        self.group_combo = QComboBox()
        self.group_combo.addItems(["小学", "初中", "高中"])
        self.group_combo.setCurrentText("高中")
        self.group_combo.currentTextChanged.connect(self._on_group_changed)
        control_bar.addWidget(self.group_combo)

        self.draw_btn = QPushButton("开始抽签")
        self.draw_btn.clicked.connect(self._draw_lottery)
        control_bar.addWidget(self.draw_btn)

        self.reset_btn = QPushButton("重置系统")
        self.reset_btn.clicked.connect(self._reset)
        control_bar.addWidget(self.reset_btn)

        self.export_btn = QPushButton("导出结果")
        self.export_btn.clicked.connect(self._export)
        control_bar.addWidget(self.export_btn)

        control_bar.addStretch()
        right_layout.addLayout(control_bar)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["📝任务", "📍工程点", "🔢区域/细节"])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        right_layout.addWidget(self.result_table)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setStyleSheet("background-color: #f8f9fa;")
        right_layout.addWidget(self.detail_text)

        main_layout.addWidget(right_widget)

    def _on_group_changed(self, text):
        self.current_group = text

    def _draw_lottery(self):
        available = [i for i in range(1, 10) if i not in (5, 6)]
        random.shuffle(available)

        rec_proj = available.pop()
        rec_zone = random.randint(1, 4)

        four_cup_proj = random.choice([5, 6])
        three_cup_proj = 5 if four_cup_proj == 6 else 6
        stack_zones = random.sample(range(1, 5), 3)
        # 分配颜色：两个红色，一个绿色（随机顺序）
        colors = ["红", "红", "绿"]
        random.shuffle(colors)

        bridge_proj = available.pop()
        colors = ["红", "蓝", "绿"]
        random.shuffle(colors)

        station_proj = available.pop()
        cup_zone = random.randint(1, 4)
        ball_zone = random.randint(1, 4)
        while ball_zone == cup_zone:
            ball_zone = random.randint(1, 4)

        self.lottery_data = {
            "物料回收": {
                "工程点": rec_proj,
                "区域": rec_zone,
                "说明": f"工程{rec_proj} 区域{rec_zone}"
            },
            "建设服务区": {
                "工程点_4杯": four_cup_proj,
                "工程点_3杯": three_cup_proj,
                "叠放区域": stack_zones,
                "区域颜色": colors,
                "说明": f"4个纸杯在工程{four_cup_proj}，3个纸杯在工程{three_cup_proj}，叠放区域：{', '.join(map(str, stack_zones))}，颜色顺序：{', '.join(colors)}"
            },
            "搭建桥梁": {
                "工程点": bridge_proj,
                "颜色顺序": colors,
                "说明": f"工程{bridge_proj}，颜色顺序（从下至上）：{' → '.join(colors)}"
            },
            "建设加油站": {
                "工程点": station_proj,
                "纸杯区域": cup_zone,
                "泡沫球区域": ball_zone,
                "说明": f"工程{station_proj}，纸杯区域{cup_zone}，泡沫球区域{ball_zone}"
            }
        }

        self._update_table()
        self._update_detail_text()
        self.map_view.update_dynamic_items(self.lottery_data)

    def _update_table(self):
        self.result_table.setRowCount(len(self.lottery_data))
        for row, (task, info) in enumerate(self.lottery_data.items()):
            self.result_table.setItem(row, 0, QTableWidgetItem(task))
            if task == "建设服务区":
                proj_text = f"工程{info['工程点_4杯']} / 工程{info['工程点_3杯']}"
            else:
                proj_text = str(info["工程点"])
            self.result_table.setItem(row, 1, QTableWidgetItem(proj_text))
            if task == "物料回收":
                zone_text = f"区域{info['区域']}"
            elif task == "建设服务区":
                zone_text = f"叠放区域：{', '.join(map(str, info['叠放区域']))}"
            elif task == "搭建桥梁":
                zone_text = " → ".join(info["颜色顺序"])
            elif task == "建设加油站":
                zone_text = f"杯{info['纸杯区域']} 球{info['泡沫球区域']}"
            else:
                zone_text = ""
            self.result_table.setItem(row, 2, QTableWidgetItem(zone_text))

    def _update_detail_text(self):
        text = f"【组别】{self.current_group}\n\n"
        for task, info in self.lottery_data.items():
            text += f"▶ {task}\n"
            if task == "物料回收":
                text += f"   工程点：{info['工程点']}，回收区域：{info['区域']}\n"
            elif task == "建设服务区":
                text += f"   4个纸杯位置：工程{info['工程点_4杯']}\n"
                text += f"   3个纸杯位置：工程{info['工程点_3杯']}，叠放区域：{', '.join(map(str, info['叠放区域']))}\n"
                if self.current_group == "小学":
                    text += "   小学组只需叠好两个红色纸杯。\n"
                else:
                    text += "   三个纸杯（2红1绿）需按颜色顺序叠放：红、红、绿（从下至上）。\n"
            elif task == "搭建桥梁":
                text += f"   工程点：{info['工程点']}\n"
                text += f"   颜色顺序（从下至上）：{' → '.join(info['颜色顺序'])}\n"
                if self.current_group == "小学":
                    text += "   小学组只需堆叠两个原料即可。\n"
                else:
                    text += "   初中、高中需按颜色顺序正确堆叠三个原料。\n"
            elif task == "建设加油站":
                text += f"   工程点：{info['工程点']}\n"
                text += f"   纸杯区域：{info['纸杯区域']}，泡沫球区域：{info['泡沫球区域']}\n"
            text += "\n"
        self.detail_text.setText(text)

    def _reset(self):
        self.lottery_data = {}
        self.result_table.setRowCount(0)
        self.detail_text.clear()
        self.map_view.update_dynamic_items({})

    def _export(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            desktop = winreg.QueryValueEx(key, "Desktop")[0]
            winreg.CloseKey(key)
        except:
            desktop = os.path.expanduser("~/Desktop")
        file_path = os.path.join(desktop, "道路工程抽签结果.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"组别：{self.current_group}\n\n")
            for task, info in self.lottery_data.items():
                f.write(f"{task}\n")
                if task == "物料回收":
                    f.write(f"  工程点：{info['工程点']}，区域：{info['区域']}\n")
                elif task == "建设服务区":
                    f.write(f"  4个纸杯位置：工程{info['工程点_4杯']}\n")
                    f.write(f"  3个纸杯位置：工程{info['工程点_3杯']}，叠放区域：{', '.join(map(str, info['叠放区域']))}\n")
                elif task == "搭建桥梁":
                    f.write(f"  工程点：{info['工程点']}\n")
                    f.write(f"  颜色顺序（从下至上）：{' → '.join(info['颜色顺序'])}\n")
                elif task == "建设加油站":
                    f.write(f"  工程点：{info['工程点']}\n")
                    f.write(f"  纸杯区域：{info['纸杯区域']}，泡沫球区域：{info['泡沫球区域']}\n")
                f.write("\n")
        QMessageBox.information(self, "导出成功", f"结果已保存至：{file_path}")

if __name__ == "__main__":
    # 在程序启动时注册
    atexit.register(delete_file_at_exit)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
