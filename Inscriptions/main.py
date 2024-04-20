from concurrent.futures import ThreadPoolExecutor
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
 
 
num_transactions = 100 # Number of transactions to send
 
 
private_key = ' ' # private key without 0x
sender_address = '0x....' # your address
recipient_address = '0x....' # your address
 
 
web3 = Web3(HTTPProvider('https://1rpc.io/matic')) # https://chainlist.org/chain/137
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
 
 
 
def send_transaction(nonce):
    gas_price = web3.eth.gas_price
    max_priority_fee_per_gas = gas_price
    max_fee_per_gas = int(1.5 * gas_price)
    hex_data = '0x646174613a2c7b2270223a227072632d3230222c226f70223a226d696e74222c227469636b223a22706f6c73222c22616d74223a22313030303030303030227d'
 
    transaction_params = {
        'from': sender_address,
        'to': recipient_address,
        'value': web3.to_wei(0, 'ether'),
        'nonce': nonce,
        'gas': 22024,
        'maxFeePerGas': max_fee_per_gas,
        'maxPriorityFeePerGas': max_priority_fee_per_gas,
        'data': hex_data,
        'chainId': 137,
    }
 
    transaction = web3.eth.account.sign_transaction(transaction_params, private_key)
    transaction_hash = web3.eth.send_raw_transaction(transaction.rawTransaction)
    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash, timeout=120)
 
    return {
        'transaction_hash': transaction_hash.hex(),
        'transaction_link': f'https://polygonscan.com/tx/{transaction_hash.hex()}',
        'block_number': transaction_receipt['blockNumber'],
        'block_link': f'https://polygonscan.com/block/countdown/{transaction_receipt["blockNumber"]}',
    }
 
 
 
current_nonce = web3.eth.get_transaction_count(sender_address)
 
 
with ThreadPoolExecutor() as executor:
    results = list(executor.map(send_transaction, range(current_nonce, current_nonce + num_transactions)))
 
 
for i, result in enumerate(results):
    print(f'Transaction {i + 1} sent with hash: {result["transaction_link"]} | Block Link: {result["block_link"]}')
