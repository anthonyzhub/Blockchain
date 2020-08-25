from Block import Block
from collections import deque

import numpy as np
import pandas as pd
import zipfile
import os
import time

class Blockchain:

    # Declare static variable for add_block()
    # A static variable's value will always be remembered until program is terminated
    previous_hash_static = None

    # Difficulty of PoW algorithm
    difficulty = 2

    def __init__(self):
        
        # Create a head and tail node
        self.head = None
        self.tail = None

        # Set linked list size to 0
        self.list_size = 0

        # Create a queue of unconfirmed transactions
        self.unconfirmed_transactions = deque()

        # Create a data frame
        self.data_frame = pd.DataFrame()

    def is_empty(self):

        # OBJECTIVE: Check if list is empty
        return self.list_size == 0

    def create_hash(self, block):

        # OBJECTIVE: Before officially adding a block, increment block's nonce value until a proper hash value is computed

        """
        NOTE: A nonce is created to see how many times it will take for the computer to create a valid hash.
                A hash is valid, if it has a leading number of 0s. In this case, the number of zeros depends
                on the level of difficulty. Hence, the variable "difficulty" that is declared at the beginning
                of this class. 

                This approach is brute force because we are starting at 0. The variable will increment until
                a proper hash is calculated. So, nonce could eventually be 1_000_000_000!
        """

        # Start nonce value as 0
        block.nonce = 0

        # Compute block's hash
        hash = block.compute_hash()

        # Continue to compute a new hash until it starts with a N number of 0s.
        # Ex. 00xxxxx
        while not hash.startswith("0" * self.difficulty):

            # Increment block's nonce value and compute new hash
            block.nonce += 1
            hash = block.compute_hash()

        return hash

    def is_hash_valid(self, new_block, proposed_hash):

        # OBJECTIVE: Check if hash value meets the requirements AND hash value matches with a newly created hash value
        #
        #   1. Does proposed_hash start with N number of 0s?
        #   2. If hash is recomputed, would it return the same string?
        return (proposed_hash.startswith("0" * self.difficulty) and proposed_hash == new_block.compute_hash())

    def validate_entry(self, new_block, proposed_hash):

        # OBJECTIVE: Verify block can be added to link list by:
        #
        #   1. Does new_block have the correct previous_block_hash?
        #   2. Does new_block's hash meet the requirements

        # Get hash from last block
        old_hash = self.tail.current_block_hash

        # Stop if hash values don't match
        if new_block.previous_block_hash != old_hash:
            return False

        # Stop if block's hash value isn't valid
        if not self.is_hash_valid(new_block, proposed_hash):
            return False

        # If hash value is valid, then add it to the new block
        new_block.current_block_hash = proposed_hash

        return True

    def create_head(self, data):

        # OBJECTIVE: Create a head block with previous_hash as 0

        print("Creating a head block")

        # Create a head block with a hash
        head_block = Block(self.list_size, data, time.time(), "0")
        head_block.current_block_hash = self.create_hash(head_block)

        # Add it to link list
        self.head = head_block
        self.tail = head_block

        # Update previous_hash_static variable
        self.previous_hash_static = head_block.current_block_hash

        # Increment counter for list size
        self.list_size += 1

    def add_block(self, data):

        # OBJECTIVE: Add a block to link list

        # If list is empty, go to a dedicated function to create a head block
        if self.is_empty():

            self.create_head(data)

        print("Creating a new block")

        # Create a new block and compute a hash value
        new_block = Block(self.list_size, data, time.time(), self.previous_hash_static)
        new_block.current_block_hash = self.create_hash(new_block)

        # Get last block to update pointers
        old_block = self.tail

        old_block.next_block = new_block

        new_block.previous_block = old_block
        new_block.next_block = None

        # Update tail
        self.tail = new_block

        # Update old hash value
        self.previous_hash_static = new_block.current_block_hash

        # Update list's length
        self.list_size += 1

    def verify_chain(self):

        # Exit if link list only has <=1 block
        if self.is_empty() or self.list_size == 1:
            print("There's only <=1 blocks in the link list")
            return True

        # Get starting blocks
        tmp_block_a = self.head
        tmp_block_b = tmp_block_a.next_block

        counter = 0

        # Iterate link list
        while tmp_block_b is not None:

            # Compare hash values
            if tmp_block_b.previous_block_hash != tmp_block_a.current_block_hash:
                print("ERROR: Block #{} has a different hash value than Block #{}!".format(counter, counter - 1))
                return False

            # Update temporary blocks
            tmp_block_a = tmp_block_b
            tmp_block_b = tmp_block_b.next_block

            # Increment counter
            counter += 1

        return True


    def print_list(self):

        # OBJECTIVE: Print blockchain

        # Exit if link list is empty
        if self.is_empty():
            
            print("List is empty!")
            return None

        # Get head block
        old_block = self.head
        counter = 0

        while old_block is not None:

            # Print block's contents
            print("\nBlock Data:")
            print("\tHash: {}".format(old_block.current_block_hash))
            print("\tData: {}".format(old_block.data))
            counter += 1

            # Move to next block
            old_block = old_block.next_block

        # Print total number of blocks inside chain
        print("\nTotal Blocks: {}".format(counter))

    def download_blockchain_data(self):

        # OBJECTIVE: Write blockchain data to CSV file

        # Check if list is empty
        if self.is_empty() is True:

            print("List is empty!")
            return None

        # Get genesis block
        old_block = self.head
        dict_block = dict()
        block_num = 0

        while old_block is not None:

            # Write block's data to dictionary
            dict_block["Previous Block's Hash"] = old_block.previous_block_hash
            dict_block["Current Block's Hash"] = old_block.current_block_hash

            dict_block["Current Block's Data"] = old_block.current_block_data

            # Save dictionary to data frame
            self.data_frame = self.data_frame.append(dict_block, ignore_index=True)

            # Rename index names to Block <block_num>
            """
            1. Rename index with lambda function (nameless function)
            2. Parameter for lambda function is block_num, the variable I created as a counter
            3. The function will return a string "Block #" with # as the value of block_num
            """
            self.data_frame = self.data_frame.rename(index=lambda block_num: "Block {}".format(block_num))
            block_num+=1

            # Move to next block
            old_block = old_block.next_block_pointer

        # Write dataframe to CSV file
        csv_file_name = "Zamora-Blockchain_Data.csv"
        self.data_frame.to_csv(csv_file_name)

        # Compress CSV file
        zip_file = zipfile.ZipFile("Zamora-Blockchain.zip", mode='w') # <- Create a zip file archive for writing
        zip_file.write(csv_file_name, compress_type=zipfile.ZIP_STORED) # <- Write csv file to zip_file for compression
        zip_file.close() # <- Close file after writing to it

        # Delete uncompressed file
        os.remove(csv_file_name)
