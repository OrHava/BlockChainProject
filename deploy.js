const Web3 = require('web3').default; // or just 'web3' if using ES Modules
const fs = require('fs');

async function main() {
    // Connect to Ganache
    const web3 = new Web3('http://127.0.0.1:8545');
  
    // Get the first account from Ganache to use as the deployer
    const accounts = await web3.eth.getAccounts();
    const deployer = accounts[0];
  
    console.log('Deploying from account:', deployer);
  
    // Load the contract ABI and bytecode
    const abi = JSON.parse(fs.readFileSync('CampaignFactory_ABI.json', 'utf8'));
    const fullContractJson = require('./build/contracts/CampaignFactory.json');
    const bytecode = fullContractJson.bytecode;
  
    console.log('ABI loaded:', abi.length, 'items');
    console.log('Bytecode loaded:', bytecode.substring(0, 64) + '...');
  
    // Validate ABI
    if (!Array.isArray(abi) || abi.length === 0) {
      throw new Error('Invalid ABI: Ensure the ABI is properly defined in your JSON file.');
    }
  
    // Create a contract instance
    const CampaignFactory = new web3.eth.Contract(abi);
  
    // Deploy the contract
    const deployTx = CampaignFactory.deploy({
      data: bytecode,
    });
  
    const gas = await deployTx.estimateGas();
  
    const deployedContract = await deployTx.send({
      from: deployer,
      gas,
    });
  
    console.log('Contract deployed at:', deployedContract.options.address);
    return deployedContract.options.address;
  }

main()
  .then((address) => {
    console.log('Deployment successful. Factory address:', address);
    process.exit(0);
  })
  .catch((error) => {
    console.error('Deployment failed:', error);
    process.exit(1);
  });
