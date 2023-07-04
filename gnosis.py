import random
import time
from web3 import Web3

delay = (5, 10)     # delay between wallets
gwei = 12.7         # gwei amount


eth_rpc = 'https://ethereum.blockpi.network/v1/rpc/public'
web3 = Web3(Web3.HTTPProvider(eth_rpc))

contract_address = '0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2'
contract_abi = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"},{"indexed":false,"internalType":"address","name":"singleton","type":"address"}],"name":"ProxyCreation","type":"event"},{"inputs":[{"internalType":"address","name":"_singleton","type":"address"},{"internalType":"bytes","name":"initializer","type":"bytes"},{"internalType":"uint256","name":"saltNonce","type":"uint256"}],"name":"calculateCreateProxyWithNonceAddress","outputs":[{"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"singleton","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"createProxy","outputs":[{"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_singleton","type":"address"},{"internalType":"bytes","name":"initializer","type":"bytes"},{"internalType":"uint256","name":"saltNonce","type":"uint256"},{"internalType":"contract IProxyCreationCallback","name":"callback","type":"address"}],"name":"createProxyWithCallback","outputs":[{"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_singleton","type":"address"},{"internalType":"bytes","name":"initializer","type":"bytes"},{"internalType":"uint256","name":"saltNonce","type":"uint256"}],"name":"createProxyWithNonce","outputs":[{"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"proxyCreationCode","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"proxyRuntimeCode","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"pure","type":"function"}]'
gnosis_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def read_file(filename):
    result = []
    with open(filename, 'r') as file:
        for tmp in file.readlines():
            result.append(tmp.replace('\n', ''))

    return result


def write_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(f'{text}\n')


def format_40_accounts(addresses):
    tmp = ''
    addresses = addresses.split(';')
    for address in addresses:
        tmp += '0' * (64-len(address[2:])) + address[2:]

    return tmp


def gnosis_tx(private: str, addresses: list):
    address = web3.eth.account.privateKeyToAccount(private).address
    data1 = format_40_accounts(f'{address};{addresses}')
    # data1 = format_40_accounts(addresses)
    data = f'0xb63e800d0000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000{hex(random.randint(1, 9))[2:]}00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000620000000000000000000000000f48f2b2d2a534e402487b3ee7c18c33aec0fe5e40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000028{data1}0000000000000000000000000000000000000000000000000000000000000000'
    print(data)
    tx = gnosis_contract.functions.createProxyWithNonce(
        web3.toChecksumAddress("0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552"),
        data,
        int(time.time()*1000)
    ).build_transaction({
        'from': address,
        'nonce': web3.eth.getTransactionCount(address),
        'chainId': web3.eth.chainId
    })
    tx['maxPriorityFeePerGas'] = web3.toWei(0.1, 'gwei')
    tx['maxFeePerGas'] = web3.toWei(gwei, 'gwei')
    print(tx)
    tx_create = web3.eth.account.sign_transaction(tx, private)
    tx_hash = web3.eth.sendRawTransaction(tx_create.rawTransaction)
    write_to_file('hashes.txt', tx_hash.hex())
    print(f"Transaction hash: {tx_hash.hex()}")


def main():
    privates = read_file('privates.txt')
    addresses = read_file('addresses.txt')
    for private, addresses in zip(privates,addresses):
        gnosis_tx(private, addresses)
        time.sleep(random.randint(*delay))


if __name__ == '__main__':
    main()
