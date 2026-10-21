import json
from pathlib import Path
from web3 import Web3

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    raise ConnectionError("Failed to connect to Ganache")

print("Connected to Ganache!")
print("Chain ID:", w3.eth.chain_id)

# Load contract ABI
abi_path = Path(__file__).parent / "VotingABI.json"

with open(abi_path, "r", encoding="utf-8") as file:
    abi = json.load(file)

# Connect to the deployed Voting contract
contract_address = Web3.to_checksum_address(
    "0xa4f459e55c4a177890B9E224512DAC26F07b6E13"
)

contract = w3.eth.contract(address=contract_address, abi=abi)

# Read the contract owner
owner = contract.functions.owner().call()

print("Contract owner:", owner)

# Check voting status
voting_status = contract.functions.votingOpen().call()

if voting_status:
    print("Voting status: OPEN")
else:
    print("Voting status: CLOSED")

    # Display registered candidates
print("\nRegistered candidates:")

candidate_id = 0

while True:
    try:
        candidate = contract.functions.candidates(candidate_id).call()

        print("ID:", candidate[0])
        print("Name:", candidate[1])
        print("Votes:", candidate[2])
        print("--------------------")

        candidate_id += 1

    except Exception:
        break

print("Total candidates:", candidate_id)

# Get the administrator account
#admin = w3.eth.accounts[0]

# Add a new candidate
#tx_hash = contract.functions.addCandidate("Gabriel").transact({
 #   "from": admin
#})

# Wait for transaction confirmation
#receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#print("Transaction status:", receipt.status)
#print("Candidate added successfully!")

