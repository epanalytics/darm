/*
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
*/

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "darm.h"
#include "thumb-tbl.h"

// TODO: move to common loc
#define BITMSK_1 ((1 << 1) - 1)
#define BITMSK_2 ((1 << 2) - 1)
#define BITMSK_3 ((1 << 3) - 1)
#define BITMSK_4 ((1 << 4) - 1)
#define BITMSK_5 ((1 << 5) - 1)
#define BITMSK_6 ((1 << 6) - 1)
#define BITMSK_7 ((1 << 7) - 1)
#define BITMSK_8 ((1 << 8) - 1)
#define GETBT(__v, __o, __n) ((__v >> __o) & BITMSK_ ## __n)

static int thumb_disasm(darm_t *d, uint16_t w)
{
    uint8_t h1, h2, r1, r2;

    d->instr = thumb_instr_labels[w >> 8];
    d->instr_type = thumb_instr_types[w >> 8];
    d->isthumb = 1;
    d->size = 2;
    d->cond = C_AL;

    // TODO: handle thumb1 here only?
    // TODO: only need name lookups when >8 bits?
    switch ((uint32_t) d->instr_type){
    case T_THUMB_DST_SRC:
        d->instr = type_thumb_dstsrc_instr_lookup[GETBT(w, 11, 2)];
        d->I = B_SET;
        d->imm = GETBT(w, 6, 6);
        d->Rm = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        return 0;
    case T_THUMB_ARITH:
        d->instr = type_thumb_arith_instr_lookup[GETBT(w, 9, 1)];
        if (GETBT(w, 10, 1)){
            d->I = B_SET;
            d->imm = GETBT(w, 6, 3);
        } else {
            d->Rn = GETBT(w, 6, 3);
        }
        d->Rm = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        return 0;
    case T_THUMB_ARITH_IMM:
        d->instr = type_thumb_arithimm_instr_lookup[GETBT(w, 11, 2)];
        d->Rd = GETBT(w, 8, 3);
        d->I = B_SET;
        d->imm = GETBT(w, 0, 8);
        return 0;
    case T_THUMB_ALU:
        d->instr = type_thumb_alu_instr_lookup[GETBT(w, 6, 4)];
        d->Rm = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        return 0;

    case T_THUMB_HIREG_BX:
        h1 = GETBT(w, 7, 1);
        h2 = GETBT(w, 6, 1);

        r1 = GETBT(w, 0, 3) + (h1? 8 : 0);
        r2 = GETBT(w, 3, 3) + (h2? 8 : 0);

        switch((uint32_t)d->instr){
        case I_ADD:
            d->Rd = r1;
            d->Rn = r1;
            d->Rm = r2;
            break;
        case I_MOV:
            d->Rd = r1;
            d->Rm = r2;
            break;
        case I_CMP:
            d->Rn = r1;
            d->Rm = r2;
            break;
        case I_BX:
            d->Rm = r2;
            d->instr = h1? I_BLX : I_BX;
            break;
        }
        return 0;

    case T_THUMB_LOAD:
        d->instr = I_LDR;
        d->Rd = GETBT(w, 8, 3);
        d->I = B_SET;
        d->imm = (GETBT(w, 0, 8) << 2);
        d->Rm = PC;
        return 0;
    }
    return -1;
}

int darm_thumb_disasm(darm_t *d, uint16_t w)
{
    memset(d, 0, sizeof(darm_t));
    d->instr = I_INVLD;
    d->instr_type = T_INVLD;
    d->shift_type = S_INVLD;
    d->S = d->E = d->U = d->H = d->P = d->I = B_INVLD;
    d->R = d->T = d->W = d->M = d->N = d->B = B_INVLD;
    d->Rd = d->Rn = d->Rm = d->Ra = d->Rt = R_INVLD;
    d->Rt2 = d->RdHi = d->RdLo = d->Rs = R_INVLD;
    d->option = O_INVLD;

    switch (w >> 11) {
    case 0b11101: case 0b11110: case 0b11111:
        return -1;

    default:
        d->w = w;
        return thumb_disasm(d, w);
    }
}
