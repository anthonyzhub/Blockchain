class Block:

    # Class initializer
    def __init__(self):
        
        # Data can be any type
        self.current_hash = None
        self.prev_hash = None
        self.next_hash = None

    """
    # Setter methods
    def set_data(self, incoming_data):
        self.current_hash = incoming_data

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
        return self.current_hash
    """