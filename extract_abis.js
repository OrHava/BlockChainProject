const fs = require('fs');
const path = require('path');

function extractABI(contractName) {
    const buildPath = path.join(__dirname, 'build', 'contracts', `${contractName}.json`);
    const outputPath = path.join(__dirname, `${contractName}_ABI.json`);

    try {
        const contractJson = require(buildPath);
        fs.writeFileSync(outputPath, JSON.stringify(contractJson.abi, null, 2));
        console.log(`ABI extracted to ${outputPath}`);
    } catch (error) {
        console.error(`Error extracting ABI for ${contractName}:`, error.message);
    }
}

// Extract ABI for CampaignFactory
extractABI('CampaignFactory');

// Extract ABI for Campaign
extractABI('Campaign');


//node extract_abis.js