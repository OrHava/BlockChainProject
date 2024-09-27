import random
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from web3 import Web3
import webbrowser
import json
import sys
import requests
from web3.gas_strategies.time_based import medium_gas_price_strategy
import asyncio
from web3.exceptions import TransactionNotFound, TimeExhausted
from web3.exceptions import ContractLogicError
from eth_account import Account
import threading
import aiohttp



from ttkbootstrap import Style
from PIL import Image, ImageTk
import sv_ttk

class CampaignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campaign Donation DApp")
        self.root.geometry("1400x800")
        self.root.configure(bg="#e8eaf6")  # Light modern background
      
        # Use modern fonts
        self.default_font = ('Arial', 12)
        self.header_font = ('Arial', 16, 'bold')
        self.button_font = ('Arial', 12, 'bold')

        self.ipfs_api = 'http://127.0.0.1:5001/api/v0'
        self.ipfs_hash = None
        self.setup_ipfs()

        self.setup_web3()
        self.setup_ui()
        self.load_campaigns()
        self.start_asyncio_event_loop()

    def setup_ipfs(self):
        try:
            response = requests.post(f'{self.ipfs_api}/version')
            if response.status_code == 200:
                print(f"Connected to IPFS version: {response.json()['Version']}")
            else:
                raise Exception(f"Failed to connect to IPFS: HTTP {response.status_code}")
        except Exception as e:
            print(f"Failed to connect to IPFS: {str(e)}", file=sys.stderr)
            messagebox.showerror("IPFS Error", "Failed to connect to IPFS. Make sure your IPFS daemon is running.")

     # for local       
     #    LOCAL_GANACHE_URL = "http://127.0.0.1:8545"
    #    self.web3 = Web3(Web3.HTTPProvider(LOCAL_GANACHE_URL))
    
    #    if not self.web3.is_connected():
    #        error_msg = "Failed to connect to the local blockchain (Ganache)"
    #        print(error_msg, file=sys.stderr)
    #        messagebox.showerror("Connection Error", error_msg)
    #        self.root.quit()
    #        return

    #    print("Connected to local Ganache blockchain")

    #    # Use the first account from Ganache
    #    self.account = self.web3.eth.accounts[0]
    #    factory_address = "0xd173e6074883Cd27a3AF3e6D5096E856B17e0004"
       
    def setup_web3(self):
   
       SEPOLIA_URL = "https://go.getblock.io/d35b76ef5d0446cdbaff801450af08d2"
       self.web3 = Web3(Web3.HTTPProvider(SEPOLIA_URL))
    
       if not self.web3.is_connected():
           error_msg = "Failed to connect to the Sepolia testnet"
           print(error_msg, file=sys.stderr)
           messagebox.showerror("Connection Error", error_msg)
           self.root.quit()
           return

       print("Connected to Sepolia testnet")

       self.private_key = "0x22d18bc60d6d4a077bc61eb90372b90ac56dc7029d33874ad26faed96adfc6d2"
       self.account = Account.from_key(self.private_key)
       self.account_address = self.account.address
       print(f"Account address: {self.account_address}")

       factory_address = "0x6738B87F817917AEe4FF8c73CbE1410e4079C7AB"
       try:
           with open('CampaignFactory_ABI.json') as f:
               factory_abi = json.load(f)
           self.factory_contract = self.web3.eth.contract(address=factory_address, abi=factory_abi)
       except Exception as e:
           error_msg = f"Failed to load CampaignFactory ABI: {str(e)}"
           print(error_msg, file=sys.stderr)
           messagebox.showerror("Error", error_msg)
           self.root.quit()

       try:
           with open('Campaign_ABI.json') as f:
               self.campaign_abi = json.load(f)
       except Exception as e:
           error_msg = f"Failed to load Campaign ABI: {str(e)}"
           print(error_msg, file=sys.stderr)
           messagebox.showerror("Error", error_msg)
           self.root.quit()

    def setup_ui(self):
        # Use ttkbootstrap for a modern look
        style = Style(theme="darkly")
        
        # Enable Sun Valley theme for a modern Windows 11 look
        sv_ttk.set_theme("dark")

        self.root.configure(bg="#1e1e1e")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

        self.create_tab = ttk.Frame(self.notebook)
        self.list_tab = ttk.Frame(self.notebook)
        self.donate_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.create_tab, text="Create Campaign")
        self.notebook.add(self.list_tab, text="Campaign List")
        self.notebook.add(self.donate_tab, text="Donate")

        self.setup_create_tab()
        self.setup_list_tab()
        self.setup_donate_tab()

        # Add a cool background
        self.add_animated_background()

    def add_animated_background(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Instead of lower(), use lift() on other widgets to bring them to the front
        for child in self.root.winfo_children():
            if child != self.canvas:
                child.lift()

        self.particles = []
        for _ in range(50):
            x = random.randint(0, self.root.winfo_width())
            y = random.randint(0, self.root.winfo_height())
            r = random.randint(1, 3)
            dx = random.uniform(-0.5, 0.5)
            dy = random.uniform(-0.5, 0.5)
            color = random.choice(['#FFD700', '#87CEEB', '#98FB98'])  # Gold, Sky Blue, Pale Green
            particle = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline='')
            self.particles.append((particle, dx, dy))
        
        self.animate_particles()

    def animate_particles(self):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        for i, (particle, dx, dy) in enumerate(self.particles):
            x1, y1, x2, y2 = self.canvas.coords(particle)
            
            # Bounce off edges
            if x2 > w or x1 < 0:
                dx = -dx
            if y2 > h or y1 < 0:
                dy = -dy
            
            # Move particle
            self.canvas.move(particle, dx, dy)
            
            # Fade effect
            current_color = self.canvas.itemcget(particle, 'fill')
            r, g, b = self.root.winfo_rgb(current_color)
            r, g, b = r//256, g//256, b//256
            r = max(0, r - 1)
            g = max(0, g - 1)
            b = max(0, b - 1)
            new_color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.itemconfig(particle, fill=new_color)
            
            # Respawn particle if it's too faded
            if r + g + b < 30:
                x = random.randint(0, w)
                y = random.randint(0, h)
                r = random.randint(1, 3)
                color = random.choice(['#FFD700', '#87CEEB', '#98FB98'])
                self.canvas.coords(particle, x-r, y-r, x+r, y+r)
                self.canvas.itemconfig(particle, fill=color)
            
            self.particles[i] = (particle, dx, dy)
        
        self.root.after(50, self.animate_particles)

    def setup_create_tab(self):
        frame = ttk.Frame(self.create_tab, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Create a New Campaign", font=("Segoe UI", 24, "bold")).pack(pady=20)

        form_frame = ttk.Frame(frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Campaign Title:", font=("Segoe UI", 12)).pack(anchor=tk.W, pady=(10, 5))
        self.title_entry = ttk.Entry(form_frame, width=50, font=("Segoe UI", 12))
        self.title_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Goal Amount (ETH):", font=("Segoe UI", 12)).pack(anchor=tk.W, pady=(10, 5))
        self.goal_entry = ttk.Entry(form_frame, width=50, font=("Segoe UI", 12))
        self.goal_entry.pack(fill=tk.X, pady=(0, 10))

        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)

        create_button = ttk.Button(button_frame, text="Create Campaign", command=self.create_campaign, style="Accent.TButton")
        create_button.pack(side=tk.LEFT, padx=10)

        upload_button = ttk.Button(button_frame, text="Upload File", command=self.upload_file, style="Accent.TButton")
        upload_button.pack(side=tk.LEFT, padx=10)

        self.file_label = ttk.Label(form_frame, text="No file selected", font=("Segoe UI", 10))
        self.file_label.pack(pady=10)

    def setup_list_tab(self):
        frame = ttk.Frame(self.list_tab, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Campaign List", font=("Segoe UI", 24, "bold")).pack(pady=20)

        self.campaign_list = ttk.Treeview(frame, columns=('Title', 'Goal', 'Balance', 'Status', 'Address', 'IPFS Hash'), show='headings', style="Accent.Treeview")
        self.campaign_list.heading('Title', text='Campaign Title')
        self.campaign_list.heading('Goal', text='Goal (ETH)')
        self.campaign_list.heading('Balance', text='Current Balance (ETH)')
        self.campaign_list.heading('Status', text='Status')
        self.campaign_list.heading('Address', text='Campaign Address')
        self.campaign_list.heading('IPFS Hash', text='IPFS Hash')

        self.campaign_list.column('Title', width=150)
        self.campaign_list.column('Goal', width=100)
        self.campaign_list.column('Balance', width=100)
        self.campaign_list.column('Status', width=70)
        self.campaign_list.column('Address', width=300)
        self.campaign_list.column('IPFS Hash', width=150)

        self.campaign_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.campaign_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.campaign_list.configure(yscrollcommand=scrollbar.set)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=20)

        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.load_campaigns, style="Accent.TButton")
        refresh_button.pack(side=tk.LEFT, padx=10)

        donate_button = ttk.Button(button_frame, text="Donate to Selected", command=self.donate_to_selected, style="Accent.TButton")
        donate_button.pack(side=tk.LEFT, padx=10)

        view_button = ttk.Button(button_frame, text="View File", command=self.view_file, style="Accent.TButton")
        view_button.pack(side=tk.LEFT, padx=10)

        self.campaign_list.bind('<<TreeviewSelect>>', self.on_campaign_select)

    def setup_donate_tab(self):
        frame = ttk.Frame(self.donate_tab, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Donate to a Campaign", font=("Segoe UI", 24, "bold")).pack(pady=20)

        form_frame = ttk.Frame(frame)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Campaign Address:", font=("Segoe UI", 12)).pack(anchor=tk.W, pady=(10, 5))
        self.donate_entry = ttk.Entry(form_frame, width=50, font=("Segoe UI", 12))
        self.donate_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Amount to Donate (ETH):", font=("Segoe UI", 12)).pack(anchor=tk.W, pady=(10, 5))
        self.amount_entry = ttk.Entry(form_frame, width=50, font=("Segoe UI", 12))
        self.amount_entry.pack(fill=tk.X, pady=(0, 10))

        donate_button = ttk.Button(form_frame, text="Donate", command=self.handle_donate_button, style="Accent.TButton")
        donate_button.pack(pady=20)


    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    files = {'file': file}
                    response = requests.post(f'{self.ipfs_api}/add', files=files)
                    if response.status_code == 200:
                        result = response.json()
                        self.ipfs_hash = result['Hash']
                        file_name = file_path.split('/')[-1]
                        self.file_label.config(text=f"File uploaded: {file_name}")
                        print(f"File uploaded to IPFS with hash: {self.ipfs_hash}")
                    else:
                        raise Exception(f"Failed to upload file: HTTP {response.status_code}")
            except Exception as e:
                error_msg = f"Failed to upload file: {str(e)}"
                print(error_msg, file=sys.stderr)
                messagebox.showerror("Upload Error", error_msg)





    def add_file(self, file_path):
        with open(file_path, 'rb') as file:
            response = requests.post(f'{self.ipfs_api}/add', files={'file': file})
            if response.status_code == 200:
                return response.json()['Hash']
            else:
                raise Exception(f"Failed to add file: HTTP {response.status_code}")
    async def create_campaign_async(self):
        title = self.title_entry.get()
        goal = self.web3.to_wei(float(self.goal_entry.get()), 'ether')
        ipfs_hash = self.ipfs_hash if self.ipfs_hash else ""

        try:
            # Get the account address as a string
            account_address = self.account.address if hasattr(self.account, 'address') else self.account

            # Get nonce for the account
            nonce = self.web3.eth.get_transaction_count(account_address)

            # Get the current gas price and increase it by 10%
            gas_price = self.web3.eth.gas_price
            increased_gas_price = int(gas_price * 1.1)  # 10% higher gas price

            # Create the transaction with a higher gas price
            txn = self.factory_contract.functions.createCampaign(title, goal, ipfs_hash).build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,  # Adjust gas limit as necessary
                'gasPrice': increased_gas_price,
            })
        
            # Sign the transaction
            signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)

            # Send the transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)

            # Wait for the transaction receipt
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            success_msg = f"Campaign created successfully!\nTransaction Hash: {self.web3.to_hex(tx_hash)}\nIPFS Hash: {ipfs_hash}"
            print(success_msg)
            messagebox.showinfo("Success", success_msg)
            self.load_campaigns()

        except Exception as e:
            error_msg = f"Failed to create campaign: {str(e)}"
            print(error_msg, file=sys.stderr)
            messagebox.showerror("Error", error_msg)



    def create_campaign(self):
        asyncio.run(self.create_campaign_async())

    def load_campaigns(self):
        self.campaign_list.delete(*self.campaign_list.get_children())
        try:
            campaign_addresses = self.factory_contract.functions.getCampaigns().call()
            for campaign_address in campaign_addresses:
                campaign_contract = self.web3.eth.contract(address=campaign_address, abi=self.campaign_abi)
            
                # Fetch the updated campaign details after the donation
                title, goal, total_funds, closed, _ipfsHash = campaign_contract.functions.getCampaignDetails().call()

                # Convert goal and total funds to ETH with better precision
                goal_eth = self.web3.from_wei(goal, 'ether')
                total_funds_eth = self.web3.from_wei(total_funds, 'ether')
            
                # Show up to 6 decimal places for small values
                goal_eth_str = f"{goal_eth:.16f}"
                total_funds_eth_str = f"{total_funds_eth:.16f}"

                status = "Closed" if closed else "Open"

                # Insert the data into the campaign list
                self.campaign_list.insert('', 'end', values=(title, goal_eth_str, total_funds_eth_str, status, campaign_address, _ipfsHash))

            print(f"Loaded {len(campaign_addresses)} campaigns successfully")
        except Exception as e:
            error_msg = f"Failed to load campaigns: {str(e)}"
            print(error_msg, file=sys.stderr)
            messagebox.showerror("Error", error_msg)


    
    def on_campaign_select(self, event):
       selected_items = self.campaign_list.selection()
       if selected_items:  # Check if any item is selected
           selected_item = selected_items[0]
           campaign_address = self.campaign_list.item(selected_item)['values'][4]
           self.donate_entry.delete(0, tk.END)
           self.donate_entry.insert(0, campaign_address)
       else:
        
           self.donate_entry.delete(0, tk.END)
   
           messagebox.showinfo("Info", "Please select a campaign")

    def donate_to_selected(self):
        selected_items = self.campaign_list.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a campaign to donate to.")
            return
        
        selected_item = selected_items[0]
        campaign_address = self.campaign_list.item(selected_item)['values'][4]
        self.donate_entry.delete(0, tk.END)
        self.donate_entry.insert(0, campaign_address)
        self.notebook.select(self.donate_tab)

    def send_transaction(self, transaction):
        try:
            # Get the nonce for the account
            nonce = self.web3.eth.get_transaction_count(self.account_address, 'pending')
            transaction['nonce'] = nonce

            # Estimate gas for the transaction
            gas_estimate = self.web3.eth.estimate_gas(transaction)
            transaction['gas'] = gas_estimate

            # Use legacy transaction type
            gas_price = self.web3.eth.gas_price
            increased_gas_price = int(gas_price * 1.1)  # Increase gas price by 10%
            transaction['gasPrice'] = increased_gas_price

            # Sign the transaction with the private key
            signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=self.private_key)

            # Send the signed transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)

            # Wait for the transaction receipt
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

            return tx_receipt

        except Exception as e:
            print(f"Failed to send transaction: {str(e)}", file=sys.stderr)
            return None

    def start_asyncio_event_loop(self):
        # Create a new event loop and run it in a background thread
        self.asyncio_loop = asyncio.new_event_loop()
        threading.Thread(target=self.asyncio_loop.run_forever, daemon=True).start()

    def handle_donate_button(self):
        # Get campaign address and donation amount from the entries
        campaign_address = self.donate_entry.get()
        amount = self.amount_entry.get()

        # Run the async donation function in the asyncio event loop
        asyncio.run_coroutine_threadsafe(self.donate_to_campaign(campaign_address, amount), self.asyncio_loop)

    async def donate_to_campaign(self, campaign_address, amount):
        try:
            # Check if the account has enough balance
            balance = self.web3.eth.get_balance(self.account_address)
            if balance == 0:
                raise ValueError("Account has insufficient funds for the donation")

            # Convert the donation amount to float and check if it is greater than zero
            amount_float = float(amount)
            if amount_float <= 0:
                raise ValueError("Donation amount must be greater than zero")

            # Convert donation amount to Wei (minimum 0.000001 ETH to avoid very small amounts)
            amount_in_wei = self.web3.to_wei(amount_float, 'ether')
            if amount_in_wei < self.web3.to_wei(0.000001, 'ether'):
                raise ValueError("Donation amount is too small. Minimum is 0.000001 ETH")

            # Set up the campaign contract
           
            nonce = self.web3.eth.get_transaction_count(self.account_address)
            gas_price = self.web3.eth.gas_price
            increased_gas_price = int(gas_price * 1.1)
            chain_id = 11155111  # Sepolia testnet chain ID

            campaign_contract = self.web3.eth.contract(address=campaign_address, abi=self.campaign_abi)
            tx = campaign_contract.functions.donate().build_transaction({
               'from': self.account_address,
               'value': amount_in_wei,
               'gas': 200000,  # Estimate this value
               'gasPrice': increased_gas_price,
               'nonce': nonce,
               'chainId': chain_id,
           })

            # Sign and send the transaction
            signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Wait for transaction receipt and confirm it succeeded
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            success_msg = f"Donation successful!\nTransaction Hash: {self.web3.to_hex(tx_hash)}"
            print(success_msg)
            messagebox.showinfo("Success", success_msg)

            # Ensure that the campaigns list is refreshed after the transaction
            self.load_campaigns()

        except ValueError as e:
            error_msg = f"Failed to donate: {str(e)}"
            print(error_msg, file=sys.stderr)
            messagebox.showerror("Error", error_msg)

        except Exception as e:
            error_msg = f"Failed to donate: {str(e)}"
            print(error_msg, file=sys.stderr)
            messagebox.showerror("Error", error_msg)





    def handle_close_and_withdraw_button(self):
        # Get campaign address from the entry
        campaign_address = self.close_withdraw_entry.get()

        # Run the async close and withdraw function in the asyncio event loop
        asyncio.run_coroutine_threadsafe(self.close_and_withdraw_campaign(campaign_address), self.asyncio_loop)

    async def close_and_withdraw_campaign(self, campaign_address):
        try:
            # Set up the campaign contract
            campaign_contract = self.web3.eth.contract(address=campaign_address, abi=self.campaign_abi)

            # Check if the caller is the owner
            owner = campaign_contract.functions.owner().call()
            if owner.lower() != self.account_address.lower():
                raise ValueError("Only the campaign owner can close and withdraw funds")

            # Check if the campaign is already closed
            is_closed = campaign_contract.functions.closed().call()
            if is_closed:
                raise ValueError("Campaign is already closed")

            # Get the current nonce, gas price, and chain ID
            nonce = self.web3.eth.get_transaction_count(self.account_address)
            gas_price = self.web3.eth.gas_price
            increased_gas_price = int(gas_price * 1.1)
            chain_id = 11155111  # Sepolia testnet chain ID

            # Build the closeCampaign transaction
            close_tx = campaign_contract.functions.closeCampaign().build_transaction({
                'from': self.account_address,
                'gas': 200000,  # Estimate this value
                'gasPrice': increased_gas_price,
                'nonce': nonce,
                'chainId': chain_id,
            })

            # Sign and send the closeCampaign transaction
            signed_close_tx = self.web3.eth.account.sign_transaction(close_tx, private_key=self.private_key)
            close_tx_hash = self.web3.eth.send_raw_transaction(signed_close_tx.raw_transaction)

            # Wait for the closeCampaign transaction receipt
            close_tx_receipt = self.web3.eth.wait_for_transaction_receipt(close_tx_hash)

            # Build the withdrawFunds transaction
            withdraw_tx = campaign_contract.functions.withdrawFunds().build_transaction({
                'from': self.account_address,
                'gas': 200000,  # Estimate this value
                'gasPrice': increased_gas_price,
                'nonce': nonce + 1,  # Increment nonce for the second transaction
                'chainId': chain_id,
            })

            # Sign and send the withdrawFunds transaction
            signed_withdraw_tx = self.web3.eth.account.sign_transaction(withdraw_tx, private_key=self.private_key)
            withdraw_tx_hash = self.web3.eth.send_raw_transaction(signed_withdraw_tx.raw_transaction)

            # Wait for the withdrawFunds transaction receipt
            withdraw_tx_receipt = self.web3.eth.wait_for_transaction_receipt(withdraw_tx_hash)

            success_msg = (f"Campaign closed and funds withdrawn successfully!\n"
                           f"Close Transaction Hash: {self.web3.to_hex(close_tx_hash)}\n"
                           f"Withdraw Transaction Hash: {self.web3.to_hex(withdraw_tx_hash)}")
            print(success_msg)
            messagebox.showinfo("Success", success_msg)

            # Ensure that the campaigns list is refreshed after the transactions
            self.load_campaigns()

        except ValueError as e:
            error_msg = f"Failed to close and withdraw: {str(e)}"
            print(error_msg, file=sys.stderr)
            messagebox.showerror("Error", error_msg)

        except Exception as e:
            error_msg = f"Failed to close and withdraw: {str(e)}"
            print(error_msg, file=sys.stderr)
            messagebox.showerror("Error", error_msg)
    async def view_file_async(self):
        print("Starting view_file function")
        selected_items = self.campaign_list.selection()
        if not selected_items:
            print("No campaign selected")
            messagebox.showwarning("Warning", "Please select a campaign to view its file.")
            return

        selected_item = selected_items[0]
        ipfs_hash = self.campaign_list.item(selected_item)['values'][5]
        print(f"Selected IPFS hash: {ipfs_hash}")

        if not ipfs_hash:
            print("No IPFS hash associated with this campaign")
            messagebox.showinfo("Info", "No file associated with this campaign.")
            return

        async def check_gateway(session, url):
            try:
                print(f"Checking gateway: {url}")
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        print(f"Success: {url}")
                        return url
                    else:
                        print(f"Failed: {url} (Status: {response.status})")
            except Exception as e:
                print(f"Error checking {url}: {str(e)}")
            return None

        async def find_working_gateway():
            gateways = [
                f"http://localhost:8080/ipfs/{ipfs_hash}",
                f"https://ipfs.io/ipfs/{ipfs_hash}",
                f"https://cloudflare-ipfs.com/ipfs/{ipfs_hash}",
                f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}",
                f"https://ipfs.infura.io/ipfs/{ipfs_hash}"
            ]
        
            print(f"Searching for IPFS hash: {ipfs_hash}")
            async with aiohttp.ClientSession() as session:
                tasks = [check_gateway(session, url) for url in gateways]
                results = await asyncio.gather(*tasks)
                working_url = next((url for url in results if url), None)
                if working_url:
                    print(f"Found working gateway: {working_url}")
                else:
                    print("No working gateway found")
                return working_url

        try:
            print("Attempting to retrieve file from IPFS")
            # Show a progress indicator
            self.root.config(cursor="wait")
            self.root.update()

            # Use asyncio to check gateways concurrently
            working_url = await find_working_gateway()

            if working_url:
                print(f"Opening URL in browser: {working_url}")
                webbrowser.open(working_url)
            else:
                print("Failed to find a working gateway")
                messagebox.showerror("Error", "Failed to retrieve the file from IPFS. The content might not be available.")
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            messagebox.showerror("Error", f"Failed to open the file: {str(e)}")
        finally:
            # Reset cursor
            self.root.config(cursor="")
            print("view_file function completed")

    def view_file(self):
        asyncio.run(self.view_file_async())
    

    

if __name__ == "__main__":
    root = tk.Tk()
    app = CampaignApp(root)
    root.mainloop() 









