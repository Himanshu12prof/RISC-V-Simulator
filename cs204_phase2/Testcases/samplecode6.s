.data
var: .word 0x10001111
address: .word 0x10000050
.text
lw x5, var
lw x6, address
sw x5, 0(x6)