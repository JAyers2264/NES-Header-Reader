from bitstring import BitArray

def read_header(header_bytes):
	nes_header = ["0x4e", "0x45", "0x53", "0x1a"]
	output = ""

	# Check whether an iNES header is present

	not_an_ines_header = False
	for i in range(0,4):
		if hex(header_bytes[i]) != nes_header[i]:
			not_an_ines_header = True
		
	output+= "\n\n[Bytes 0-3]: "
	if not_an_ines_header:
		output += "This ROM does not have an iNES header..."
	else:
		output += "iNES Constant Present"

	# Output the length of PRG and CHR ROM segments in the ROM file

	prg_rom = header_bytes[4] * 16384
	chr_rom = header_bytes[5] * 8192
	cart_rom = prg_rom + chr_rom
	#print(prg_rom + 16, cart_rom)
	
	output += "\n\n[Byte 4]: The PRG ROM consists of " + str(prg_rom) + " bytes. (Addresses(?): " \
		+ str(hex(16)) + " - " + str(hex(16+prg_rom-1) + ")")
	if chr_rom > 0:
		output += "\n\n[Byte 5]: The CHR ROM consists of " + str(chr_rom) + " bytes. (Addresses(?): " \
			+ str(hex(16+prg_rom)) + " - " + str(hex(16+cart_rom-1) + ")")
	else:
		output += "\n\n[Byte 5]: This game uses CHR RAM instead of CHR ROM"

	# Read 6th byte by bits and output represented info

	flags_6 = header_bytes[6]
	flags_6_bits = bin(flags_6)[2:]
	if len(flags_6_bits) < 8:
		for i in range(0,8-len(flags_6_bits)):
			flags_6_bits = "0" + flags_6_bits

	#mapper_lower_nybble = hex(int(flags_6_bits[:4],2))
	four_screen_VRAM = int(flags_6_bits[4])
	trainer_before_PRG = int(flags_6_bits[5])
	battery_PRG = int(flags_6_bits[6])
	mirroring = int(flags_6_bits[7])
		
	if mirroring:
		output += ('\n\n[Byte 6, Bit 0] Vertical mirroring!')
	else:
		output += ('\n\n[Byte 6, Bit 0] Horizontal mirroring!')	
	
	if battery_PRG:
		output += ('\n[Byte 6, Bit 1] Cartridge contains battery-backed PRG RAM ($6000-7FFF) or other persistent memory')
	else:
		output += ('\n[Byte 6, Bit 1] No battery/persistent memory.')
		
	if trainer_before_PRG:
		output += ('\n[Byte 6, Bit 2] A 512-bit trainer is located at $7000-$7FFF before the PRG data')
	else:
		output += ('\n[Byte 6, Bit 2] No 512-bit trainer.')
		
	if four_screen_VRAM:
		output += ('\n[Byte 6, Bit 3] Ignore mirroring control; this game uses four-screen VRAM')
	else:
		output += ('\n[Byte 6, Bit 3] Use normal mirroring control')

	return output