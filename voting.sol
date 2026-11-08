
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Voting {

    address public owner;

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    Candidate[] public candidates;

    mapping(address => bool) public hasVoted;

    bool public votingOpen;

    constructor() {
        owner = msg.sender;
        votingOpen = false;
    }

    function addCandidate(string memory _name) public {
        require(msg.sender == owner, "Only the owner can add candidates");

        uint id = candidates.length;
        candidates.push(Candidate(id, _name, 0));
    }

    function vote(uint _candidateId) public {
        require(votingOpen, "Voting is closed");
        require(!hasVoted[msg.sender], "You have already voted");
        require(_candidateId < candidates.length, "Invalid candidate ID");

        hasVoted[msg.sender] = true;
        candidates[_candidateId].voteCount++;
    }

    function startVoting() public {
        require(msg.sender == owner, "Only the owner can start voting");

        votingOpen = true;
    }

    function endVoting() public {
        require(msg.sender == owner, "Only the owner can end voting");

        votingOpen = false;
    }

    function getCandidateCount() public view returns (uint) {
        return candidates.length;
    }
}
