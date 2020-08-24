class Block:

    # OBJECTIVE: To create components needed to make a block

    # Class initializer
    def __init__(self):
        
        # Create pointers to surrounding blocks
        self.prev_block_pointer = None
        self.next_block_pointer = None

        # Hold values of surrounding blocks' hash value
        self.previous_block_hash = None
        self.current_block_hash = None
        self.current_block_data = None

        # Keep uploader's signature
        self.uploader_public_key = None
