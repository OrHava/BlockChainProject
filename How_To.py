# website to mine 
# https://cloud.google.com/application/web3/faucet/ethereum/sepolia
# https://faucets.chain.link/sepolia
# https://getblock.io/faucet/eth-sepolia/

# check if send or get worked: https://sepolia.etherscan.io/

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
