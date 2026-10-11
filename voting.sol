
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
 }
