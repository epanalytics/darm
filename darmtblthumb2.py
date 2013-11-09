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

from darmbits import *

# details in the ARMv7-a reference manual
thumb16 = [
    ('BKPT #<imm8>',              1, 0, 1, 1, 1, 1, 1, 0, imm8),
    ('CBZ <Rn>, <label>',         1, 0, 1, 1, 0, 0, i, 1, imm5, Rn3),
    ('CBNZ <Rn>, <label>',        1, 0, 1, 1, 1, 0, i, 1, imm5, Rn3),
    ('CPS <iflags>',              1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, im, (0), CP3),
    ('NOP',                       1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    ('PUSH <registers>',          1, 0, 1, 1, 0, 1, 0, M, register_list8),
    ('POP <registers>',           1, 0, 1, 1, 1, 1, 0, M, register_list8),
    ('REV <Rd>, <Rm>',            1, 0, 1, 1, 1, 0, 1, 0, 0, 0, Rm3, Rd3),
    ('REV16 <Rd>, <Rm>',          1, 0, 1, 1, 1, 0, 1, 0, 0, 1, Rm3, Rd3),
    ('REVSH <Rd>, <Rm>',          1, 0, 1, 1, 1, 0, 1, 0, 1, 1, Rm3, Rd3),
    ('SEV',                       1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0),
    ('SETEND <endian_specifier>', 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, (1), E, (0), (0), (0)),
    ('SUB <Rd>,SP=<Rn>,#<imm7>',  1, 0, 1, 1, 0, 0, 0, 0, 1, imm7),
    ('SXTB <Rd>, <Rm>',           1, 0, 1, 1, 0, 0, 1, 0, 0, 1, Rm3, Rd3),
    ('SXTH <Rd>, <Rm>',           1, 0, 1, 1, 0, 0, 1, 0, 0, 0, Rm3, Rd3),
    ('UXTB <Rd>, <Rm>',           1, 0, 1, 1, 0, 0, 1, 0, 1, 1, Rm3, Rd3),
    ('UXTH <Rd>, <Rm>',           1, 0, 1, 1, 0, 0, 1, 0, 1, 0, Rm3, Rd3),
    ('WFE',                       1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0),
    ('WFI',                       1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0),
    ('YIELD',                     1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0),
]

thumb32 = [
    ('B<c>.W <label>', 1, 1, 1, 1, 0, S, cond, imm6, 1, 0, J1, 0, J2, imm11),
    ('B<c>.W <label>', 1, 1, 1, 1, 0, S,      imm10, 1, 0, J1, 1, J2, imm11),
    ('BL<c> <label>',  1, 1, 1, 1, 0, S, imm10, 1, 1, J1, 1, J2, imm11),
    ('BLX<c> <label>', 1, 1, 1, 1, 0, S, imm10H, 1, 1, J1, 0, J2, imm10L, H),
    ('BXJ<c> <Rm>',    1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, Rm, 1, 0, (0), 0, (1), (1), (1), (1), (0), (0), (0), (0), (0), (0), (0), (0)),
    ('LDM<c>.W <Rn>{!}, <registers>', 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, W, 1, Rn, P, M, (0), register_list13),
    #('LDMDB<c> <Rn>{!}, <registers>', 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, W, 1, Rn, P, M, (0), register_list),
    ('LDR<c>.W <Rt>, [<Rn>{, #<imm12>}]', 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, Rn, Rt, imm12),
    ('LDR<c> <Rt>, [<Rn>,#+/-<imm8>]',     1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, Rn, Rt, 1, P, U, W, imm8),
    ('MOV{S}<c>.W <Rd>, #<const>', 1, 1, 1, 1, 0, i, 0, 0, 0, 1, 0, S, 1, 1, 1, 1, 0, imm3, Rd, imm8),
    ('STMDB<c> <Rn>{!}, <registers>', 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, W, 0, Rn, (0), M, (0), register_list13),
    ('STR<c>.W <Rt>, [<Rn>, #<imm12>]', 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, Rn, Rt, imm12),
    ('STR<c> <Rt>, [<Rn>,#+/-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, Rn, Rt, 1, P, U, W, imm8),
    ('TBB<c> [<Rn>, <Rm>]', 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, (1), (1), (1), (1), (0), (0), (0), (0), 0, 0, 0, 0, Rm),
    ('TBH<c> [<Rn>, <Rm>, LSL #1]', 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, (1), (1), (1), (1), (0), (0), (0), (0), 0, 0, 0, 1, Rm),
]

# stupid stuff like LSL-ed operands and negative constants and SP specific encodings
# and optional args and thumb2 with split constants
# are commented out because they throw warnings and need fmt string specificers
thumb32xxx = [
    ('ADC{S}<c> <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 1, 0, 1, 0, S, Rn, 0, imm3, Rd, imm8),
    ('ADC{S}<c>.W <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    #('ADD{S}<c>.W <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 1, 0, 0, 0, S, Rn, 0, imm3, Rd, imm8),
    ('ADDW<c> <Rd>, <Rn>, #<imm12>', 1, 1, 1, 1, 0, i, 1, 0, 0, 0, 0, 0, Rn, 0, imm3, Rd, imm8),
    ('ADD{S}<c>.W <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    ('ADD{S}<c>.W <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    #('ADD{S}<c>.W <Rd>, SP, #<const>', 1, 1, 1, 1, 0, i, 0, 1, 0, 0, 0, S, 1, 1, 0, 1, 0, imm3, Rd, imm8),
    ('ADDW<c> <Rd>, SP, #<imm12>', 1, 1, 1, 1, 0, i, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, imm3, Rd, imm8),
    ('ADD{S}<c>.W <Rd>, SP, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, S, 1, 1, 0, 1, (0), imm3, Rd, imm2, type_, Rm),
    ('ADD{S}<c>.W <Rd>, SP, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, S, 1, 1, 0, 1, (0), imm3, Rd, imm2, type_, Rm),
    ('ADR<c>.W <Rd>, <label>', 1, 1, 1, 1, 0, i, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, imm3, Rd, imm8),
    ('ADR<c>.W <Rd>, <label>', 1, 1, 1, 1, 0, i, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, imm3, Rd, imm8),
    ('AND{S}<c> <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 0, 0, 0, 0, S, Rn, 0, imm3, Rd, imm8),
    ('AND{S}<c>.W <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    #('ASR{S}<c>.W <Rd>, <Rm>, #<imm>', 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), imm3, Rd, imm2, 1, 0, Rm),
    ('ASR{S}<c>.W <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, S, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('BFC<c> <Rd>, #<lsb>, #<width>', 1, 1, 1, 1, 0, (0), 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, imm3, Rd, imm2, (0), msb),
    ('BFI<c> <Rd>, <Rn>, #<lsb>, #<width>', 1, 1, 1, 1, 0, (0), 1, 1, 0, 1, 1, 0, Rn, 0, imm3, Rd, imm2, (0), msb),
    ('BIC{S}<c> <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 0, 0, 0, 1, S, Rn, 0, imm3, Rd, imm8),
    ('BIC{S}<c>.W <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    ('CLREX<c>', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, (1), (1), (1), (1), 1, 0, (0), 0, (1), (1), (1), (1), 0, 0, 1, 0, (1), (1), (1), (1)),
    ('CLZ<c> <Rd>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 0, 0, Rm),
    ('CMN<c> <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 1, 0, 0, 0, 1, Rn, 0, imm3, 1, 1, 1, 1, imm8),
    ('CMN<c>.W', 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, Rn, (0), imm3, 1, 1, 1, 1, imm2, type_, Rm),
    #('CMP<c>.W <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 1, 1, 0, 1, 1, Rn, 0, imm3, 1, 1, 1, 1, imm8),
    ('CMP<c>.W <Rn>, <Rm> {, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, Rn, (0), imm3, 1, 1, 1, 1, imm2, type_, Rm),
    ('DBG<c> #<option>', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 1, 1, 1, 1, option),
    ('DMB<c> <option>', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, (1), (1), (1), (1), 1, 0, (0), 0, (1), (1), (1), (1), 0, 1, 0, 1, option),
    ('DSB<c> <option>', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, (1), (1), (1), (1), 1, 0, (0), 0, (1), (1), (1), (1), 0, 1, 0, 0, option),
    ('EOR{S}<c> <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 0, 1, 0, 0, S, Rn, 0, imm3, Rd, imm8),
    ('EOR{S}<c>.W <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    ('ISB<c> <option>', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, (1), (1), (1), (1), 1, 0, (0), 0, (1), (1), (1), (1), 0, 1, 1, 0, option),
    #('IT{<x>{<y>{<z>}}} <firstcond>', 1, 0, 1, 1, 1, 1, 1, 1, firstcond, mask),
    #('IT{<x>{<y>{<z>}}} <firstcond>', 1, 0, 1, 1, 1, 1, 1, 1, firstcond, mask),
    ('LDR<c>.W <Rt>, <label>', 1, 1, 1, 1, 1, 0, 0, 0, U, 1, 0, 1, 1, 1, 1, 1, Rt, imm12),
    #('LDR<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm),
    #('LDR<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm),
    #('LDRB<c>.W <Rt>, [<Rn>{, #<imm12>}]', 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, Rn, Rt, imm12),
    #('LDRB<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, Rn, Rt, 1, P, U, W, imm8),
    #('LDRB<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, Rn, Rt, 1, P, U, W, imm8),
    ('LDRB<c> <Rt>, <label>', 1, 1, 1, 1, 1, 0, 0, 0, U, 0, 0, 1, 1, 1, 1, 1, Rt, imm12),
    #('LDRB<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm),
    ('LDRBT<c> <Rt>, [<Rn>, #<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, Rn, Rt, 1, 1, 1, 0, imm8),
    ('LDRD<c> <Rt>, <Rt2>, [<Rn>{, #+/-<imm>}]', 1, 1, 1, 0, 1, 0, 0, P, U, 1, W, 1, Rn, Rt, Rt2, imm8),
    ('LDRD<c> <Rt>, <Rt2>, <label>', 1, 1, 1, 0, 1, 0, 0, P, U, 1, W, 1, 1, 1, 1, 1, Rt, Rt2, imm8),
    ('LDREX<c> <Rt>, [<Rn>{, #<imm>}]', 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, Rn, Rt, (1), (1), (1), (1), imm8),
    ('LDREXB<c> <Rt>, [<Rn>]', 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, Rt, (1), (1), (1), (1), 0, 1, 0, 0, (1), (1), (1), (1)),
    ('LDREXD<c> <Rt>, <Rt2>, [<Rn>]', 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, Rt, Rt2, 0, 1, 1, 1, (1), (1), (1), (1)),
    ('LDREXH<c> <Rt>, [<Rn>]', 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, Rt, (1), (1), (1), (1), 0, 1, 0, 1, (1), (1), (1), (1)),
    #('LDRH<c>.W <Rt>, [<Rn>{, #<imm12>}]', 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, Rn, Rt, imm12),
    #('LDRH<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, Rn, Rt, 1, P, U, W, imm8),
    #('LDRH<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, Rn, Rt, 1, P, U, W, imm8),
    ('LDRH<c> <Rt>, <label>', 1, 1, 1, 1, 1, 0, 0, 0, U, 0, 1, 1, 1, 1, 1, 1, Rt, imm12),
    #('LDRH<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm),
    ('LDRHT<c> <Rt>, [<Rn>, #<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, Rn, Rt, 1, 1, 1, 0, imm8),
    ('LDRSB<c> <Rt>, [<Rn>, #<imm12>]', 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, Rn, Rt, imm12),
    #('LDRSB<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, Rt, 1, P, U, W, imm8),
    ('LDRSB<c> <Rt>, <label>', 1, 1, 1, 1, 1, 0, 0, 1, U, 0, 0, 1, 1, 1, 1, 1, Rt, imm12),
    #('LDRSB<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm),
    ('LDRSBT<c> <Rt>, [<Rn>, #<imm8>]', 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, Rt, 1, 1, 1, 0, imm8),
    ('LDRSH<c> <Rt>, [<Rn>, #<imm12>]', 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, Rn, Rt, imm12),
    #('LDRSH<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, Rn, Rt, 1, P, U, W, imm8),
    ('LDRSH<c> <Rt>, <label>', 1, 1, 1, 1, 1, 0, 0, 1, U, 0, 1, 1, 1, 1, 1, 1, Rt, imm12),
    #('LDRSH<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm),
    ('LDRSHT<c> <Rt>, [<Rn>, #<imm8>]', 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, Rn, Rt, 1, 1, 1, 0, imm8),
    ('LDRT<c> <Rt>, [<Rn>, #<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, Rn, Rt, 1, 1, 1, 0, imm8),
    #('LSL{S}<c>.W <Rd>, <Rm>, #<imm5>', 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), imm3, Rd, imm2, 0, 0, Rm),
    ('LSL{S}<c>.W <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, S, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    #('LSR{S}<c>.W <Rd>, <Rm>, #<imm>', 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), imm3, Rd, imm2, 0, 1, Rm),
    ('LSR{S}<c>.W <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, S, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('MLA<c> <Rd>, <Rn>, <Rm>, <Ra>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, Rn, Ra, Rd, 0, 0, 0, 0, Rm),
    ('MLS<c> <Rd>, <Rn>, <Rm>, <Ra>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, Rn, Ra, Rd, 0, 0, 0, 1, Rm),
    ('MOVW<c> <Rd>, #<imm16>', 1, 1, 1, 1, 0, i, 1, 0, 0, 1, 0, 0, imm4, 0, imm3, Rd, imm8),
    ('MOV{S}<c>.W <Rd>, <Rm>', 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), 0, 0, 0, Rd, 0, 0, 0, 0, Rm),
    ('MOVT<c> <Rd>, #<imm16>', 1, 1, 1, 1, 0, i, 1, 0, 1, 1, 0, 0, imm4, 0, imm3, Rd, imm8),
    ('MRS<c> <Rd>, <spec_reg>', 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, Rd, (0), (0), 0, (0), (0), (0), (0), (0)),
    #('MSR<c> <spec_reg>, <Rn>', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, Rn, 1, 0, (0), 0, mask, 0, 0, (0), (0), 0, (0), (0), (0), (0), (0)),
    ('MUL<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('MVN{S}<c> <Rd>, #<const>', 1, 1, 1, 1, 0, i, 0, 0, 0, 1, 1, S, 1, 1, 1, 1, 0, imm3, Rd, imm8),
    ('MVN{S}<c>.W <Rd>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, S, 1, 1, 1, 1, (0), imm3, Rd, imm2, type_, Rm),
    ('NOP<c>.W', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ('ORN{S}<c> <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 0, 0, 1, 1, S, Rn, 0, imm3, Rd, imm8),
    ('ORN{S}<c> <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    ('ORR{S}<c> <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 0, 0, 1, 0, S, Rn, 0, imm3, Rd, imm8),
    ('ORR{S}<c>.W <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    #('PKHBT<c> <Rd>, <Rn>, <Rm>{, LSL #<imm>}', 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, S, Rn, (0), imm3, Rd, imm2, tb, T, Rm),
    ('PLD{W}<c> [<Rn>, #<imm12>]', 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, W, 1, Rn, 1, 1, 1, 1, imm12),
    ('PLD{W}<c> [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, W, 1, Rn, 1, 1, 1, 1, 1, 1, 0, 0, imm8),
    ('PLD<c> <label>', 1, 1, 1, 1, 1, 0, 0, 0, U, 0, (0), 1, 1, 1, 1, 1, 1, 1, 1, 1, imm12),
    #('PLD{W}<c> [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, W, 1, Rn, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, imm2, Rm),
    ('PLI<c> [<Rn>, #<imm12>]', 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, Rn, 1, 1, 1, 1, imm12),
    ('PLI<c> [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, 1, 1, 1, 1, 1, 1, 0, 0, imm8),
    ('PLI<c> <label>', 1, 1, 1, 1, 1, 0, 0, 1, U, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, imm12),
    #('PLI<c> [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, imm2, Rm),
    ('POP<c>.W <registers>', 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, P, M, (0), register_list),
    ('POP<c>.W <registers>', 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, Rt, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0),
    #('PUSH<c>.W <registers>', 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, (0), M, (0), register_list),
    #('PUSH<c>.W <registers>', 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, Rt, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0),
    ('QADD<c> <Rd>, <Rm>, <Rn>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 0, 0, Rm),
    ('QADD16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm),
    ('QADD8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm),
    ('QASX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm),
    ('QDADD<c> <Rd>, <Rm>, <Rn>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 0, 1, Rm),
    ('QDSUB<c> <Rd>, <Rm>, <Rn>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 1, 1, Rm),
    ('QSAX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm),
    ('QSUB<c> <Rd>, <Rm>, <Rn>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 1, 0, Rm),
    ('QSUB16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm),
    ('QSUB8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm),
    ('RBIT<c> <Rd>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 1, 0, Rm),
    ('REV<c>.W <Rd>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 0, 0, Rm),
    ('REV16<c>.W <Rd>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 0, 1, Rm),
    ('REVSH<c>.W <Rd>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 1, 1, Rm),
    ('ROR{S}<c> <Rd>, <Rm>, #<imm>', 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), imm3, Rd, imm2, 1, 1, Rm),
    ('ROR{S}<c>.W <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, S, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('RRX{S}<c> <Rd>, <Rm>', 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), 0, 0, 0, Rd, 0, 0, 1, 1, Rm),
    ('RSB{S}<c>.W <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 1, 1, 1, 0, S, Rn, 0, imm3, Rd, imm8),
    ('RSB{S}<c> <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    ('SADD16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('SADD8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('SASX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('SBC{S}<c> <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 1, 0, 1, 1, S, Rn, 0, imm3, Rd, imm8),
    ('SBC{S}<c>.W <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    ('SBFX<c> <Rd>, <Rn>, #<lsb>, #<width>', 1, 1, 1, 1, 0, (0), 1, 1, 0, 1, 0, 0, Rn, 0, imm3, Rd, imm2, (0), widthm1),
    ('SDIV<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, Rn, (1), (1), (1), (1), Rd, 1, 1, 1, 1, Rm),
    ('SEL<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 0, 0, Rm),
    ('SEV<c>.W', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
    ('SHADD16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm),
    ('SHADD8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm),
    ('SHASX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm),
    ('SHSAX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm),
    ('SHSUB16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm),
    ('SHSUB8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm),
    ('SMLA<x><y><c> <Rd>, <Rn>, <Rm>, <Ra>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, Ra, Rd, 0, 0, N, M, Rm),
    ('SMLAD{X}<c> <Rd>, <Rn>, <Rm>, <Ra>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, Rn, Ra, Rd, 0, 0, 0, M, Rm),
    ('SMLAL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 0, 0, 0, 0, Rm),
    ('SMLAL<x><y><c> <RdLo>, <RdHi>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 1, 0, N, M, Rm),
    ('SMLALD{X}<c> <RdLo>, <RdHi>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 1, 1, 0, M, Rm),
    ('SMLAW<y><c> <Rd>, <Rn>, <Rm>, <Ra>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, Rn, Ra, Rd, 0, 0, 0, M, Rm),
    ('SMLSD{X}<c> <Rd>, <Rn>, <Rm>, <Ra>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, Rn, Ra, Rd, 0, 0, 0, M, Rm),
    ('SMLSLD{X}<c> <RdLo>, <RdHi>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, Rn, RdLo, RdHi, 1, 1, 0, M, Rm),
    ('SMMLA{R}<c> <Rd>, <Rn>, <Rm>, <Ra>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, Rn, Ra, Rd, 0, 0, 0, R, Rm),
    ('SMMLS{R}<c> <Rd>, <Rn>, <Rm>, <Ra>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, Rn, Ra, Rd, 0, 0, 0, R, Rm),
    ('SMMUL{R}<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, R, Rm),
    ('SMUAD{X}<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, M, Rm),
    ('SMUL<x><y><c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, N, M, Rm),
    ('SMULL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, Rn, RdLo, RdHi, 0, 0, 0, 0, Rm),
    ('SMULW<y><c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, M, Rm),
    ('SMUSD{X}<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, M, Rm),
    #('SSAT<c> <Rd>, #<imm>, <Rn>{, <shift>}', 1, 1, 1, 1, 0, (0), 1, 1, 0, 0, sh, 0, Rn, 0, imm3, Rd, imm2, (0), sat_imm),
    #('SSAT16<c> <Rd>, #<imm>, <Rn>', 1, 1, 1, 1, 0, (0), 1, 1, 0, 0, 1, 0, Rn, 0, 0, 0, 0, Rd, 0, 0, (0), (0), sat_imm),
    ('SSAX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('SSUB16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('SSUB8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('STM<c>.W <Rn>{!}, <registers>', 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, W, 0, Rn, (0), M, (0), register_list),
    # TODO: make sure this is a dup of above
    #('STR<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm),
    ('STRB<c>.W <Rt>, [<Rn>, #<imm12>]', 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, Rn, Rt, imm12),
    #('STRB<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, Rn, Rt, 1, P, U, W, imm8),
    #('STRB<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, Rn, Rt, 1, P, U, W, imm8),
    #('STRB<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm),
    ('STRBT<c> <Rt>, [<Rn>, #<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, Rn, Rt, 1, 1, 1, 0, imm8),
    ('STRD<c> <Rt>, <Rt2>, [<Rn>{, #+/-<imm>}]', 1, 1, 1, 0, 1, 0, 0, P, U, 1, W, 0, Rn, Rt, Rt2, imm8),
    ('STREX<c> <Rd>, <Rt>, [<Rn>{, #<imm>}]', 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, Rn, Rt, Rd, imm8),
    ('STREXB<c> <Rd>, <Rt>, [<Rn>]', 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, Rn, Rt, (1), (1), (1), (1), 0, 1, 0, 0, Rd),
    ('STREXD<c> <Rd>, <Rt>, <Rt2>, [<Rn>]', 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, Rn, Rt, Rt2, 0, 1, 1, 1, Rd),
    ('STREXH<c> <Rd>, <Rt>, [<Rn>]', 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, Rn, Rt, (1), (1), (1), (1), 0, 1, 0, 1, Rd),
    ('STRH<c>.W <Rt>, [<Rn>{, #<imm12>}]', 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, Rn, Rt, imm12),
    #('STRH<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, Rn, Rt, 1, P, U, W, imm8),
    #('STRH<c> <Rt>, [<Rn>, #-<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, Rn, Rt, 1, P, U, W, imm8),
    #('STRH<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm),
    ('STRHT<c> <Rt>, [<Rn>, #<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, Rn, Rt, 1, 1, 1, 0, imm8),
    ('STRT<c> <Rt>, [<Rn>, #<imm8>]', 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, Rn, Rt, 1, 1, 1, 0, imm8),
    #('SUB{S}<c>.W <Rd>, <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 1, 1, 0, 1, S, Rn, 0, imm3, Rd, imm8),
    ('SUBW<c> <Rd>, <Rn>, #<imm12>', 1, 1, 1, 1, 0, i, 1, 0, 1, 0, 1, 0, Rn, 0, imm3, Rd, imm8),
    #('SUB{S}<c>.W <Rd>, <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, S, Rn, (0), imm3, Rd, imm2, type_, Rm),
    # TODO:
    #('SUB{S}<c>.W <Rd>, SP, #<const>', 1, 1, 1, 1, 0, i, 0, 1, 1, 0, 1, S, 1, 1, 0, 1, 0, imm3, Rd, imm8),
    ('SUBW<c> <Rd>, SP, #<imm12>', 1, 1, 1, 1, 0, i, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, imm3, Rd, imm8),
    ('SUB{S}<c> <Rd>, SP, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, S, 1, 1, 0, 1, (0), imm3, Rd, imm2, type_, Rm),
    ('SXTAB<c> <Rd>, <Rn>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('SXTAB16<c> <Rd>, <Rn>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('SXTAH<c> <Rd>, <Rn>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('SXTB<c>.W <Rd>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('SXTB16<c> <Rd>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('SXTH<c>.W <Rd>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('TEQ<c> <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 0, 1, 0, 0, 1, Rn, 0, imm3, 1, 1, 1, 1, imm8),
    ('TEQ<c> <Rn>, <Rm>{, <shift>}', 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, Rn, (0), imm3, 1, 1, 1, 1, imm2, type_, Rm),
    ('TST<c> <Rn>, #<const>', 1, 1, 1, 1, 0, i, 0, 0, 0, 0, 0, 1, Rn, 0, imm3, 1, 1, 1, 1, imm8),
    ('TST<c>.W', 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, Rn, (0), imm3, 1, 1, 1, 1, imm2, type_, Rm),
    ('UADD16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm),
    ('UADD8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm),
    ('UASX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm),
    ('UBFX<c> <Rd>, <Rn>, #<lsb>, #<width>', 1, 1, 1, 1, 0, (0), 1, 1, 1, 1, 0, 0, Rn, 0, imm3, Rd, imm2, (0), widthm1),
    ('UDF<c>.W #<imm16>', 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, imm4, 1, 0, 1, 0, imm12),
    ('UDIV<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, Rn, (1), (1), (1), (1), Rd, 1, 1, 1, 1, Rm),
    ('UHADD16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm),
    ('UHADD8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm),
    ('UHASX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm),
    ('UHSAX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm),
    ('UHSUB16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm),
    ('UHSUB8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm),
    ('UMAAL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, Rn, RdLo, RdHi, 0, 1, 1, 0, Rm),
    ('UMLAL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, Rn, RdLo, RdHi, 0, 0, 0, 0, Rm),
    ('UMULL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, Rn, RdLo, RdHi, 0, 0, 0, 0, Rm),
    ('UQADD16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm),
    ('UQADD8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm),
    ('UQASX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm),
    ('UQSAX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm),
    ('UQSUB16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm),
    ('UQSUB8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm),
    ('USAD8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm),
    ('USADA8<c> <Rd>, <Rn>, <Rm>, <Ra>', 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, Rn, Ra, Rd, 0, 0, 0, 0, Rm),
    #('USAT<c> <Rd>, #<imm5>, <Rn>{, <shift>}', 1, 1, 1, 1, 0, (0), 1, 1, 1, 0, sh, 0, Rn, 0, imm3, Rd, imm2, (0), sat_imm),
    #('USAT16<c> <Rd>, #<imm4>, <Rn>', 1, 1, 1, 1, 0, (0), 1, 1, 1, 0, 1, 0, Rn, 0, 0, 0, 0, Rd, 0, 0, (0), (0), sat_imm),
    ('USAX<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm),
    ('USUB16<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm),
    ('USUB8<c> <Rd>, <Rn>, <Rm>', 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm),
    ('UXTAB<c> <Rd>, <Rn>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('UXTAB16<c> <Rd>, <Rn>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, Rd, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('UXTAH<c> <Rd>, <Rn>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('UXTB<c>.W <Rd>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('UXTB16<c> <Rd>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('UXTH<c>.W <Rd>, <Rm>{, <rotation>}', 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm),
    ('WFE<c>.W', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
    ('WFI<c>.W', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1),
    ('YIELD<c>.W', 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
]

if __name__ == '__main__':
    num = 0
    for description in thumb16:
        instr = description[0]
        bits = description[1:]

        bits = [1 if type(x) == int else x.bitsize for x in bits]
        if sum(bits) != 16:
            print(instr, bits, sum(bits))
        num += 1
    print "Verified " + str(num) + " 16-bit thumb2 instructions"

    num = 0
    for description in thumb32:
        instr = description[0]
        bits = description[1:]

        bits = [1 if type(x) == int else x.bitsize for x in bits]
        if sum(bits) != 32:
            print(instr, bits, sum(bits))
        num += 1
    print "Verified " + str(num) + " 32-bit thumb2 instructions"
