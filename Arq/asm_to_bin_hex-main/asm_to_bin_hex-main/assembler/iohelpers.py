# ---------------------------
# I/O helpers: read assembly, write hex/bin
# ---------------------------

def write_hex_bin(machine, hexfile, binfile):
    with open(hexfile, 'w') as hf, open(binfile, 'w') as bf:
        for addr, word in machine:
            hf.write(f"{word:08x}\n")
            bf.write(f"{word:032b}\n")