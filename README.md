# Smart Contract Deployment Guide

## Overview

This guide provides detailed instructions on how to deploy the smart contracts for the Campaign DApp, install necessary dependencies, and extract ABIs from the compiled contracts.

## Prerequisites

Ensure you have the following installed on your machine:

- **Node.js** (LTS version recommended)
- **Python** (version 3.x)
- **Truffle** (`npm install -g truffle`)
- **Ganache** (for local testing, optional)
- **IPFS** (for decentralized storage)

## Project Setup

1. **Clone the Repository**

   Open your terminal and run:

   ```bash
   git clone <your-repo-url>
   cd <your-project-directory>


#  Install Node Modules

## Navigate to your project directory and install the required Node.js packages:

bash
Copy code
npm install
Install Python Libraries

## Create a virtual environment (optional but recommended) and install the required libraries:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install web3 python-dotenv requests aiohttp ttkbootstrap
Extracting ABIs
To extract the ABI from the compiled contract JSON files, follow these steps:

## Ensure you have the extract_abis.js file in your project.

## Run the following command:

bash
Copy code
node extract_abis.js
This will generate Campaign_ABI.json and CampaignFactory_ABI.json files in your project directory.

# Deploying Smart Contracts
## Configure Environment Variables

## Create a .env file in your project root and add the following variables:

Copy code
MNEMONIC="your mnemonic here"
GETBLOCK_API_KEY="your getBlock API key here"
SEPOLIA_URL="https://go.getblock.io/your_api_key_here"
FACTORY_ADDRESS="your_factory_contract_address_here"


# Deploy to Sepolia Network

## Use the Truffle migration command to deploy your contracts:

bash
Copy code
truffle migrate --network sepolia
Make sure your truffle-config.js is properly set up for the Sepolia network.

# Running the Application
## To run the Python GUI application, execute the following command:

bash
Copy code
python campaign_gui.py
Ensure the IPFS daemon is running if you are using IPFS for storage.

# Additional Notes
Make sure to never expose your mnemonic or private keys in public repositories.
Update gas settings and network configurations as needed in your truffle-config.js.
For further enhancements, refer to Truffle and Web3.js documentation.