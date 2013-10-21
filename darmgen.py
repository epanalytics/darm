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
import darmbits as db
import darmtbl
import darmtblthumb
import darmtblthumb2
import darmtblvfp
import darmtblneon
import itertools
import string
import sys
import textwrap
import re

dtypes = 'F64 F32 F16 S32 S16 U32 U16 64 32'.split()
dtype_re_1 = re.compile('.*\.([F|S|U]?\d\d)$')
dtype_re_2 = re.compile('.*\.([F|S|U]\d\d)\.([F|S|U]\d\d)$')

# armv7_lookup_bits = 8     # XXXXXXXX........ ................
thumb_lookup_bits = 10      # XXXXXXXXXX......
thumb2_16_lookup_bits = 7   # ....XXXXXXX.....
thumb2_lookup_bits = 15     # ...XXXXXXXXX.... X...............

thumb_lookup_bitMask =     '1111111111000000'
thumb2_16_lookup_bitMask = '0000111111100000'
#thumb2_lookup_bitMask =    '0001111111110001' + '0000000000000000' # FIXME code didn't match above documentation
thumb2_lookup_bitMask =    '0001101110010000' + '1111111100010000'

def selectBits(allBits, bitMask):
    assert(len(bitMask) == len(allBits))
    retval = []
    for i in range(len(bitMask)):
        if bitMask[i] == '1':
            retval.append(allBits[i])
    return retval


def struct_definition(name, arr):
    a = arr
    return 'typedef struct _%s {\n' % (name) +\
        string.join(['    ' + a[i][1] + '  ' + a[i][0] + ';' for i in range(len(arr))], '\n') +\
        '} %s;\n\n' % (name)

def bins(n, l):
    s = bin(n)
    while len(s) - 2 < l:
        s = s[:2] + '0' + s[2:]
    return s

def instruction_lookup_table(arr, size, kind):
    """Lookup table for all relevant instruction features."""    
    values = []
    t = 2**size
    for k in range(t):
        s = ''
        if not arr.has_key(k):
            s += '{ I_INVLD, T_INVLD, NULL}'
        else:
            a = arr[k]
            s += '{ I_%s, T_%s, "%s"}' % (a[0], a[1][1], a[2])
        if k < t-1:
            s += ','
        s = '/* %s */ ' % (bins(k, size)) + s
        values.append(s)

    return 'darm_lookup_t %s_instr_lookup[%d] = {' % (kind, t) + \
        '\n' + string.join(values, '\n') + '\n};'

def instruction_name(x):
    return x.split('{')[0].split('<')[0].split()[0]


def instruction_names(arr):
    """List of all unique instruction names."""
    return ['INVLD'] + sorted(set(instruction_name(x) for x in arr))


def enum_table(name, arr):
    """Enumeration."""
    text = '\n    '.join(textwrap.wrap(', '.join(arr), 74))
    return 'typedef enum _%s_t {\n    %s\n} %s_t;\n' % (name, text, name)


def typed_table(typ, name, arr):
    """A table with a given type."""
    text = '\n    '.join(textwrap.wrap(', '.join(arr), 74))

    # if it's not a pointer, append a space
    if typ[-1] != '*':
        typ += ' '
    return '%s %s[] = {\n    %s\n};\n' % (typ, name, text)


def string_table(name, arr):
    """A string table."""
    return typed_table('const char *', name, ('"%s"' % x for x in arr))


def instruction_names_enum(arr):
    """Enumeration of all instruction names."""
    return enum_table('darm_instr',
                      ['I_%s' % x for x in instruction_names(arr)] +
                      ['I_INSTRCNT'])


def instruction_names_table(arr):
    """Table of strings of all instructions."""
    return string_table('darm_mnemonics', instruction_names(arr))


def instruction_types_table(arr, kind):
    """Lookup table for the types of instructions."""
    arr = ['T_%s' % arr[x][1][1] if x in arr else 'T_INVLD'
           for x in range(256)]
    return typed_table('darm_enctype_t', '%s_instr_types' % kind, arr)

def instruction_names_index_table(arr, kind):
    """Lookup table for instruction label for each instruction index."""
    arr = ['I_%s' % arr[x][0] if x in arr else 'I_INVLD'
           for x in range(256)]
    return typed_table('darm_instr_t', '%s_instr_labels' % kind, arr)

def instruction_format_strings_table(arr, kind):
    """Format string for each instruction index."""
    arr = ['"%s"' % arr[x][2] if x in arr else 'NULL'
           for x in range(256)]
    return typed_table('const char*', '%s_instr_formats' % kind, arr)

def type_lookup_table(name, *args):
    """Create a lookup table for a certain instruction type."""
    arr = ('I_%s' % x.upper() if x else 'I_INVLD' for x in args)
    return typed_table('darm_instr_t', '%s_instr_lookup' % name, arr)


def type_encoding_enum(enumname, arr):
    text = []
    for _, name, info, encodings, _, affects in arr:
        text.append(
            '    // info:\n' +
            '    // %s\n    //\n' % info +
            '    // encodings:\n    // ' +
            '\n    // '.join(encodings) + '\n    //\n' +
            '    // affects:\n    // ' +
            '\n    // '.join(textwrap.wrap(', '.join(affects), 74)) + '\n' +
            '    T_%s,' % name)

    return 'typedef enum _%s_t {\n%s\n} %s_t;\n' % (enumname,
                                                    '\n\n'.join(text),
                                                    enumname)


def type_encoding_table(tblname, arr):
    """Table of strings of all instructions."""
    return string_table(tblname, (x[1] for x in arr))

def format_string(full):
    # a set of rules to transform a string representation as given by the
    # armv7 manual, into our own custom format string
    rules = [
        # if this instruction updates the condition flags, then an S is added
        # to the end of the instruction
        '{S}', 's',

        # if this instruction is conditional, then the condition under which
        # it executes is appended to the instruction
        '<c>', 'c',

        # implicitly-used regs
        'PC=<Rn>', '<Rn>',
        'SP=<Rn>', '<Rn>',
        'SP=<Rd>', '<Rd>',

        # implied shift TBH
        'LSL #1', 'S',

        # VFP/SIMD data types
        'DD', 'DY',
        '.F64', 'D',
        '.F32', 'D',
        '.F16', 'D',
        '.S32', 'D',
        '.S16', 'D',
        '.U32', 'D',
        '.U16', 'D',
        '.64',  'D',
        '.32',  'D',

        # memory address
        '[<Rn>,<Rm>]', 'M',
        '[<Rn>,#<imm5>]', 'M',
        '[<Rn>,#<imm8>]', 'M',
        '[<Rn>,#+/-<imm8>]', 'M',
        '[<Rn>,#+/-<imm12>]', 'M',
        '[<Rn>,+/-<Rm>{,<shift>}]', 'M',
        '[<Rn>,#+<imm>]', 'M',
        '[<Rn>,#-<imm>]', 'M',

        # memory address with Rn as base register and an immediate or Rm
        # operand as offset
        '[<Rn>]', 'B',
        '#+/-<imm12>', 'O',
        '#+/-<imm8>', 'O',
        '#+/-<imm5>', 'O',
        '+/-<Rm>', 'O',

        # various register operands
        '<Rd>', 'd',
        '<Rd3>', 'd',
        '<Rdn>', 'd',
        '<Rdn3>', 'd',
        '<Dd>', 'd',
        '<Sd>', 'd',
        '<Rn>', 'n',
        '<Rn3>', 'n',
        '<Dn>', 'n',
        '<Sn>', 'n',
        '<Rm>', 'm',
        '<Rm3>', 'm',
        '<Dm>', 'm',
        '<Sm>', 'm',
        '<Sm1>', '1',
        '<Ra>', 'a',
        '<Rt>', 't',
        '<Rt2>', '2',
        '<RdHi>', 'h',
        '<RdLo>', 'l',

        # immediate values
        '#0.0',    'i',
        '#<const>', 'i',
        '#<imm>', 'i',
        '#<imm2>', 'i',
        '#<imm3>', 'i',
        '#<imm4>', 'i',
        '#<imm5>', 'i',
        '#<imm7>', 'i',
        '#<imm8>', 'i',
        '#<imm12>', 'i',
        '#<imm16>', 'i',
        '#<imm24>', 'i',

        # immediate and register shift
        '{,<shift>}', 'S',
        '#<shift>', 'S',
        '<type> <Rs>', 'S',

        # some bit instructions take a lsb and width as operand
        '#<lsb>', 'L',
        '#<width>', 'w',

        # for branch instructions
        '<label>', 'b',

        # option immediate for various obscure instructions
        '#<option>', 'o',

        # either a list of registers, reglist, or a single register
        '<registers>', 'r',

        # vfp register list
        '<list>', 'r',

        # exclamation mark to specify the write-back bit
        '{!}', '!',

        # the SETEND instruction takes a one or zero as operand
        '<endian_specifier>', 'e',

        # some signed multiplication instructions take an X flag, which
        # means that you can swap halfwords of the second operand
        '{X}', 'x',

        # certain signed multiplication instructions take these flags in
        # order to swap halfwords that are being used
        '<x><y>', 'X',

        # rounding flag for various signed multiplication instructions
        '{R}', 'R',

        # rotation of operands
        '{,<rotation>}', 'A',

        # the PKH instruction has either a TB or BT postfix, specified by
        # the T member of the darm object
        '<T>', 'T',

        # forced 32-bit implementation
        '.W', 'W',
    ]

    instr = instruction_name(full)

    while True:
        f = full

        # apply all rules
        for k, v in zip(*[iter(rules)]*2):
            full = full.replace(k, v)

        full = full.replace(',', '').replace(' ', '')

        if f == full:
            break

    # strip the instruction
    full = full[len(instr):]

    return full


def generate_format_strings(arr):
    ret = {}

    for row in arr:
        full = row[0]

        instr = instruction_name(full)
        full = format_string(full)

        if instr not in ret:
            ret[instr] = [full]
        elif ret[instr][0] == full[:len(ret[instr][0])]:
            ret[instr][0] = full
        else:
            ret[instr].append(full)

    return ret

def magic_open(fname):
    # python magic!
    sys.stdout = open(fname, 'w')

    # print the license
    print('/*')
    print(__doc__.strip())
    print('*/')

    print('/* This file was generated by darmgen.py. Do not edit! */')

d = darmtbl
d2 = darmtblthumb
d3 = darmtblthumb2

def bit_crossp(insn):
    identifier = []
    for field in insn[1:]:
        if field == 0 or field == (0):
            identifier.append('0')
        elif field == 1 or field == (1):
            identifier.append('1')
        else:
            identifier += ['01'] * field.bitsize

    return identifier

def bit_index(bits):
    t = 0
    c = 1
    for b in range(len(bits)-1,-1,-1):
        if bits[b] == '1':
            t += c
        c *= 2
    return t

def generate_mask(table, size):
    all_insns = []
    for insn in table:
        crossp = bit_crossp(insn)
        all_insns.append(crossp)
    poss = []
    for i in range(size):
        t = {}
        for insn in all_insns:
            t[insn[i]] = True
        poss.append(t)

    mask = '0' * size

    #print poss
    for i in range(size):
        if poss[i].has_key('0') and poss[i].has_key('1'):
            mask = mask[0:i] + '1' + mask[i+1:]
        

    return mask

def bits_pos(insn, field, inst = False):
    p = 0
    for f in reversed(insn[1:]):
        l = 0
        if f == 0 or f == 1 or f == (0) or f == (1):
            l = 1
        else:
            l = f.bitsize

        if not inst and field == f:
            return p, l, f
        elif inst and isinstance(f, field):
            return p, l, f

        p += l

    return None, None, None

def insert_field(insn, table, name, opts = []):
    for n in [name] + opts:
        p, l, f = bits_pos(insn, eval('db.%s' % n))
        if p != None:
            assert(not table.has_key(name))
            table[name] = FieldGrab_ShiftMask((p, l))

def insert_field_imm(insn, table):
    p, l, f = bits_pos(insn, db.imm, True)
    if p != None:
        assert(not table.has_key('imm'))
        assert(isinstance(f, db.imm))
        table['imm'] = FieldGrab_Immediate((p, l), f.args)    

class FieldGrab:
    def __init__(self):
        pass

    def __repr__(self):
        return '{.type=%s}' % ('F_INVLD')

class FieldGrab_StringConst(FieldGrab):
    def __init__(self, string):
        self.str = string

    def __repr__(self):
        return '{.type=%s, .str="%s"}' % ('F_STRING_CONST', self.str)

class FieldGrab_ShiftMask(FieldGrab):
    def __init__(self, tup):
        self.shift = int(tup[0])
        self.bits = int(tup[1])

    def __repr__(self):
        return '{.type=%s, .shift=%d, .mask=%d}' % ('F_SHIFT_MASK', self.shift, self.bits)

class FieldGrab_Immediate(FieldGrab_ShiftMask):
    def __init__(self, tup, iargs):
        self.shift = int(tup[0])
        self.bits = int(tup[1])

        self.extend = 0
        if iargs.has_key('s'):
            self.extend = iargs['s']

        self.mult = 0
        if iargs.has_key('m'):
            self.mult = iargs['m']

    def __repr__(self):
        return '{.type=%s, .shift=%d, .mask=%d, .extend=%d, .mult=%d}' % ('F_IMMEDIATE', self.shift, self.bits, self.extend, self.mult)

class InstructionLoad:
    def __init__(self, i):
        self.insn = i

    def __str__(self):
        t = {}
        desc = self.insn[0]
        #t['desc'] = FieldGrab_StringConst(desc)
        t['format'] = '"' + format_string(desc) + '"'
        t['instr'] = 'I_' + instruction_name(desc)

        t['dtype'] = 'D_INVLD'
        t['stype'] = 'D_INVLD'
        r = dtype_re_1.findall(desc.split()[0])
        if len(r) > 0:
            t['dtype'] = 'D_' + r[0]
        r = dtype_re_2.findall(desc.split()[0])
        if len(r) > 0:
            t['dtype'] = 'D_' + r[0][0]
            t['stype'] = 'D_' + r[0][1]

        insert_field(self.insn, t, 'cond')
        insert_field(self.insn, t, 'Rn', ['Sn', 'Dn'])
        insert_field(self.insn, t, 'Rd', ['Sd', 'Dd'])
        insert_field(self.insn, t, 'Rm', ['Sm', 'Dm'])

        insert_field_imm(self.insn, t)

        s = '{'
        for k in t:
            s += '.%s = %s, ' % (k, str(t[k]))
        s += '}'
        return s

    def __repr__(self):
        return str(self)

def notype(*x):
    return (0,) + x

def armv7(*x):
    return (1,) + x

def thumb(*x):
    return (2,) + x

def thumb2_16(*x):
    return (3,) + x

def thumb2(*x):
    return (4,) + x

# we specify various instruction types
instr_types = [
    notype('INVLD', 'Invalid or non-existent type',
           ['I_INVLD'], lambda x, y, z: False),
    armv7('ADR', 'ADR Instruction, which is an optimization of ADD',
          ['ADR<c> <Rd>,<label>'], lambda x, y, z: y[:3] == 'ADR'),
    armv7('UNCOND', 'All unconditional instructions',
          ['ins <endian_specifier>', 'ins [<Rn>,#+/-<imm12>]',
           'ins [<Rn>,#<imm12>]', 'ins', 'ins #<option>', 'ins <label>'],
          lambda x, y, z: False),
    armv7('MUL', 'All multiplication instructions',
          ['ins{S}<c> <Rd>,<Rn>,<Rm>', 'ins{S}<c> <Rd>,<Rn>,<Rm>,<Ra>',
           'ins{S}<c> <RdLo>,<RdHi>,<Rn>,<Rm>'],
          lambda x, y, z: x[1:5] == (0,)*4 and x[-5:-1] == (1, 0, 0, 1)),
    armv7('STACK0', 'Various STR and LDR instructions',
          ['ins<c> <Rt>,[<Rn>,#+/-<imm12>]', 'ins<c> <Rt>,[<Rn>],#+/-<imm12>',
           'ins<c> <Rt>,[<Rn>],+/-<Rm>{,<shift>}'],
          lambda x, y, z: x[1:3] == (0, 1) and not (x[3] == 1 == x[-2])),
    armv7('STACK1', 'Various unprivileged STR and LDR instructions',
          ['ins<c> <Rt>,[<Rn>],+/-<Rm>', 'ins<c> <Rt>,[<Rn>]{,#+/-<imm8>}'],
          lambda x, y, z: x[-5] == 1 and x[-2] == 1 and x[-4:-2] != (0, 0) and
          x[1:5] == (0, 0, 0, 0) and x[7] == 1),
    armv7('STACK2', 'Various other STR and LDR instructions',
          ['ins<c> <Rt>,<Rt2>,[<Rn>],+/-<Rm>',
           'ins<c> <Rt>,[<Rn>],+/-<Rm>',
           'ins<c> <Rt>,<Rt2>,[<Rn>],#+/-<imm8>',
           'ins<c> <Rt>,<Rt2>,[<Rn>,#+/-<imm8>]',
           'ins<c> <Rt>,[<Rn>,#+/-<imm8>]', ],
          lambda x, y, z: x[1:4] == (0,)*3 and x[-2] == 1 and x[-5] == 1 and
          x[-4:-2] != (0, 0) and not x[-1] in (0, 1) and
          not (x[4] == 0 and x[7] == 1)),
    armv7('ARITH_SHIFT',
          'Arithmetic instructions which take a shift for the second source',
          ['ins{S}<c> <Rd>,<Rn>,<Rm>{,<shift>}',
           'ins{S}<c> <Rd>,<Rn>,<Rm>,<type> <Rs>'],
          lambda x, y, z: d.Rn in x and d.Rd in x and x[-3] == d.type_
          and x[-1] == d.Rm),
    armv7('ARITH_IMM',
          'Arithmetic instructions which take an immediate as second source',
          ['ins{S}<c> <Rd>,<Rn>,#<const>'],
          lambda x, y, z: d.Rn in x and d.Rd in x and d.imm12 in x),
    armv7('BITS', 'Bit field magic',
          [], lambda x, y, z: d.lsb in x),
    armv7('BRNCHSC', 'Branch and System Call instructions',
          ['B(L)<c> <label>', 'SVC<c> #<imm24>'],
          lambda x, y, z: x[-1] == d.imm24),
    armv7('BRNCHMISC', 'Branch and Misc instructions',
          ['B(L)X(J)<c> <Rm>', 'BKPT #<imm16>', 'MSR<c> <spec_reg>,<Rn>'],
          lambda x, y, z: x[1:9] == (0, 0, 0, 1, 0, 0, 1, 0) and
          not y[0] == 'Q'),
    armv7('MOV_IMM', 'Move immediate to a register (possibly negating it)',
          ['ins{S}<c> <Rd>,#<const>'],
          lambda x, y, z: x[-1] == d.imm12 and x[-2] == d.Rd),
    armv7('CMP_OP', 'Comparison instructions which take two operands',
          ['ins<c> <Rn>,<Rm>{,<shift>}', 'ins<c> <Rn>,<Rm>,<type> <Rs>'],
          lambda x, y, z: x[-1] == d.Rm and x[-3] == d.type_ and
          (x[-4] == d.imm5 and x[-8:-4] == (0, 0, 0, 0) or
           x[-5] == d.Rs and x[-9:-5] == (0, 0, 0, 0))),
    armv7('CMP_IMM', 'Comparison instructions which take an immediate',
          ['ins<c> <Rn>,#<const>'],
          lambda x, y, z: x[-1] == d.imm12 and x[-6] == d.Rn),
    armv7('OPLESS', 'Instructions which don\'t take any operands',
          ['ins<c>'],
          lambda x, y, z: len(x) == 29),
    armv7('DST_SRC', 'Manipulate and move a register to another register',
          ['ins{S}<c> <Rd>,<Rm>', 'ins{S}<c> <Rd>,<Rm>,#<imm>',
           'ins{S}<c> <Rd>,<Rn>,<Rm>'],
          lambda x, y, z: z == 26 or z == 27),
    armv7('LDSTREGS', 'Load or store multiple registers at once',
          ['ins<c> <Rn>{!},<registers>'],
          lambda x, y, z: x[-1] == d.register_list),
    armv7('BITREV', 'Bit reverse instructions',
          ['ins<c> <Rd>,<Rm>'],
          lambda x, y, z: x[-1] == d.Rm and x[-10] == d.Rd and
          x[-11] != d.Rn),
    armv7('MISC', 'Various miscellaneous instructions',
          ['ins{S}<c> <Rd>,<Rm>,<type> <Rs>', 'ins{S}<c> <Rd>,<Rm>{,<shift>}',
           'ins<c> #<imm4>', 'ins<c> #<option>',
           'ins<c> <Rd>,<Rn>,<Rm>{,<type> #<imm>}', 'ins<c> <Rd>,<Rn>,<Rm>'],
          lambda x, y, z: instruction_name(y) in ('MVN', 'SMC', 'DBG', 'PKH',
                                                  'SEL')),
    armv7('SM', 'Various signed multiply instructions', [],
          lambda x, y, z: y[:2] == 'SM'),
    armv7('PAS', 'Parallel signed and unsigned addition and subtraction',
          ['ins<c> <Rd>,<Rn>,<Rm>'],
          lambda x, y, z: z in (97, 98, 99, 101, 102, 103)),
    armv7('SAT', 'Saturating addition and subtraction instructions',
          ['ins<c> <Rd>,<Rn>,<Rm>'],
          lambda x, y, z: y[0] == 'Q'),
    armv7('SYNC', 'Synchronization primitives',
          ['ins{B}<c> <Rt>,<Rt2>,[<Rn>]', 'ins<c> <Rd>,<Rt>,[<Rn>]',
           'ins<c> <Rt>,<Rt2>,[<Rn>]', 'ins<c> <Rt>,[<Rn>]'],
          lambda x, y, z: x[1:5] == (0, 0, 0, 1) and
          (x[-5:-1] == (1, 0, 0, 1) or x[-8:-4] == (1, 0, 0, 1))),
    armv7('PUSR', 'Packing, unpacking, saturation, and reversal instructions',
          ['ins<c> <Rd>,#<imm>,<Rn>', 'ins<c> <Rd>,#<imm>,<Rn>{,<shift>}',
           'ins<c> <Rd>,<Rn>,<Rm>{,<rotation>}',
           'ins<c> <Rd>,<Rm>{,<rotation>}'],
          lambda x, y, z: x[1:6] == (0, 1, 1, 0, 1)),

    # TODO: harmonize insn classes across armv7, thumb, thumb2

    # thumb1 (16-bit)
    thumb('DST_SRC', 'Manipulate and move a register to another register',
          ['ins{S} <Rd>,<Rm>', 'ins{S} <Rd>,<Rm>,#<imm>'],
          lambda x, y, z: x[0:3] == (0, 0, 0) and x[3:5] != (1, 1)),
    thumb('ARITH', 'Add/subtract',
          ['ins{S} <Rd>,<Rm>', 'ins{S} <Rd>,<Rm>,#<imm3>', 'ins{S} <Rd>,<Rm>,<Rn>'],
          lambda x, y, z: x[0:5] == (0, 0, 0, 1, 1)),
    thumb('ARITH_IMM', 'Move/compare/add/subtract immediate',
          ['ins{S} <Rd>,#<imm8>', 'ins <Rn>,#<imm8>', 'ins{S} <Rdn>,#<imm8>'],
          lambda x, y, z: x[0:3] == (0, 0, 1)),
    thumb('ALU', 'ALU operations',
          ['ins{S} <Rd>,<Rm>', 'ins{S} <Rn>,<Rm>', 'ins{S} <Rdn>,<Rm>'],
          lambda x, y, z: x[0:6] == (0, 1, 0, 0, 0, 0)),
    thumb('HIREG_BX', 'Hi register operations/branch exchange',
          ['ins <Rd>,<Rm>', 'ins <Rdn> <Rm>', 'ins <Rm>'],
          lambda x, y, z: x[0:6] == (0, 1, 0, 0, 0, 1)),
    thumb('LOAD_PCREL', 'PC-relative load',
          ['ins <Rt>,[PC,#+/-<imm8>]'],
          lambda x, y, z: x[0:5] == (0, 1, 0, 0, 1)),
    thumb('LDST_REG', 'Load/store with register offset',
          ['ins <Rt>,[<Rn>,<Rm>]'],
          lambda x, y, z: x[0:4] == (0, 1, 0, 1)),
    thumb('LDST_IMM', 'Load/store with immediate offset',
          ['ins <Rt>,[<Rn>]', 'ins <Rt>,[<Rn>,#+/-<imm5>]'],
          lambda x, y, z: x[0:3] == (0, 1, 1) or x[0:4] == (1, 0, 0, 0)),
    thumb('LDST_SPREL', 'SP-relative load/store',
          ['ins <Rt>,[SP,#+/-<imm8>]'],
          lambda x, y, z: x[0:4] == (1, 0, 0, 1)),
    thumb('LOAD_ADDR', 'Calculate memory address',
          ['ins <Rd>,SP,#<imm8>', 'ins <Rd>,PC,#<imm8>'],
          lambda x, y, z: x[0:4] == (1, 0, 1, 0)),
    thumb('ADD_SP', 'Add offset to SP',
          ['ins SP,SP,#+/-<imm7>'],
          lambda x, y, z: x[0:8] == (1, 0, 1, 1, 0, 0, 0, 0)),
    thumb('PSHPOP', 'Push/pop registers to stack',
          ['ins <registers'],
          lambda x, y, z: x[0:4] == (1, 0, 1, 1) and x[5:7] == (1, 0)),
    thumb('LDST_MULTI', 'Multiple load/store',
          ['ins <Rn>!,<registers>'],
          lambda x, y, z: x[0:4] == (1, 1, 0, 0)),
    thumb('BR_COND', 'Conditional branch',
          ['ins<c> <label>'],
          lambda x, y, z: x[0:4] == (1, 1, 0, 1) and x[4:8] != (1, 1, 1, 1)),
    thumb('SWINT', 'Software interrupt',
          ['ins #<imm8>'],
          lambda x, y, z: x[0:8] == (1, 1, 0, 1, 1, 1, 1, 1)),
    thumb('BR_UNCOND', 'Unconditional branch',
          ['ins <label>'],
          lambda x, y, z: x[0:5] == (1, 1, 1, 0, 0)),

    # 16-bit thumb2
    thumb2_16('BR_CONDZERO', 'Compare and branch on zero',
              ['ins <label>'],
              lambda x, y, z: x[0:4] == (1, 0, 1, 1) and x[5] == 0 and x[7] == 1),
    thumb2_16('DATA_EXTEND', 'Signed/unsigned extend word/byte',
              ['ins<c> <Rd>,<Rm>'],
              lambda x, y, z: x[0:4] == (1, 0, 1, 1) and x[4:8] == (0, 0, 1, 0)),
    thumb2_16('PSHPOP', 'Push/pop multiple registers',
              ['ins <registers>'],
              lambda x, y, z: x[0:4] == (1, 0, 1, 1) and x[5:7] == (1, 0)),
    thumb2_16('SETEND', 'Set endian-ness',
              ['ins <end>'],
              lambda x, y, z: x[0:4] == (1, 0, 1, 1) and x[4:11] == (0, 1, 1, 0, 0, 1, 0)),
    thumb2_16('PROC_STATE', 'Change processor state',
              ['ins <flags>'],
              lambda x, y, z: x[0:4] == (1, 0, 1, 1) and x[4:11] == (0, 1, 1, 0, 0, 1, 1)),
    thumb2_16('BYTE_REVERSE', 'Byte reverse word/halfword',
              ['ins <Rd>,<Rm>'],
              lambda x, y, z: x[0:4] == (1, 0, 1, 1) and x[4:8] == (1, 0, 1, 0)),
    thumb2_16('BREAKPOINT', 'Breakpoint',
              ['ins <arg>'],
              lambda x, y, z: x[0:4] == (1, 0, 1, 1) and x[4:8] == (1, 1, 1, 0)),
    thumb2_16('IT', 'If-then and hints',
              ['ins'],
              lambda x, y, z: x[0:4] == (1, 0, 1, 1) and x[4:8] == (1, 1, 1, 1)),

    # 32-bit thumb2
    thumb2('BRANCH', 'Branch and miscellaneous control',
           ['ins<c> <label>', 'ins<c> <Rm>'],
           lambda x, y, z: z[0:5] == ['1', '1', '1', '1', '0'] and z[16:17] == ['1']),
    thumb2('TABLE_BRANCH', 'Table branch',
           ['ins<c> <Rn> <Rm>'],
           lambda x, y, z: z[0:12] == ['1', '1', '1', '0', '1', '0', '0', '0', '1', '1', '0', '1']),
    thumb2('MOV_IMM', 'Move immediate',
           ['ins{S}<c> <Rd>,#<const>'],
           lambda x, y, z: z[0:5] == ['1', '1', '1', '1', '0'] and z[6:11] == ['0', '0', '0', '1', '0'] and z[12:17] == ['1', '1', '1', '1', '0']),

    # vfp, these are dummies that never are found true, but create the correct type T_<class>_VFP
    armv7('FP',            'VFP/SIMD', ['ins<c>'], lambda x, y, z: False),
    armv7('SIMD_DATAPROC', 'VFP/SIMD', ['ins<c>'], lambda x, y, z: False),
    armv7('VFP_DATAPROC',  'VFP/SIMD', ['ins<c>'], lambda x, y, z: False),
    armv7('VFP_LDST',      'VFP/SIMD', ['ins<c>'], lambda x, y, z: False),
    armv7('SIMD_LDST',     'VFP/SIMD', ['ins<c>'], lambda x, y, z: False),
    armv7('VFP_SHORTMOVE', 'VFP/SIMD', ['ins<c>'], lambda x, y, z: False),
    armv7('VFP_LONGMOVE',  'VFP/SIMD', ['ins<c>'], lambda x, y, z: False),
    thumb('FP',            'VFP/SIMD', ['ins'], lambda x, y, z: False),
    thumb('SIMD_DATAPROC', 'VFP/SIMD', ['ins'], lambda x, y, z: False),
    thumb('VFP_DATAPROC',  'VFP/SIMD', ['ins'], lambda x, y, z: False),
    thumb('VFP_LDST',      'VFP/SIMD', ['ins'], lambda x, y, z: False),
    thumb('SIMD_LDST',     'VFP/SIMD', ['ins'], lambda x, y, z: False),
    thumb('VFP_SHORTMOVE', 'VFP/SIMD', ['ins'], lambda x, y, z: False),
    thumb('VFP_LONGMOVE',  'VFP/SIMD', ['ins'], lambda x, y, z: False),
]

def write_header(extension, mask):
    magic_open(extension + '-tbl.h')
    print('#ifndef __DARM_' + extension.upper() + '_TBL__')
    print('#define __DARM_' + extension.upper() + '_TBL__')
    print('#include <stdint.h>')
    print('#include "darm-tbl.h"')

    print('extern darm_fieldloader_t ' + extension  + '_lookup[%d];' % (2**mask.count('1')))
    print('#endif')

def write_table(extension, mask, table):
    magic_open(extension + '-tbl.c')
    print('#include "' + extension + '-tbl.h"')

    e = FieldGrab()
    se = repr(e)
    print('#define _EMPTY_LDR %s' % ('{ .format = 0, .instr = I_INVLD, .dtype = D_INVLD, .stype = D_INVLD, .cond = %s, .Rn = %s, .Rm = %s, .Rd = %s}' % (se, se, se, se)))

    print('darm_fieldloader_t ' + extension + '_lookup[%d] = {' % (2**mask.count('1')))
    for i in range(len(table)):
        if table[i] == None:
            print('_EMPTY_LDR,/* %d */' % (i))
        else:
            print(repr(table[i]) + ',/* %d */' % (i))
    print('};')

def create_table(insns, mask):
    # create a table indexed by masked bits of instruction (instruction may go to multiple places in table)
    table = [None for i in range(2**mask.count('1'))]
    for insn in insns:
        # create a loader for this instruction
        loader = InstructionLoad(insn)

        # get all possible bit-strings for this instruction/bitmask
        crossp = selectBits(bit_crossp(insn), mask)
        for p in itertools.product(*crossp):
            idx = bit_index(p)

            # fill in the table with the loader and check for conflicts with other instructions
            if table[idx] != None and False:
                print "WARNING_CONFLICT"
                print idx
                print table[idx]
                print loader
                print p
                print mask
                #assert(table[idx] == None)

            table[idx] = loader
    return table

if __name__ == '__main__':
    armv7_table, thumb_table, thumb2_16_table, thumb2_table = {}, {}, {}, {}

    # the last item (a list) will contain the instructions affected by this
    # encoding type
    instr_types = [list(x) + [[]] for x in instr_types]

    # prepend the instruction set to the encoding types
    insns_types = '', 'ARM_', 'THUMB_', 'THUMB2_16_', 'THUMB2_'
    instr_types = [[x[0]] + [insns_types[x[0]] + x[1]] + x[2:6]
                   for x in instr_types]

    # list of encoding types which should not be emitted in the table (because
    # they are handled somewhere else, in a somewhat hardcoded fashion)
    type_ignore = 'ARM_MUL', 'ARM_STACK0', 'ARM_STACK1', 'ARM_STACK2', \
        'ARM_SAT', 'ARM_SYNC', 'ARM_PUSR', 'ARM_ADR'

    for description in darmtbl.ARMv7:
        instr = description[0]
        bits = description[1:]

        identifier = []
        remainder = []
        for x in range(1 if bits[0] == darmtbl.cond else 4, len(bits)):
            if isinstance(bits[x], int):
                identifier.append(str(bits[x]))
            elif len(identifier) + bits[x].bitsize > 8:
                identifier += ['01'] * (8-len(identifier))
                remainder = bits[x:]
            else:
                identifier += ['01'] * bits[x].bitsize

        # first handle all unconditional instructions, i.e., whitelist those
        # instructions that have already been implemented
        if bits[:4] == (1, 1, 1, 1) and \
                bits[4:7] in ((0, 0, 0), (0, 1, 0), (0, 1, 1), (1, 0, 1)):
            # hardcoded index for the T_UNCOND type encoding
            instr_types[2][-1].append(instr)
            continue

        for x in itertools.product(*identifier[:8]):
            idx = sum(int(x[y])*2**(7-y) for y in range(8))

            # for each conditional instruction, check which type of
            # instruction this is
            for y in instr_types:
                if y[0] == 1 and bits[0] == d.cond and y[4](bits, instr, idx):
                    if not y[1] in type_ignore:
                        armv7_table[idx] = instruction_name(instr), y
                    y[-1].append(instr)
                    break

    def fillTable(allDescriptions, table, inslen, bitmask, typenum):
        sys.stderr.write("\nFilling table\n")
        for description in allDescriptions:
            instr = description[0]
            bits = description[1:]
            sys.stderr.write("Adding instruction " + instr + " : " + str(bits) + "\n")

            # Verify bitcount
            bitcount = sum(1 if isinstance(x, int) else x.bitsize for x in bits)
            assert(bitcount == inslen and "incorrect instruction length")
            if bitcount != inslen:
                continue

            allBits = []

            # Stringify the bit-list
            for x in bits:
                if isinstance(x, int):
                    allBits.append(str(x))
                else:
                    allBits += ['01'] * x.bitsize

            # Select id bits from bit-list
            idbits = selectBits(allBits, bitmask)

            # iterate over each possible encoding, expanding '01' entries
            for enc in itertools.product(*idbits):
                # use concatenated idbits value as index
                idx = sum(int(enc[y])*2**(len(idbits)-1-y) for y in range(len(idbits)))

                # find instruction class
                classEntry = None
                for entry in instr_types:
                    if entry[0] != typenum:
                        continue
                    if entry[4](bits, enc, allBits):
                        classEntry = entry
                        break
                if classEntry == None:
                    sys.stderr.write("Could not find class for instruction " + instruction_name(instr) + ", bits " + str(allBits) + "\n")
                else:
                    if idx in table and table[idx][0] != instruction_name(instr):
                        sys.stderr.write("table collision for " + instruction_name(instr) + " with " + str(table[idx][0]) + "\n")
                    table[idx] = [instruction_name(instr), entry, format_string(instr)]
                    entry[-1].append(instr)


                #for entry in (_ for _ in instr_types if _[0] == typenum):
                #    # check if instruction matches class
                #    if entry[4](bits, enc, allBits):
                #        if idx in table and table[idx][0] != instruction_name(instr):
                #            sys.stderr.write("table collision for " + instruction_name(instr) + " with " + str(table[idx][0]) + "\n")
                #        table[idx] = [instruction_name(instr), entry, format_string(instr)]
                #        inserted = True
                #        # add instruction to list in type
                #        entry[-1].append(instr)
                #        break
                #if not inserted:

    fillTable(darmtblthumb.thumbs, thumb_table, 16, thumb_lookup_bitMask, 2)
    fillTable(darmtblthumb2.thumb16, thumb2_16_table, 16, thumb2_16_lookup_bitMask, 3)
    fillTable(darmtblthumb2.thumb32, thumb2_table, 32, thumb2_lookup_bitMask, 4)

    # make a list of unique instructions affected by each encoding type,
    # we remove the first item from the instruction names, as this is I_INVLD
    instr_types = [x[:5] + [instruction_names(x[5])[1:]] for x in instr_types]

    #
    # darm-tbl.h
    #

    magic_open('darm-tbl.h')

    fmtstrs = generate_format_strings(darmtbl.ARMv7)
    # until we remove all unused instructions..
    instrcnt = len(open('instructions.txt').readlines())

    # print required headers
    print('#ifndef __DARM_TBL__')
    print('#define __DARM_TBL__')
    print('#include <stdint.h>')

    # print type info for each encoding type
    print(type_encoding_enum('darm_enctype', instr_types))

    # print all instruction labels
    print(instruction_names_enum(open('instructions.txt')))
    count = len(instruction_names(open('instructions.txt')))
    print('extern const char *darm_mnemonics[%d];' % count)
    print('extern const char *darm_enctypes[%d];' % len(instr_types))
    print('extern const char *darm_registers[16];')
    print('extern const char *darm_F32_registers[32];')
    print('extern const char *darm_F64_registers[32];')
    print('extern const char *darm_F128_registers[16];')
    print('extern const char *darm_datatypes[%d];' % (len(dtypes) + 1))

    # define constants 0b0 up upto 0b11111111
    for x in range(256):
        print('#define %s %d' % (bin(x)[1:], x))

    # define partial constants with leading zeroes, such as 0b0001
    for x in range(2, 7):
        for y in itertools.product('01', repeat=x):
            num = ''.join(y)
            print('#define b%s %d' % (num, int(num, 2)))

    print(struct_definition('darm_lookup_t',\
                                [['instr', 'uint32_t'],\
                                 ['instr_type', 'uint32_t'],\
                                 ['format', 'char*']]))

    print(enum_table('darm_field', ['F_%s' % (i)\
                     for i in ['INVLD', 'SHIFT_MASK', 'STRING_CONST', 'IMMEDIATE']]))

    print(enum_table('darm_datatype', ['D_%s' % (i)\
                     for i in ['INVLD'] + dtypes]))

    print(struct_definition('darm_fieldgrab_t',\
                                [['type', 'darm_field_t'],\
                                 ['str', 'const char*'],\
                                 ['shift', 'uint32_t'],\
                                 ['mask', 'uint32_t'],\
                                 ['extend', 'uint32_t'],\
                                 ['mult', 'uint32_t']]))

    print(struct_definition('darm_fieldloader_t',\
                                [['instr', 'darm_instr_t'],\
                                 ['format', 'const char*'],\
                                 ['dtype', 'darm_datatype_t'],\
                                 ['stype', 'darm_datatype_t'],\
                                 ['imm', 'darm_fieldgrab_t'],\
                                 ['cond', 'darm_fieldgrab_t'],\
                                 ['Rm', 'darm_fieldgrab_t'],\
                                 ['Rd', 'darm_fieldgrab_t'],\
                                 ['Rn', 'darm_fieldgrab_t']]))

    print('#endif')

    #
    # thumb-tbl.h
    #

    magic_open('thumb-tbl.h')

    # print required headers
    print('#ifndef __DARM_THUMB_TBL__')
    print('#define __DARM_THUMB_TBL__')
    print('#include <stdint.h>')
    print('#include "darm-tbl.h"')

    # print some required definitions
    print('extern const char *thumb_registers[9];')
    print('extern darm_lookup_t thumb_instr_lookup[%d];' % (2**thumb_lookup_bits))
    print('extern darm_lookup_t thumb2_16_instr_lookup[%d];' % (2**thumb2_16_lookup_bits))
    print('extern darm_lookup_t thumb2_instr_lookup[%d];' % (2**thumb2_lookup_bits))

    print('#endif')

    #
    # armv7-tbl.h
    #

    magic_open('armv7-tbl.h')

    # print required headers
    print('#ifndef __DARM_ARMV7_TBL__')
    print('#define __DARM_ARMV7_TBL__')
    print('#include <stdint.h>')
    print('#include "darm-tbl.h"')

    # print some required definitions
    print('extern darm_enctype_t armv7_instr_types[256];')
    def type_lut(name, bits):
        print('extern darm_instr_t type_%s_instr_lookup[%d];' % (name, 2**bits))

    print('extern darm_instr_t armv7_instr_labels[256];')
    type_lut('shift', 4)
    type_lut('brnchmisc', 4)
    type_lut('opless', 3)
    type_lut('uncond2', 3)
    type_lut('mul', 3)
    type_lut('stack0', 5)
    type_lut('stack1', 3)
    type_lut('stack2', 3)
    type_lut('bits', 2)
    type_lut('pas', 6)
    type_lut('sat', 2)
    type_lut('sync', 4)
    type_lut('pusr', 4)

    print('extern const char *armv7_format_strings[%d][3];' % instrcnt)
    print('#endif')

    #
    # darm-tbl.c
    #

    magic_open('darm-tbl.c')
    print('#include <stdio.h>')
    print('#include <stdint.h>')
    print('#include "darm-tbl.h"')
    print(instruction_names_table(open('instructions.txt')))
    print(type_encoding_table('darm_enctypes', instr_types))

    reg = 'r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 r12 SP LR PC'
    print(string_table('darm_registers', reg.split()))

    reg_F32 = ['s%d' % (i) for i in range(32)]
    print(string_table('darm_F32_registers', reg_F32))

    reg_F64 = ['d%d' % (i) for i in range(32)]
    print(string_table('darm_F64_registers', reg_F64))

    reg_F128 = ['q%d' % (i) for i in range(16)]
    print(string_table('darm_F128_registers', reg_F128))

    print(string_table('darm_datatypes', ['INVLD'] + dtypes))

    #
    # thumb-tbl.c
    #

    magic_open('thumb-tbl.c')
    print('#include <stdio.h>')
    print('#include <stdint.h>')
    print('#include "thumb-tbl.h"')

    reg = 'r0 r1 r2 r3 r4 r5 r6 r7 LR'
    print(string_table('thumb_registers', reg.split()))

    # single structure for all lookups
    print(instruction_lookup_table(thumb_table, thumb_lookup_bits, 'thumb'))
    print(instruction_lookup_table(thumb2_16_table, thumb2_16_lookup_bits, 'thumb2_16'))
    print(instruction_lookup_table(thumb2_table, thumb2_lookup_bits, 'thumb2'))


    #
    # armv7-tbl.c
    #

    magic_open('armv7-tbl.c')
    print('#include <stdio.h>')
    print('#include <stdint.h>')
    print('#include "armv7-tbl.h"')

    # print a table containing all the types of instructions
    print(instruction_types_table(armv7_table, 'armv7'))

    # print a table containing the instruction label for each entry
    print(instruction_names_index_table(armv7_table, 'armv7'))

    # print a lookup table for the shift type (which is a sub-type of
    # the dst-src type), the None types represent instructions of the
    # STR family, which we'll handle in the next handler, T_STR.
    t_shift = {
        0b0000: 'lsl',
        0b0001: 'lsl',
        0b0010: 'lsr',
        0b0011: 'lsr',
        0b0100: 'asr',
        0b0101: 'asr',
        0b0110: 'ror',
        0b0111: 'ror',
        0b1000: 'lsl',
        0b1001: None,
        0b1010: 'lsr',
        0b1011: None,
        0b1100: 'asr',
        0b1101: None,
        0b1110: 'ror',
        0b1111: None}

    print(type_lookup_table('type_shift',
                            *[t_shift[x] for x in range(16)]))

    t4 = 'msr', 'bx', 'bxj', 'blx', None, 'qsub', None, 'bkpt', 'smlaw', \
        None, 'smulw', None, 'smlaw', None, 'smulw', None
    print(type_lookup_table('type_brnchmisc', *t4))

    t_opless = 'nop', 'yield', 'wfe', 'wfi', 'sev', None, None, None
    print(type_lookup_table('type_opless', *t_opless))

    t_uncond2 = None, 'clrex', None, None, 'dsb', 'dmb', 'isb', None
    print(type_lookup_table('type_uncond2', *t_uncond2))

    t_mul = 'mul', 'mla', 'umaal', 'mls', 'umull', 'umlal', \
        'smull', 'smlal'
    print(type_lookup_table('type_mul', *t_mul))

    t_stack0 = {
        0b00000: 'str',
        0b00001: 'ldr',
        0b00010: 'strt',
        0b00011: 'ldrt',
        0b00100: 'strb',
        0b00101: 'ldrb',
        0b00110: 'strbt',
        0b00111: 'ldrbt',
        0b01000: 'str',
        0b01001: 'ldr',
        0b01010: 'strt',
        0b01011: 'ldrt',
        0b01100: 'strb',
        0b01101: 'ldrb',
        0b01110: 'strbt',
        0b01111: 'ldrbt',
        0b10000: 'str',
        0b10001: 'ldr',
        0b10010: 'str',
        0b10011: 'ldr',
        0b10100: 'strb',
        0b10101: 'ldrb',
        0b10110: 'strb',
        0b10111: 'ldrb',
        0b11000: 'str',
        0b11001: 'ldr',
        0b11010: 'str',
        0b11011: 'ldr',
        0b11100: 'strb',
        0b11101: 'ldrb',
        0b11110: 'strb',
        0b11111: 'ldrb',
    }

    print(type_lookup_table('type_stack0',
                            *[t_stack0[x] for x in range(32)]))

    t_stack1 = None, None, 'strht', 'ldrht', None, 'ldrsbt', \
        None, 'ldrsht'
    print(type_lookup_table('type_stack1', *t_stack1))

    t_stack2 = None, None, 'strh', 'ldrh', 'ldrd', 'ldrsb', \
        'strd', 'ldrsh'
    print(type_lookup_table('type_stack2', *t_stack2))

    print(type_lookup_table('type_bits', None, 'sbfx', 'bfi', 'ubfx'))

    t_pas = {
        0b000: 'add16',
        0b001: 'asx',
        0b010: 'sax',
        0b011: 'sub16',
        0b100: 'add8',
        0b111: 'sub8',
    }
    t_pas_prefix = 's', 'q', 'sh', 'u', 'uq', 'uh'
    t_pas = dict(((1 + (idx > 2) + idx) * 2**3 + k, x + v)
                 for idx, x in enumerate(t_pas_prefix)
                 for k, v in t_pas.items())
    print(type_lookup_table('type_pas',
                            *[t_pas.get(x) for x in range(64)]))

    print(type_lookup_table('type_sat', 'qadd', 'qsub', 'qdadd', 'qdsub'))

    t_sync = 'swp', None, None, None, 'swpb', None, None, None, \
        'strex', 'ldrex', 'strexd', 'ldrexd', 'strexb', 'ldrexb', \
        'strexh', 'ldrexh'
    print(type_lookup_table('type_sync', *t_sync))

    t_pusr = 'sxtab16', 'sxtb16', None, None, 'sxtab', 'sxtb', \
        'sxtah', 'sxth', 'uxtab16', 'uxtb16', None, None, \
        'uxtab', 'uxtb', 'uxtah', 'uxth'
    print(type_lookup_table('type_pusr', *t_pusr))



    t_alu = 'and', 'eor', 'lsl', 'lsr', 'asr', 'adc', 'sbc', 'ror', \
        'tst', 'rsb', 'cmp', 'cmn', 'orr', 'mul', 'bic', 'mvn'
    print type_lookup_table('type_thumb_alu', *t_alu)

    lines = []
    for instr, fmtstr in fmtstrs.items():
        fmtstr = ', '.join('"%s"' % x for x in set(fmtstr))
        lines.append('    [I_%s] = {%s},' % (instr, fmtstr))
    print('const char *armv7_format_strings[%d][3] = {' % instrcnt)
    print('\n'.join(sorted(lines)))
    print('};')


    #print generate_mask(darmtbl.ARMv7, 32)
    #print generate_mask(darmtblthumb.thumbs, 16)
    #print generate_mask(darmtblthumb2.thumb16, 16)
    #sys.stderr.write("thumb32 mask: " + generate_mask(darmtblthumb2.thumb32, 32) + "\n")
    #print generate_mask(darmtblvfp.thumbvfp, 32)


    insns = darmtblvfp.armvfp
    mask = generate_mask(insns, 32)
    sys.stderr.write("vfp mask: 0b" + mask + "\n")
    table = create_table(insns, mask)
    write_header('armvfp', mask)
    write_table('armvfp', mask, table)

    insns = darmtblvfp.thumbvfp
    mask = generate_mask(insns, 32)
    sys.stderr.write("thumb vfp mask: 0b" + mask + "\n")
    table = create_table(insns, mask)
    write_header('thumbvfp', mask)
    write_table('thumbvfp', mask, table)

    insns = darmtblneon.thumbneon
    mask = generate_mask(insns, 32)
    sys.stderr.write("neon mask 0b" + mask + "\n")
    table = create_table(insns, mask)
    write_header('thumbneon', mask)
    write_table('thumbneon', mask, table)


