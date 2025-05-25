import json
from collections import deque

class Item:
    def __init__(self, id, name, description, category):
        self.id = id
        self.name = name
        self.description = description
        self.category = category

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Description: {self.description}, Category: {self.category}"


class StackUndo:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop() if self.stack else None

    def is_empty(self):
        return len(self.stack) == 0


class PriorityQueueManager:
    def __init__(self):
        self.urgent_queue = deque()
        self.normal_queue = deque()

    def enqueue(self, item, priority):
        if priority.lower() == 'urgent':
            self.urgent_queue.append(item)
        else:
            self.normal_queue.append(item)

    def dequeue(self):
        if self.urgent_queue:
            return self.urgent_queue.popleft()
        elif self.normal_queue:
            return self.normal_queue.popleft()
        return None


class LinkedListManager:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def delete(self, id):
        for i, item in enumerate(self.items):
            if item.id == id:
                del self.items[i]
                return True
        return False

    def find(self, id):
        for item in self.items:
            if item.id == id:
                return item
        return None

    def get_all(self):
        return self.items


class BSTNode:
    def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None


class BSTManager:
    def __init__(self):
        self.root = None

    def insert(self, item):
        def _insert(node, item):
            if not node:
                return BSTNode(item)
            if item.id < node.item.id:
                node.left = _insert(node.left, item)
            elif item.id > node.item.id:
                node.right = _insert(node.right, item)
            return node

        self.root = _insert(self.root, item)

    def search(self, id):
        def _search(node, id):
            if not node:
                return None
            if node.item.id == id:
                return node.item
            elif id < node.item.id:
                return _search(node.left, id)
            else:
                return _search(node.right, id)

        return _search(self.root, id)


def save_to_file(items, filename="items.json"):
    with open(filename, "w") as f:
        json.dump([item.__dict__ for item in items], f)


def load_from_file(filename="items.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [Item(**item) for item in data]
    except FileNotFoundError:
        return []


def main():
    undo_stack = StackUndo()
    priority_queue = PriorityQueueManager()
    list_manager = LinkedListManager()
    bst_manager = BSTManager()

    # Load saved data
    for item in load_from_file():
        list_manager.add(item)
        bst_manager.insert(item)

    while True:
        print("\n1. Add Item\n2. View Items\n3. Update Item\n4. Delete Item\n5. Undo Delete\n6. Search Item\n7. Save\n8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            id = input("Enter ID: ")
            if bst_manager.search(id):
                print("Item already exists.")
                continue
            name = input("Name: ")
            desc = input("Description: ")
            cat = input("Category: ")
            prio = input("Priority (urgent/normal): ")
            item = Item(id, name, desc, cat)
            list_manager.add(item)
            bst_manager.insert(item)
            priority_queue.enqueue(item, prio)
            print("Item added.")

        elif choice == "2":
            print("--- Items ---")
            for item in list_manager.get_all():
                print(item)

        elif choice == "3":
            id = input("Enter ID to update: ")
            item = list_manager.find(id)
            if item:
                item.name = input("New name: ")
                item.description = input("New description: ")
                item.category = input("New category: ")
                print("Updated.")
            else:
                print("Not found.")

        elif choice == "4":
            id = input("Enter ID to delete: ")
            item = list_manager.find(id)
            if item:
                list_manager.delete(id)
                undo_stack.push(item)
                print("Deleted.")
            else:
                print("Not found.")

        elif choice == "5":
            restored = undo_stack.pop()
            if restored:
                list_manager.add(restored)
                bst_manager.insert(restored)
                print("Undo done.")
            else:
                print("Nothing to undo.")

        elif choice == "6":
            id = input("Enter ID to search: ")
            item = bst_manager.search(id)
            print(item if item else "Not found.")

        elif choice == "7":
            save_to_file(list_manager.get_all())
            print("Items saved.")

        elif choice == "8":
            save_to_file(list_manager.get_all())
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
