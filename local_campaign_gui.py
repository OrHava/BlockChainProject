import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import filedialog
from web3 import Web3
import webbrowser
import json
import sys
import ipfshttpclient
import requests


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

    def setup_web3(self):
        GANACHE_URL = "http://127.0.0.1:8545"
        self.web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        if self.web3.is_connected():
            print("Connected to local Ethereum network")
        else:
            error_msg = "Failed to connect to the Ethereum network"
            print(error_msg, file=sys.stderr)
            messagebox.showerror("Connection Error", error_msg)
            self.root.quit()

        self.account = self.web3.eth.accounts[0]
        factory_address = "0xC1F80895B011A87aAA680B7A106BEF6A9Dee6d6B"  # Contract address
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
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=self.default_font)
        style.configure('TButton', font=self.button_font)
        style.configure('TLabel', font=self.default_font)
        style.configure('Treeview.Heading', font=self.header_font)

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

    def setup_create_tab(self):
        frame = ttk.Frame(self.create_tab, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Campaign Title:", font=self.default_font).grid(column=0, row=0, sticky=tk.W, pady=10)
        self.title_entry = ttk.Entry(frame, width=50)
        self.title_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(frame, text="Goal Amount (ETH):", font=self.default_font).grid(column=0, row=1, sticky=tk.W, pady=10)
        self.goal_entry = ttk.Entry(frame, width=50)
        self.goal_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(frame, text="Create Campaign", command=self.create_campaign, style="TButton").grid(column=1, row=2, sticky=tk.E, pady=20)
        ttk.Button(frame, text="Upload File", command=self.upload_file, style="TButton").grid(column=1, row=3, sticky=tk.E, pady=5)

        self.file_label = ttk.Label(frame, text="No file selected", font=self.default_font)
        self.file_label.grid(column=1, row=4, sticky=tk.W, pady=10)

    def setup_list_tab(self):
        frame = ttk.Frame(self.list_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        self.campaign_list = ttk.Treeview(frame, columns=('Title', 'Goal', 'Balance', 'Status', 'Address', 'IPFS Hash'), show='headings')
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

        button_frame = ttk.Frame(frame, padding="10")
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Refresh", command=self.load_campaigns, style="TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Donate to Selected", command=self.donate_to_selected, style="TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="View File", command=self.view_file, style="TButton").pack(side=tk.LEFT, padx=10)

        self.campaign_list.bind('<<TreeviewSelect>>', self.on_campaign_select)

    def setup_donate_tab(self):
        frame = ttk.Frame(self.donate_tab, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Campaign Address:", font=self.default_font).grid(column=0, row=0, sticky=tk.W, pady=10)
        self.donate_entry = ttk.Entry(frame, width=50)
        self.donate_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(frame, text="Amount to Donate (ETH):", font=self.default_font).grid(column=0, row=1, sticky=tk.W, pady=10)
        self.amount_entry = ttk.Entry(frame, width=50)
        self.amount_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(frame, text="Donate", command=self.donate_to_campaign, style="TButton").grid(column=1, row=2, sticky=tk.E, pady=20)

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


    def setup_donate_tab(self):
        frame = ttk.Frame(self.donate_tab, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Campaign Address:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.donate_entry = ttk.Entry(frame, width=50)
        self.donate_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(frame, text="Amount to Donate (ETH):").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(frame, width=50)
        self.amount_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(frame, text="Donate", command=self.donate_to_campaign).grid(column=1, row=2, sticky=tk.E, pady=20)

    def add_file(self, file_path):
        with open(file_path, 'rb') as file:
            response = requests.post(f'{self.ipfs_api}/add', files={'file': file})
            if response.status_code == 200:
                return response.json()['Hash']
            else:
                raise Exception(f"Failed to add file: HTTP {response.status_code}")
    
    def create_campaign(self):
        title = self.title_entry.get()
        goal = self.web3.to_wei(float(self.goal_entry.get()), 'ether')
    
        # Use the self.ipfs_hash that is set in the upload_file function
        ipfs_hash = self.ipfs_hash if self.ipfs_hash else ""

        try:
            tx_hash = self.factory_contract.functions.createCampaign(title, goal, ipfs_hash).transact({'from': self.account})
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            success_msg = f"Campaign created successfully!\nTransaction Hash: {self.web3.to_hex(tx_hash)}\nIPFS Hash: {ipfs_hash}"
            print(success_msg)
            messagebox.showinfo("Success", success_msg)
            self.load_campaigns()
        except Exception as e:
            error_msg = f"Failed to create campaign: {str(e)}"
            print(error_msg, file=sys.stderr)
            messagebox.showerror("Error", error_msg)



    def load_campaigns(self):
        self.campaign_list.delete(*self.campaign_list.get_children())
        try:
            campaign_count = self.factory_contract.functions.getCampaigns().call()
            for i in range(len(campaign_count)):
                campaign_address = campaign_count[i]
                campaign_contract = self.web3.eth.contract(address=campaign_address, abi=self.campaign_abi)
                title, goal, total_funds, closed, _ipfsHash = campaign_contract.functions.getCampaignDetails().call()
                goal_eth = self.web3.from_wei(goal, 'ether')
                total_funds_eth = self.web3.from_wei(total_funds, 'ether')
                status = "Closed" if closed else "Open"
                self.campaign_list.insert('', 'end', values=(title, f"{goal_eth:.2f}", f"{total_funds_eth:.2f}", status, campaign_address, _ipfsHash))
            print(f"Loaded {len(campaign_count)} campaigns successfully")
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

    def donate_to_campaign(self):
        campaign_address = self.donate_entry.get()
        amount = self.web3.to_wei(float(self.amount_entry.get()), 'ether')

        try:
            campaign_contract = self.web3.eth.contract(address=campaign_address, abi=self.campaign_abi)
            tx_hash = campaign_contract.functions.donate().transact({'from': self.account, 'value': amount})
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            success_msg = f"Donation successful!\nTransaction Hash: {self.web3.to_hex(tx_hash)}"
            print(success_msg)
            messagebox.showinfo("Success", success_msg)
            self.load_campaigns()
        except Exception as e:
            error_msg = f"Failed to donate: {str(e)}"
            print(error_msg, file=sys.stderr)
            messagebox.showerror("Error", error_msg)
    def view_file(self):
        selected_items = self.campaign_list.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a campaign to view its file.")
            return

        selected_item = selected_items[0]
        _ipfsHash = self.campaign_list.item(selected_item)['values'][5]

        if _ipfsHash:
            try:
                # Try local gateway first
                local_url = f"http://localhost:8080/ipfs/{_ipfsHash}"
                response = requests.get(local_url, timeout=5)
                if response.status_code == 200:
                    webbrowser.open(local_url)
                    return

                # If local fails, try public gateways
                gateways = [
                    f"https://ipfs.io/ipfs/{_ipfsHash}",
                    f"https://cloudflare-ipfs.com/ipfs/{_ipfsHash}",
                    f"https://gateway.pinata.cloud/ipfs/{_ipfsHash}",
                    f"https://ipfs.infura.io/ipfs/{_ipfsHash}"
                ]

                for gateway_url in gateways:
                    try:
                        response = requests.get(gateway_url, timeout=5)
                        if response.status_code == 200:
                            webbrowser.open(gateway_url)
                            return
                    except requests.RequestException:
                        continue

                messagebox.showerror("Error", "Failed to retrieve the file from IPFS. The content might not be available.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open the file: {str(e)}")
        else:
            messagebox.showinfo("Info", "No file associated with this campaign.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CampaignApp(root)
    root.mainloop() 