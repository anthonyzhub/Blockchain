class Node:

    # Class initializer
    def __init__(self):
        
        # Global variables
        data = None
        prev_hash = None
        next_hash = None

    # Setter methods
    def set_data(self, incoming_data):
        self.data = incoming_data

    def set_prev_hash(self, prev_hash):
        self.prev_hash = prev_hash

    def set_next_hash(self, next_hash):
        self.next_hash = next_hash

    # Getter methods
    def get_prev_hash(self):
        return self.prev_hash

    def get_next_hash(self):
        return self.next_hash

    def get_data(self):
        return self.data
