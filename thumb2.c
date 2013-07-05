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
#define IS_THUMB2_32BIT(__sw) ((((__sw >> 13) & 0b111) == 0b111) && (((__sw >> 11) & 0b11) != 0b00))

int darm_thumb2_disasm16(darm_t *d, uint16_t w)
{
    darm_lookup_t* lkup;

    lkup = &(thumb2_16_instr_lookup[GETBT(w, 5, 7)]);
    if (I_INVLD == lkup->instr) return -1;

    //printf("look idx %d\n", GETBT(w, 5, 7));

    d->instr = lkup->instr;
    d->instr_type = lkup->instr_type;
    d->mode = M_THUMB2_16;
    d->size = 2;
    d->cond = C_AL;    

    switch((uint32_t)d->instr_type){
    case T_THUMB2_BR_CONDZERO:
        d->Rn = GETBT(w, 0, 3);
        d->I = B_SET;
        d->imm = GETBT(w, 3, 5);
        return 0;

    case T_THUMB2_DATA_EXTEND:
        d->Rm = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        return 0;

    case T_THUMB2_PSHPOP:
        d->W = B_SET;
        d->reglist = GETBT(w, 0, 8);
        return 0;

    case T_THUMB2_SETEND:
        d->E = GETBT(w, 3, 1);
        return 0;

    case T_THUMB2_PROC_STATE:
        d->S = B_SET;
        d->cpsr = (GETBT(w, 0, 3) << 6);
        return 0;

    case T_THUMB2_BYTE_REVERSE:
        d->Rm = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        return 0;

    case T_THUMB2_BREAKPOINT:
        return 0;

    case T_THUMB2_IT:
        d->instr = I_IT;

        switch(GETBT(w, 8, 4)){
        case 0b0000:
            d->instr = I_NOP;
            break;
        case 0b0001:
            d->instr = I_YIELD;
            break;
        case 0b0010:
            d->instr = I_WFE;
            break;
        case 0b0011:
            d->instr = I_WFI;
            break;
        case 0b0100:
            d->instr = I_SEV;
            break;
        }

        if (GETBT(w, 0, 4)){
            if (I_IT != d->instr){
                return -1;
            }
        }

        // I_IT instructions should never appear in assembled code
        if (I_IT == d->instr) return -1;
        return 0;

    default:
        return -1;
    }

    return -1;
}

int darm_thumb2_disasm(darm_t *d, uint16_t w, uint16_t w2)
{
    (void)d; (void) w; (void) w2;
    uint16_t tmp = 0;
    int ret;
    
    // try 16bit first
    if (!IS_THUMB2_32BIT(w)){
        // first try thumb1
        ret = darm_thumb_disasm(d, w);

        // if thumb1 fails, try 16-bit thumb2
        if (ret){
            return darm_thumb2_disasm16(d, w);
        }

        return ret;
    }

    d->size = 4;
    d->mode = M_THUMB2;

    // 32-bit


    /*

    d->instr = thumb_instr_labels[w >> 8];
    d->instr_type = thumb_instr_types[w >> 8];
    d->mode = M_THUMB;
    
    // TODO: detect 32-bit thumb2
    d->size = 2;

    // TODO: squashes 16/32bit together?
    d->cond = C_AL;
    switch ((uint32_t) d->instr_type) {
    case T_THUMB_ONLY_IMM8:
        d->I = B_SET;
        d->imm = w & 0xff;
        return 0;
    case T_THUMB_PUSHPOP:
        if((w>>11) & 1)
            d->instr = I_POP;
        else
            d->instr = I_PUSH;
        d->reglist = ((w) & BITMSK_8);
        d->reglist |= (((w>>8)&1)<<14); // or in the LR(9th bit)
        return 0;
    case T_THUMB_REG_IMM:
        tmp = (w>>11) & 0b11;
        if(tmp == 0b10)
            d->instr = I_ADDS;
        else if(tmp == 0b11)
            d->instr = I_SUBS;
        else if(tmp == 0b00)
            d->instr = I_MOVS;
        d->Rd = (w >> 8) & 0b111;
        d->imm = w & BITMSK_8;
        d->I = B_SET;
        return 0;
    case T_THUMB_ARITH_REG_REG:
        tmp = (w>>9) & 0b11;
        if(tmp == 0b1)
            d->instr = I_SUBS;
        else if (tmp == 0b0)
            d->instr = I_ADDS;
        d->Rd = (w) & 0b111;
        d->Rn = (w>>3) & 0b111;
        d->Rm = (w>>6) & 0b111;
        return 0;

    case T_THUMB_ARITH_STACK:
        d->Rn = SP;
        d->I = B_SET;
        switch((w >> 11)){
        case 0b10101:
            d->Rd = (w >> 8) & 0b111;
            d->imm = (w & BITMSK_8) << 2;
            return 0;
        case 0b10110:
            d->instr = (w >> 7) & 1 ? I_SUB : I_ADD;
            d->Rd = SP;
            d->imm = (w & BITMSK_7) << 2;
            return 0;
        }
    }
        */
    return -1;
}
