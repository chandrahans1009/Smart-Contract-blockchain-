from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()

with open('./Solid.sol','r') as file:
     solidity_code=file.read()
    
compiled_sol=compile_standard(
     {
          "language":"Solidity",
      "sources":{"Solid.sol":{"content": solidity_code}},
      "settings":{
           "outputSelection":{
                "*":{"*":["abi","metadata","evm.bytecode","evm.sourceMap"]}
           }
      },
     },
     solc_version="0.8.0",
)
with open('compiled_code.json','w') as file:

 bytecode=compiled_sol["contracts"]["Solid.sol"]["Solid"]["evm"]["bytecode"]["object"]
 abi=compiled_sol["contracts"]["Solid.sol"]["Solid"]["abi"]
 w3=Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chainid=5777
publickey="0xA801616FC88E402370d48EE7Af0E2D95C3d37626"
privatekey=os.getenv("PRIVATE_KEY")
print(privatekey)

Solid=w3.eth.contract(abi=abi,bytecode=bytecode)
nonce=w3.eth.get_block_transaction_count(publickey)
#build
transcation=Solid.constructor().build_transaction({"chainId":chainid, "from":publickey, "nonce":nonce})
#sign
sign_txn=w3.eth.account.sign_transaction(transcation,privatekey)
#send 


 