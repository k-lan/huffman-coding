import heapq as hq


# heapify(iterable) - converts iterable (list) into heap data structure
# heappush(heap, ele) - inserts element into heap, adjusts order at same time
# heappop(heap) - pops smallest (first) element


class Node:
    def __init__(self, count, left_child, right_child):
        self.count = count
        self.left_child = left_child
        self.right_child = right_child
        self.direction = ''

    def is_leaf(self):
        return False

    def set_left(self, new_left):
        self.left_child = new_left

    def set_right(self, new_right):
        self.right_child = new_right

    def get_left(self):
        return self.left_child

    def get_right(self):
        return self.right_child

    def get_count(self):
        return self.count

    #  Either 0 or 1 (Left or Right)
    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def __lt__(self, other):
        return self.count < other.count

    def __eq__(self, other):
        return self.count == other.count


class LeafNode(Node):
    def __init__(self, symbol, count):
        super().__init__(count, None, None)
        self.symbol = symbol

    def is_leaf(self):
        return True


def build_tree(F: dict):
    """
    Takes F and builds binary tree, returning root node T
    Args:
        F: dictionary of frequencies

    Returns:
        T: Root node
    """
    leaves = []

    for key in F:  # Create bottom level
        leaves.append(LeafNode(key, F[key]))

    hq.heapify(leaves)  # turn leaves into priority queue

    while len(leaves) > 1:  # Build Tree
        left_child = hq.heappop(leaves)
        right_child = hq.heappop(leaves)

        # Set direction of each node. If left child it is 0.
        left_child.set_direction('0')
        right_child.set_direction('1')

        frequency = left_child.get_count() + right_child.get_count()
        new_node = Node(frequency, left_child, right_child)
        hq.heappush(leaves, new_node)

    T = hq.heappop(leaves)

    return T


# Huffman codes for all leaf nodes
codes = dict()


def get_code_map(root):
    """
    helper class for returning codes, this is lazy method of creating the dictionary as the dict is outside the method.
    Args:
        root: Root node

    Returns:
        dictionary form code map.
    """
    build_code_map(root)
    return codes


def build_code_map(node, val=''):
    """
    Args:
        node: node to build map from, preferrably the root node.
        val: Used for recursion, user should not input this value.

    Returns:
        No return value, however it will put values into above dictionary "codes"

    Note: Used this blog post to build this function:
    https://towardsdatascience.com/huffman-encoding-python-implementation-8448c3654328
    Blog used nifty use of recursion that was simple and elegant.
    """
    code = val + node.get_direction()  # Huffman code for current node

    if node.get_left():  # Has a left child
        build_code_map(node.get_left(), code)

    if node.get_right():  # Has a right child
        build_code_map(node.get_right(), code)

    if node.is_leaf():  # Is leaf, add coding to code map.
        codes[node.symbol] = code


class HuffmanCode:
    def __init__(self, F):
        self.T = build_tree(F)
        self.C = get_code_map(self.T)
        # TODO: Construct the Huffman Code and set C and T properly!

    def encode(self, m):
        """
        Uses self.C to encode a binary message.
.    
        Parameters:
            m: A plaintext message.
        
        Returns:
            The binary encoding of the plaintext message obtained using self.C.
        """
        encoding = ""

        for ch in m:
            encoding += self.C[ch]

        return encoding

    def decode(self, encoded):
        """
        Uses self.T to decode a binary message c = encode(m).
.    
        Parameters:
            encoded: A message encoded in binary using self.encode.
        
        Returns:
            The original plaintext message m decoded using self.T.
        """
        message = ""

        node = self.T
        for i in range(len(encoded)):
            if encoded[i] == '0':
                node = node.get_left()
            else:
                node = node.get_right()

            if node.is_leaf():
                message += node.symbol
                node = self.T

        return message


def get_frequencies(s):
    """
    Computes a frequency table for the input string "s".
    
    Parameters:
        s: A string.
        
    Returns:
        A frequency table F such that F[c] = (# of occurrences of c in s).
    """

    F = dict()

    for char in s:
        if char in F:
            F[char] += 1
        else:
            F[char] = 1

    return F


#  Run to see an example of Huffman code
def main():
    print('')
    print("Demonstration of Huffman Coder for the string 'Hello this is Kaelans iteration of Huffman Codes'")
    str1 = "Hello this is Kaelans iteration of Huffman Codes"
    freq = get_frequencies(str1)

    print(F"frequency of above string is get_frequencies(str): {freq}")
    print('')

    huff = HuffmanCode(freq)
    print("C codes HuffmanCode(freq): ", huff.C)
    print('')

    encoded = huff.encode(str1)
    print(F"Encoded version of above string encode(str): {encoded}")
    print('')

    decoded = huff.decode(encoded)
    print(F"Decoded version from encoded huff.decode(encoded): {decoded}")


if __name__ == '__main__':
    main()
