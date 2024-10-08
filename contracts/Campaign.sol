// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

contract Campaign {
    address public owner;
    string public title;
    uint public goal;
    uint public totalFunds;
    string public ipfsHash;
    bool public closed;

    mapping(address => uint) public donations;

    event DonationReceived(address indexed donor, uint amount);
    event CampaignClosed();

    constructor(address creator, string memory _title, uint _goal, string memory _ipfsHash) {
        owner = creator;
        title = _title;
        goal = _goal;
        ipfsHash = _ipfsHash;
        closed = false;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the campaign owner can call this");
        _;
    }

    modifier isOpen() {
        require(!closed, "Campaign is closed");
        _;
    }

    function donate() public payable isOpen {
        require(msg.value > 0, "Donation must be greater than zero");
        donations[msg.sender] += msg.value;
        totalFunds += msg.value;
        emit DonationReceived(msg.sender, msg.value);

        if (totalFunds >= goal) {
            closeCampaign();
        }
    }

    function closeCampaign() public onlyOwner isOpen {
        closed = true;
        emit CampaignClosed();
    }

    function withdrawFunds() public onlyOwner {
        require(closed, "Campaign must be closed before withdrawing");
        payable(owner).transfer(address(this).balance);
    }

    function getCampaignDetails() public view returns (string memory, uint, uint, bool, string memory) {
        return (title, goal, totalFunds, closed, ipfsHash);
    }

    function getDonations(address donor) public view returns (uint) {
        return donations[donor];
    }
}
