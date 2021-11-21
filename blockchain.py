import hashlib
import json
from time import time
from typing import Optional

from pydantic import BaseModel


class Block(BaseModel):
    index: int
    timestamp: float
    transactions: list
    proof: int
    previous_hash: Optional[str]


class Blockchain():
    """Blockchain class"""

    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Create the genesis block
        self.new_block(previous_hash="1", proof=1)

    def new_block(self, proof: int, previous_hash: str = None) -> Block:
        """Creates new block in the blockchain

        Args:
            proof (int): The proof given by the Proof of Work algorithm
            previous_hash (str, optional): Hash of previous Block. Defaults to None.

        Returns:
            Block: New Block
        """
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(self.last_block),
        )

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """Creates a new transaction to go into the next mined Block

        Args:
            sender (str): Address of the Sender
            recipient (str): Address of the Recipient
            amount (int): Amount

        Returns:
            int: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        })

        return self.last_block.index + 1

    @staticmethod
    def hash(block: Block) -> str:
        """Creates a SHA-256 hash of a Block

        Args:
            block (Block): block

        Returns:
            str: hash
        """

        block_string = json.dumps(block.dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Block:
        """Get last block

        Returns:
            Block: last block
        """
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        """Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - p is the previous proof, and p' is the new proof

        Args:
            last_proof (int):

        Returns:
            int: proof number
        """
        proof = 0
        while self.is_valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def is_valid_proof(last_proof: int, proof: int) -> bool:
        """Validates the Proof:
        Does hash(last_proof, proof) contain 4 leading zeroes?

        Args:
            last_proof (int): Previous Proof
            proof (int): Current Proof

        Returns:
            bool: True if correct, False if not.
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
