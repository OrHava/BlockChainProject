// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "./Campaign.sol";

contract CampaignFactory {
    Campaign[] public campaigns;
    
    event CampaignCreated(address campaignAddress, address creator, string title, uint goal, string ipfsHash);

    function createCampaign(string memory _title, uint _goal, string memory _ipfsHash) public {
        Campaign newCampaign = new Campaign(msg.sender, _title, _goal, _ipfsHash);
        campaigns.push(newCampaign);
        emit CampaignCreated(address(newCampaign), msg.sender, _title, _goal, _ipfsHash);
    }

    function getCampaignCount() public view returns (uint) {
        return campaigns.length;
    }

    function getCampaigns() public view returns (Campaign[] memory) {
        return campaigns;
    }
}