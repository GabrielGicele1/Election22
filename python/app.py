
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
    "0xAc52052FB787cc57CDD77E474c6d998910E77F9A"
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

candidate_count = contract.functions.getCandidateCount().call()

for candidate_id in range(candidate_count):
    candidate = contract.functions.candidates(candidate_id).call()

    print("ID:", candidate[0])
    print("Name:", candidate[1])
    print("Votes:", candidate[2])
    print("--------------------")

print("Total candidates:", candidate_count)

print("Total candidates:", candidate_count)


  # MAIN MENU


def show_transaction(receipt):
    print("Transaction Hash:", receipt["transactionHash"].hex())
    print("Block Number:", receipt["blockNumber"])
    print("Transaction Status:", "SUCCESS" if receipt["status"] == 1 else "FAILED")


while True:
    print("\n===== BLOCKCHAIN VOTING SYSTEM =====")
    print("1 - Display candidates")
    print("2 - Add candidate")
    print("3 - Start voting")
    print("4 - Cast a vote")
    print("5 - Display election results")
    print("6 - Check voting status")
    print("7 - End voting")
    print("0 - Exit")

    choice = input("\nChoose an option: ")

    if choice == "0":
        print("Exiting Voting System...")
        break

    elif choice == "1":
        print("\n===== REGISTERED CANDIDATES =====")
        candidate_count = contract.functions.getCandidateCount().call()

        for candidate_id in range(candidate_count):
            candidate = contract.functions.candidates(candidate_id).call()
            print("ID:", candidate[0])
            print("Name:", candidate[1])
            print("Votes:", candidate[2])
            print("--------------------")

        print("Total candidates:", candidate_count)

    elif choice == "2":
        print("\n===== ADD CANDIDATE =====")
        name = input("Enter candidate name: ").strip()

        if not name:
            print("Candidate name cannot be empty.")
        else:
            try:
                tx_hash = contract.functions.addCandidate(name).transact(
                    {"from": owner}
                )
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

                if receipt.status == 1:
                    print("Candidate added successfully!")
                else:
                    print("Failed to add candidate.")

                show_transaction(receipt)

            except Exception as error:
                print("Candidate registration rejected!")
                print("Error:", error)

    elif choice == "3":
        print("\n===== START VOTING =====")

        if contract.functions.votingOpen().call():
            print("Voting is already OPEN.")
        else:
            try:
                tx_hash = contract.functions.startVoting().transact(
                    {"from": owner}
                )
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

                if receipt.status == 1:
                    print("Voting started successfully!")
                else:
                    print("Failed to start voting.")

                show_transaction(receipt)

            except Exception as error:
                print("Failed to start voting!")
                print("Error:", error)

    elif choice == "4":
        print("\n===== CAST A VOTE =====")

        if not contract.functions.votingOpen().call():
            print("Voting is CLOSED. You cannot vote.")
        else:
            candidate_input = input("Enter candidate ID: ")

            if not candidate_input.isdigit():
                print("Invalid candidate ID.")
            else:
                candidate_id = int(candidate_input)
                candidate_count = contract.functions.getCandidateCount().call()

                if candidate_id >= candidate_count:
                    print("Invalid candidate ID.")
                else:
                    accounts = w3.eth.accounts

                    print("\n===== AVAILABLE ACCOUNTS =====")
                    for index, account in enumerate(accounts):
                        print(f"{index} - {account}")

                    account_choice = input("\nChoose voter account: ")

                    if not account_choice.isdigit():
                        print("Invalid account selection.")
                    elif int(account_choice) >= len(accounts):
                        print("Account does not exist.")
                    else:
                        voter = accounts[int(account_choice)]

                        try:
                            if contract.functions.hasVoted(voter).call():
                                print("This account has already voted.")
                            else:
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

                                show_transaction(receipt)

                        except Exception as error:
                            print("Vote rejected!")
                            print("Error:", error)

    elif choice == "5":
        print("\n===== ELECTION RESULTS =====")
        total_votes = 0
        candidate_count = contract.functions.getCandidateCount().call()

        for candidate_id in range(candidate_count):
            candidate = contract.functions.candidates(candidate_id).call()

            print("ID:", candidate[0])
            print("Candidate:", candidate[1])
            print("Votes:", candidate[2])
            print("--------------------")

            total_votes += candidate[2]

        print("Total votes:", total_votes)

  

