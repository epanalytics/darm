"""
Copyright (c) 2013, Jurriaan Bremer
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the darm developer(s) nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

class Bitsize:
    def __init__(self, name, bitsize, comment):
        self.name = name
        self.bitsize = bitsize
        self.comment = comment

    def __repr__(self):
        return '<%s:%d>' % (self.name, self.bitsize)

class imm(Bitsize):
    def __init__(self, bits, args):
        self.name = 'imm%d' % (bits)
        self.bitsize = bits
        self.comment = 'Immediate'
        self.args = args

cond          = Bitsize('cond', 4, 'Conditional Flags')
Rd            = Bitsize('Rd', 4, 'Destination Register')
Rd3           = Bitsize('Rd', 3, 'Destination Register')
Rs            = Bitsize('Rs', 3, 'Shift Immediate')
Rn            = Bitsize('Rn', 4, 'N Register')
Rn3           = Bitsize('Rn', 3, 'N Register')
Rm            = Bitsize('Rm', 4, 'Shift Register')
Rm3           = Bitsize('Rm', 3, 'Shift Register')
Rt            = Bitsize('Rt', 4, 'Transferred Register')
Rt3           = Bitsize('Rt', 3, 'Transferred Register')
Rt2           = Bitsize('Rt2', 4, 'Second Ternary Register')
Ra            = Bitsize('Ra', 4, 'Accumulate Register')
Rdm           = Bitsize('Rdm', 4, 'Destination & M Register')
Rdm3          = Bitsize('Rdm', 3, 'Destination & M Register')
Rdn           = Bitsize('Rdn', 4, 'Destination & N Register')
Rdn3          = Bitsize('Rdn', 3, 'Destination & N Register')
S             = Bitsize('S', 1, 'Update Conditional Flags')
type_         = Bitsize('type', 2, 'Shift Type')
msb           = Bitsize('msb', 5, 'Most Significant Bit')
lsb           = Bitsize('lsb', 5, 'Least Significant Bit')
register_list8= Bitsize('register_list', 8, 'Register List')
register_list = Bitsize('register_list', 16, 'Register List')
E             = Bitsize('E', 1, 'Endian Specifier')
msr           = Bitsize('msr', 2, 'Move to Special Register mask')
rotate        = Bitsize('rotate', 2, 'Rotation Type')
H             = Bitsize('H', 1, 'Sign Extension Bit for BL(X)')
option        = Bitsize('option', 4, 'Option for Debug Hint')
W             = Bitsize('W', 1, 'Some Bit for LDM')
widthm1       = Bitsize('widthm1', 5, 'Bit Width Minus One')
M             = Bitsize('M', 1, 'High 16bits for Rm')
N             = Bitsize('N', 1, 'High 16bits for Rn')
DN            = Bitsize('DN', 1, 'High 16bits for Rdn')
RdHi          = Bitsize('RdHi', 4, 'High 32bits for Rd')
RdLo          = Bitsize('RdLo', 4, 'Low 32bits for Rd')
R             = Bitsize('R', 1, 'Round Integer')
sat_imm4      = Bitsize('sat_imm4', 4, 'Saturate Immediate')
sat_imm5      = Bitsize('sat_imm5', 5, 'Saturate Immediate')
sh            = Bitsize('sh', 1, 'Immediate Shift Value')
opc1          = Bitsize('opc1', 4, 'Coprocessor Operation Code')
opc2          = Bitsize('opc2', 3, 'Coprocessor Information')
CRn           = Bitsize('CRn', 4, 'Coprocessor Operand Register')
CRd           = Bitsize('CRd', 4, 'Coprocessor Destination Register')
coproc        = Bitsize('coproc', 4, 'Coprocessor Number')
CPOpc         = Bitsize('CPOpc', 3, 'Coprocessor Operation Mode')
CRm           = Bitsize('CRm', 4, 'Coprocessor Operand Register')
U             = Bitsize('U', 1, 'Addition flag for PLD')
P             = Bitsize('P', 1, 'Protected Mode Flag?')
D             = Bitsize('D', 1, 'User-defined bit')
tb            = Bitsize('tb', 1, 'Is PKH in TB form or not?')
imm4H         = Bitsize('imm4H', 4, 'High Word Register')
imm4L         = Bitsize('imm4L', 4, 'Low Word Register')
im            = Bitsize('im', 1, 'CPS interrupt mask')
CP3           = Bitsize('CP3', 3, 'CPS flag affects')

Qd            = Bitsize('Qd', 4, 'Quadword Destination Register')
Qn            = Bitsize('Qn', 4, 'Quadword First Operand Register')
Qm            = Bitsize('Qm', 4, 'Quadword Second Operand Register')
Dd            = Bitsize('Dd', 4, 'Doubleword Destination Register')
Dn            = Bitsize('Dn', 4, 'Doubleword First Operand Register')
Dm            = Bitsize('Dm', 4, 'Doubleword Second Operand Register')
Sd            = Bitsize('Sd', 4, 'Single-Precision Destination Register')
Sn            = Bitsize('Sn', 4, 'Single-Precision First Operand Register')
Sm            = Bitsize('Sm', 4, 'Single-Precision Second Operand Register')


i             = Bitsize('imm1', 1, 'Immediate')
J1            = Bitsize('J1', 1, 'Immediate')
J2            = Bitsize('J2', 1, 'Immediate')
imm2          = Bitsize('imm2', 2, 'Immediate')
imm3          = Bitsize('imm3', 3, 'Immediate')
imm4          = Bitsize('imm4', 4, 'Immediate')
imm4H         = Bitsize('imm4H', 4, 'Immediate')
imm4L         = Bitsize('imm4L', 4, 'Immediate')
imm5          = Bitsize('imm5', 5, 'Immediate')
imm6          = Bitsize('imm6', 6, 'Immediate')
imm7          = Bitsize('imm7', 7, 'Immediate')
imm8          = Bitsize('imm8', 8, 'Immediate')
imm10         = Bitsize('imm10', 10, 'Immediate')
imm10H        = Bitsize('imm10H', 10, 'Immediate')
imm10L        = Bitsize('imm10L', 10, 'Immediate')
imm11         = Bitsize('imm11', 11, 'Immediate')
imm12         = Bitsize('imm12', 12, 'Immediate')
imm24         = Bitsize('imm24', 24, 'Immediate')

