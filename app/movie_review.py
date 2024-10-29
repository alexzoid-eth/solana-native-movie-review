from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction as TransactionInstruction
from solders.system_program import ID as SystemProgramID
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.transaction import Transaction, AccountMeta
from solana.rpc.types import TxOpts
from borsh_construct import U8, String, CStruct
import asyncio
import json
import os

# Program ID for the movie review program
PROGRAM_ID = Pubkey.from_string("9t4MNpDCv1PUNKD5P4b8ymfXk539TjfxpchJiHUbp6Ki")

# Define the instruction layout using borsh_construct
REVIEW_INSTRUCTION_LAYOUT = CStruct(
    "variant" / U8,
    "title" / String,
    "rating" / U8,
    "description" / String,
)

# Account size calculation
ACCOUNT_SIZE = 1000

def serialize_movie_instruction(variant: int, title: str, rating: int, description: str) -> bytes:
    """Serializes the instruction data using Borsh serialization."""
    return REVIEW_INSTRUCTION_LAYOUT.build({
        "variant": variant,
        "title": title,
        "rating": rating,
        "description": description
    })

async def add_movie_review():
    # Connect to devnet
    client = AsyncClient("https://api.devnet.solana.com")
    
    # Load private key from JSON file
    keypair_path = os.path.join(os.path.dirname(__file__), "../../wallet-keypair.json")
    
    try:
        with open(keypair_path, 'r') as f:
            keypair_data = json.load(f)
            keypair = Keypair.from_bytes(bytes(keypair_data))
    except FileNotFoundError:
        print(f"Please ensure {keypair_path} exists with your keypair data")
        return
    except json.JSONDecodeError:
        print(f"Error reading JSON from {keypair_path}")
        return
    
    # Movie review details - matching TypeScript example
    title = "movie3"
    rating = 5
    description = "A great movie"
    
    # Find review PDA - matching the TypeScript implementation
    review_pda_seeds = [bytes(keypair.pubkey()), bytes(title, 'utf-8')]
    review_pda, review_bump = Pubkey.find_program_address(review_pda_seeds, PROGRAM_ID)
    
    print(f"Reviewer: {keypair.pubkey()}")
    print(f"Review PDA: {review_pda}")
    
    # Get minimum balance for rent exemption
    rent_exemption = await client.get_minimum_balance_for_rent_exemption(ACCOUNT_SIZE)
    print(f"Rent exemption: {rent_exemption} lamports")
    
    # Create instruction data
    instruction_data = serialize_movie_instruction(0, title, rating, description)
    
    try:
        # Get recent blockhash
        recent_blockhash = await client.get_latest_blockhash()
        
        # Create transaction
        transaction = Transaction()
        transaction.recent_blockhash = recent_blockhash.value.blockhash
        transaction.fee_payer = keypair.pubkey()
        
        # Create the instruction matching TypeScript accounts exactly
        instruction = TransactionInstruction(
            program_id=PROGRAM_ID,
            accounts=[
                AccountMeta(pubkey=keypair.pubkey(), is_signer=True, is_writable=False),
                AccountMeta(pubkey=review_pda, is_signer=False, is_writable=True),
                AccountMeta(pubkey=SystemProgramID, is_signer=False, is_writable=False),
            ],
            data=instruction_data
        )
        
        transaction.add(instruction)
        
        # Sign and send transaction
        transaction.sign(keypair)
        serialized_tx = transaction.serialize()
        
        tx_opts = TxOpts(preflight_commitment=Confirmed)
        signature = await client.send_raw_transaction(serialized_tx, opts=tx_opts)
        
        print(f"Transaction sent! Signature: {signature.value}")
        print(f"View transaction: https://explorer.solana.com/tx/{signature.value}?cluster=devnet")
        
        # Wait for confirmation
        await client.confirm_transaction(signature.value, commitment=Confirmed)
        print("Transaction confirmed!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        
    await client.close()

if __name__ == "__main__":
    asyncio.run(add_movie_review())