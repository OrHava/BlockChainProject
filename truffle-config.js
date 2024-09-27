require('dotenv').config(); // Load environment variables from .env file
const HDWalletProvider = require('@truffle/hdwallet-provider');
const mnemonic = process.env.MNEMONIC; // Access mnemonic from environment variable
const getBlockApiKey = process.env.GETBLOCK_API_KEY; // Access API key from environment variable

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",     // Localhost
      port: 8545,            // Standard Ethereum port
      network_id: "*",       // Any network (default: none)
    },
    sepolia: {
      provider: () => new HDWalletProvider(mnemonic, `https://go.getblock.io/${getBlockApiKey}`),
      network_id: 11155111,  // Sepolia network ID
      gas: 5000000,          // Gas limit for Sepolia
      gasPrice: 2500000000,  // 1 Gwei gas price (adjust as needed)
      confirmations: 1,      // Wait for 1 block confirmation
      timeoutBlocks: 500,    // Number of blocks before timing out deployment
      skipDryRun: true,      // Skip dry run before migrations
      networkCheckTimeout: 1000000, // Increase the network timeout for Sepolia
    },
  },
  compilers: {
    solc: {
      version: "0.8.23",     // Solidity compiler version
      settings: {
        optimizer: {
          enabled: true,
          runs: 2000,       // Optimize for maximum performance
        },
        evmVersion: "paris" // Target the 'paris' hard fork (Ethereum's latest version)
      }
    }
  }
};


