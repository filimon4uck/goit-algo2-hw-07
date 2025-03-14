import timeit
from functools import lru_cache


class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, current_node):
        if data < current_node.data:
            if current_node.left_node:
                self._insert_node(data, current_node.left_node)
            else:
                current_node.left_node = Node(data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(data, current_node.right_node)
            else:
                current_node.right_node = Node(data, current_node)

    def find(self, data):
        node = self.root
        while node is not None:
            if data < node.data:
                node = node.left_node
            elif data > node.data:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None

    def _splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif (
                node == node.parent.left_node
                and node.parent == node.parent.parent.left_node
            ):
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif (
                node == node.parent.right_node
                and node.parent == node.parent.parent.right_node
            ):
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            elif node == node.parent.left_node:
                self._rotate_right(node.parent)
                self._rotate_left(node.parent)
            else:
                self._rotate_left(node.parent)
                self._rotate_right(node.parent)
        return node.data

    def _rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child


@lru_cache
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    if n <= 1:
        return n

    result = tree.find(n)
    if result is None:
        a, b = 0, 1
        for i in range(2, n + 1):
            a, b = b, a + b
        result = b
        tree.insert(n)
    return result


def measure_time(func, args):
    start = timeit.default_timer()
    func(*args)
    return timeit.default_timer() - start


def main():
    ns = range(0, 1001, 50)
    lru_times = []
    splay_times = []

    for n in ns:
        lru_times.append(measure_time(fibonacci_lru, (n,)))
        splay_tree = SplayTree()
        splay_times.append(measure_time(fibonacci_splay, (n, splay_tree)))

    import matplotlib.pyplot as plt

    plt.plot(ns, lru_times, label="LRU Cache", color="blue")
    plt.plot(ns, splay_times, label="Splay Tree", color="orange")
    plt.xlabel("n (Fibonacci index)")
    plt.ylabel("Time (s)")
    plt.title("Fibonacci Calculation Time: LRU Cache vs Splay Tree")
    plt.legend()
    plt.show()

    print("n\tLRU Cache Time (s)\tSplay Tree Time (s)")
    print("---------------------------------------------")
    for i, n in enumerate(ns):
        print(f"{n}\t{lru_times[i]:.8f}\t	{splay_times[i]:.8f}")


if __name__ == "__main__":
    main()
