class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1
        self.color= 1  


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

    #二叉树查找节点
    def search(self, root, val):
        if root is None:
            return
        if root.val == val:
            return root
        elif val < root.val:
            return self.search(root.left, val)
        elif val > root.val:
            return self.search(root.right, val)

    #普通二叉树删除节点
    def remove(self, root: Node, val: int) -> Node:
        if not root:
            return root

        if val < root.val:
            root.left = self.remove(root.left, val)
        elif val > root.val:
            root.right = self.remove(root.right, val)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            else:
                min_node = root.right
                while min_node.left:
                    min_node = min_node.left
                root.val = min_node.val
                root.right = self.remove(root.right, min_node.val)

        if root.val == val:
            self.root = root

        return root
    
    #avl 函数

    def height(self, node):
        if not node:
            return -1
        return node.height

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y


    def singleRightRotate(self,node):
        k1=node.right
        node.right=k1.left
        k1.left=node
        node.height=max(self.height(node.right),self.height(node.left))+1
        k1.height=max(self.height(k1.right),node.height)+1
        return k1

    def singleLeftRotate(self,node):
        k1=node.left
        node.left=k1.right
        k1.right=node
        node.height=max(self.height(node.right),self.height(node.left))+1
        k1.height=max(self.height(k1.left),node.height)+1
        return k1

    def doubleRightRotate(self,node):
        node.right=self.singleLeftRotate(node.right)
        return self.singleRightRotate(node)

    def doubleLeftRotate(self,node):
        node.left=self.singleRightRotate(node.left)
        return self.singleLeftRotate(node)







    def findMax(self):
        if self.root is None:
            return None
        else:
            return self._findMax(self.root)
            
    def _findMax(self,node):
        if node.right:
            return self._findMax(node.right)
        else:
            return node

    def findMin(self):
        if self.root is None:
            return None
        else:
            return self._findMin(self.root)
    def _findMin(self,node):
        if node.left:
            return self._findMin(node.left)
        else:
            return node

    #avl树构建
    def build_avl_tree(self, val):
        if not val:
            return None
        val = sorted(val)
        mid = len(val) // 2
        root = Node(val[mid])

        left_tree = self.build_avl_tree(val[:mid])
        right_tree = self.build_avl_tree(val[mid + 1:])
        
        root.left = left_tree
        root.right = right_tree
        
        return root

    #avl树插入
    def avl_insert(self, root, val):
        
        if not root:
            return Node(val)
    
        elif val < root.val:
            root.left = self.avl_insert(root.left, val)

        else:
            root.right = self.avl_insert(root.right, val)


        root.height = 1 + max(self.height(root.left), self.height(root.right))

        balance = self.balance(root)


        if balance > 1 and val < root.left.val:
            return self.right_rotate(root)

    
        if balance < -1 and val > root.right.val:
            return self.left_rotate(root)

    
        if balance > 1 and val > root.left.val:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)


        if balance < -1 and val < root.right.val:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

    
        return root

    def insert_value(self, val):
        self.root = self.avl_insert(self.root, val)

        #avl树的删除
    def delete(self, val, node):
        if node is None:
            print("not in a tree")
        # 递归删除左子树
        elif val < node.val:
            node.left = self.delete(val, node.left)
            # 删除左子树后,检查是否需要右旋或双右旋
            if (self.height(node.right) - self.height(node.left)) == 2:
                if self.height(node.right.right) >= self.height(node.right.left):
                    node = self.singleRightRotate(node)
                else:
                    node = self.doubleRightRotate(node)
            node.height = max(self.height(node.left), self.height(node.right)) + 1
    
        elif val > node.val:
            node.right = self.delete(val, node.right)
            
            if (self.height(node.left) - self.height(node.right)) == 2:
                if self.height(node.left.left) >= self.height(node.left.right):
                    node = self.singleLeftRotate(node)
                else:
                    node = self.doubleLeftRotate(node)
            node.height = max(self.height(node.left), self.height(node.right)) + 1
        # 如果当前节点是要删除的节点,且有左右子树
        elif node.left and node.right:
            if node.left.height <= node.right.height:
                minNode = self._findMin(node.right)
                node.val = minNode.val
                node.right = self.delete(node.val, node.right)

            else:
                maxNode = self._findMax(node.left)
                node.val = maxNode.val
                node.left = self.delete(node.val, node.left)

            node.height = max(self.height(node.left), self.height(node.right)) + 1
        else:
         
            if node.right:
                node = node.right

            else:
                node = node.left
        return node


    def delete_value(self,val):
        self.root=self.delete(val,self.root)



def inorder_traverse(node=None):
    if node is None:
        return []   
    result = []
    result.extend(inorder_traverse(node.left))
    if node.val:
        result.append(node.val)
    result.extend(inorder_traverse(node.right))
    return result



def preorder_traverse(node=None):
    if node is None:
        return []
    result = []
    if node.val:
        result.append(node.val)
    result.extend(preorder_traverse(node.left))
    result.extend(preorder_traverse(node.right))
    return result

def postorder_traverse(node=None):
    if node is None:
        return []
    result = []
    result.extend(postorder_traverse(node.left))
    result.extend(postorder_traverse(node.right))
    if node.val:
        result.append(node.val)
    return result


def max_depth(node):
    if node is None:
        return 0
    left_depth = max_depth(node.left)
    right_depth = max_depth(node.right)
    return max(left_depth, right_depth) + 1