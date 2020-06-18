from Block import Block
from Hash import Hash

class LinkList:

    def __init__(self):
        
        # Set head node as blank
        self.genesis_block = None

        # Set starting size to 0
        self.list_size = 0

    def get_genesis_block(self):
        # OBJECTIVE: Get head node
        return self.genesis_block

    def get_size(self):
        # OBJECTIVE: Get list's size
        return self.list_size

    def is_empty(self):
        # OBJECTIVE: Check if list is empty
        return self.get_size() == 0

    def add_block(self, incoming_data):
        # OBJECTIVE: Append a block at the end of the chain

        # Immediately encrypt incoming_hash
        hash_class = Hash()
        
        # Decide on how to encrypt incoming_data (whether it's a list or not)
        if hash_class.isDataList(incoming_data):
            incoming_hash = hash_class.encrypt_list(incoming_data)
        else:
            incoming_hash = hash_class.encrypt_data(incoming_data)

        # If list is empty, automatically add incoming_hash as head block
        if self.is_empty():

            # Create a new block
            new_head_block = Block()

            # Create links for block
            new_head_block.prev_hash = None # <- Genesis block doesn't have a previous hash because it's the first
            new_head_block.current_hash = incoming_hash
            new_head_block.next_hash = None # <- Set to None until a new block is created

            # Set new_head_block as genesis_block
            self.genesis_block = new_head_block

        else:

            # Create a new node and pass incoming_hash to it
            new_block = Block()
            new_block.current_hash = incoming_hash
            new_block.next_hash = None

            # Go to last block inside of chain
            current_block = self.genesis_block

            while current_block.next_hash is not None:
                current_block = current_block.next_hash

            # Update previous node's link to next block
            current_block.next_hash = new_block
            new_block.prev_hash = current_block

        # Update list's length
        self.list_size += 1

    def print_list(self):        
        # OBJECTIVE: Print all blocks inside of chain

        # If chain is empty, return error message
        if self.is_empty():
            print("List is empty")
            return None

        # Start from head node with starting position of 0
        current_block = self.genesis_block
        position = 0

        # Condition is True, if current_block has hash
        while current_block is not None:

            # Update position
            position += 1

            # Print block's hash
            print("{}. {}".format(position, current_block.current_hash))

            # Move to next node
            current_block = current_block.next_hash