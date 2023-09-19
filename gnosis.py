import time
import random
from web3 import Web3
from datetime import datetime
from colorama import Fore, init
from eth_account import Account

from config import *
init()

colors = {
    'time': Fore.MAGENTA,
    'account_info': Fore.CYAN,
    'message': Fore.BLUE,
    'error_message': Fore.RED,
    'reset': Fore.RESET
}

web3 = Web3(Web3.HTTPProvider(op_rpc))
eth_web3 = Web3(Web3.HTTPProvider(eth_rpc))
Account.enable_unaudited_hdwallet_features()
safe_contract = web3.eth.contract(address=web3.to_checksum_address(safe_address), abi=safe_abi)


def read_file(filename, read_type='r'):
    result = []
    with open(filename, read_type) as file:
        for tmp in file.readlines():
            result.append(tmp.strip())

    return result


def write_to_file(filename, text, write_type='a'):
    with open(filename, write_type) as file:
        file.write(f'{text}\n')


def new_print(message_type, message, is_error=False):
    print(f'{colors["time"]}{datetime.now().strftime("%d %H:%M:%S")}{colors["account_info"]} | {message_type} |'
          f' {colors[(["message", "error_message"])[is_error]]}{message}{colors["reset"]}')


def wait_normal_gwei():
    while (eth_gwei := web3.from_wei(eth_web3.eth.gas_price, 'gwei')) > max_gwei:
        new_print('INFO', f"Current gas fee {eth_gwei} gwei > {max_gwei} gwei. Waiting for 17 seconds...")
        time.sleep(17)


def to_data(string: str):
    return '0' * (64 - len(string)) + string


def initializer_generator(owners_count: int, wallets: list):
    wallets_len = len(wallets)
    data_wallets_len = to_data(hex(wallets_len)[2:])

    wallets_count = hex(int(20 * (wallets_len + 1) / 10))[2:]
    if len(wallets_count) > 1:
        pre_data_wallets_count = str(1 + int(wallets_count[0])) + wallets_count[1:] + '0'
    else:
        pre_data_wallets_count = '1' + wallets_count + '0'
    data_wallets_count = to_data(pre_data_wallets_count)

    wallets_data = ''
    for address in wallets:
        address_data = to_data(address[2:])
        wallets_data += address_data

    data_owners_count_ = to_data(hex(owners_count)[2:])

    generated_initializer = f'0xb63e800d0000000000000000000000000000000000000000000000000000000000000100{data_owners_count_}0000000000000000000000000000000000000000000000000000000000000000{data_wallets_count}000000000000000000000000017062a1de2fe6b99be3d9d37841fed19f573804000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000{data_wallets_len}{wallets_data}0000000000000000000000000000000000000000000000000000000000000000'
    return generated_initializer


def create_safe(private: str, additional_addresses: list):
    address = web3.eth.account.from_key(private).address
    print([address,],additional_addresses)
    safe_addresses = [address,] + additional_addresses

    if type(safe_owner_count).__name__ != 'tuple' and type(safe_owner_count).__name__ != 'int':
        raise TypeError("Only integers or tuples are allowed")

    if type(safe_owner_count).__name__ == 'tuple':
        initializer = initializer_generator(random.randint(*safe_owner_count), safe_addresses)
    elif type(safe_owner_count).__name__ == 'int':
        initializer = initializer_generator(safe_owner_count, safe_addresses)

    try:
        tx = safe_contract.functions.createProxyWithNonce(
            '0xfb1bffC9d739B8D520DaF37dF666da4C687191EA', initializer, int(time.time()*1000)
        ).build_transaction({
            'from': address,
            'nonce': web3.eth.get_transaction_count(address),
            'gasPrice': web3.eth.gas_price,
            'chainId': web3.eth.chain_id,
        })

        tx_create = web3.eth.account.sign_transaction(tx, private)
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        new_print(address, f'Safe created: {tx_hash.hex()}')
        write_to_file('safe created hashes .txt', f'{private};{address};{tx_hash.hex()}')
    except Exception as error:
        new_print(address, f'Error: {error}', is_error=True)


def main():
    privates = read_file('privates.txt')
    if type(safe_users).__name__ == 'str':
        additional_addresses_lists = [addresses_list.split(';') for addresses_list in read_file('addresses.txt')]
    else:
        additional_addresses_lists = []
        for _ in range(len(privates)):
            tmp = []
            for _ in range(random.randint(*safe_users)-1):
                account, mnemonic = web3.eth.account.create_with_mnemonic()
                address_ = account.address
                private_ = account.key.hex()
                tmp.append(address_)
                write_to_file('fake wallets.txt', f'{address_};{private_};{mnemonic}')
            additional_addresses_lists.append(tmp)

    for private, additional_addresses in zip(privates, additional_addresses_lists):
        create_safe(private, additional_addresses)


if __name__ == '__main__':
    main()
