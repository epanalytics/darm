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
#include <ctype.h>
#include <stdint.h>
#include <assert.h>

#include "darm.h"

#define APPEND(out, ptr) \
    do { \
        const char *p = ptr; \
        if(p != NULL) while (*p != 0) *out++ = *p++; \
    } while (0);

int utoa(unsigned int value, char *out, int base)
{
    char buf[30]; unsigned int i, counter = 0;

    if(value == 0) {
        buf[counter++] = '0';
    }

    for (; value != 0; value /= base) {
        buf[counter++] = "0123456789abcdef"[value % base];
    }

    for (i = 0; i < counter; i++) {
        out[i] = buf[counter - i - 1];
    }

    return counter;
}

int32_t sign_ext32(int32_t v, uint32_t len){
    return ((v << (32 - len)) >> (32 - len));
}

int darm_str(const darm_t *d, darm_str_t *str)
{
    if(d->instr == I_INVLD || d->instr >= ARRAYSIZE(darm_mnemonics)) {
        fprintf(stderr, "darm_str: invalid instruction\n");
        return -1;
    }

    // the format string index (armv7 only)
    uint32_t idx = 0;

    // the offset in the format string
    uint32_t off = 0;

    // argument index
    uint32_t arg = 0;

    // pointers to the arguments
    char *args[] = {str->arg[0], str->arg[1], str->arg[2], str->arg[3]};

    char *shift = str->shift;

    // format tracking
    const char** ptrs = NULL;
    const char* phony[3];

    // ptr to the output mnemonic
    char *mnemonic = str->mnemonic;
    APPEND(mnemonic, darm_mnemonic_name(d->instr));

    if(M_ARM != d->mode){
        for (idx = 0; idx < 3; idx++){
            phony[idx] = NULL;
        }

        switch (d->mode){
        case M_THUMB:
            phony[0] = THUMB_INSTR_LOOKUP(d->w).format;
            break;
        case M_THUMB2_16:
            phony[0] = THUMB2_16_INSTR_LOOKUP(d->w).format;
            break;
        case M_THUMB2:
            phony[0] = THUMB2_INSTR_LOOKUP(d->w).format;
            break;
        case M_ARM_VFP:
            if(IS_ARM_VFP_DPI(d->w)) {
                phony[0] = ARM_VFP_DPI_LOOKUP(d->w).format;
            } else if(IS_ARM_VFP_LDST(d->w)) {
                phony[0] = ARM_VFP_LDST_LOOKUP(d->w).format;
            } else assert(0);
            break;
        case M_ARM_NEON:
            if(IS_ARM_SIMD_DPI(d->w)) {
                phony[0] = ARM_NEON_DPI_LOOKUP(d->w).format;
            } else if(IS_ARM_SIMD_LDST(d->w)) {
                phony[0] = ARM_NEON_LDST_LOOKUP(d->w).format;
            } else assert(0);
        case M_THUMB2_VFP:
            if(IS_THUMB_VFP_DPI(d->w)) {
                phony[0] = THUMB_VFP_DPI_LOOKUP(d->w).format;
            } else if(IS_THUMB_VFP_LDST(d->w)) {
                phony[0] = THUMB_VFP_LDST_LOOKUP(d->w).format;
            } else assert(0);
            break;
        case M_THUMB2_NEON:
            if(IS_THUMB_SIMD_DPI(d->w)) {
                phony[0] = THUMB_NEON_DPI_LOOKUP(d->w).format;
            } else if(IS_THUMB_SIMD_LDST(d->w)) {
                phony[0] = THUMB_NEON_LDST_LOOKUP(d->w).format;
            } else assert(0);
            break;
        default:
            fprintf(stderr, "darm_str: invalid mode %u\n", d->mode);
            return -1;
        }
        ptrs = phony;
        idx = 0;
    } else
        ptrs = armv7_format_strings[d->instr];
    if(ptrs[0] == NULL) {
        fprintf(stderr, "darm_str: no format for mode %u\n", d->mode);
        return -1;
    }
    //printf("format is %s\n", ptrs[0]);

    for (char ch; (ch = ptrs[idx][off]) != 0; off++) {
        //printf("got %c %d\n", ch, ch);
        switch (ch) {
        case 'D':
            APPEND(mnemonic, ".");
            APPEND(mnemonic, darm_datatype_name(d->dtype));
            continue;

        case 'Y':
            APPEND(mnemonic, ".");
            APPEND(mnemonic, darm_datatype_name(d->stype));
            continue;

        case 's':
            if(d->S == B_SET) {
                *mnemonic++ = 'S';
            }
            continue;

        case 'c':
            APPEND(mnemonic, darm_condition_name(d->cond, 1));
            continue;

        case 'd':
            if(d->Rd == R_INVLD) break;
            APPEND(args[arg], darm_any_register_name(d->Rd, d->dtype));
            arg++;
            continue;

        case 'n':
            if(d->Rn == R_INVLD) break;
            APPEND(args[arg], darm_any_register_name(d->Rn, (d->dtype == d->stype)? d->dtype: d->stype));
            arg++;
            continue;

        case 'm':
            if(d->Rm == R_INVLD) break;
            APPEND(args[arg], darm_any_register_name(d->Rm, (d->dtype == d->stype)? d->dtype: d->stype));
            arg++;
            continue;

        case '1':
            // always Rm+1
            if(d->Rm == R_INVLD) break;
            APPEND(args[arg], darm_register_name(d->Rm + 1));
            arg++;
            continue;

        case 'a':
            if(d->Ra == R_INVLD) break;
            APPEND(args[arg], darm_register_name(d->Ra));
            arg++;
            continue;

        case 't':
            if(d->Rt == R_INVLD) break;
            APPEND(args[arg], darm_register_name(d->Rt));
            arg++;
            continue;

        case '2':
            // first check if Rt2 is actually set
            if(d->Rt2 != R_INVLD) {
                APPEND(args[arg], darm_register_name(d->Rt2));
                arg++;
                continue;
            }
            // for some instructions, Rt2 = Rt + 1
            else if(d->Rt != R_INVLD) {
                APPEND(args[arg], darm_register_name(d->Rt + 1));
                arg++;
                continue;
            }
            break;

        case 'h':
            if(d->RdHi == R_INVLD) break;
            APPEND(args[arg], darm_register_name(d->RdHi));
            arg++;
            continue;

        case 'l':
            if(d->RdLo == R_INVLD) break;
            APPEND(args[arg], darm_register_name(d->RdLo));
            arg++;
            continue;

        case 'i':
            // check if an immediate has been set
            if(d->I != B_SET) break;

            *args[arg]++ = '#';
            if(d->imm > 0x1000) {
                *args[arg]++ = '0';
                *args[arg]++ = 'x';
                args[arg] += utoa(d->imm, args[arg], 16);
            }
            else {
                args[arg] += utoa(d->imm, args[arg], 10);
            }
            arg++;
            continue;

        case 'S':
            // is there even a shift?
            if(d->shift_type == S_INVLD) continue;

            if(d->P == B_SET) {
                // we're still inside the memory address
                shift = args[arg] - 1;
                *shift++ = ',';
                *shift++ = ' ';
            }

            if(d->Rs == R_INVLD) {
                const char *type; uint32_t imm;
                if(darm_immshift_decode(d, &type, &imm) == 0) {
                    APPEND(shift, type);
                    *shift++ = ' ';
                    *shift++ = '#';
                    shift += utoa(imm, shift, 10);
                }
                else if(d->P == B_SET) {
                    // we're still in the memory address, but there was
                    // no shift, so we have to revert the shift pointer so
                    // it will write a closing bracket again
                    shift -= 2;
                }
            }
            else {
                APPEND(shift, darm_shift_type_name(d->shift_type));
                *shift++ = ' ';
                APPEND(shift, darm_register_name(d->Rs));
            }

            if(d->P == B_SET) {
                // close the memory address
                *shift++ = ']';

                // reset shift
                args[arg] = shift;
                shift = str->shift;
            }
            continue;

        case '!':
            if(d->W == B_SET) {
                *args[arg-1]++ = '!';
            }
            continue;

        case 'e':
            args[arg] += utoa(d->E, args[arg], 10);
            continue;

        case 'x':
            if(d->M == B_SET) {
                *mnemonic++ = 'x';
            }
            continue;

        case 'X':
            // if the flags are not set, then this instruction doesn't take
            // the (B|T)(B|T) postfix
            if(d->N == B_INVLD || d->M == B_INVLD) break;

            *mnemonic++ = d->N == B_SET ? 'T' : 'B';
            *mnemonic++ = d->M == B_SET ? 'T' : 'B';
            continue;

        case 'R':
            if(d->R == B_SET) {
                *mnemonic++ = 'R';
            }
            continue;

        case 'T':
            APPEND(mnemonic, d->T == B_SET ? "TB" : "BT");
            continue;

        case 'r':
            if(d->ext_registers != 0) {
                args[arg] += darm_extension_reglist(d, args[arg]);
            } else if(d->reglist != 0) {
                args[arg] += darm_reglist(d->reglist, args[arg]);
            }
            else {
                *args[arg]++ = '{';
                APPEND(args[arg], darm_register_name(d->Rt));
                *args[arg]++ = '}';
            }
            continue;

        case 'L':
            *args[arg]++ = '#';
            args[arg] += utoa(d->lsb, args[arg], 10);
            arg++;
            continue;

        case 'W':
            *mnemonic++ = '.';
            *mnemonic++ = 'W';
            continue;

        case 'w':
            *args[arg]++ = '#';
            args[arg] += utoa(d->width, args[arg], 10);
            arg++;
            continue;

        case 'o':
            *args[arg]++ = '#';
            args[arg] += utoa(d->option, args[arg], 10);
            arg++;
            continue;

        case 'B':
            *args[arg]++ = '[';
            APPEND(args[arg], darm_register_name(d->Rn));

            // if post-indexed or the index is not even set, then we close
            // the memory address
            if(d->P != B_SET) {
                *args[arg++]++ = ']';
            }
            else {
                *args[arg]++ = ',';
                *args[arg]++ = ' ';
            }
            continue;

        case 'O':
            // if the Rm operand is set, then this is about the Rm operand,
            // otherwise it's about the immediate
            if(d->Rm != R_INVLD) {

                // negative offset
                if(d->U == B_UNSET) {
                    *args[arg]++ = '-';
                }

                APPEND(args[arg], darm_any_register_name(d->Rm, d->dtype));

                // if post-indexed this was a stand-alone operator one
                if(d->P == B_UNSET) {
                    arg++;
                }
            }
            // if there's an immediate, append it
            else if(d->imm != 0) {
                // negative offset?
                APPEND(args[arg], d->U == B_UNSET ? "#-0x" : "#0x");
                args[arg] += utoa(d->imm, args[arg], 16);
            }
            else {
                // there's no immediate, so we have to remove the ", " which
                // was introduced by the base register of the memory address
                args[arg] -= 2;
            }

            // if pre-indexed, close the memory address, but don't increase
            // arg so we can alter it in the shift handler
            if(d->P == B_SET) {
                *args[arg]++ = ']';
            }
            continue;

        case 'b':
            // BLX first checks for branch and only then for the conditional
            // version which takes the Rm as operand, so let's see if the
            // branch stuff has been initialized yet
            if(d->instr == I_BLX && d->H == B_INVLD) break;

            APPEND(args[arg], "#0x");
            args[arg] += utoa(d->imm, args[arg], 16);
            continue;

        case 'M':
            *args[arg]++ = '[';
            APPEND(args[arg], darm_register_name(d->Rn));
            *args[arg]++ = ',';
            *args[arg]++ = ' ';

            // if the Rm operand is defined, then we use that optionally with
            // a shift, otherwise there might be an immediate value as offset
            if(d->Rm != R_INVLD) {
                APPEND(args[arg], darm_register_name(d->Rm));

                const char *type; uint32_t imm;
                if(darm_immshift_decode(d, &type, &imm) == 0) {
                    *args[arg]++ = ',';
                    *args[arg]++ = ' ';
                    APPEND(args[arg], type);
                    *args[arg]++ = ' ';
                    *args[arg]++ = '#';
                    args[arg] += utoa(imm, args[arg], 10);
                }
            }
            else {
                // negative offset?
                APPEND(args[arg], d->U == B_UNSET ? "#-0x" : "#0x");
                args[arg] += utoa(d->imm, args[arg], 16);
            }

            *args[arg]++ = ']';
            continue;

        case 'A':
            if(d->rotate != 0) {
                APPEND(args[arg], "ROR #");
                args[arg] += utoa(d->rotate, args[arg], 10);
            }
            continue;

            // TODO: for TBB/TBH print these outside all args?
        case '[':
        case ']':
        case ':':
        case '{':
        case '}':
        case '6':
        case '4':
        case '#':
        case '-':
            continue;

        default:
            fprintf(stderr, "darm_str: malformed format: %c of %s for %s\n", ch, ptrs[0], darm_mnemonic_name(d->instr));
            return -1;
        }

        // TODO: anything but armv7
        if (M_ARM != d->mode) break;

        if(ptrs[++idx] == NULL || idx == 3) {
            fprintf(stderr, "darm_str: ???\n");
            return -1;
        }
        off--;
    }

    *mnemonic = *args[0] = *args[1] = *args[2] = *args[3] = *shift = 0;

    char *instr = str->instr;
    APPEND(instr, str->mnemonic);

    for (int i = 0; i < 4 && args[i] != str->arg[i]; i++) {
        if(i != 0) *instr++ = ',';
        *instr++ = ' ';
        APPEND(instr, str->arg[i]);
    }

    if(shift != str->shift) {
        *instr++ = ',';
        *instr++ = ' ';
        APPEND(instr, str->shift);
    }

    *instr = 0;
    return 0;
}

int darm_str2(const darm_t *d, darm_str_t *str, int lowercase)
{
    if(darm_str(d, str) < 0) {
        return -1;
    }

    if(lowercase != 0) {
        // just lowercase the entire object, including null-bytes
        char *buf = (char *) str;
        for (uint32_t i = 0; i < sizeof(darm_str_t); i++) {
            buf[i] = tolower(buf[i]);
        }
    }
    return 0;
}

int darm_extension_reglist(darm_t* d, char *out)
{
    assert(d->ext_registers > 0);
    if(d->ext_registers == 0) return -1;

    char *base = out;

    *out++ = '{';

    darm_reg_t first = d->Rd;
    int i;
    for(i = 0; i < d->ext_registers; ++i) {
        APPEND(out, darm_register_name(d->Rd + i));
        APPEND(out, ", ");
    }

    out[-1] = '}';
    out[0] = 0;

    return out - base;
}


int darm_reglist(uint16_t reglist, char *out)
{
    char *base = out;

    if(reglist == 0) return -1;

    *out++ = '{';

    while (reglist != 0) {
        // count trailing zero's
        int32_t reg, start = __builtin_ctz(reglist);

        // most registers have length two
        *(uint16_t *) out = *(uint16_t *) darm_registers[start];
        out[2] = darm_registers[start][2];
        out += 2 + (out[2] != 0);

        for (reg = start; reg == __builtin_ctz(reglist); reg++) {
            // unset this bit
            reglist &= ~(1 << reg);
        }

        // if reg is not start + 1, then this means that a series of
        // consecutive registers have been identified
        if(reg != start + 1) {
            // if reg is start + 2, then this means that two consecutive
            // registers have been found, but we prefer the notation
            // {r0,r1} over {r0-r1} in that case
            *out++ = reg == start + 2 ? ',' : '-';
            *(uint16_t *) out = *(uint16_t *) darm_registers[reg-1];
            out[2] = darm_registers[reg-1][2];
            out += 2 + (out[2] != 0);
        }
        *out++ = ',';
    }

    out[-1] = '}';
    *out = 0;
    return out - base;
}

void darm_dump(const darm_t *d)
{
    printf(
        "encoded:       0x%08x\n"
        "instr:         I_%s\n"
        "instr-type:    T_%s\n",
        d->w, darm_mnemonic_name(d->instr),
        darm_enctype_name(d->instr_type));

    if(d->cond == C_UNCOND) {
        printf("cond:          unconditional\n");
    }
    else if(d->cond != C_INVLD) {
        printf("cond:          C_%s\n", darm_condition_name(d->cond, 0));
    }

    if(D_INVLD != d->dtype){
        printf("dtype:         D_%s\n", darm_datatype_name(d->dtype));
    }
    if(D_INVLD != d->stype){
        printf("stype:         D_%s\n", darm_datatype_name(d->stype));
    }

#define PRINT_REG(reg) if(d->reg != R_INVLD) \
    printf("%-5s          %s\n", #reg ":", darm_register_name(d->reg))
#define PRINT_DEST_REG(reg) if(d->reg != R_INVLD)                  \
    printf("%-5s          %s\n", #reg ":", darm_any_register_name(d->reg, d->dtype))
#define PRINT_SOURCE_REG(reg) if(d->reg != R_INVLD)                  \
    printf("%-5s          %s\n", #reg ":", darm_any_register_name(d->reg, (d->dtype == d->stype)? d->dtype: d->stype))

    PRINT_DEST_REG(Rd);
    PRINT_SOURCE_REG(Rn);
    PRINT_SOURCE_REG(Rm);
    PRINT_REG(Ra);
    PRINT_REG(Rt);
    PRINT_REG(Rt2);
    PRINT_REG(RdHi);
    PRINT_REG(RdLo);

    if(d->I == B_SET) {
        printf("imm:           0x%08x  %d\n", d->imm, d->imm);
    }

#define PRINT_FLAG(flag, comment, comment2) if(d->flag != B_INVLD) \
    printf("%s:             %d   (%s)\n", #flag, d->flag, \
        d->flag == B_SET ? comment : comment2)

    PRINT_FLAG(B, "swap one byte", "swap four bytes");
    PRINT_FLAG(S, "updates conditional flag",
        "does NOT update conditional flags");
    PRINT_FLAG(E, "change to big endian", "change to little endian");
    PRINT_FLAG(U, "add offset to address", "subtract offset from address");
    PRINT_FLAG(H, "Thumb2 instruction is two-byte aligned",
        "Thumb2 instruction is four-byte aligned");
    PRINT_FLAG(P, "pre-indexed addressing", "post-indexed addressing");
    PRINT_FLAG(M, "take the top halfword as source",
        "take the bottom halfword as source");
    PRINT_FLAG(N, "take the top halfword as source",
        "take the bottom halfword as source");
    PRINT_FLAG(T, "PKHTB form", "PKHBT form");
    PRINT_FLAG(R, "round the result", "do NOT round the result");
    PRINT_FLAG(W, "write-back", "do NOT write-back");

    if(d->option != O_INVLD) {
        printf("option:        %d\n", d->option);
    }

    if(d->rotate != 0) {
        printf("rotate:        %d\n", d->rotate);
    }

    if(d->shift_type != S_INVLD) {
        if(d->Rs == R_INVLD) {
            printf(
                "type:          %s (shift type)\n"
                "shift:         %-2d  (shift constant)\n",
                darm_shift_type_name(d->shift_type), d->shift);
        }
        else {
            printf(
                "type:          %s (shift type)\n"
                "Rs:            %s  (register-shift)\n",
                darm_shift_type_name(d->shift_type),
                darm_register_name(d->Rs));
        }
    }

    if(d->lsb != 0 || d->width != 0) {
        printf(
            "lsb:           %d\n"
            "width:         %d\n",
            d->lsb, d->width);
    }

    if(d->reglist != 0) {
        char reglist[64];
        darm_reglist(d->reglist, reglist);
        printf("reglist:       %s\n", reglist);
    }

    printf("\n");
}

// darm internal functions
int extract_insn_bits(darm_fieldgrab_t* t, uint32_t def, uint32_t w){
    int ret = def;
    if (F_SHIFT_MASK == t->type){
        ret = GETBT(w, t->shift, t->mask);
    }
    return ret;
}

const char* extract_string_const(darm_fieldgrab_t* t, char* def){
    const char* ret = def;
    if (F_STRING_CONST == t->type){
        ret = t->str;
    }
    return ret;
}

int extract_imm(darm_fieldgrab_t* t, uint32_t w){
    int imm;
    if (F_IMMEDIATE != t->type){
        return 0;
    }
    t->type = F_SHIFT_MASK;
    imm = extract_insn_bits(t, 0, w);
    t->type = F_IMMEDIATE;
    if (t->extend == 1){
        imm = sign_ext32(imm, t->mask);
    }
    if (t->mult > 0){
        imm *= t->mult;
    }
    return imm;
}

