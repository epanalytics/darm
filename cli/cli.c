#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

#define MASK_16BIT (0x0000ffff)
#define ARM_INSN_LIMIT (4)
#define BUF_LIMIT (1024)

void print_usage(const char* prg, const char* msg){
    fprintf(stderr, "usage: %s\n", prg);
    fprintf(stderr, "\t-help\t\t\t\tprint this help message\n");
    fprintf(stderr, "\t-le|-be\t\t\t\tlittle or big endian (default: little)\n");
    fprintf(stderr, "\t-armv7|-thumb|-thumb2\t\tarmv7, thumb or thumb2 mode (default: armv7)\n");
    fprintf(stderr, "\t-xin|-file <file>:<offset>\tuse stdin with hex text, or a file + offset (default: stdin)\n");
    fprintf(stderr, "\t-pc <value>\t\t\tset the value of PC (default: 0)\n");
    fprintf(stderr, "\t-len <value>\t\t\tset the number of bytes to disassemble (default: go until EOF)\n");
    fprintf(stderr, "\t-verbose\t\t\tprint detailed instruction info\n");

    if (msg != NULL){
        fprintf(stderr, "\nerror: %s\n", msg);
        exit(1);
    }

    exit(0);
}

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
        fprintf(stderr, "error: %c is not a hex character\n", c);
        exit(4);
    }
    return t;
}

uint8_t hex_to_uint8t(char c1, char c2){
    return (hex_value(c1) << 4) | (hex_value(c2));
}

uint32_t hex_to_uint32_be(const char* str){
    uint32_t t = 0;
    t |= (hex_to_uint8t(str[0], str[1]) << 0 );
    t |= (hex_to_uint8t(str[2], str[3]) << 8 );
    t |= (hex_to_uint8t(str[4], str[5]) << 16);
    t |= (hex_to_uint8t(str[6], str[7]) << 24);

    return t;
}

uint32_t hex_to_uint32(const char* str){
    uint32_t t = 0;
    t |= (hex_to_uint8t(str[0], str[1]) << 24);
    t |= (hex_to_uint8t(str[2], str[3]) << 16);
    t |= (hex_to_uint8t(str[4], str[5]) << 8 );
    t |= (hex_to_uint8t(str[6], str[7]) << 0);

    return t;
}

int main(int argc, char** argv){

    int i, j, k, use_stdin = 1, print_help = 0, verbose = 0;
    char* line = NULL;
    size_t lnsz;

    darm_t d;
    darm_str_t s;
    isa wisa = A_ARMV7;
    endian wendian = E_LITTLE;

    uint32_t wa;
    uint16_t wt1;
    uint16_t wt2;
    uint32_t pc = 0;
    uint32_t len = 0;
    uint32_t consumed = 0;

    char insn_buf[BUF_LIMIT];
    memset(&insn_buf, 0, BUF_LIMIT);

    for (i = 1; i < argc; i++){
        if (!strcmp(argv[i], "-help") || !strcmp(argv[i], "-h") || !strcmp(argv[i], "--help")){
            print_help = 1;
        } else if (!strcmp(argv[i], "-be")){
            // TODO: support this
            wendian = E_BIG;
            print_usage(argv[0], "-be option not supported");
        } else if (!strcmp(argv[i], "-le")){
            wendian = E_LITTLE;
        } else if (!strcmp(argv[i], "-armv7")){
            wisa = A_ARMV7;
        } else if (!strcmp(argv[i], "-thumb")){
            wisa = A_THUMB;
        } else if (!strcmp(argv[i], "-thumb2")){
            wisa = A_THUMB2;
        } else if (!strcmp(argv[i], "-xin")){
            use_stdin = 1;
        } else if (!strcmp(argv[i], "-file")){
            // TODO: support this
            use_stdin = 0;
            print_usage(argv[0], "-file option not supported");
        } else if (!strcmp(argv[i], "-pc")){
            if (argc == i + 1){
                print_usage(argv[0], "-pc option requires an argument");
            }
            pc = strtol(argv[i + 1], NULL, 0);
            i++;
        } else if (!strcmp(argv[i], "-len")){
            if (argc == i + 1){
                print_usage(argv[0], "-len option requires an argument");
            }
            len = strtol(argv[i + 1], NULL, 0);
            i++;
        } else if (!strcmp(argv[i], "-verbose")){
            verbose = 1;
        }  else {
            print_usage(argv[0], "invalid option found");
        }
    }

    if (1 == print_help){
        print_usage(argv[0], NULL);
    }

    while (1){

        if (-1 == getline(&line, &lnsz, stdin)){
            break;
        }

        fprintf(stdout, "line: %s\n", line);

        // TODO: save bytes across lines, disasm incrementally
        memset(&insn_buf, 0, BUF_LIMIT);

        j = strlen(line);
        k = 0;
        for (i = 0; i < j; i++){
            if (line[i] != ' ' && line[i] != '\t'){
                insn_buf[k] = line[i];
                k++;
            }
        }

        wa = hex_to_uint32(insn_buf);

        // TODO: check for error in disasm
        switch (wisa){

        case A_ARMV7:
            darm_armv7_disasm(&d, wa);
            break;

        case A_THUMB:
            wt1 = (uint16_t)wa;
            darm_thumb_disasm(&d, wt1);
            break;

        case A_THUMB2:
            wt1 = (wa & MASK_16BIT);
            wt2 = (wa >> 16) & MASK_16BIT;
            // TODO: handle BE and correct ordering
            darm_thumb2_disasm(&d, wt1, wt2);
            break;

        default:
            fprintf(stderr, "error: unexpected ISA found\n");
            exit(2);
        }

        // TODO: add an option for case (last arg)?
        darm_str2(&d, &s, 1);
        fprintf(stdout, "0x%08x:\t%s\n", pc + consumed, s.instr);

        if (1 == verbose){
            darm_dump(&d);
        } 

        // TODO: assumes 32bit insn
        consumed += 4;
        if (consumed >= len){
            break;
        }
    }

    return 0;
}

