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

# just thumb1 here
# https://ece.uwaterloo.ca/~ece222/ARM/ARM7-TDMI-manual-pt3.pdf
# http://www.ittc.ku.edu/~kulkarni/research/thumb_ax.pdf
thumbs = [
    # THUMB_DST_SRC
    ('ADDS <Rd>, <Rn>, <Rm>',    0, 0, 0, 1, 1, 0, 0, Rm3, Rn3, Rd3),
    ('ADDS <Rd>, <Rm>, #<imm3>', 0, 0, 0, 1, 1, 1, 0, imm3, Rn3, Rd3),
    ('SUBS <Rd>, <Rn>, <Rm>',    0, 0, 0, 1, 1, 0, 1, Rm3, Rn3, Rd3),
    ('SUBS <Rd>, <Rm>, #<imm3>', 0, 0, 0, 1, 1, 1, 1, imm3, Rn3, Rd3),

    # THUMB_ARITH
    ('ASR <Rd>, <Rm>, #<imm5>', 0, 0, 0, 1, 0, imm5, Rm3, Rd3),
    ('LSL <Rd>, <Rm>, #<imm5>', 0, 0, 0, 0, 0, imm5, Rm3, Rd3),
    ('LSR <Rd>, <Rm>, #<imm5>', 0, 0, 0, 0, 1, imm5, Rm3, Rd3),
    ('MOVS <Rd>, <Rm>',       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Rm3, Rd3), # special case of LSL

    # THUMB_ARITH_IMM
    ('ADDS <Rdn>, #<imm8>', 0, 0, 1, 1, 0, Rdn3, imm8),
    ('CMP <Rn>, #<imm8>',     0, 0, 1, 0, 1, Rn3, imm8),
    ('MOVS <Rd>, #<imm8>',  0, 0, 1, 0, 0, Rd3, imm8),
    ('SUBS <Rdn>, #<imm8>', 0, 0, 1, 1, 1, Rdn3, imm8),

    # THUMB_ALU
    ('ADC <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, Rm3, Rdn3),
    ('AND <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, Rm3, Rdn3),
    ('ASR <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, Rm3, Rdn3),
    ('BIC <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, Rm3, Rdn3),
    ('CMN <Rn>, <Rm>',  0, 1, 0, 0, 0, 0, 1, 0, 1, 1, Rm3, Rn3),
    ('CMP <Rn>, <Rm>',  0, 1, 0, 0, 0, 0, 1, 0, 1, 0, Rm3, Rn3),
    ('EOR <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, Rm3, Rdn3),
    ('LSL <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, Rm3, Rdn3),
    ('LSR <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, Rm3, Rdn3),
    ('MUL <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, Rm3, Rdn3),
    ('MVN <Rd>, <Rm>',  0, 1, 0, 0, 0, 0, 1, 1, 1, 1, Rm3, Rd3),
    ('ORR <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, Rm3, Rdn3),
    ('ROR <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, Rm3, Rdn3),
    ('RSB <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, Rm3, Rdn3),
    ('SBC <Rdn>, <Rm>', 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, Rm3, Rdn3),
    ('TST <Rn>, <Rm>',  0, 1, 0, 0, 0, 0, 1, 0, 0, 0, Rm3, Rn3),

    # THUMB_HIREGBX
    ('ADD <Rdn>, <Rm>', 0, 1, 0, 0, 0, 1, 0, 0, M, DN, Rm3, Rdn3),
    ('BLX <Rm>',        0, 1, 0, 0, 0, 1, 1, 1, 1, Rm, (0), (0), (0)),
    ('BX <Rm>',         0, 1, 0, 0, 0, 1, 1, 1, 0, Rm, (0), (0), (0)),
    ('CMP <Rn>, <Rm>',  0, 1, 0, 0, 0, 1, 0, 1, M, N, Rm3, Rn3),
    ('MOV <Rd>, <Rm>',  0, 1, 0, 0, 0, 1, 1, 0, M, D, Rm3, Rd3),

    # THUMB_LOAD_PCREL
    ('LDR <Rt>, [PC=<Rn>,#<imm8>]', 0, 1, 0, 0, 1, Rt3, imm8),

    # THUMB_LDST_REGOFF
    ('LDR <Rt>, [<Rn>,<Rm>]',   0, 1, 0, 1, 1, 0, 0, Rm3, Rn3, Rt3),
    ('LDRB <Rt>, [<Rn>,<Rm>]',  0, 1, 0, 1, 1, 1, 0, Rm3, Rn3, Rt3),
    ('LDRH <Rt>, [<Rn>,<Rm>]',  0, 1, 0, 1, 1, 0, 1, Rm3, Rn3, Rt3),
    ('LDRSB <Rt>, [<Rn>,<Rm>]', 0, 1, 0, 1, 0, 1, 1, Rm3, Rn3, Rt3),
    ('LDRSH <Rt>, [<Rn>,<Rm>]', 0, 1, 0, 1, 1, 1, 1, Rm3, Rn3, Rt3),
    ('STR <Rt>, [<Rn>,<Rm>]',   0, 1, 0, 1, 0, 0, 0, Rm3, Rn3, Rt3),
    ('STRB <Rt>, [<Rn>,<Rm>]',  0, 1, 0, 1, 0, 1, 0, Rm3, Rn3, Rt3),
    ('STRH <Rt>, [<Rn>,<Rm>]',  0, 1, 0, 1, 0, 0, 1, Rm3, Rn3, Rt3),

    # THUMB_LDST_IMM
    ('LDR <Rt>, [<Rn>,#<imm5>]',  0, 1, 1, 0, 1, imm5, Rn3, Rt3),
    ('LDRB <Rt>, [<Rn>,#<imm5>]', 0, 1, 1, 1, 1, imm5, Rn3, Rt3),
    ('LDRH <Rt>, [<Rn>,#<imm5>]', 1, 0, 0, 0, 1, imm5, Rn3, Rt3),
    ('STR <Rt>, [<Rn>,#<imm5>]',  0, 1, 1, 0, 0, imm5, Rn3, Rt3),
    ('STRB <Rt>, [<Rn>,#<imm5>]', 0, 1, 1, 1, 0, imm5, Rn3, Rt3),
    ('STRH <Rt>, [<Rn>,#<imm5>]', 1, 0, 0, 0, 0, imm5, Rn3, Rt3),

    # THUMB_LDST_SPREL
    ('LDR <Rt>, [SP=<Rn>,#<imm8>]', 1, 0, 0, 1, 1, Rt3, imm8),
    ('STR <Rt>, [SP=<Rn>,#<imm8>]', 1, 0, 0, 1, 0, Rt3, imm8),

    # THUMB_LOAD_ADDR (like LEA in x86)
    ('ADD <Rd>, SP=<Rn>, #<imm8>', 1, 0, 1, 0, 1, Rd3, imm8),
    ('ADR <Rd>, PC=<Rn>, #<imm8>', 1, 0, 1, 0, 0, Rd3, imm8),

    # THUMB_ADD_SP
    ('ADD SP=<Rd>, SP=<Rn>, #<imm7>', 1, 0, 1, 1, 0, 0, 0, 0, 0, imm7),
    ('SUB SP=<Rd>, SP=<Rn>, #<imm7>', 1, 0, 1, 1, 0, 0, 0, 0, 1, imm7),

    # THUMB_PSHPOP
    ('POP <registers>',  1, 0, 1, 1, 1, 1, 0, P, register_list8),
    ('PUSH <registers>', 1, 0, 1, 1, 0, 1, 0, M, register_list8),

    # THUMB_LDST_MULTI
    ('LDM <Rn>!, <registers>', 1, 1, 0, 0, 1, Rn3, register_list8),
    ('STM <Rn>!, <registers>', 1, 1, 0, 0, 0, Rn3, register_list8),

    # THUMB_BR_COND
    ('B<c> <label>', 1, 1, 0, 1, cond, imm8),

    # THUMB_SWINT
    ('SVC #<imm8>', 1, 1, 0, 1, 1, 1, 1, 1, imm8),

    # THUMB_BR_UNCOND
    ('B <label>', 1, 1, 1, 0, 0, imm11),
]

if __name__ == '__main__':
    num = 0
    for description in thumbs:
        instr = description[0]
        bits = description[1:]

        bits = [1 if type(x) == int else x.bitsize for x in bits]
        if sum(bits) != 16:
            print(instr, bits, sum(bits))
        num += 1
    print "Verified " + str(num) + " thumb1 instructions"
