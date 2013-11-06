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
#include <assert.h>

#include "darm.h"
#include "thumb-tbl.h"
#include "ext-tbl.h"

int darm_thumb2_disasm32(darm_t *d, uint32_t w)
{
    darm_lookup_t* lkup;
    uint32_t op, op1, op2;

    d->w = w;
    d->size = 4;
    d->mode = M_THUMB2;
    d->cond = C_AL;    

    lkup = &(THUMB2_INSTR_LOOKUP(w));
    if (I_INVLD == lkup->instr) {
        fprintf(stderr, "darm_thumb2_disasm32: null lookup: %u for 0x%lx\n", THUMB2_LOOKUP_INDEX(w), w);
        return -1;
    }

    d->instr = lkup->instr;
    d->instr_type = lkup->instr_type;

    switch((uint32_t)d->instr_type){
    case T_THUMB2_BRANCH:
        op = GETBT(w, 20, 7);
        op1 = GETBT(w, 12, 3);
        op2 = GETBT(w, 8, 4);
        op2 |= 0;

        // Conditional branch
        if (0b0 == GETBT(op1, 2, 1) && 0b0 == GETBT(op1, 0, 1) && 0b111 != GETBT(op, 3, 3)){
            d->instr = I_B; 
            d->cond = GETBT(w, 22, 4);

            d->I = B_SET;
            d->imm = (GETBT(w, 16,  6) << 12) | (GETBT(w, 0, 11) << 1);
            d->imm = sign_ext32(d->imm, 18);
        }

        // Unconditional branch
        else if (0b0 == GETBT(op1, 2, 1) && 0b1 == GETBT(op1, 0, 1)){
            d->instr = I_B; 

            d->I = B_SET;
            d->imm = (GETBT(w, 16, 10) << 12) | (GETBT(w, 0, 11) << 1);
            d->imm = sign_ext32(d->imm, 22);
        }

        // Branch and exchange Jazelle
        else if (0b0 == GETBT(op1, 2, 1) && 0b0 == GETBT(op1, 0, 1) && 0b0111100 == op){
            d->instr = I_BXJ;
            d->Rm = GETBT(w, 16, 4);
        }

        // Branch with link
        else if (0b1 == GETBT(op1, 2, 1) && 0b1 == GETBT(op1, 0, 1)){
            d->instr = I_BL;

            d->I = B_SET;
            d->imm = (GETBT(w, 16, 10) << 12) | (GETBT(w, 0, 11) << 1);
            d->imm = sign_ext32(d->imm, 22);
        }

        // Branch with link and exchange
        else if (0b1 == GETBT(op1, 2, 1) && 0b0 == GETBT(op1, 0, 1)){
            d->instr = I_BLX;
            d->H = GETBT(w, 0, 1);

            // TODO: when added to PC, PC must first be 4-aligned
            d->I = B_SET;
            d->imm = (GETBT(w, 16, 10) << 12) | (GETBT(w, 1, 10) << 2);
            d->imm = sign_ext32(d->imm, 22);
        }

        else {
            fprintf(stderr, "darm_thumb2_disasm32: unhandled branch\n");
            return -1;
        }

        return 0;

    case T_THUMB2_TABLE_BRANCH:
        d->Rn = GETBT(w, 16, 4);
        d->Rm = GETBT(w, 0, 4);

        d->instr = GETBT(w, 4, 1)? I_TBH: I_TBB;
        if (I_TBH == d->instr){
            d->shift_type = S_LSL;
            d->shift = 1;
        }

        return 0;
        
    default:
        fprintf(stderr, "darm_thumb2_disasm32: unhandled type: %d\n", d->instr_type);
        return -1;

    }
    fprintf(stderr, "darm_thumb2_disasm32: unreachable\n");
    return -1;

}

int darm_thumb2_disasm16(darm_t *d, uint16_t w)
{
    darm_lookup_t* lkup;

    lkup = &(THUMB2_16_INSTR_LOOKUP(w));
    if (I_INVLD == lkup->instr) {
        fprintf(stderr, "darm_thumb2_disasm16: null lookup: %u\n", THUMB2_16_LOOKUP_INDEX(w));
        return -1;
    }

    d->w = w;
    d->instr = lkup->instr;
    d->instr_type = lkup->instr_type;
    d->mode = M_THUMB2_16;
    d->size = 2;
    d->cond = C_AL;    

    switch((uint32_t)d->instr_type){
    case T_THUMB2_16_BR_CONDZERO:
        d->Rn = GETBT(w, 0, 3);
        d->I = B_SET;
        d->imm = GETBT(w, 3, 5) << 1;
        return 0;

    case T_THUMB2_16_DATA_EXTEND:
        d->Rm = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        return 0;

    case T_THUMB2_16_PSHPOP:
        d->W = B_SET;
        d->reglist = GETBT(w, 0, 8);
        return 0;

    case T_THUMB2_16_SETEND:
        d->E = GETBT(w, 3, 1);
        return 0;

    case T_THUMB2_16_PROC_STATE:
        d->S = B_SET;
        d->cpsr = (GETBT(w, 0, 3) << 6);
        return 0;

    case T_THUMB2_16_BYTE_REVERSE:
        d->Rm = GETBT(w, 3, 3);
        d->Rd = GETBT(w, 0, 3);
        return 0;

    case T_THUMB2_16_BREAKPOINT:
        return 0;

    case T_THUMB2_16_IT:
        d->instr = I_IT;

        switch(GETBT(w, 4, 4)){
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
        default:
            fprintf(stderr, "bits 8-12 are 0x%x\n", GETBT(w, 8, 4));
        }

        if (GETBT(w, 0, 4)){
            if (I_IT != d->instr){
                fprintf(stderr, "failure 1\n");
                return -1;
            }
        }

        // I_IT instructions should never appear in assembled code
        if (I_IT == d->instr) { fprintf(stderr, "failure 2\n");return -1;}
        return 0;

    default:
        fprintf(stderr, "failure 3\n");
        return -1;
    }

    fprintf(stderr, "failure 4\n");
    return -1;
}

static int load_fields(darm_t *d, uint32_t w, darm_fieldloader_t* f)
{
    int dp, ti, dd, m;

    // extract fields using field loader
    d->dtype = f->dtype;
    d->stype = f->stype;
    d->instr = f->instr;

    d->stype = d->dtype; // FIXME not true for long operations

    d->imm = extract_imm(&(f->imm), w);
    if (d->imm) d->I = B_SET;

    // d->cond = UNCONDITIONAL ?
    d->cond = extract_insn_bits(&(f->cond), C_AL, w);
    d->Rn = extract_insn_bits(&(f->Rn), R_INVLD, w) + f->RnBase;
    d->Rm = extract_insn_bits(&(f->Rm), R_INVLD, w) + f->RmBase;
    d->Rd = extract_insn_bits(&(f->Rd), R_INVLD, w) + f->RdBase;

    // handle special cases
    switch((uint32_t)d->instr){
        // TODO: use some subset of T_ARM_VFP_DATAPROC?
    case I_VCVT:
        ti = GETBT(w, 18, 1);
        dp = GETBT(w,  8, 1);
        dd = GETBT(w, 22, 1);
        m = GETBT(w, 5, 1);
        if (ti){
            d->Rd = (d->Rd << 1) | dd;
            if (dp) d->Rm = (m << 4) | d->Rm;
            else d->Rm = (d->Rm << 1) | m;
        } else {
            d->Rm = (d->Rm << 1) | m;
            if (dp) d->Rd = (dd << 4) | d->Rd;
            else d->Rd = (d->Rd << 1) | dd;
        }

        break;

    case I_VMOV:
    case I_VMRS:
    case I_VMSR:
        // If the instruction didn't explicitly say what size, it's encoded in bit 8
        if(d->dtype == D_INVLD) {
            m = GETBT(w, 8, 1);
            if (m)
                d->dtype = D_F64;
            else d->dtype = D_F32;
        }
        break;

    case I_VLDM:
    case I_VLDMIA:
    case I_VLDMDB:
    case I_VSTM:
    case I_VSTMIA:
    case I_VSTMDB:
        // base register of list is Vd
        // number of registers is
        // imm8 if 32bit registers
        // imm8/2 if 64bit registers
        if(d->dtype == D_64) {
            d->ext_registers = extract_imm(&(f->imm), w)/2;
        } else if(d->dtype == D_32) {
            d->ext_registers = extract_imm(&(f->imm), w);
        } else {
            fprintf(stderr, "thumb2_disas_neon: datatype error for VLDM/VSTM: %d\n", d->dtype);
            return -1;
        }
        
    }
    return 0;
}


static darm_fieldloader_t* get_fieldloader(darm_t *d, uint32_t w)
{
    darm_fieldloader_t* f;
    if(IS_THUMB_SIMD_DPI(w)) {
        f = &(THUMB_NEON_DPI_LOOKUP(w));
        d->mode = M_THUMB2_NEON;
        d->instr_type = T_THUMB_SIMD_DATAPROC;
    } else if(IS_THUMB_SIMD_LDST(w)) {
        f = &(THUMB_NEON_LDST_LOOKUP(w));
        d->mode = M_THUMB2_NEON;
        d->instr_type = T_THUMB_SIMD_LDST;
    } else if(IS_THUMB_VFP_DPI(w)) {
        f = &(THUMB_VFP_DPI_LOOKUP(w));
        d->mode = M_THUMB2_VFP;
        d->instr_type = T_THUMB_VFP_DATAPROC;
    } else if(IS_THUMB_VFP_LDST(w)) {
        f = &(THUMB_VFP_LDST_LOOKUP(w));
        d->mode = M_THUMB2_VFP;
        d->instr_type = T_THUMB_VFP_LDST;
    } else {
        return NULL;
    }

    return f;
}

int darm_thumb2_disasm(darm_t *d, uint16_t w, uint16_t w2)
{
    (void)d; (void) w; (void) w2;
    uint32_t tmp = 0;
    int ret;
    
    memset(d, 0, sizeof(darm_t));
    d->instr = I_INVLD;
    d->instr_type = T_INVLD;
    d->shift_type = S_INVLD;
    d->S = d->E = d->U = d->H = d->P = d->I = B_INVLD;
    d->R = d->T = d->W = d->M = d->N = d->B = B_INVLD;
    d->dtype = d->stype = D_INVLD;
    d->Rd = d->Rn = d->Rm = d->Ra = d->Rt = R_INVLD;
    d->Rt2 = d->RdHi = d->RdLo = d->Rs = R_INVLD;
    d->option = O_INVLD;

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

    // try 32-bit
    tmp = (((uint32_t)w) << 16) | ((uint32_t)w2);
    d->w = tmp;
    darm_fieldloader_t* f = get_fieldloader(d, tmp);
    if(f != NULL) {
        if(f->instr == I_INVLD) {
            fprintf(stderr, "thumb2.c: null lookup for 0x%lx\n", w);
            return -1;
        }
        return load_fields(d, tmp, f);
    } else {
        return darm_thumb2_disasm32(d, tmp);
    }

    fprintf(stderr, "darm_thumb2_disasm: unreachable\n");
    return -1;
}
