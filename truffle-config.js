const HDWalletProvider = require('@truffle/hdwallet-provider');
const mnemonic = "sport venue say series language genre shy bullet obey spell artwork damp"; // Your mnemonic
const getBlockApiKey = "d35b76ef5d0446cdbaff801450af08d2"; // Replace with your actual GetBlock API key

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




// const HDWalletProvider = require('@truffle/hdwallet-provider');
// const infuraKey = "30da3c915e4b4e909160dd295610c8fa"; // Your Infura Project ID
// const mnemonic = "sport venue say series language genre shy bullet obey spell artwork damp"; // Your mnemonic

// module.exports = {
//   networks: {
//     sepolia: {
//       provider: () => new HDWalletProvider(mnemonic, `https://sepolia.infura.io/v3/${infuraKey}`),
//       network_id: 11155111,  // Sepolia network ID
//       gas: 10000000,         // Increase gas limit to 10,000,000
//       gasPrice: 1000000000,  // 1 gwei gas price
//       confirmations: 2,      // Number of confirmations to wait between deployments
//       timeoutBlocks: 200,    // Timeout duration for deployment
//       skipDryRun: true       // Skip dry run before migrations
//     },
//   },
//   compilers: {
//     solc: {
//       version: "0.8.21",      // Solidity compiler version
//       settings: {
//         optimizer: {
//           enabled: true,
//           runs: 1000           // Optimizer settings
//         },
//         evmVersion: "paris"    // Compatible EVM version for Sepolia
//       }
//     }
//   }
// };
