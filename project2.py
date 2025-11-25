import tkinter as tk
import random

# Node and Circular Doubly Linked List Classes
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None

    # Append a node to the end of the list
    def append(self, data):
        new_node = Node(data)
        if not self.head:  # If list is empty
            self.head = new_node
            new_node.next = new_node  # Point to itself
            new_node.prev = new_node
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    # Insert a node at the start of the list
    def insert_at_start(self, data):
        new_node = Node(data)
        if not self.head:  # If list is empty
            self.head = new_node
            new_node.next = new_node  # Point to itself
            new_node.prev = new_node
        else:
            tail = self.head.prev
            new_node.next = self.head
            new_node.prev = tail
            tail.next = new_node
            self.head.prev = new_node
            self.head = new_node  # Update head

    # Insert a node between two existing nodes
    def insert_between(self, prev_node, data):
        if not prev_node:
            return None
        new_node = Node(data)
        next_node = prev_node.next
        prev_node.next = new_node
        new_node.prev = prev_node
        new_node.next = next_node
        next_node.prev = new_node

    # Clear the entire linked list
    def clear(self):
        self.head = None

# GUI Class for Visualizing the Linked List
class LinkedListVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Circular Doubly Linked List Visualizer")
        self.canvas = tk.Canvas(master, width=1000, height=400, bg="white")
        self.canvas.pack()

        self.cdll = CircularDoublyLinkedList()  # Instance of CircularDoublyLinkedList
        self.node_widgets = []  # Stores visual nodes (circles, text)

    # Method to generate random colors for nodes
    def get_random_color(self):
        colors = ["lightblue", "lightgreen", "lightcoral", "lightpink", "lightsalmon", "lightgoldenrod", "lightcyan"]
        return random.choice(colors)

    # Method to draw a node at (x, y) position on the canvas
    def draw_node(self, data, x, y):
        node_radius = 20
        color = self.get_random_color()  # Get a random color for the node
        node = self.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill=color)
        text = self.canvas.create_text(x, y, text=str(data))
        self.node_widgets.append((node, text))

    # Updates the entire linked list visualization
    def update_list(self):
        self.canvas.delete("all")  # Clear the canvas
        if not self.cdll.head:
            return
        
        x, y = 50, 200  # Initial position to draw nodes
        node = self.cdll.head
        previous_x = None

        while True:
            self.draw_node(node.data, x, y)  # Draw node

            # If there is a previous node, draw the bidirectional arrows (forward and backward links)
            if previous_x is not None:
                # Forward link (next)
                self.canvas.create_line(previous_x + 20, y, x - 20, y, arrow=tk.LAST, fill="blue")
                # Backward link (prev)
                self.canvas.create_line(x - 20, y, previous_x + 20, y, arrow=tk.FIRST, fill="red")

            previous_x = x
            x += 120  # Move position to the right for the next node
            node = node.next
            if node == self.cdll.head:  # Stop if we looped back to the head
                break

    # Insert a node at the end of the list
    def insert(self, data):
        self.cdll.append(data)
        self.update_list()

    # Insert a node at the start of the list
    def insert_at_start(self, data):
        self.cdll.insert_at_start(data)
        self.update_list()

    # Insert a node between two nodes
    def insert_between(self, prev_index, data):
        prev_node = self.get_node_by_index(prev_index)
        self.cdll.insert_between(prev_node, data)
        self.update_list()

    # Get node by its index for insertion between nodes
    def get_node_by_index(self, index):
        node = self.cdll.head
        count = 0
        if not node:
            return None
        while count < index:
            node = node.next
            if node == self.cdll.head:  # Loop back to head
                return None
            count += 1
        return node

    # Clear the linked list visualization
    def clear_list(self):
        self.cdll.clear()
        self.update_list()

# Controls Class for User Interaction (Buttons, Inputs)
class Controls:
    def __init__(self, master, visualizer):
        self.visualizer = visualizer

        # Entry for data to insert (can be multiple comma-separated values)
        self.entry = tk.Entry(master)
        self.entry.pack()

        # Button to insert multiple values at the end
        self.insert_button = tk.Button(master, text="Insert at End", command=self.insert_multiple)
        self.insert_button.pack()

        # Button to insert at start
        self.insert_start_button = tk.Button(master, text="Insert at Start", command=self.insert_at_start)
        self.insert_start_button.pack()

        # Button to insert between nodes
        self.insert_between_button = tk.Button(master, text="Insert Between", command=self.insert_between)
        self.insert_between_button.pack()

        # Entry for index where to insert the node between two nodes
        self.index_entry = tk.Entry(master)
        self.index_entry.pack()

        # Button to clear the linked list
        self.clear_button = tk.Button(master, text="Clear All", command=self.clear_all)
        self.clear_button.pack()

    # Get data and insert multiple nodes at the end of the list
    def insert_multiple(self):
        data = self.entry.get()
        if data:
            # Split the input string by commas and strip any whitespace
            elements = [elem.strip() for elem in data.split(",")]
            for elem in elements:
                self.visualizer.insert(elem)

    # Get data and insert nodes at the start
    def insert_at_start(self):
        data = self.entry.get()
        if data:
            # Split the input string by commas and strip any whitespace
            elements = [elem.strip() for elem in data.split(",")]
            for elem in elements:
                self.visualizer.insert_at_start(elem)

    # Get data and insert between nodes based on index
    def insert_between(self):
        data = self.entry.get()
        if data and self.index_entry.get().isdigit():
            prev_index = int(self.index_entry.get())
            # Ensure the index is valid
            if prev_index >= 0 and self.visualizer.get_node_by_index(prev_index):
                self.visualizer.insert_between(prev_index, data)
            else:
                print("Invalid index!")  # Handle invalid index cases

    # Clear input fields and linked list
    def clear_all(self):
        self.entry.delete(0, tk.END)  # Clear the input entry
        self.index_entry.delete(0, tk.END)  # Clear the index entry
        self.visualizer.clear_list()  # Clear the visualization

# Main Function to Initialize the GUI
if __name__ == "__main__":
    root = tk.Tk()
    visualizer = LinkedListVisualizer(root)  # Instantiate the visualizer
    controls = Controls(root, visualizer)  # Instantiate the controls
    root.mainloop()
