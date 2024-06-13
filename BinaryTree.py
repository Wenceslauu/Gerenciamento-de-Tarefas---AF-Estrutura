class NodeTree:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class Task:
    def __init__(self, description, priority, due_date):
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def __str__(self):
        return f"Descrição: {self.description}, Prioridade: {self.priority}, Data de Vencimento: {self.due_date.strftime('%d/%m/%Y')}"

    def __eq__(self, other):
        return self.description == other.description

    def __lt__(self, other):
        return self.description < other.description


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert_rec(self.root, key)

    def _insert_rec(self, root, key):
        if root is None:
            return NodeTree(key)
        if key.description < root.key.description:
            root.left = self._insert_rec(root.left, key)
        elif key.description > root.key.description:
            root.right = self._insert_rec(root.right, key)
        return root

    def delete(self, key):
        self.root = self._delete_rec(self.root, key)

    def _delete_rec(self, root, key):
        if root is None:
            return root

        if key.description < root.key.description:
            root.left = self._delete_rec(root.left, key)
        elif key.description > root.key.description:
            root.right = self._delete_rec(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            min_larger_node = self._get_min(root.right)
            root.key = min_larger_node.key
            root.right = self._delete_rec(root.right, min_larger_node.key)
        return root

    def _get_min(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    def search(self, key):
        return self._search_rec(self.root, key)

    def _search_rec(self, root, key):
        if root is None:
            return False
        if key.description == root.key.description:
            return True
        elif key.description < root.key.description:
            return self._search_rec(root.left, key)
        else:
            return self._search_rec(root.right, key)

    def inorder(self):
        res = []
        self._inorder_rec(self.root, res)
        return res

    def _inorder_rec(self, root, res):
        if root:
            self._inorder_rec(root.left, res)
            res.append(root.key)
            self._inorder_rec(root.right, res)

    def display(self, node=None, level=0, prefix="Root: "):
        if node is not None:
            print(" " * (level * 4) + prefix + str(node.key))
            if node.left:
                self.display(node.left, level + 1, "L--- ")
            if node.right:
                self.display(node.right, level + 1, "R--- ")

    def display_alphabetical(self):
        print("\nTarefas em ordem alfabética (estrutura da árvore):")
        self.display(self.root)
        print()
