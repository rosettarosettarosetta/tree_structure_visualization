from tree import Node


class RBTree():
    def __init__(self, root_val=None):
        self.NULL = Node(root_val)
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL

    def clear(self):
        self.NULL = Node (None) 
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL

    def minimum(self, node):
        while node.left != self.NULL:
            node = node.left
        return node
   
    def LR ( self , x ) :
        y = x.right                                     
        x.right = y.left                                 
        if y.left != self.NULL :
            y.left.parent = x

        y.parent = x.parent                              
        if x.parent == None :                            
            self.root = y                                
        elif x == x.parent.left :
            x.parent.left = y
        else :
            x.parent.right = y
        y.left = x
        x.parent = y


   
    def RR ( self , x ) :
        y = x.left                                      
        x.left = y.right                                
        if y.right != self.NULL :
            y.right.parent = x

        y.parent = x.parent                              
        if x.parent == None :                            
            self.root = y                                
        elif x == x.parent.right :
            x.parent.right = y
        else :
            x.parent.left = y
        y.right = x
        x.parent = y


    def __rb_transplant ( self , u , v ) :
        if u.parent == None :
            self.root = v
        elif u == u.parent.left :
            u.parent.left = v
        else :
            u.parent.right = v
        v.parent = u.parent


    #插入

    def fixInsert(self, k):
        while k.parent.color == 1:         # 父结点是红色               
            if k.parent == k.parent.parent.right:      # 父节点是否是祖父节点的右子节点:    
                u = k.parent.parent.left       # 叔叔
                if u.color == 1:                         
                    u.color = 0                          
                    k.parent.color = 0                  
                    k.parent.parent.color = 1             # 祖
                    k = k.parent.parent                   # 指向祖父节点
                else:
                    if k == k.parent.left:               #  左子节点
                        k = k.parent
                        self.RR(k)                        # 对父节点进行右旋转
                    k.parent.color = 0                   # 父
                    k.parent.parent.color = 1            
                    self.LR(k.parent.parent)             # 对祖父节点进行左旋转
            else:                                           #父节点是祖父节点的左子节点
                u = k.parent.parent.right                 
                if u.color == 1:                         
                    u.color = 0                          
                    k.parent.color = 0
                    k.parent.parent.color = 1             
                    k = k.parent.parent                   
                else:
                    if k == k.parent.right:               
                        k = k.parent
                        self.LR(k)                        
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.RR(k.parent.parent)              
            if k == self.root:                            
                break
        self.root.color = 0   

    def insertNode(self, key):
        node = Node(key)
        node.parent = None
        node.val = key
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1                                  

        y = None
        x = self.root

        while x != self.NULL :                          
            y = x
            if node.val < x.val :
                x = x.left
            else :
                x = x.right

        node.parent = y                                 
        if y == None :                                   
            self.root = node
        elif node.val < y.val :                         
            y.left = node
        else :
            y.right = node

        if node.parent == None :                      
            node.color = 0
            return

        if node.parent.parent == None :              
            return

        self.fixInsert ( node )                       


    #删除

    def delete_node ( self , val ) :
        self.delete_node_helper ( self.root , val ) 

    def delete_node_helper ( self , node , key ) :
        z = self.NULL
        while node != self.NULL :                         
            if node.val == key :
                z = node

            if node.val <= key :
                node = node.right
            else :
                node = node.left

        if z == self.NULL :                               
            print ( "Value not present in Tree !!" )
            return

        y = z
        y_original_color = y.color                          
        if z.left == self.NULL :                       
            x = z.right                                        
            self.__rb_transplant ( z , z.right )          
        elif (z.right == self.NULL) :                      
            x = z.left                                    
            self.__rb_transplant ( z , z.left )            
        else :                                            
            y = self.minimum ( z.right )      # 找到要删除节点的后继节点              
            y_original_color = y.color                     
            x = y.right
            if y.parent == z :                            
                x.parent = y                  # 如果后继节点是要删除节点的右子节点,调整指针              
            else :
                self.__rb_transplant ( y , y.right )
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant ( z , y )
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            # 如果被删除节点原来是黑色,需要调用 fixDelete 函数来修复红黑树
        if y_original_color == 0 :                         
            self.fixDelete ( x )


        

    def fixDelete ( self , x ) :
        while x != self.root and x.color == 0 :          
            if x == x.parent.left :                      
                s = x.parent.right                       
                if s.color == 1 :                         
                    s.color = 0                          
                    x.parent.color = 1                    
                    self.LR ( x.parent )                 
                    s = x.parent.right
                if s.left.color == 0 and s.right.color == 0 :
                    s.color = 1                          
                    x = x.parent
                else :
                    if s.right.color == 0 :              
                        s.left.color = 0                
                        s.color = 1                       
                        self.RR ( s )                     
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0                   
                    s.right.color = 0
                    self.LR ( x.parent )                 
                    x = self.root
            else :                                       
                s = x.parent.left                        
                if s.color == 1 :                        
                    s.color = 0                          
                    x.parent.color = 1                   
                    self.RR ( x.parent )                
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0 :
                    s.color = 1
                    x = x.parent
                else :
                    if s.left.color == 0 :                
                        s.right.color = 0                
                        s.color = 1
                        self.LR ( s )                    
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.RR ( x.parent )
                    x = self.root
        x.color = 0



