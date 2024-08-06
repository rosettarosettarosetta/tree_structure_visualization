    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)



    def get_height(self, node):
        if not node:
            return 0
        return node.height

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



    def get_balance(self, node):
        if not node:
            return 0
        return self.get_balance(node.left) - self.get_balance(node.right)

    def min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.min_value_node(node.left)

    #avl树插入
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

    #avl 的删除
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

                # 找到后继节点
                temp = self.min_value_node(root.right)
                root.val = temp.val

                # 删除后继节点
                root.right = self.avl_delete(root.right, temp.val)

            if root is None:
                return root

            # 更新高度
            root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

            # 检查平衡因子并进行旋转
            balance = self.get_balance(root)
            print(root.val, balance)

            if balance > 1 and max_depth(root.left) >= max_depth(root.right):
                return self.rotate_right(root)
            if balance > 1 and max_depth(root.left) < max_depth(root.right):
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)
            if balance < -1 and max_depth(root.right) <= max_depth(root.left):
                return self.rotate_left(root)
            if balance < -1 and max_depth(root.right) > max_depth(root.left):
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

            return root

    def Avl_delete(self, val):
        self.root = self.avl_delete(self.root, val)