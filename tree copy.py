class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1
        self.color='b'

def find_min(self, node=None):
    if not node:
        node = self.root

    while node.left:
        node = node.left

    return node

def find_min_max(node, is_min=True):
    min_max = node
    parent = None
    if is_min:
        while min_max.left is not None:
            parent = min_max
            min_max = min_max.left
    else:
        while min_max.right is not None:
            parent = min_max
            min_max = min_max.right
    return min_max, parent


class BinaryTree:
    def __init__(self, root_val=None):
        self.root = Node(root_val)
    
    def rootset(self, val):
        self.root = Node(val)

    def clear(self):
        self.root = Node(None)

    def insert(self, val, node=None):
        if not node:
            node = self.root
        
        if isinstance(val, list):
            for v in val:
                self.insert(v, node)
        else:
            if val < node.val:
                if node.left:
                    self.insert(val, node.left)
                else:
                    node.left = Node(val)
            else:
                if node.right:
                    self.insert(val, node.right)
                else:
                    node.right = Node(val)


    def find(self, val, node=None, level=0):
        if not node:
            node = self.root

        if isinstance(val, list):
            for v in val:
                ans, lvl = self.find(v, node)
                if ans:
                    return ans, lvl
            return None, None
        else:
            if val == node.val:
                return node, level
            elif val < node.val:
                if node.left:
                    return self.find(val, node.left, level+1)
                else:
                    return None, None
            else:
                if node.right:
                    return self.find(val, node.right, level+1)
                else:
                    return None, None


    def remove(self, val, node=None):
        if not node:
            node = self.root

        if isinstance(val, list):
            for v in val:
                node = self.remove(v, node)
            return node, None
        else:        
            current = self.root
            parent = None
            while current is not None and current.val != val:
                parent = current
                if val < current.val:
                    current = current.left
                else:
                    current = current.right
        
            if current is None:
                return None
            
            if current.left is None and current.right is None:
                if parent is None:
                    self.root = None
                else:
                    if parent.left == current:
                        parent.left = None
                    else:
                        parent.right = None
                return None
            
            if current.left is None or current.right is None:
                child = current.left if current.left is not None else current.right
                if parent is None:
                    self.root = child
                else:
                    if parent.left == current:
                        parent.left = child
                    else:
                        parent.right = child
                return child
            
            min_node, min_parent = find_min_max(current.right, is_min=True)
            current.val = min_node.val
            current.right = self.delete(min_node.val)
            return current



    def avl_shape_refresh(self):
        self.get_height(self.root)

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def avl_insert(self, root, val):
        if root is None:
            return Node(val)
        
        if isinstance(val, list):
            for v in val:
                root = self.avl_insert(root, v)
            return root
        else:
            if val < root.val:
                root.left = self.avl_insert(root.left, val)
            elif val > root.val:
                root.right = self.avl_insert(root.right, val)
            else:
                return root

            root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
            balance = self.get_balance(root)

            if balance > 1 and val < root.left.val:
                return self.rotate_right(root)
            if balance < -1 and val > root.right.val:
                return self.rotate_left(root)
            if balance > 1 and val > root.left.val:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)
            if balance < -1 and val < root.right.val:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

            return root

    def Avl_insert(self, val):
        self.root = self.avl_insert(self.root, val)

    def build_avl_tree(self, values):
        if not values:
            return None

        mid = len(values) // 2
        root = Node(values[mid])

        left_tree = self.build_avl_tree(values[:mid])
        right_tree = self.build_avl_tree(values[mid + 1:])
        
        root.left = left_tree
        root.right = right_tree
        
        return root

    def build_tree(self, values):
        self.root = self.build_avl_tree(values)
        
    def min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.min_value_node(node.left)

    def avl_delete(self, root, val):
        if root is None:
            return root

        if isinstance(val, list):
            for v in val:
                root = self.avl_delete(root, v)
            return root
        else:
            if val < root.val:
                root.left = self.avl_delete(root.left, val)
            elif val > root.val:
                root.right = self.avl_delete(root.right, val)
            else:
                if root.left is None:
                    temp = root.right
                    root = None
                    return temp
                elif root.right is None:
                    temp = root.left
                    root = None
                    return temp

                temp = self.min_value_node(root.right)
                root.val = temp.val
                root.right = self.avl_delete(root.right, temp.val)

            if root is None:
                return root

            root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
            balance = self.get_balance(root)

            if balance > 1 and self.get_balance(root.left) >= 0:
                return self.rotate_right(root)
            if balance > 1 and self.get_balance(root.left) < 0:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)
            if balance < -1 and self.get_balance(root.right) <= 0:
                return self.rotate_left(root)
            if balance < -1 and self.get_balance(root.right) > 0:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

            return root

    def Avl_delete(self, val):
        self.root = self.avl_delete(self.root, val)




    def rb_insert(self, node: Node) -> None:
        if self.root is None:
            node.color = 'b'
            self.root = node
            return

        currentNode = self.root
        while currentNode is not None:
            parent = currentNode
            if node.val < currentNode.val:
                if currentNode.left is None:
                    currentNode.left = node
                    break
                currentNode = currentNode.left
            else:
                if currentNode.right is None:
                    currentNode.right = node
                    break
                currentNode = currentNode.right

        node.parent = parent
        self.__rbinsert_balance(node)

    def __rbinsert_balance(self, node: Node):
        while node != self.root and node.parent.color == 'r':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color == 'r':
                    node.parent.color = 'b'
                    uncle.color = 'b'
                    node.parent.parent.color = 'r'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    node.parent.color = 'b'
                    node.parent.parent.color = 'r'
                    self.rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.color == 'r':
                    node.parent.color = 'b'
                    uncle.color = 'b'
                    node.parent.parent.color = 'r'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    node.parent.color = 'b'
                    node.parent.parent.color = 'r'
                    self.rotate_left(node.parent.parent)
        self.root.color = 'b'

    def rb_delete(self,node):
        # 首先搜索节点，判断该节点是否存在
        if self.root==None:
            # 该树为空树
            return
        currentNode=self.root
        while currentNode:
            if currentNode.val==node.val:
                break
            elif currentNode.val>node.val:
                currentNode=currentNode.left
            else:
                currentNode=currentNode.right
        if currentNode==None:
            # 该节点不存在
            return
        dnode=currentNode #待删除节点
        self.__rbdelete(dnode) #节点删除完毕
    def __rbdelete(self,dnode:Node):
        if dnode.left==None and dnode.right==None:
            if dnode.color=='r':
                # 红色的叶子节点
                pnode=dnode.parent
                if pnode.left==dnode:
                    pnode.left=None
                else:
                    pnode.right=None
            else:
                pnode=dnode.parent
                if pnode==None:
                    self.root==None
                    return
                # 先执行平衡操作，再删除节点
                self.__rbdelete_blackleaf_balance(dnode)
                if pnode.left==dnode:
                    pnode.left=None
                else:
                    pnode.right=None
                # 黑色的叶子节点 
        elif dnode.left==None and dnode.right:
            # 删除节点含有一个右子节点，对应黑红
            pnode=dnode.parent
            cnode=dnode.right
            print("xxxx",pnode.val)
            if pnode.left==dnode:
                pnode.left=cnode
            else:
                pnode.right=cnode
            cnode.parent=pnode
            cnode.color='b'
        elif dnode.left and dnode.right==None:
            # 删除节点含有一个左子节点，对应黑红
            pnode=dnode.parent
            cnode=dnode.left
            if pnode.left==dnode:
                pnode.left=cnode
            else:
                pnode.right=cnode
            cnode.parent=pnode
            cnode.color='b'
        else:
            # 删除节点，含有两个子节点
            # 用前驱节点替换，转情况1、2、3
            prenode=dnode.left
            while prenode.right:
                prenode=prenode.right
            dnode.val=prenode.val
            self.__rbdelete(prenode)
    def rb__delete_blackleaf_balance(self,dnode:Node)->None:
        if dnode.parent==None:
            return
        pnode=dnode.parent
        flag1=0 if pnode.left==dnode else 1
        if flag1:
            snode=pnode.left
        else:
            snode=pnode.right
        if snode.color=='b':
            # 兄弟节点为黑色
            if snode.left==None and snode.right==None:
                # 兄弟节点的两个子节点全黑
                if pnode.color=='b':
                    # 父节点为黑
                    snode.color='r'
                    self.rb__delete_blackleaf_balance(pnode)
                else:
                    # 父节点为红色
                    pnode.color='b'
                    snode.color='r'
                    return
            else:
                # 兄弟节点的子节点不为全黑
                if flag1:
                    # snode为pnode的左子节点
                    if snode.left==None:
                        # sl为黑色
                        sl,sr=snode.left,snode.right
                        pnode.left=sr
                        sr.parent=pnode
                        sr.color='b'
                        sr.left=snode
                        snode.parent=sr
                        snode.color='r'
                        snode.right=None
                        self.rb__delete_blackleaf_balance(dnode)
                    else:
                        # sl为红色
                        gnode=pnode.parent
                        if gnode:
                            flag2=0 if gnode.left==pnode else 1
                        else:
                            flag2=2
                        if flag2==1:
                            gnode.right=snode
                        elif flag2==0:
                            gnode.left=snode
                        else:
                             # 祖父节点不存在，此时树的根节点由pnode变为snode
                            self.root=snode
                        snode.color,pnode.color=pnode.color,snode.color
                        snode.parent=gnode
                        sl,sr=snode.left,snode.right
                        snode.right=pnode
                        pnode.parent=snode
                        pnode.left=sr
                        sl.color='b'
                        if sr:
                            sr.parent=pnode
                        return
                else:
                    # snode为pnode的右子节点
                    if snode.right==None:
                        # sr为黑色
                        sl,sr=snode.left,snode.right
                        pnode.right=sl
                        sl.parent=pnode
                        sl.color='b'
                        sl.right=snode
                        snode.parent=sl
                        snode.color='r'
                        snode.left=None
                        self.rb__delete_blackleaf_balance(dnode)
                    else:
                        # sr为红色
                        gnode=pnode.parent
                        if gnode:
                            flag2=0 if gnode.left==pnode else 1
                        else:
                            flag2=2
                        if flag2==1:
                            gnode.right=snode
                        elif flag2==0:
                            gnode.left=snode
                        else:
                            # 祖父节点不存在，此时树的根节点由pnode变为snode
                            self.root=snode
                        snode.color,pnode.color=pnode.color,snode.color
                        snode.parent=gnode
                        sl,sr=snode.left,snode.right
                        snode.left=pnode
                        pnode.parent=snode
                        pnode.right=sl
                        sr.color='b'
                        if sl:
                            sl.parent=pnode
                        return
        else:
            #兄弟节点为红色
            gnode=pnode.parent
            sl,sr=snode.left,snode.right
            flag2=0 if gnode.left==pnode else 1
            if flag2:
                gnode.right=snode
            else:
                gnode.left=snode
            snode.parent=gnode
            snode.color='b'
            pnode.color='r'
            pnode.parent=snode
            if flag1:
                # 兄弟节点为左子节点
                snode.right=pnode
                pnode.left=sr
                sr.parent=pnode
            else:
                # 兄弟节点为右子节点
                snode.left=pnode
                pnode.right=sl
                sl.parent=pnode
            self.rb__delete_blackleaf_balance(dnode)

def inorder_traverse(node=None):
    if node is None:
        return []   
    result = []
    result.extend(inorder_traverse(node.left))
    result.append(node.val)
    result.extend(inorder_traverse(node.right))
    return sorted(arr)