class Block:

    # Class initializer
    def __init__(self):
        
        # Create pointers to surrounding blocks
        self.prev_block_pointer = None
        self.next_block_pointer = None

        # Hold values of surrounding blocks' hash value
        self.current_block_hash = None
        self.prev_block_hash = None
        self.next_block_hash = None
