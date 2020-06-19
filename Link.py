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

    def add_block(self, incoming_hash):
        # OBJECTIVE: Append a block at the end of the chain

        # Create instance of Hash class
        hash_class = Hash()
        
        # Decide on how to encrypt incoming_data (whether it's a list or not)
        if hash_class.isDataList(incoming_hash):
            incoming_hash = hash_class.encrypt_list(incoming_hash)
        else:
            incoming_hash = hash_class.encrypt_data(incoming_hash)

        # If list is empty, automatically add incoming_hash as head block
        if self.is_empty():

            # Create a new block
            new_head_block = Block()

            # Create links for block
            new_head_block.prev_block_pointer = None
            new_head_block.prev_block_hash = None # <- Genesis block doesn't have a previous hash because it's the first
            
            new_head_block.current_block_hash = incoming_hash
            
            new_head_block.next_block_pointer = None
            new_head_block.next_block_hash = None # <- Set to None until a new block is created

            # Set new_head_block as genesis_block
            self.genesis_block = new_head_block

        else:

            # Create a new node and pass incoming_hash to it
            new_block = Block()
            new_block.current_block_hash = incoming_hash

            # Go to last block inside of chain
            current_block = self.genesis_block

            while current_block.next_block_pointer is not None:
                current_block = current_block.next_block_pointer

            # Update current_block's pointer and hash value
            current_block.next_block_pointer = new_block
            current_block.next_block_hash = new_block.current_block_hash

            # Update new_block's pointers and hash values
            new_block.prev_block_pointer = current_block
            new_block.prev_block_hash = current_block.current_block_hash

            new_block.next_block_pointer = None
            new_block.next_block_hash = None

        # Update list's length
        self.list_size += 1

    def verify_chain(self):

        # OBJECTIVE: To verify chain hasn't been broken
        # NOTE: A chain is broken if a block A has different hash records of block B.

        # Set previous, current, and next block for iteration
        old_block = None
        current_block = self.genesis_block
        next_block = current_block.next_block_pointer

        # genesis_block shouldn't have any previous hashes, but still have a record of the next block's hash
        if current_block.prev_block_hash == None and current_block.next_block_hash == current_block.next_block_pointer.current_block_hash:
            
            # Update blocks position
            old_block = current_block
            current_block = current_block.next_block_pointer
            next_block = current_block.next_block_pointer

        else:

            # Print data inside genesis_block
            print("Inside Genesis Block:")
            print("\tPrevious Hash: {}".format(current_block.prev_block_hash))
            print("\tNext Hash: {}\n".format(current_block.next_block_hash))

            # Print suppose data
            print("Suppose Data:")
            print("\tPrevious Hash: {}".format(old_block)) # genesis_block doesn't have prev_block_hash because it's the 1st
            print("\tNext Hash: {}".format(next_block.current_block_hash))

            return False

        # Iterate chain until the last block
        while current_block.next_block_pointer is not None:

            # Condition:
            #   1. Current block's previous hash record must match previous block's hash
            #   2. Current block's next hash record must mast next block's hash
            if current_block.prev_block_hash == old_block.current_block_hash and current_block.next_block_hash == next_block.current_block_hash:
                
                # Update blocks position
                old_block = current_block
                current_block = current_block.next_block_pointer
                next_block = current_block.next_block_pointer
            
            else:

                # Print data inside genesis_block
                print("Inside {} Block:".format(current_block.current_block_hash))
                print("\tPrevious Hash: {}".format(current_block.prev_block_hash))
                print("\tNext Hash: {}\n".format(current_block.next_block_hash))

                # Print suppose data
                print("Suppose Data:")
                print("\tPrevious Hash: {}".format(old_block.current_block_hash))
                print("\tNext Hash: {}".format(next_block.current_block_hash))

                return False

        # Return True, if exceptions haven't been raised
        return True

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
            print("\nBlock Data:")
            print("\tCurrent Block Hash Value: {}".format(current_block.current_block_hash))
            print("\tPrevious Block Hash Value: {}".format(current_block.prev_block_hash))
            print("\tNext Block Hash Value: {}".format(current_block.next_block_hash))

            # Move to next node
            current_block = current_block.next_block_pointer

        # Print total number of blocks inside chain
        print("Total Blocks: {}".format(position))
