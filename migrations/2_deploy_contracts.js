const { deployProxy } = require('@openzeppelin/truffle-upgrades');
const CampaignFactory = artifacts.require('CampaignFactory');

module.exports = async function (deployer) {
  // Deploy the CampaignFactory contract as an upgradeable proxy
  await deployProxy(CampaignFactory, [], { deployer });
};
