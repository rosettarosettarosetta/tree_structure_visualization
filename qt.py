import sys
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTextCodec
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QPushButton, QLineEdit, QTextEdit, QGraphicsLineItem
from PyQt5.QtGui import QFont, QBrush, QColor, QPen
from tree import BinaryTree, Node ,inorder_traverse,preorder_traverse,postorder_traverse,max_depth
import random
import re
from red_black  import RB_tree
from memory_profiler import memory_usage
from rb import RBTree

QTextCodec.setCodecForLocale(QTextCodec.codecForName("UTF-8"))
font = QFont("STZHONGS", 12)
RED = True
BLACK = False

class HelloWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("沈辰 202221147064 作业5")
        self.setGeometry(500, 500, 1500, 1200) 

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

        self.Dital_box = QVBoxLayout()
        v_layout_down.addLayout(self.Dital_box, 5)
        self.title_label = QLabel('二叉树属性', self)
        self.Dital_box.addWidget(self.title_label, 1)
        self.dital_box = QTextEdit()
        self.dital_box.setReadOnly(True)
        self.dital_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.Dital_box.addWidget(self.dital_box, 8)

        self.Compare_box = QVBoxLayout()
        v_layout_down.addLayout(self.Compare_box, 5)
        self.ctitle_label = QLabel('性能分析', self)
        self.Compare_box.addWidget(self.ctitle_label, 1)
        self.compare_box = QTextEdit()
        self.compare_box.setReadOnly(True)
        self.compare_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.Compare_box.addWidget(self.compare_box, 8)
        text="二叉查找树：\n 查找：O（n）\t插入：O（n）\t删除：O（n）\nAVL树：\n 查找：O（logn）\t插入：O（logn）\t删除：O（logn）\n红黑树：\n 查找：O（logn）\t插入：O（logn）\t删除：O（logn）\n"
        text+="AVL树优点：\n查找操作更稳定，占用内存更少\n缺点：插入和删除操作更慢\n"
        text+="红黑树优点：\n插入和删除操作更快、更稳定，查找操作更稳定\n缺点：占用内存更多\n"
        self.compare_box.setPlainText(text)
        self.tree=BinaryTree()
        # self.red_black_tree=RB_tree()
        self.red_black_tree=RBTree()




    def draw_tree(self,root, scene, x, y, level, target=None, rb=False):
        if root and root.val is not None:
            node_radius = 20
            node = QGraphicsEllipseItem(x - node_radius, y - node_radius, node_radius * 2, node_radius * 2)

            if target and root.val in target:
                node.setBrush(QBrush(QColor(221, 160, 221)))
            elif not rb:
                node.setBrush(QBrush(QColor(5, 255, 255)))  # 设置节点颜色为青色
            elif rb and (root.color == 'b'or root.color == 0):
                node.setBrush(QBrush(QColor(200, 200, 200)))
            elif rb and (root.color == 'r' or root.color == 1):
            # elif rb and root.color == 1:
                node.setBrush(QBrush(QColor(255, 0, 127)))

            node.setPen(Qt.black)
            scene.addItem(node)

            # 添加节点值
            text = scene.addText(str(root.val))
            text.setFont(QFont("Arial", 12))
            text.setPos(x - text.boundingRect().width() / 2, y - text.boundingRect().height() / 2)

            # 设置水平间距和垂直间距
            base_horizontal_spacing = 270
            horizontal_spacing = base_horizontal_spacing / (level + 1)
            vertical_spacing = 100

            # 绘制连接线
            if root.left and root.left.val is not None:
                line_x = x - horizontal_spacing
                line_y = y + vertical_spacing
                line = QGraphicsLineItem(x, y + node_radius, line_x, line_y - node_radius)
                line.setPen(QPen(QColor(0, 0, 0)))  # 设置连接线颜色为黑色
                scene.addItem(line)
                self.draw_tree(root.left, scene, line_x, line_y, level + 1, target, rb=rb)
            if root.right and root.right.val is not None:
                line_x = x + horizontal_spacing
                line_y = y + vertical_spacing
                line = QGraphicsLineItem(x, y + node_radius, line_x, line_y - node_radius)
                line.setPen(QPen(QColor(0, 0, 0)))  # 设置连接线颜色为黑色
                scene.addItem(line)
                self.draw_tree(root.right, scene, line_x, line_y, level + 1, target, rb=rb)



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

    def onAVLBtnClicked(self):
        self.usual_btn.setChecked(False)
        self.avl_btn.setChecked(True)
        self.rb_btn.setChecked(False)


    def onRBBtnClicked(self):
        self.usual_btn.setChecked(False)
        self.avl_btn.setChecked(False)
        self.rb_btn.setChecked(True)

    def on_refresh_clicked(self):
        self.graph_scene.clear()
        self.tree.clear()
        self.red_black_tree.clear()


    #生成
    def generate_button_issue(self):
        self.graph_scene.clear()
        self.tree.clear()
        self.red_black_tree.clear()
        if not self.input_box.text():
            nums = []
            while len(nums) < 10:
                num = random.randint(1, 100)
                if num not in nums:
                    nums.append(num)
        else :
            value = self.input_box.text()
            self.input_box.clear()
            nums = [int(num) for num in re.findall(r'\d+', value)]
        new_text = "组成树的数：\n" + str(nums)

        if self.usual_btn.isChecked():
            self.tree.rootset(nums[0])
            for num in nums[1:]:
                self.tree.insert(num)
            self.draw_tree(self.tree.root, self.graph_scene, 250, 50, 1)
            new_text += "\n中序遍历为：\n" + str(inorder_traverse(self.tree.root))
            new_text += "\n前序遍历为：\n" + str(preorder_traverse(self.tree.root))
            new_text += "\n后序遍历为：\n" + str(postorder_traverse(self.tree.root))
            new_text += "\n深度为：\n" + str(max_depth(self.tree.root))
            self.dital_box.setPlainText(new_text)
        elif self.avl_btn.isChecked():
            self.tree.root=None
            self.tree.root=self.tree.build_avl_tree(nums)
            self.draw_tree(self.tree.root, self.graph_scene, 250, 50, 1)
            new_text += "\n中序遍历为：\n" + str(inorder_traverse(self.tree.root))
            new_text += "\n前序遍历为：\n" + str(preorder_traverse(self.tree.root))
            new_text += "\n后序遍历为：\n" + str(postorder_traverse(self.tree.root))
            new_text += "\n深度为：\n" + str(max_depth(self.tree.root))
            self.dital_box.setPlainText(new_text)
        elif self.rb_btn.isChecked():
            self.tree.root=None
            for x in nums:
                self.red_black_tree.insertNode(x)
            self.draw_tree(self.red_black_tree.root, self.graph_scene, 250, 50, 1,rb=True)
            new_text += "\n中序遍历为：\n" + str(inorder_traverse(self.red_black_tree.root))
            new_text += "\n前序遍历为：\n" + str(preorder_traverse(self.red_black_tree.root))
            new_text += "\n后序遍历为：\n" + str(postorder_traverse(self.red_black_tree.root))
            new_text += "\n深度为：\n" + str(max_depth(self.red_black_tree.root)-1)
            self.dital_box.setPlainText(new_text)



    #插入
    def insert_btn_issue(self):
        self.graph_scene.clear()
        value = self.input_box.text()
        self.input_box.clear()
        nums = [int(num) for num in re.findall(r'\d+', value)]
        new_text = "插入的数：\n" + str(nums)
        if self.usual_btn.isChecked():
            self.dital_box.setPlainText(new_text)
            self.tree.insert(nums)
            self.draw_tree(self.tree.root, self.graph_scene, 250, 50, 1,nums)
            new_text += "\n中序遍历为：\n" + str(inorder_traverse(self.tree.root))
            new_text += "\n前序遍历为：\n" + str(preorder_traverse(self.tree.root))
            new_text += "\n后序遍历为：\n" + str(postorder_traverse(self.tree.root))
            new_text += "\n深度为：\n" + str(max_depth(self.tree.root))
        elif self.avl_btn.isChecked():
            # self.tree.AVl_insert(nums,self.tree.root)
            for x in nums:
                self.tree.insert_value(x)
            self.draw_tree(self.tree.root, self.graph_scene, 250, 50, 1,nums)
            new_text += "\n中序遍历为：\n" + str(inorder_traverse(self.tree.root))
            new_text += "\n前序遍历为：\n" + str(preorder_traverse(self.tree.root))
            new_text += "\n后序遍历为：\n" + str(postorder_traverse(self.tree.root))
            new_text += "\n深度为：\n" + str(max_depth(self.tree.root))
        elif self.rb_btn.isChecked():
            for x in nums:
                self.red_black_tree.insertNode(x)
            self.draw_tree(self.red_black_tree.root, self.graph_scene, 250, 50, 1,nums,rb=True)
            new_text += "\n中序遍历为：\n" + str(inorder_traverse(self.red_black_tree.root))
            new_text += "\n前序遍历为：\n" + str(preorder_traverse(self.red_black_tree.root))
            new_text += "\n后序遍历为：\n" + str(postorder_traverse(self.red_black_tree.root))
            new_text += "\n深度为：\n" + str(max_depth(self.red_black_tree.root)-1)
        self.dital_box.setPlainText(new_text)
        


    def  search_btn_issue (self):
        value = self.input_box.text()
        self.input_box.clear()
        nums = [int(num) for num in re.findall(r'\d+', value)]
        if self.usual_btn.isChecked() or self.avl_btn.isChecked():
            for x in nums:
                ans=self.tree.search(self.tree.root,x)
            self.draw_tree(self.tree.root, self.graph_scene, 250, 50, 1,nums)
        elif self.rb_btn.isChecked():
            self.draw_tree(self.red_black_tree.root, self.graph_scene, 250, 50, 1,nums,rb=True)


    def delete_btn_issue (self):
        value = self.input_box.text()
        self.input_box.clear()
        self.graph_scene.clear()
        nums = [int(num) for num in re.findall(r'\d+', value)]
        if self.usual_btn.isChecked():
            for x in nums:
                self.tree.remove(self.tree.root,x)
            self.draw_tree(self.tree.root, self.graph_scene, 250, 50, 1)
        elif self.avl_btn.isChecked():
            for x in nums:
                self.tree.delete_value(x)
            self.draw_tree(self.tree.root, self.graph_scene, 250, 50, 1)
        elif self.rb_btn.isChecked():
            for x in nums:
                self.red_black_tree.delete_node(x)
            self.draw_tree(self.red_black_tree.root, self.graph_scene, 250, 50, 1,rb=True)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HelloWindow()
    window.show() 
    sys.exit(app.exec_())