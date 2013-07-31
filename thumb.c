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

static int thumb_disasm(darm_t *d, uint16_t w)
{
    uint8_t h1, h2, r1, r2;
    darm_lookup_t* lkup;

    lkup = &(thumb_instr_lookup[w >> 6]);
    if (I_INVLD == lkup->instr) return -1;

    d->instr = lkup->instr;
    d->instr_type = lkup->instr_type;
    d->mode = M_THUMB;
    d->size = 2;
    d->cond = C_AL;

    switch ((uint32_t) d->instr_type){

    case T_THUMB_DST_SRC:
        d->S = B_SET;
        d->I = B_SET;
        d->imm = GETBT(w, 6, 5);
        d->Rm = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        return 0;

    case T_THUMB_ARITH:
        d->S = B_SET;
        d->Rm = GETBT(w, 6, 3);
        if (GETBT(w, 10, 1)){
            d->I = B_SET;
            d->imm = d->Rm;
            d->Rm = R_INVLD;
        }
        d->Rn = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        return 0;

    case T_THUMB_ARITH_IMM:
        d->S = B_SET;
        d->Rn = GETBT(w, 8, 3);
        d->Rd = d->Rn;
        if (I_MOVS == d->instr){
            d->Rn = R_INVLD;
        }
        if (I_CMP == d->instr){
            d->Rd = R_INVLD;
        }
        d->I = B_SET;
        d->imm = GETBT(w, 0, 8);
        return 0;

    case T_THUMB_ALU:
        d->S = B_SET;
        d->Rm = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        d->Rn = d->Rd;
        if (I_CMN == d->instr || I_CMP == d->instr){
            d->Rd = R_INVLD;
        }
        if (I_MVN == d->instr){
            d->Rn = R_INVLD;
        }
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
            d->S = B_SET;
            break;
        case I_BLX:
        case I_BX:
            d->Rm = r2;
            d->instr = h1? I_BLX : I_BX;
            break;
        default:
            return -1;
        }
        return 0;

    case T_THUMB_LOAD_PCREL:
        d->P = B_SET;
        d->Rt = GETBT(w, 8, 3);
        d->I = B_SET;
        d->imm = (GETBT(w, 0, 8) << 2);
        d->Rn = PC;
        // TODO: add 4 more to imm?
        return 0;

    case T_THUMB_LDST_REG:
        d->P = B_SET;
        d->Rt = GETBT(w, 0, 3);
        d->Rn = GETBT(w, 3, 3);
        d->Rm = GETBT(w, 6, 3);
        return 0;

    case T_THUMB_LDST_IMM:
        d->P = B_SET;
        d->Rt = GETBT(w, 0, 3);
        d->Rn = GETBT(w, 3, 3);
        d->I = B_SET;
        if (I_LDRB == d->instr || I_STRB == d->instr){
            d->imm = (GETBT(w, 6, 5) << 0);
        } else if (I_LDRH == d->instr || I_STRH == d->instr){
            d->imm = (GETBT(w, 6, 5) << 1);
        } else if (I_LDR == d->instr || I_STR == d->instr){
            d->imm = (GETBT(w, 6, 5) << 2);
        } else {
            return -1;
        }
        return 0;        

    case T_THUMB_LDST_SPREL:
    case T_THUMB_LOAD_ADDR:
        if (I_ADD == d->instr || I_ADR == d->instr){
            d->P = B_INVLD;
            d->Rd = GETBT(w, 8, 3);
        } else {
            d->P = B_SET;
            d->Rt = GETBT(w, 8, 3);
        }
        d->I = B_SET;
        d->imm = (GETBT(w, 0, 8) << 2);
        d->Rn = SP;
        if (I_ADR == d->instr){
            d->Rn = PC;
        }
        return 0;

    case T_THUMB_ADD_SP:
        d->Rd = SP;
        d->Rn = SP;
        d->I = B_SET;
        d->imm = (GETBT(w, 0, 7) << 2);
        return 0;

    case T_THUMB_PSHPOP:
        // TODO: implicit SP def/use
        d->reglist = GETBT(w, 0, 8);
        if (GETBT(w, 8, 1)){
            if (I_PUSH == d->instr) d->reglist |= (1 << LR);
            else if (I_POP == d->instr) d->reglist |= (1 << PC);
            else return -1;
        }
        return 0;

    case T_THUMB_LDST_MULTI:
        d->reglist = GETBT(w, 0, 8);
        d->W = B_SET;
        d->Rn = GETBT(w, 8, 3);
        return 0;

    case T_THUMB_BR_COND:
    case T_THUMB_SWINT:
        d->cond = GETBT(w, 8, 4);
        d->I = B_SET;
        d->imm = GETBT(w, 0, 8);
        if (I_SVC != d->instr) d->imm <<= 1;
        if (T_THUMB_BR_COND == d->instr_type){
            d->imm = sign_ext32(d->imm, 8);
        }
        if (d->cond == 0b1110) return -1;
        return 0;

    case T_THUMB_BR_UNCOND:
        d->I = B_SET;
        d->imm = (GETBT(w, 0, 11) << 1);
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
    d->dtype = D_INVLD;
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
