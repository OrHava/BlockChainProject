from web3 import Web3
import tkinter as tk
from tkinter import messagebox
import json

# # Connect to Sepolia Testnet via Infura
# INFURA_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"
# web3 = Web3(Web3.HTTPProvider(INFURA_URL))
# Connect to local Ganache instance
GANACHE_URL = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Check connection
if web3.is_connected():
    print("Connected to Ethereum Sepolia Testnet")
else:
    print("Connection failed")

# # MetaMask Account & Private Key
# account = "YOUR_METAMASK_ACCOUNT"
# private_key = "YOUR_METAMASK_PRIVATE_KEY"


# Use the first account provided by Ganache
account = web3.eth.accounts[0]
# No need for private key when using Ganache's unlocked accounts


# Contract details
contract_address = "0x6329D3B702C0fDeA9B9971FA9055B7E83688F425" #local  > contract address:    0x6329D3B702C0fDeA9B9971FA9055B7E83688F425
with open('CampaignFactory_ABI.json') as f:
    abi = json.load(f)
contract = web3.eth.contract(address=contract_address, abi=abi)

# Create GUI using Tkinter
class CampaignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campaign Donation DApp")

        # Create Campaign UI
        self.title_label = tk.Label(root, text="Campaign Title:")
        self.title_label.grid(row=0, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1)

        self.goal_label = tk.Label(root, text="Goal Amount (ETH):")
        self.goal_label.grid(row=1, column=0)
        self.goal_entry = tk.Entry(root)
        self.goal_entry.grid(row=1, column=1)

        self.create_button = tk.Button(root, text="Create Campaign", command=self.create_campaign)
        self.create_button.grid(row=2, column=1)

        # Donate UI
        self.donate_label = tk.Label(root, text="Campaign Address:")
        self.donate_label.grid(row=3, column=0)
        self.donate_entry = tk.Entry(root)
        self.donate_entry.grid(row=3, column=1)

        self.amount_label = tk.Label(root, text="Amount to Donate (ETH):")
        self.amount_label.grid(row=4, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=4, column=1)

        self.donate_button = tk.Button(root, text="Donate", command=self.donate_to_campaign)
        self.donate_button.grid(row=5, column=1)
    def create_campaign(self):
        title = self.title_entry.get()
        goal = web3.to_wei(float(self.goal_entry.get()), 'ether')
        ipfs_hash = "ipfs://your_ipfs_hash_here"  # Placeholder for IPFS integration

        # Send transaction
        tx_hash = contract.functions.createCampaign(title, goal, ipfs_hash).transact({'from': account})
        messagebox.showinfo("Transaction Sent", f"Tx Hash: {web3.to_hex(tx_hash)}")

    def donate_to_campaign(self):
        campaign_address = self.donate_entry.get()
        amount = web3.to_wei(float(self.amount_entry.get()), 'ether')

        # Send transaction
        tx_hash = contract.functions.donate().transact({'from': account, 'value': amount})
        messagebox.showinfo("Transaction Sent", f"Tx Hash: {web3.to_hex(tx_hash)}")
    # def create_campaign(self):
    #     title = self.title_entry.get()
    #     goal = web3.toWei(float(self.goal_entry.get()), 'ether')
    #     ipfs_hash = "ipfs://your_ipfs_hash_here"  # Placeholder for IPFS integration

    #     # Build transaction
    #     tx = contract.functions.createCampaign(title, goal, ipfs_hash).buildTransaction({
    #         'from': account,
    #         'nonce': web3.eth.getTransactionCount(account),
    #         'gas': 2000000,
    #         'gasPrice': web3.toWei('5', 'gwei')
    #     })

    #     # Sign and send transaction
    #     signed_tx = web3.eth.account.signTransaction(tx, private_key)
    #     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    #     messagebox.showinfo("Transaction Sent", f"Tx Hash: {web3.toHex(tx_hash)}")

    # def donate_to_campaign(self):
    #     campaign_address = self.donate_entry.get()
    #     amount = web3.toWei(float(self.amount_entry.get()), 'ether')

    #     # Build transaction
    #     tx = contract.functions.donate().buildTransaction({
    #         'from': account,
    #         'value': amount,
    #         'nonce': web3.eth.getTransactionCount(account),
    #         'gas': 200000,
    #         'gasPrice': web3.toWei('5', 'gwei')
    #     })

    #     # Sign and send transaction
    #     signed_tx = web3.eth.account.signTransaction(tx, private_key)
    #     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    #     messagebox.showinfo("Transaction Sent", f"Tx Hash: {web3.toHex(tx_hash)}")


root = tk.Tk()
app = CampaignApp(root)
root.mainloop()





# website to mine 
# https://cloud.google.com/application/web3/faucet/ethereum/sepolia
# https://faucets.chain.link/sepolia
# https://getblock.io/faucet/eth-sepolia/

# commands: ganache in one node and in other node: truffle compile -> truffle migrate -> take  > contract address:    0x7e1755897E15d3A83BE6696E7C482bF23aA1E6
# commands:   node extract_abis.js  

#PS C:\Users\or656\BlockChainProject> ipfs config Addresses.Gateway /ip4/127.0.0.1/tcp/8081
# do this in windows powershell:  ipfs daemon



###  truffle migrate --network sepolia  /// in one terminal truffle dashboard  and truffle migrate --network dashboard


#  truffle migrate --network dashboard

# Compiling your contracts...
# ===========================
# > Compiling .\contracts\Campaign.sol
# > Compiling .\contracts\CampaignFactory.sol
# > Artifacts written to C:\Users\or656\BlockChainProject\build\contracts
# > Compiled successfully using:
#    - solc: 0.8.23+commit.f704f362.Emscripten.clang


# Starting migrations...
# ======================
# > Network name:    'dashboard'
# > Network id:      11155111
# > Block gas limit: 30000000 (0x1c9c380)


# 2_deploy_contracts.js
# =====================

#    Deploying 'CampaignFactory'
#    ---------------------------
#    > transaction hash:    0x2cb02ed00e1da0fc075e7943dc5acf3c75da1224459d95cd1897f39eefbd406esage.
#    > Blocks: 1            Seconds: 28
#    > contract address:    0x7a3FC66639bd928F2da3aB66cBb6ffd85B1EAe98
#    > block number:        6750854
#    > block timestamp:     1727177928
#    > account:             0x1e55dC69F540784698Bf43fAA8c0De77A05aaeBc
#    > balance:             2.431719958384778432
#    > gas used:            1056078 (0x101d4e)
#    > gas price:           40.855848456 gwei
#    > value sent:          0 ETH
#    > total cost:          0.043146962725715568 ETH


#    Deploying 'ProxyAdmin'
#    ----------------------
#    > transaction hash:    0x0781d97cc311a66a1ff5b0e679a3f6845bccdb603e7e4ee41da1ea885b0a4727sage.
#    > Blocks: 2            Seconds: 56
#    > contract address:    0xF7Bfae7bA6f78DEC0C2a5C559F718DC7eCC50a4b
#    > block number:        6750857
#    > block timestamp:     1727177988
#    > account:             0x1e55dC69F540784698Bf43fAA8c0De77A05aaeBc
#    > balance:             2.413891136908265462
#    > gas used:            443289 (0x6c399)
#    > gas price:           40.21940873 gwei
#    > value sent:          0 ETH
#    > total cost:          0.01782882147651297 ETH


#    Deploying 'TransparentUpgradeableProxy'
#    ---------------------------------------
#    > transaction hash:    0xf2e0cd51e9a6b0f60250b8229aebe0311c4f59fe09f22a642219402b9b7d3fb6sage.
#    > Blocks: 1            Seconds: 20
#    > contract address:    0x6738B87F817917AEe4FF8c73CbE1410e4079C7AB
#    > block number:        6750859
#    > block timestamp:     1727178012
#    > account:             0x1e55dC69F540784698Bf43fAA8c0De77A05aaeBc
#    > balance:             2.384347348776757502
#    > gas used:            609530 (0x94cfa)
#    > gas price:           48.469785132 gwei
#    > value sent:          0 ETH
#    > total cost:          0.02954378813150796 ETH

#    > Saving artifacts
#    -------------------------------------
#    > Total cost:     0.090519572333736498 ETH

# Summary
# =======
# > Total deployments:   3
# > Final cost:          0.090519572333736498 ETH
