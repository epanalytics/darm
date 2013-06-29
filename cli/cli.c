/*
Copyright (c) 2013, Michael Laurenzano
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

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "../darm.h"

typedef enum _endian {
    E_LITTLE,
    E_BIG,

    E_INVLD = -1,
} endian;

typedef enum _isa {
    A_ARMV7,
    A_THUMB,
    A_THUMB2,
    
    A_INVLD = -1,
} isa;

typedef enum _pcase {
    P_UPPER = 0,
    P_LOWER = 1,

    P_INVLD = -1,
} pcase;

#define BUF_LIMIT (1024)

#define CLI_ERROR(__code, ...) fprintf(stderr, "error: " __VA_ARGS__); exit(__code);

/*#define _CLI_DEBUG*/
#ifdef _CLI_DEBUG
#define DEBUG(...) __VA_ARGS__
#else
#define DEBUG(...)
#endif

#define IS_HEX_NUMER(__c) (__c >= '0' && __c <= '9')
#define IS_HEX_LOWER(__c) (__c >= 'a' && __c <= 'f')
#define IS_HEX_UPPER(__c) (__c >= 'A' && __c <= 'F')
uint8_t hex_value(char c){
    uint8_t t = 0;
    if (IS_HEX_NUMER(c)){
        t = c - '0';
    } else if (IS_HEX_LOWER(c)){
        t = c - 'a' + 0xa;
    } else if (IS_HEX_UPPER(c)){
        t = c - 'A' + 0xa;
    } else {
        CLI_ERROR(2, "%c is not a hex character\n", c);
    }
    return t;
}
#define HEX_TO_UINT8(__c1, __c2) ((hex_value(__c1) << 4) | (hex_value(__c2)))
#define BYTES_TO_UINT32(__b1, __b2, __b3, __b4) ((__b1 << 24) | (__b2 << 16) | (__b3 << 8) | (__b4))
#define BYTES_TO_UINT16(__b1, __b2) ((__b1 << 8) | (__b2))

void print_usage(const char* prg, const char* msg){
    fprintf(stderr, "usage: %s\n", prg);
    fprintf(stderr, "\t-help\t\t\t\tprint this help message\n");
    fprintf(stderr, "\t-le|-be\t\t\t\tlittle or big endian (default: little)\n");
    fprintf(stderr, "\t-armv7|-thumb|-thumb2\t\tarmv7, thumb or thumb2 mode (default: armv7)\n");
    fprintf(stderr, "\t-xin|-file <file>\t\tuse stdin with hex text, or a file + offset (default: stdin)\n");
    fprintf(stderr, "\t-pc <value>\t\t\tset the value of PC (default: 0)\n");
    fprintf(stderr, "\t-len <value>\t\t\tset the number of bytes to disassemble (default: go until EOF)\n");
    fprintf(stderr, "\t-off <value>\t\t\toffset in file to start disasm (default: 0)\n");
    fprintf(stderr, "\t-lower|-upper\t\t\tuse upper/lower case when printing instructions (default: lower)\n");
    fprintf(stderr, "\t-verbose\t\t\tprint detailed instruction info\n");

    if (msg != NULL){
        fprintf(stderr, "\nerror: %s\n", msg);
        exit(1);
    }

    exit(0);
}

int main(int argc, char** argv){

    int i, j, ret;
    uint32_t ui;

    char* line = NULL;
    char* end;
    size_t lnsz;
    char c1, c2;

    FILE* in_file = NULL;
    char* fname = NULL;

    darm_t d;
    darm_str_t s;
    isa wisa = A_ARMV7;
    endian wendian = E_LITTLE;
    int lu = P_LOWER;

    uint8_t use_stdin = 1;
    uint8_t print_help = 0;
    uint8_t verbose = 0;
    uint32_t pc = 0;
    uint32_t len = -1;
    uint32_t consumed = 0;
    uint32_t offset = 0;

    uint8_t insn_buf[BUF_LIMIT];
    uint32_t buf_len = 0;
    uint32_t insn32;
    uint16_t insn16;

    memset(&insn_buf, 0, BUF_LIMIT);
    memset(&s, 0, sizeof(s));

    for (i = 1; i < argc; i++){
        if (!strcmp(argv[i], "-help") || !strcmp(argv[i], "-h") || !strcmp(argv[i], "--help")){
            print_help = 1;
        } else if (!strcmp(argv[i], "-be")){
            /* TODO: support this option */
            wendian = E_BIG;
            print_usage(argv[0], "-be option not supported");
        } else if (!strcmp(argv[i], "-le")){
            wendian = E_LITTLE;
        } else if (!strcmp(argv[i], "-armv7")){
            wisa = A_ARMV7;
        } else if (!strcmp(argv[i], "-thumb")){
            wisa = A_THUMB;
            print_usage(argv[0], "THUMB set not yet supported by darm");
        } else if (!strcmp(argv[i], "-thumb2")){
            wisa = A_THUMB2;
            print_usage(argv[0], "THUMB2 set not yet supported by darm");
        } else if (!strcmp(argv[i], "-xin")){
            use_stdin = 1;
        } else if (!strcmp(argv[i], "-file")){
            if (argc == i + 1){
                print_usage(argv[0], "-file option requires an argument");
            }

            use_stdin = 0;
            fname = argv[++i];
        } else if (!strcmp(argv[i], "-pc")){
            if (argc == i + 1){
                print_usage(argv[0], "-pc option requires an argument");
            }

            pc = strtol(argv[++i], &end, 0);
            if (*end){
                print_usage(argv[0], "invalid argument to -pc");
            }
        } else if (!strcmp(argv[i], "-len")){
            if (argc == i + 1){
                print_usage(argv[0], "-len option requires an argument");
            }

            len = strtol(argv[++i], NULL, 0);
            if (*end){
                print_usage(argv[0], "invalid argument to -len");
            }
        } else if (!strcmp(argv[i], "-off")){
            if (argc == i + 1){
                print_usage(argv[0], "-off option requires an argument");
            }

            offset = strtol(argv[++i], NULL, 0);
            if (*end){
                print_usage(argv[0], "invalid argument to -len");
            }
        } else if (!strcmp(argv[i], "-verbose")){
            verbose = 1;
        } else if (!strcmp(argv[i], "-lower")){
            lu = P_LOWER;
        } else if (!strcmp(argv[i], "-upper")){
            lu = P_UPPER;
        }  else {
            print_usage(argv[0], "invalid option found");
        }
    }

    if (1 == print_help){
        print_usage(argv[0], NULL);
    }

    if (!use_stdin){
        in_file = fopen(fname, "rb");
        if (in_file == NULL){
            print_usage(argv[0], "argument to -file cannot be opened");
        }
        fseek(in_file, offset, SEEK_SET);
    }

    switch (wisa){
    case A_ARMV7:
        lnsz = 4;
        break;
    case A_THUMB:
        lnsz = 2;
        break;
    default:
        CLI_ERROR(3, "unexpected instruction set %d found\n", wisa);
    }


    c1 = c2 = 0;
    while (1){

        if (use_stdin){
            if (-1 == getline(&line, &i, stdin)){
                break;
            }

            DEBUG(fprintf(stdout, "line: %s\n", line));

            j = strlen(line);
            for (i = 0; i < j; i++){
                if (line[i] != ' ' && line[i] != '\t' && line[i] != '\n'){
                    if (c1 == 0){
                        c1 = line[i];
                    } else if (c2 == 0){
                        c2 = line[i];
                        insn_buf[buf_len++] = HEX_TO_UINT8(c1, c2);
                        c1 = c2 = 0;
                    }
                }
            }

        } else {
            j = fread(insn_buf, 1, BUF_LIMIT, in_file);
            if (j == 0){
                break;
            }
            DEBUG(fprintf(stdout, "read %d bytes from %s\n", j, fname));
            buf_len += j;
        }

        DEBUG(fprintf(stdout, "insn_buf prepre: %x\n", insn_buf));

        while (buf_len >= lnsz){
            ret = 0;

            switch (wisa){
            case A_ARMV7:
                if (use_stdin){
                    insn32 = BYTES_TO_UINT32(insn_buf[0], insn_buf[1], insn_buf[2], insn_buf[3]);
                } else {
                    insn32 = BYTES_TO_UINT32(insn_buf[3], insn_buf[2], insn_buf[1], insn_buf[0]);
                }
                ret = darm_armv7_disasm(&d, insn32);
                break;

            case A_THUMB:
                if (use_stdin){
                    insn16 = BYTES_TO_UINT16(insn_buf[0], insn_buf[1]);
                } else {
                    insn16 = BYTES_TO_UINT16(insn_buf[1], insn_buf[0]);
                }
                ret = darm_thumb_disasm(&d, insn16);
                break;

            default:
                CLI_ERROR(3, "unexpected instruction set %d found\n", wisa);
            }

            if (ret){
                darm_dump(&d);
                CLI_ERROR(4, "disassembler returned error after %d bytes\n", consumed);
            }

            ret = darm_str2(&d, &s, lu);
            if (ret){
                darm_dump(&d);
                CLI_ERROR(5, "darm_str returned error\n");
            }

            if (P_LOWER == lu){
                fprintf(stdout, "0x%08x:\t%x\t%s\n", pc + consumed, d.w, s.instr);
            } else {
                fprintf(stdout, "0x%08X:\t%X\t%s\n", pc + consumed, d.w, s.instr);
            }

            if (verbose){
                darm_dump(&d);
            }

            consumed += lnsz;
            if (len && consumed >= len){
                break;
            }

            for (ui = 0; ui < buf_len; ui++){
                insn_buf[ui] = insn_buf[ui + lnsz];
            }
            memset(&insn_buf[ui], 0, lnsz);

            buf_len -= lnsz;
 
        }

        if (len && consumed >= len){
            break;
        }
    }

    return 0;
}

