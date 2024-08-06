from tree import Node

class RB_tree(object):
    def __init__(self)->None:
        self.root=None

        # 无参构造函数
    def clear(self)->None:
        self.root=None

    def insert(self,node:Node)->None:
        # print(node.val)
        if self.root==None:
            node.color='b'
            self.root=node
            # print("1")
            return
        # 不为空树
        currentNode=self.root
        while True:
            if node.val<currentNode.val:
                if currentNode.left==None:
                    currentNode.left=node
                    node.parent=currentNode
                    break
                else:
                    currentNode=currentNode.left
            else:
                if currentNode.right==None:
                    currentNode.right=node
                    node.parent=currentNode
                    break
                else:
                    currentNode=currentNode.right
        # 插入结束开始进行平衡操作
        self.__insertBalance(node)

    def __insertBalance(self, node: Node):
        """
        插入平衡函数
        """
        pNode = node.parent
        if pNode is None:
            # 该节点为根节点
            node.color = 'b'
            return
        if pNode.color == 'b':
            # 父节点为黑色,已满足红黑树性质,无需调整
            return

        gNode = pNode.parent
        if gNode is None:
            # 如果祖父节点不存在,直接将父节点染黑即可
            pNode.color = 'b'
            return

        # 确定父节点和叔叔节点的位置关系
        flag1 = 0 if gNode.left == pNode else 1
        uNode = gNode.left if flag1 == 0 else gNode.right

        if uNode is not None and uNode.color == 'r':
            # 叔叔节点为红色
            pNode.color = 'b'
            uNode.color = 'b'
            gNode.color = 'r'
            self.__insertBalance(gNode)
        else:
            # 叔叔节点为黑色或不存在
            flag2 = 0 if pNode.left == node else 1
            if flag1 == 0 and flag2 == 0:
                # 父左子左
                self.__rotateRight(gNode)
                pNode.color, gNode.color = gNode.color, pNode.color
            elif flag1 == 1 and flag2 == 1:
                # 父右子右
                self.__rotateLeft(gNode)
                pNode.color, gNode.color = gNode.color, pNode.color
            elif flag1 == 0 and flag2 == 1:
                # 父左子右
                self.__rotateLeft(pNode)
                self.__rotateRight(gNode)
                node.color, pNode.color, gNode.color = gNode.color, node.color, pNode.color
            elif flag1 == 1 and flag2 == 0:
                # 父右子左
                self.__rotateRight(pNode)
                self.__rotateLeft(gNode)
                node.color, pNode.color, gNode.color = gNode.color, node.color, pNode.color
            else:
                # 处理在红色结点的情况下，他的子叶结点还为红色的错误
                if pNode.left is not None and pNode.left.color == 'r':
                    pNode.left.color = 'b'
                if pNode.right is not None and pNode.right.color == 'r':
                    pNode.right.color = 'b'
                if pNode.right is None or (pNode.right is not None and pNode.right.color == 'b'):
                    pNode.color = 'b'
                    gNode.color = 'r'
                    self.__insertBalance(gNode)

    def delete(self,val):
        # 首先搜索节点，判断该节点是否存在
        if self.root==None:
            # 该树为空树
            return
        currentNode=self.root
        while currentNode:
            if currentNode.val==val:
                break
            elif currentNode.val>val:
                currentNode=currentNode.left
            else:
                currentNode=currentNode.right
        if currentNode==None:
            # 该节点不存在
            return
        dnode=currentNode #待删除节点
        self.__delete(dnode) #节点删除完毕
    def __delete(self,dnode:Node):
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
                self.__delete_blackleaf_balance(dnode)
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
            self.__delete(prenode)
    def __delete_blackleaf_balance(self,dnode:Node)->None:
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
                    self.__delete_blackleaf_balance(pnode)
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
                        self.__delete_blackleaf_balance(dnode)
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
                        self.__delete_blackleaf_balance(dnode)
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
            self.__delete_blackleaf_balance(dnode)
# 红黑树中序遍历
def mid(root:Node):
    if root==None:
        return
    mid(root.left)
    if root.left:
        left=root.left.val
    else:
        left=None
    if root.right:
        right=root.right.val
    else:
        right=None
    if root.parent:
        f=root.parent.val
    else:
        f=None
    print(root.val,root.color,f,left,right)
    mid(root.right)

# # 代码测试
# data=[10,20,15,30]
# rd=RB_tree()
# for x in data:
#     node=Node(x)
#     rd.insert(node)
# rd.delete(10)
# mid(rd.root)


    def avl_insert(self, val,root):
        if root is None:
            return Node(val)
        
        if isinstance(val, list):
            for v in val:
                root = self.avl_insert(v,root)
            return root
        else:
            if val < root.val:
                root.left = self.avl_insert( val,root.left)
            elif val > root.val:
                root.right = self.avl_insert(val,root.right)
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