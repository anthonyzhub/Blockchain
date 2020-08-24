import time
import json

from hashlib import sha256

class Block:

    # OBJECTIVE: To create components needed to make a block

    # Class initializer
    def __init__(self, index, data, timestamp, previous_block_hash, current_block_hash, nonce=0):
        
        # Block's position and plain data
        self.index = index
        self.data = data

        # Block'stime of creation
        self.timestamp = timestamp

        # Save hashes
        self.previous_block_hash = previous_block_hash
        self.current_block_hash = current_block_hash

        self.nonce = nonce

    def compute_hash(self):

        # OBJECTIVE: Compute hash value of block's contents
        
        # Create a dictionary in JSON format and sort keys
        json_string = json.dumps(self.__dict__, sort_keys=True)

        # Return hash value of block's content
        return sha256(json_string.encode()).hexdigest()