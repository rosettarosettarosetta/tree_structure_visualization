class Node:
    def __init__(self, data=None, left=None, right=None,height=-1):
        self.data = data
        self.left = left
        self.right = right
        self.height = height
    
def search (root, key):
    if root is None or root.data == key:
        return root
    if root.data < key:
        return search(root.right, key)
    return search(root.left, key)

def delete(root, key):
    if root is None:
        return root

    # 如果要删除的节点是根节点
    if root.data == key:
        # 如果根节点只有右子树
        if root.left is None:
            return root.right
        # 如果根节点只有左子树
        elif root.right is None:
            return root.left
        # 如果根节点有左右子树
        else:
            # 找到右子树的最小节点
            temp = root.right
            while temp.left is not None:
                temp = temp.left
            # 将右子树的最小节点数据替换到根节点
            root.data = temp.data
            # 递归删除右子树的最小节点
            root.right = delete(root.right, temp.data)

    # 如果要删除的节点在左子树中
    elif root.data > key:
        root.left = delete(root.left, key)

    # 如果要删除的节点在右子树中
    else:
        root.right = delete(root.right, key)

    return root

def insert ( root,  key):
    if root is None:
        return Node(key)
    if root.data < key:
        root.right = insert(root.right, key)
    if root.data > key:
        root.left = insert(root.left, key)
    return root


def avl ( root, key):
    def _update_height(node: Node) -> int:

        if not node:
            return 0
        
        left_height = _update_height(node.left)
        right_height = _update_height(node.right)
        
        return max(left_height, right_height) + 1

    def _rotate_right(node: Node) -> Node:
        l = node.left
        l_r = l.right

        node.left = l_r
        l.right = node

        node.height = _update_height(node)
        l.height = _update_height(l)

        return l
        pass

    # 右旋
    def rotate_right(self, p, c):
        s2 = c.rchild
        p.lchild = s2
        if s2:
            s2.parent = p
        c.rchild = p
        p.parent = c
 
        p.bf = 0
        c.bf = 0
        return c
 
    # 右旋-左旋
    def rotate_right_left(self, p, c):
        g = c.lchild
        self.rotate_right(p, c)
        self.rotate_left(g, c)
        if g.bf > 0:
            p.bf = -1
            c.bf = 0
        elif g.bf < 0:
            p.bf = 0
            c.bf = 1
        else:
            p.bf = 0
            c.bf = 0
        return g
 
    # 左旋-右旋
    def rotate_left_right(self, p, c):
        g = c.rchild
        self.rotate_left(c, g)
        self.rotate_right(p, c)
        if g.bf < 0:
            p.bf = 1
            c.bf = 0
        elif g.bf > 0:
            p.bf = 0
            c.bf = -1
        else:
            p.bf = 0
            c.bf = 0
        return g


class AVLTree:
    def __init__(self):
        self.root = None

    # 获取节点高度
    def _height(self, node):
        return node.height if node else 0

    # 更新节点高度
    def _update_height(self, node):
        node.height = max(self._height(node.left), self._height(node.right)) + 1

    # 获取平衡因子
    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)


   # 左旋
    def _left_rotate(self, y):
        x = y.right
        T2 = x.left

        x.left = y
        y.right = T2

        self._update_height(y)
        self._update_height(x)

        return x

    # 右旋
    def _right_rotate(self, x):
        y = x.left
        T2 = y.right

        y.right = x
        x.left = T2

        self._update_height(x)
        self._update_height(y)

        return y

    # 左右旋
    def _left_right_rotate(self, z):
        z.left = self._left_rotate(z.left)
        return self._right_rotate(z)

    # 右左旋
    def _right_left_rotate(self, z):
        z.right = self._right_rotate(z.right)
        return self._left_rotate(z)
   # 插入节点

    def insert(self, root, key):
        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 更新节点高度
        self._update_height(root)

        # 获取平衡因子
        balance = self._balance_factor(root)

        # 平衡性维护
        if balance > 1:
            if key < root.left.key:
                return self._right_rotate(root)
            else:
                return self._left_right_rotate(root)
        if balance < -1:
            if key > root.right.key:
                return self._left_rotate(root)
            else:
                return self._right_left_rotate(root)

        return root

    def insert_key(self, key):
        self.root = self.insert(self.root, key)

  # 删除节点
    def delete(self, root, key):
        if not root:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # 节点包含一个或零个子节点
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            # 节点包含两个子节点，找到右子树的最小节点
            temp = self._min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        # 更新节点高度
        self._update_height(root)

        # 获取平衡因子
        balance = self._balance_factor(root)

        # 平衡性维护
        if balance > 1:
            if self._balance_factor(root.left) >= 0:
                return self._right_rotate(root)
            else:
                return self._left_right_rotate(root)
        if balance < -1:
            if self._balance_factor(root.right) <= 0:
                return self._left_rotate(root)
            else:
                return self._right_left_rotate(root)

        return root

    def delete_key(self, key):
        self.root = self.delete(self.root, key)


   # 查询节点
    def search(self, root, key):
        if not root or root.key == key:
            return root

        if root.key < key:
            return self.search(root.right, key)
        return self.search(root.left, key)

    def search_key(self, key):
        return self.search(self.root, key)
