import sys
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTextCodec
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QPushButton, QLineEdit, QTextEdit, QGraphicsLineItem
from PyQt5.QtGui import QFont, QBrush, QColor, QPen
from tree import BinaryTree, Node
import random
import re

QTextCodec.setCodecForLocale(QTextCodec.codecForName("UTF-8"))
font = QFont("STZHONGS", 12)



def draw_tree(root, scene, x, y, level, target=None,rb=False):
    if root:
        node_radius = 20
        node = QGraphicsEllipseItem(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2)

        if target and root.val in target:
            node.setBrush(QBrush(QColor(221, 160, 221)))  
        elif not rb :
            node.setBrush(QBrush(QColor(5, 255, 255)))  # 设置节点颜色为青色
        elif rb and root.color=='b':
            node.setBrush(QBrush(QColor(200, 200, 200)))
        elif rb and root.color=='r':
            node.setBrush(QBrush(QColor(255, 0, 127)))

        node.setPen(Qt.black)
        scene.addItem(node)

        # 添加节点值
        text = scene.addText(str(root.val))
        text.setFont(QFont("Arial", 12))
        text.setPos(x - text.boundingRect().width() / 2, y - text.boundingRect().height() / 2)

        # 绘制连接线
        if root.left:
            line_x = x- 100+20*level
            # line_x = x - 100 * level
            line_y = y + 100 + node_radius
            line = QGraphicsLineItem(x, y + node_radius, line_x, line_y)
            line.setPen(QPen(QColor(0, 0, 0)))  # 设置连接线颜色为黑色
            scene.addItem(line)
            draw_tree(root.left, scene, line_x, line_y, level + 1, target,rb=rb)
        if root.right:
            # line_x = x + 100 * level
            line_x = x + 100 -20*level
            line_y = y + 100 + node_radius
            line = QGraphicsLineItem(x, y + node_radius, line_x, line_y)
            line.setPen(QPen(QColor(0, 0, 0)))  # 设置连接线颜色为黑色
            scene.addItem(line)
            draw_tree(root.right, scene, line_x, line_y, level + 1, target,rb=rb)


class HelloWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("沈辰 202221147064 作业5")
        self.setGeometry(500, 500, 2000, 1500)

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.graph_scene = QGraphicsScene()
        self.graph_view = QGraphicsView(self.graph_scene)
        self.graph_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.graph_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.graph_view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.graph_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.graph_view.setDragMode(QGraphicsView.ScrollHandDrag)
        main_layout.addWidget(self.graph_view, 1)


        self.zoom_factor = 1.0
        self.graph_view.wheelEvent = self.zoom_view
        self.ctrl_pressed = False

        # self.circle = QGraphicsEllipseItem(-500, -500, 1000, 1000)
        # self.circle.setBrush(Qt.blue)
        # self.graph_scene.addItem(self.circle)

        v_layout = QVBoxLayout()
        main_layout.addLayout(v_layout, 1)
        v_layout_up = QVBoxLayout()
        v_layout_down = QVBoxLayout()
        v_layout.addLayout(v_layout_up, 3)# ??? 
        v_layout.addLayout(v_layout_down, 7)#？

        self.generate_button = QPushButton("生成")
        self.generate_button.setFont(font)
        v_layout_up.addWidget(self.generate_button, 1)
        self.generate_button.clicked.connect(self.generate_button_issue)

        self.inputbox_layout = QHBoxLayout()
        v_layout_up.addLayout(self.inputbox_layout, 3)
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("输入指定测试树（只写数字，用“,”隔开）")
        self.inputbox_layout.addWidget(self.input_box)
        # self.inputcorrect_button = QPushButton("确定")
        # self.inputbox_layout.addWidget(self.inputcorrect_button, 2)


        operate = QHBoxLayout()
        v_layout_up.addLayout(operate, 1)
        self.insert_btn = QPushButton("插入")
        self.search_btn = QPushButton("查找")
        self.delete_btn = QPushButton("删除")
        operate.addWidget(self.insert_btn)
        operate.addWidget(self.search_btn)
        operate.addWidget(self.delete_btn)
        self.insert_btn.clicked.connect(self.insert_btn_issue)
        self.search_btn.clicked.connect(self.search_btn_issue)
        self.delete_btn.clicked.connect(self.delete_btn_issue)



        attributes = QHBoxLayout()
        v_layout_up.addLayout(attributes, 1)
        self.usual_btn = QPushButton("普通")
        self.avl_btn = QPushButton("AVL树")
        self.rb_btn = QPushButton("红黑树")
        
        # 将按钮添加到水平布局中
        attributes.addWidget(self.usual_btn)
        attributes.addWidget(self.avl_btn)
        attributes.addWidget(self.rb_btn)
        
        # 设置按钮的选中状态
        self.usual_btn.setCheckable(True)
        self.avl_btn.setCheckable(True)
        self.rb_btn.setCheckable(True)
        self.usual_btn.setChecked(True)
        
        # 监听按钮的点击事件
        self.usual_btn.clicked.connect(self.onUsualBtnClicked)
        self.avl_btn.clicked.connect(self.onAVLBtnClicked)
        self.rb_btn.clicked.connect(self.onRBBtnClicked)

        self.refreash_button = QPushButton("刷新")
        self.refreash_button.clicked.connect(self.on_refresh_clicked)
        self.refreash_button.setFont(font)
        v_layout_up.addWidget(self.refreash_button, 1)

        self.dital_box = QTextEdit()
        self.dital_box.setReadOnly(True)
        self.dital_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        v_layout_down.addWidget(self.dital_box, 1)

        self.compare_box = QTextEdit()
        self.compare_box.setReadOnly(True)
        self.compare_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        v_layout_down.addWidget(self.compare_box, 1)

        self.tree=BinaryTree()

    def zoom_view(self, event):
        if event.modifiers() & Qt.ControlModifier:
            self.ctrl_pressed = True
            if event.angleDelta().y() > 0:
                # 放大
                self.zoom_factor *= 1.1
            else:
                # 缩小
                self.zoom_factor *= 0.9
            self.graph_view.scale(self.zoom_factor, self.zoom_factor)
        else:
            self.ctrl_pressed = False

    def onUsualBtnClicked(self):
        self.usual_btn.setChecked(True)
        self.avl_btn.setChecked(False)
        self.rb_btn.setChecked(False)
        # 执行普通算法的相关操作

    def onAVLBtnClicked(self):
        self.usual_btn.setChecked(False)
        self.avl_btn.setChecked(True)
        self.rb_btn.setChecked(False)
        # self.tree.inorder_traverse()
        # draw_tree(self.tree.root, self.graph_scene, 250, 50, 1)


    def onRBBtnClicked(self):
        self.usual_btn.setChecked(False)
        self.avl_btn.setChecked(False)
        self.rb_btn.setChecked(True)
        # 执行红黑树算法的相关操作

    def on_refresh_clicked(self):
        self.graph_scene.clear()
        # 在这里重新添加你想显示的图形元素

    #生成
    def generate_button_issue(self):
            nums = [random.randint(1, 100) for _ in range(10)]
            self.tree.clear()
            self.graph_scene.clear()
            if self.usual_btn.isChecked():
                self.tree.rootset(nums[0])
                for num in nums[1:]:
                    self.tree.insert(num)
                draw_tree(self.tree.root, self.graph_scene, 250, 50, 1)
            elif self.avl_btn.isChecked():
                nums = sorted(nums)
                self.tree.root=None
                self.tree.build_tree(nums)
                draw_tree(self.tree.root, self.graph_scene, 250, 50, 1)
            elif self.rb_btn.isChecked():
                self.tree.root=None
                for x in nums:
                    node=Node(x)
                    self.tree.rb_insert(node)
                draw_tree(self.tree.root, self.graph_scene, 250, 50, 1,rb=True)


    #插入
    def insert_btn_issue(self):
        value = self.input_box.text()
        nums = [int(num) for num in re.findall(r'\d+', value)]
        if self.usual_btn.isChecked():
            self.tree.insert(nums)
            draw_tree(self.tree.root, self.graph_scene, 250, 50, 1,nums)
        elif self.avl_btn.isChecked():
            self.tree.Avl_insert(nums)
            draw_tree(self.tree.root, self.graph_scene, 250, 50, 1,nums)
        elif self.rb_btn.isChecked():
            for x in nums:
                node=Node(x)
                self.tree.rb_insert(node)
            draw_tree(self.tree.root, self.graph_scene, 250, 50, 1,nums,rb=True)
        


    def  search_btn_issue (self):
        value = self.input_box.text()
        nums = [int(num) for num in re.findall(r'\d+', value)]
        ans,level=self.tree.find(nums)
        draw_tree(self.tree.root, self.graph_scene, 250, 50, 1,nums)


    def delete_btn_issue (self):
        value = self.input_box.text()
        nums = [int(num) for num in re.findall(r'\d+', value)]
        if self.usual_btn.isChecked():
            self.tree.remove(nums)
            draw_tree(self.tree.root, self.graph_scene, 250, 50, 1)
        elif self.avl_btn.isChecked():
            self.tree.Avl_delete(nums)
            draw_tree(self.tree.root, self.graph_scene, 250, 50, 1)
        elif self.rb_btn.isChecked():
            for x in nums:
                node=self.tree.find(x)
                self.tree.rb_delete(node)
            draw_tree(self.tree.root, self.graph_scene, 250, 50, 1,rb=True)
        







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelloWindow()
    window.show() 
    sys.exit(app.exec_())