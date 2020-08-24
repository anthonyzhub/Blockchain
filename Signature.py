from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import cryptography.exceptions
import os

# Documentation: https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

class Signature:

    # OBJECTIVE: To digital sign a block's data as proof of verification

    def __init__(self):
        
        self.rsa_private_key = None
        self.rsa_public_key = None
        self.signature = None
        self.user_name = os.environ['USER'] # <- Cannot find 'WHOAMI'
        self.PRIVATE_FILE_NAME = "{}-Private_Key.pem".format(self.user_name)
        self.PUBLIC_FILE_NAME = "{}-Public_Key.pem".format(self.user_name)

    def format_data(self, data):

        # OBJECTIVE: Change data to string as bytes and change it to a string if needed

        if type(data) is str:

            # Transform data to bytes
            data = bytes(data, "UTF-8")

        else:

            # Change data type and transform it
            data = bytes(str(data), "UTF-8")

        # Return edited data
        return data

    def generate_keys(self):

        # OBJECTIVE: To generate a public-private key using RSA

        """
        NOTE:
        1. public_exponent - The public exponent of the new key. Default is 65537.
        2. key_size - How big the key is in bits.
        3. backend - Generates a new RSA private from default_backend(). This implements RSABackend.
        """

        # Generate a pair of keys
        self.rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

        # From the private key derived the public key
        self.rsa_public_key = self.rsa_private_key.public_key()

        print("=== Generated Keys ===")

    def load_keys(self):

        # OBJECTIVE: Collect user's keys if they were already created

        # NOTE: If keys were created, check project's working directory

        try:

            # Open private key PEM file
            with open(self.PRIVATE_FILE_NAME, "rb") as private_file:

                # Save private_file's content to rsa_private_key
                self.rsa_private_key = serialization.load_pem_private_key(
                    private_file.read(),
                    password=None, # <- Password wasn't given upon creation
                    backend=default_backend()
                )

            # Open public key PEM file
            with open(self.PUBLIC_FILE_NAME, "rb") as public_file:

                # Save public_file's content to rsa_public_key
                self.rsa_public_key = serialization.load_pem_public_key(
                    public_file.read(),
                    backend=default_backend()
                )
            print(self.rsa_public_key)
            print("=== Loaded Keys ===")

            return True

        except FileNotFoundError as err:
            
            print("Couldn't find or open file(s), so new keys will be generated!")
            print("Error Message: {}\n".format(err))

            return False

    def write_keys(self):

        # OBJECTIVE: To write the keys in a PEM file

        # Create a PEM file for the private key. The command below will serialize it.
        private_pem_file = self.rsa_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Write the file in binary format
        with open(self.PRIVATE_FILE_NAME, "wb") as private_file:

            # Write private key to file
            private_file.write(private_pem_file)

        # Create a file for the public key. The command below will serialize it
        public_pem_file = self.rsa_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        
        # Write the file in binary format
        with open(self.PUBLIC_FILE_NAME, "wb") as public_file:

            # Write public key to file
            public_file.write(public_pem_file)

        print("=== Wrote Keys ===")

    def sign_block_data(self, block_data):

        # OBJECTIVE: To sign binary data with user's private key

        """
        NOTE:
        A signature requires a specific hash function and padding to use
        PSS is recommended for protocols or applications. 
        PKCS1v15 supports legacy protocols.

        Also, signing and verifying must be done within the same function, or signature will be invalid.
        """

        # Digitally sign a block's data
        self.signature = self.rsa_private_key.sign(
            block_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
                ),
            hashes.SHA256()
        )

        print("=== Signed Data ===")

        # Verify signature by decrypting signed data with signature
        try:
            
            self.rsa_public_key.verify(
                self.signature,
                block_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            print("=== Signature Verified ===")

        except cryptography.exceptions.InvalidSignature as err:

            # Print error message and exit program
            print("Error message: {}".format(err))
            exit()

    def encrypt_data(self, unencrypted_data):

        # OBJECTIVE: To encrypt data before adding it to blockchain

        """
        NOTE:
        Valid paddings for encryption are OAEP and PKCS1v15.
        OAEP is recommended for protocols or applications.
        PKCS1v15 should be used to support legacy protocols.
        """

        # Change unencrypted_data to bytes
        unencrypted_data = self.format_data(unencrypted_data)

        # Encrypt data with user's public key using SHA256
        cipher = self.rsa_public_key.encrypt(
            unencrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        print("=== Encrypted Data ===")

        # Return cipher text
        return cipher

    def decrypt_data(self, cipher):

        # OBJECTIVE: To decrypt data from a block if user has correct private key

        # Decrypt cipher
        plain = self.rsa_private_key.decrypt(
            cipher,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        print("=== Decrypted Data ===")

        # Return decrypted data
        return plain

    def agenda(self, data):

        # OBJECTIVE: Use this function to call other functions

        # Check if keys PEM file already exist
        if self.load_keys() == False:

            # Generate and save keys
            self.generate_keys()
            self.write_keys()

        # Encrypt data
        cipher = self.encrypt_data(data)

        # Sign encrypted data and verify signature
        self.sign_block_data(cipher)

        # Return encrypted data and user's public key
        return cipher, self.rsa_public_key