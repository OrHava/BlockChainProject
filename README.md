# Smart Contract Deployment Guide

## Smart Contract Overview

This project includes a smart contract for managing crowdfunding campaigns. The `Campaign` contract allows:

- Creation of a campaign with a title, funding goal, and IPFS hash for additional details
- Donations from supporters
- Automatic closure when the funding goal is reached
- Manual closure by the campaign owner
- Withdrawal of funds by the owner after campaign closure
- Tracking of individual donations and total funds raised
- Retrieval of campaign details and donation information

Key features:
- Ownership control
- Goal-based auto-closure
- IPFS integration for decentralized data storage
- Event emission for donations and campaign closure

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Extracting ABIs](#extracting-abis)
- [Deploying Smart Contracts](#deploying-smart-contracts)
- [Running the Application](#running-the-application)
- [Additional Notes](#additional-notes)

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

### 1. Clone the Repository

Open your terminal and run:

```bash
git clone <your-repo-url>
cd <your-project-directory>
```

### 2. Install Node Modules

Navigate to your project directory and install the required Node.js packages:

```bash
npm install
```

### 3. Install Python Libraries

Create a virtual environment (optional but recommended) and install the required libraries:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install web3 python-dotenv requests aiohttp ttkbootstrap
```

## Extracting ABIs

To extract the ABI from the compiled contract JSON files:

1. Ensure you have the `extract_abis.js` file in your project.
2. Run the following command:

```bash
node extract_abis.js
```

This will generate `Campaign_ABI.json` and `CampaignFactory_ABI.json` files in your project directory.

## Deploying Smart Contracts

### Configure Environment Variables

Create a `.env` file in your project root and add the following variables:

```
MNEMONIC="your mnemonic here"
GETBLOCK_API_KEY="your getBlock API key here"
SEPOLIA_URL="https://go.getblock.io/your_api_key_here"
FACTORY_ADDRESS="your_factory_contract_address_here"
PRIVATE_KEY="your_PRIVATE_KEY_here""
```

### Deploy to Sepolia Network

Use the Truffle migration command to deploy your contracts:

```bash
truffle migrate --network sepolia
or
truffle migrate --network dashboard
```

Make sure your `truffle-config.js` is properly set up for the Sepolia network.

## Running the Application

To run the Python GUI application, execute the following command:

```bash
python campaign_gui.py
```

Ensure the IPFS daemon is running if you are using IPFS for storage.

## Additional Notes

- 🔒 Never expose your mnemonic or private keys in public repositories.
- ⚙️ Update gas settings and network configurations as needed in your `truffle-config.js`.
- 📚 For further enhancements, refer to [Truffle](https://trufflesuite.com/docs/) and [Web3.js](https://web3js.readthedocs.io/) documentation.

---

For any issues or questions, please open an issue in the repository or contact the maintainer.

## UI Pics


Happy coding! 🚀