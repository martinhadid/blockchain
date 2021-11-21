from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel

from blockchain import Blockchain

app = FastAPI(title="Blockchain with FastApi")

blockchain = Blockchain()
node_identifier = str(uuid4()).replace("-", "")


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: int


class Response(BaseModel):
    message: Optional[str]
    new_chain: Optional[List[dict]]
    total_nodes: Optional[list]
    chain: Optional[List[dict]]
    length: Optional[int]
    index: Optional[int]
    transactions: Optional[List[dict]]
    proof: Optional[int]
    previous_hash: Optional[str]


@app.get("/chain/", status_code=200, response_model=Response, response_model_exclude_unset=True)
async def get_blockchain() -> dict:
    """Gives users the full Blockchain.

    Returns:
        dict: chains, length of list
    """
    return {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }


@app.post("/transactions/new/", status_code=201, response_model=Response, response_model_exclude_unset=True)
async def new_transaction(payload: Transaction) -> dict:
    """
    Creates a new transaction to a block

    Args:
        values (Transaction): new transaction to be created

    Returns:
        dict: Response message
    """
    index = blockchain.new_transaction(
        sender=payload.sender,
        recipient=payload.recipient,
        amount=payload.amount
    )
    return {
        "message": f"Transaction will be added to Block {index}"
    }


@app.get("/mine/", status_code=200, response_model=Response, response_model_exclude_unset=True)
async def mine() -> dict:
    """
    Mine a new block

    Returns:
        dict: message, index, transaction, proof, previous hash
    """
    # Run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    # Receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    return {
        "message": "New Block Forged",
        "index": block.index,
        "transactions": block.transactions,
        "proof": block.proof,
        "previous_hash": block.previous_hash,
    }
