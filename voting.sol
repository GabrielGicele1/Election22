
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Voting {

    // Address of the contract administrator
    address public owner;

    // Candidate information
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    // Store candidates
    Candidate[] public candidates;

    // Track addresses that have voted
    mapping(address => bool) public hasVoted;

    // Voting status
    bool public votingOpen;

    // Set the administrator when deployed
    constructor() {
        owner = msg.sender;
        votingOpen = false;
    }

    // Add a new candidate (only owner)
    function addCandidate(string memory _name) public {
        require(
            msg.sender == owner,
            "Only the owner can add candidates"
        );

        uint id = candidates.length;
        candidates.push(Candidate(id, _name, 0));
    }

    // Start voting (only owner)
    function startVoting() public {
        require(
            msg.sender == owner,
            "Only the owner can start voting"
        );

        votingOpen = true;
    }

    function endVoting() public {
    require(msg.sender == owner, "Only the owner can end voting");
    votingOpen = false;
}

    // Allow users to vote
    function vote(uint _candidateId) public {

        // Check if voting is open
        require(votingOpen, "Voting is closed");

        // Check if voter has already voted
        require(
            !hasVoted[msg.sender],
            "You have already voted"
        );

        // Check if candidate exists
        require(
            _candidateId < candidates.length,
            "Invalid candidate ID"
        );

        // Mark voter as having voted
        hasVoted[msg.sender] = true;

        // Increase candidate's vote count
        candidates[_candidateId].voteCount++;
    }
}

