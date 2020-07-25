from Block import Block
from Hash import Hash

class LinkList:

    # Declare static variable for add_block()
    # A static variable's value will always be remembered until program is terminated
    previous_hash_static = None

    def __init__(self):
        
        # Set head node as blank
        self.genesis_block = None

        # Initialize Hash class
        self.hash_class = Hash()

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

    def add_block(self, new_unencrypted_data):
        # OBJECTIVE: Append a block at the end of the chain

        # Create instance of Hash class
        self.hash_class = Hash()

        # Encrypt data
        new_encrypted_data = self.hash_class.encrypt_data(new_unencrypted_data)

        # If list is empty, automatically add incoming_hash as head block
        if self.is_empty():

            # Create a new block
            new_head_block = Block()

            # Create links for block
            new_head_block.prev_block_pointer = None
            new_head_block.next_block_pointer = None
            
            # Add encrypted and unencrypted data to block
            new_head_block.previous_block_hash = None
            new_head_block.current_block_hash = new_encrypted_data
            new_head_block.current_block_data = new_unencrypted_data # Add unencrypted data for verification later on

            # Set new_head_block as genesis_block
            self.genesis_block = new_head_block

        else:

            # Create a new node and pass incoming_hash to it
            new_block = Block()
            new_block.current_block_hash = new_encrypted_data
            new_block.current_block_data = new_unencrypted_data

            # Go to last block inside of chain
            current_block = self.genesis_block

            while current_block.next_block_pointer is not None:
                current_block = current_block.next_block_pointer

            # Update current_block's pointer and hash value
            current_block.next_block_pointer = new_block

            # Update new_block's pointers and hash values
            new_block.previous_block_hash = self.previous_hash_static
            new_block.prev_block_pointer = current_block
            new_block.next_block_pointer = None

        # Update list's length
        self.list_size += 1

        # Save new encrypted data to previous_hash_static
        self.previous_hash_static = new_encrypted_data

    def verify_chain(self):

        # OBJECTIVE: Verify block chain was not tampered with by comparing hashes between 2 blocks

        # Check if list is empty or only has 1 block inside the chain
        if self.is_empty() or self.list_size == 1:
            
            print("Blockchain is empty or only has 1 block.")
            return None

        # Get 1st 2 block
        current_block = self.genesis_block
        next_block = current_block.next_block_pointer

        while next_block is not None:
            
            # Return "False" if hashes between current_block and next_block don't match
            if current_block.current_block_hash != next_block.previous_block_hash:
                
                print("Invalid chain!")
                return False

            # Move to next block
            current_block = next_block
            next_block = next_block.next_block_pointer

        # Return "True" if previous if-statement wasn't triggered
        return True

    def print_list(self):

        # OBJECTIVE: Print block chain

        if self.is_empty():
            
            print("List is empty!")
            return None

        # Get starting block
        current_block = self.genesis_block
        position = 0

        while current_block is not None:

            # Update position
            position += 1

            # Print block's contents
            print("\nBlock Data:")
            print("\tHash Value: {}".format(current_block.current_block_hash))
            print("\tData: {}".format(current_block.current_block_data))

            # Move to next block
            current_block = current_block.next_block_pointer

        # Print total number of blocks inside chain
        print("\nTotal Blocks: {}".format(position))