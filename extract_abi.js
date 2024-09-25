const fs = require('fs');
const path = require('path');

const contractName = 'CampaignFactory'; // Replace with your contract name
const buildPath = path.join(__dirname, 'build', 'contracts', `${contractName}.json`);
const outputPath = path.join(__dirname, `${contractName}_ABI.json`);

const contractJson = require(buildPath);
fs.writeFileSync(outputPath, JSON.stringify(contractJson.abi, null, 2));

console.log(`ABI extracted to ${outputPath}`);