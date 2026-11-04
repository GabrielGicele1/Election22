
import json
from pathlib import Path
from web3 import Web3

# Connect to Ganache
ganache_url = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if not w3.is_connected():
    raise ConnectionError("Failed to connect to Ganache")

print("Connected to Ganache!")
print("Chain ID:", w3.eth.chain_id)

# Load contract ABI
abi_path = Path(__file__).parent / "votingABI.json"

with open(abi_path, "r", encoding="utf-8") as file:
    abi = json.load(file)

# Contract address
contract_address = Web3.to_checksum_address(
    "0x96241FB84f4b40A738aD0bcD1713973ff59F241c"
)

# Connect to the Voting contract
contract = w3.eth.contract(
    address=contract_address,
    abi=abi
)

# Check contract deployment
print("Connected RPC:", ganache_url)
print("Contract address:", contract_address)
print("Latest block:", w3.eth.block_number)

contract_code = w3.eth.get_code(contract_address)
print("Contract exists:", len(contract_code) > 0)

if len(contract_code) == 0:
    raise RuntimeError("Contract not found on Ganache")

# Get contract owner
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



# REGISTER CANDIDATES 


# admin = w3.eth.accounts[0]

# tx_hash = contract.functions.addCandidate("Gabriel").transact({
#     "from": admin
# })
# receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print("Transaction status:", receipt.status)

# tx_hash = contract.functions.addCandidate("Lula").transact({
#     "from": admin
# })
# receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print("Transaction status:", receipt.status)



# START VOTING 


# admin = w3.eth.accounts[0]

# tx_hash = contract.functions.startVoting().transact({
#     "from": admin
# })
# receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print("Start voting transaction status:", receipt.status)



# VOTE FOR GABRIEL 


# voter = w3.eth.accounts[1]

# tx_hash = contract.functions.vote(0).transact({
#     "from": voter
# })
# receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print("Vote transaction status:", receipt.status)

# TEST: Prevent duplicate voting

#voter = w3.eth.accounts[1]

#try:
 #   tx_hash = contract.functions.vote(1).transact({
  #      "from": voter
   # })

   # receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print("Transaction status:", receipt.status)

#except Exception as error:
 #   print("Duplicate vote rejected!")
  #  print("Error:", error)

  # TEST: Vote using a different account

# voter2 = w3.eth.accounts[2]

# tx_hash = contract.functions.vote(1).transact({
#     "from": voter2
# })

# receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# print("Second vote transaction status:", receipt.status)

# TEST: End voting

# admin = w3.eth.accounts[0]

# tx_hash = contract.functions.endVoting().transact({
#    "from": admin
# })

# receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# print("End voting transaction status:", receipt.status)

# TEST: Prevent voting after election is closed

#voter3 = w3.eth.accounts[3]

#try:
 #   tx_hash = contract.functions.vote(0).transact({
  #      "from": voter3
   # })

    #receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print("Transaction status:", receipt.status)

#except Exception as error:
 #   print("Vote rejected: Election is closed!")
  #  print("Error:", error)

  # MAIN MENU



# ==========================================
# MAIN MENU
# ==========================================

while True:
    print("\n===== BLOCKCHAIN VOTING SYSTEM =====")
    print("1 - Display candidates")
    print("2 - Check voting status")
    print("3 - Cast a vote")
    print("4 - Display election results")
    print("0 - Exit")

    choice = input("\nChoose an option: ")

    if choice == "0":
        print("Exiting Voting System...")
        break

    elif choice == "1":
        print("\n===== REGISTERED CANDIDATES =====")

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

    elif choice == "2":
        voting_status = contract.functions.votingOpen().call()

        print("\n===== VOTING STATUS =====")

        if voting_status:
            print("Voting is OPEN")
        else:
            print("Voting is CLOSED")

    elif choice == "3":
        print("\n===== CAST A VOTE =====")

        voting_status = contract.functions.votingOpen().call()

        if not voting_status:
            print("Voting is CLOSED. You cannot vote.")

        else:
            print("Voting is OPEN.")

            candidate_id = input("Enter candidate ID: ")

            if not candidate_id.isdigit():
                print("Invalid candidate ID.")

            else:
                candidate_id = int(candidate_id)

                voter = w3.eth.accounts[3]

                try:
                    tx_hash = contract.functions.vote(
                        candidate_id
                    ).transact({"from": voter})

                    receipt = w3.eth.wait_for_transaction_receipt(
                        tx_hash
                    )

                    if receipt.status == 1:
                        print("Vote registered successfully!")
                    else:
                        print("Vote transaction failed.")

                except Exception as error:
                    print("Vote rejected!")
                    print("Error:", error)

    elif choice == "4":
        print("Displaying election results...")

    else:
        print("Invalid option. Please try again.")
