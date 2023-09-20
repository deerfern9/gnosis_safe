# op | era | base | polygon | eht | bsc | arb
chain = 'bsc'

# owners of gnosis safe 1 - one stable owner / (1, 10) random up to 10 owners
safe_owner_count = (1, 3)
# additional addresses that will be added to safe.
# (int_min, int_max) - setting will generate random addresses that will add them to gnosis safe
# 'custom' - before adding this setting, make sure you add your addresses to the addresses.txt file in the correct format
safe_users = (5, 10)
# delays between creating safes
delay = (30, 300)
# maximum allowed gwei on the ethereum network to create gnosis safe
max_gwei = 25

rpcs = {
    'op': 'https://optimism.blockpi.network/v1/rpc/public',
    'era': 'https://zksync-era.blockpi.network/v1/rpc/public',
    'base': 'https://base.blockpi.network/v1/rpc/public',
    'eth': 'https://ethereum.blockpi.network/v1/rpc/public',
    'polygon': 'https://polygon.blockpi.network/v1/rpc/public',
    'bsc': 'https://bsc.blockpi.network/v1/rpc/public',
    'arb': 'https://arbitrum.blockpi.network/v1/rpc/public',
}

safe_abi = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"},{"indexed":false,"internalType":"address","name":"singleton","type":"address"}],"name":"ProxyCreation","type":"event"},{"inputs":[{"internalType":"address","name":"_singleton","type":"address"},{"internalType":"bytes","name":"initializer","type":"bytes"},{"internalType":"uint256","name":"saltNonce","type":"uint256"}],"name":"calculateCreateProxyWithNonceAddress","outputs":[{"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"singleton","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"createProxy","outputs":[{"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_singleton","type":"address"},{"internalType":"bytes","name":"initializer","type":"bytes"},{"internalType":"uint256","name":"saltNonce","type":"uint256"},{"internalType":"contract IProxyCreationCallback","name":"callback","type":"address"}],"name":"createProxyWithCallback","outputs":[{"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_singleton","type":"address"},{"internalType":"bytes","name":"initializer","type":"bytes"},{"internalType":"uint256","name":"saltNonce","type":"uint256"}],"name":"createProxyWithNonce","outputs":[{"internalType":"contract GnosisSafeProxy","name":"proxy","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"proxyCreationCode","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"proxyRuntimeCode","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"pure","type":"function"}]'

safe_addresses = {
    'op': '0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC',
    'era': '0xDAec33641865E4651fB43181C6DB6f7232Ee91c2',
    'base': '0xC22834581EbC8527d974F8a1c97E1bEA4EF910BC',
    'eht': '0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2',
    'polygon': '0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2',
    'bsc': '0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2',
    'arb': '0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2',
}
