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
thumbvfp = [
    ('VABS<c>.F64 <Dd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 0, Dd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VABS<c>.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 0, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VADD<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 1, 1, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),    
    ('VADD<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 1, 1, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),    
    ('VCMP<c>.F64 <Dd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 0, Dd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VCMP<c>.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 0, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VCMPE<c>.F64 <Dd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 0, Dd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VCMPE<c>.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 0, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCMP<c>.F64 <Dd>, #0.0', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 1, Dd, 1, 0, 1, 1, 0, 1, (0), 0, (0), (0), (0), (0)),
    ('VCMP<c>.F32 <Sd>, #0.0', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 1, Sd, 1, 0, 1, 0, 0, 1, (0), 0, (0), (0), (0), (0)),
    ('VCMPE<c>.F64 <Dd>, #0.0', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 1, Dd, 1, 0, 1, 1, 1, 1, (0), 0, (0), (0), (0), (0)),
    ('VCMPE<c>.F32 <Sd>, #0.0', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 1, Sd, 1, 0, 1, 0, 1, 1, (0), 0, (0), (0), (0), (0)),

    ('VCVTB<c>.F32.F16 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 1, 0, Sd, 1, 0, 1, (0), 0, 1, M, 0, Dm),
    ('VCVTB<c>.F16.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 1, 1, Sd, 1, 0, 1, (0), 0, 1, M, 0, Sm),
    ('VCVTT<c>.F32.F16 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 1, 0, Sd, 1, 0, 1, (0), 1, 1, M, 0, Dm),
    ('VCVTT<c>.F16.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 1, 1, Sd, 1, 0, 1, (0), 1, 1, M, 0, Sm),

    ('VCVT<c>.F64.F32 <Dd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 1, 1, Dd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCVT<c>.F32.F64 <Sd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 1, 1, Dd, 1, 0, 1, 1, 1, 1, M, 0, Sm),
    ('VCVTR<c>.S32.F64 <Sd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VCVTR<c>.S32.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VCVTR<c>.U32.F64 <Sd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 0, Sd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VCVTR<c>.U32.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 0, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VCVT<c>.S32.F64 <Sd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VCVT<c>.S32.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCVT<c>.U32.F64 <Sd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 0, Sd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VCVT<c>.U32.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 0, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCVT<c>.F64.S32 <Dd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 0, 0, Dd, 1, 0, 1, 1, 1, 1, M, 0, Sm),
    ('VCVT<c>.F32.S32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 0, 0, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCVT<c>.F64.U32 <Dd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 0, 0, Dd, 1, 0, 1, 1, 0, 1, M, 0, Sm),
    ('VCVT<c>.F32.U32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 0, 0, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VCVT<c>.S16.F64 <Dd>, <Dd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 0, Dd, 1, 0, 1, 1, 0, 1, i, 0, imm4),
    ('VCVT<c>.U16.F64 <Dd>, <Dd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 1, Dd, 1, 0, 1, 1, 0, 1, i, 0, imm4),
    ('VCVT<c>.S32.F64 <Dd>, <Dd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 0, Dd, 1, 0, 1, 1, 1, 1, i, 0, imm4),
    ('VCVT<c>.U32.F64 <Dd>, <Dd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 1, Dd, 1, 0, 1, 1, 1, 1, i, 0, imm4),
    ('VCVT<c>.S16.F32 <Sd>, <Sd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 0, Sd, 1, 0, 1, 0, 0, 1, i, 0, imm4),
    ('VCVT<c>.U16.F32 <Sd>, <Sd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 1, Sd, 1, 0, 1, 0, 0, 1, i, 0, imm4),
    ('VCVT<c>.S32.F32 <Sd>, <Sd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 0, Sd, 1, 0, 1, 0, 1, 1, i, 0, imm4),
    ('VCVT<c>.U32.F32 <Sd>, <Sd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 1, Sd, 1, 0, 1, 0, 1, 1, i, 0, imm4),
    ('VCVT<c>.F64.S16 <Dd>, <Dd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 0, Dd, 1, 0, 1, 1, 0, 1, i, 0, imm4),
    ('VCVT<c>.F64.U16 <Dd>, <Dd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 1, Dd, 1, 0, 1, 1, 0, 1, i, 0, imm4),
    ('VCVT<c>.F64.S32 <Dd>, <Dd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 0, Dd, 1, 0, 1, 1, 1, 1, i, 0, imm4),
    ('VCVT<c>.F64.U32 <Dd>, <Dd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 1, Dd, 1, 0, 1, 1, 1, 1, i, 0, imm4),
    ('VCVT<c>.F32.S16 <Sd>, <Sd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 0, Sd, 1, 0, 1, 0, 0, 1, i, 0, imm4),
    ('VCVT<c>.F32.U16 <Sd>, <Sd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 1, Sd, 1, 0, 1, 0, 0, 1, i, 0, imm4),
    ('VCVT<c>.F32.S32 <Sd>, <Sd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 0, Sd, 1, 0, 1, 0, 1, 1, i, 0, imm4),
    ('VCVT<c>.F32.U32 <Sd>, <Sd>, #<fbits>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 1, Sd, 1, 0, 1, 0, 1, 1, i, 0, imm4),

    ('VDIV<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 0, 0, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),    
    ('VDIV<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 0, 0, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),

    ('VFNMA<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 0, 1, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),    
    ('VFNMA<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 0, 1, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),
    ('VFNMS<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 0, 1, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),    
    ('VFNMS<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 0, 1, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),
    ('VFMA<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 0, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),    
    ('VFMA<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 0, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),
    ('VFMS<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 0, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),    
    ('VFMS<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 0, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),

    ('VLDMIA<c>.64 <Rn>, <list>' , 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 0, 1, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VLDMIA<c>.32 <Rn>, <list>' , 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 0, 1, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VLDMIA<c>.64 <Rn>!, <list>', 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 1, 1, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VLDMIA<c>.32 <Rn>!, <list>', 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 1, 1, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VLDMDB<c>.64 <Rn>!, <list>', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 1, 1, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VLDMDB<c>.32 <Rn>!, <list>', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 1, 1, Rn, Sd, 1, 0, 1, 0, imm8),

    ('VLDR<c>.64 <Dd>, [<Rn>,#+<imm>]', 1, 1, 1, 0, 1, 1, 0, 1, 1, D, 0, 1, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VLDR<c>.64 <Dd>, [<Rn>,#-<imm>]', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 0, 1, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VLDR<c>.32 <Sd>, [<Rn>,#+<imm>]', 1, 1, 1, 0, 1, 1, 0, 1, 1, D, 0, 1, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VLDR<c>.32 <Sd>, [<Rn>,#-<imm>]', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 0, 1, Rn, Sd, 1, 0, 1, 0, imm8),


    #('VLDR<c> <Dd>, <label>', 1, 1, 1, 0, 1, 1, 0, 1, U, D, 0, 1, Rn, Vd, 1, 0, 1, 1, imm8), FIXME U depends on value of label
    #('VLDR<c> <Dd>, [PC, #-0]', 1, 1, 1, 0, 1, 1, 0, 1, U, D, 0, 1, Rn, Vd, 1, 0, 1, 1, imm8),


    ('VMLA<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 0, 0, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),
    ('VMLA<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 0, 0, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),
    ('VMLS<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 0, 0, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),
    ('VMLS<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 0, 0, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),

    ('VMOV<c>.F64 <Dd>, #<imm>',         1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, imm4H, Dd, 1, 0, 1, 1, (0), 0, (0), 0, imm4L),
    ('VMOV<c>.F32 <Sd>, #<imm>',         1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, imm4H, Sd, 1, 0, 1, 0, (0), 0, (0), 0, imm4L),
    ('VMOV<c>.F64 <Dd>, <Dm>',           1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 0, Dd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VMOV<c>.F32 <Sd>, <Sm>',           1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 0, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VMOV<c> <Sm>, <Sm1>, <Rt>, <Rt2>', 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, Rt2, Rt, 1, 0, 1, 0, 0, 0, M, 1, Sm),
    ('VMOV<c> <Rt>, <Rt2>, <Sm>, <Sm1>', 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, Rt2, Rt, 1, 0, 1, 0, 0, 0, M, 1, Sm),
    ('VMOV<c> <Dm>, <Rt>, <Rt2>',        1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, Rt2, Rt, 1, 0, 1, 1, 0, 0, M, 1, Dm),
    ('VMOV<c> <Rt>, <Rt2>, <Dm>',        1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, Rt2, Rt, 1, 0, 1, 1, 0, 0, M, 1, Dm),
    ('VMOV<c> <Sn>, <Rt>',               1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, Sn, Rt, 1, 0, 1, 0, N, (0), (0), 1, (0), (0), (0), (0)),
    ('VMOV<c> <Rt>, <Sn>',               1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, Sn, Rt, 1, 0, 1, 0, N, (0), (0), 1, (0), (0), (0), (0)),
    ('VMOV<c>.32 <Dd[x]>, <Rt>',         1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, Dd, Rt, 1, 0, 1, 1, D, 0, 0, 1, (0), (0), (0), (0)),
    ('VMOV<c>.32 <Rt>, <Dn[x]>',         1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, Dn, Rt, 1, 0, 1, 1, N, 0, 0, 1, (0), (0), (0), (0)),

    ('VMRS<c> <Rt>, FPSID', 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMRS<c> <Rt>, FPSCR', 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMRS<c> <Rt>, MVFR1', 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMRS<c> <Rt>, MVFR0', 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMRS<c> <Rt>, FPEXC', 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),

    ('VMSR<c> FPSCR, <Rt>', 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMSR<c> FPSID, <Rt>', 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMSR<c> FPEXC, <Rt>', 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),

    ('VMUL<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 1, 0, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),
    ('VMUL<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 1, 0, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),

    ('VNEG<c>.F64 <Dd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 1, Dd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VNEG<c>.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 1, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),

    ('VNMLA<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 0, 1, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),
    ('VNMLA<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 0, 1, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),
    ('VNMLS<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 0, 1, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),
    ('VNMLS<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 0, 1, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),

    ('VNMUL<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 1, 0, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),
    ('VNMUL<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 1, 0, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),

    ## TODO: distinguish between these two VPOP
    ('VPOP<c>.64 <list>', 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 1, 1, 1, 1, 0, 1, Dd, 1, 0, 1, 1, imm8),
    ('VPOP<c>.32 <list>', 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 0, imm8),

    ('VPUSH<c>.64 <list>', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 1, 0, 1, 1, 0, 1, Dd, 1, 0, 1, 1, imm8),
    ('VPUSH<c>.32 <list>', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 1, 0, 1, 1, 0, 1, Sd, 1, 0, 1, 0, imm8),

    ('VSQRT<c>.F64 <Dd>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 1, Dd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VSQRT<c>.F32 <Sd>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 1, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),

    ('VSTMIA<c>.64 <Rn>, <list>' , 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 0, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTMIA<c>.32 <Rn>, <list>' , 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 0, 0, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VSTMIA<c>.64 <Rn>!, <list>', 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 1, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTMIA<c>.32 <Rn>!, <list>', 1, 1, 1, 0, 1, 1, 0, 0, 1, D, 1, 0, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VSTMDB<c>.64 <Rn>!, <list>', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 1, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTMDB<c>.32 <Rn>!, <list>', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 1, 0, Rn, Sd, 1, 0, 1, 0, imm8),

    ('VSTR<c>.64 <Dd>, [<Rn>,#+<imm>]', 1, 1, 1, 0, 1, 1, 0, 1, 1, D, 0, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTR<c>.64 <Dd>, [<Rn>,#-<imm>]', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 0, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTR<c>.32 <Sd>, [<Rn>,#+<imm>]', 1, 1, 1, 0, 1, 1, 0, 1, 1, D, 0, 0, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VSTR<c>.32 <Sd>, [<Rn>,#-<imm>]', 1, 1, 1, 0, 1, 1, 0, 1, 0, D, 0, 0, Rn, Sd, 1, 0, 1, 0, imm8),

    ('VSUB<c>.F64 <Dd>, <Dn>, <Dm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 1, 1, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),    
    ('VSUB<c>.F32 <Sd>, <Sn>, <Sm>', 1, 1, 1, 0, 1, 1, 1, 0, 0, D, 1, 1, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm)


]

armvfp = [
    ('VMLA<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 0, D, 0, 0, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),
    ('VMLA<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 0, D, 0, 0, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),
    ('VMLS<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 0, D, 0, 0, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),
    ('VMLS<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 0, D, 0, 0, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),
    ('VNMLA<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 0, D, 0, 1, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),
    ('VNMLA<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 0, D, 0, 1, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),
    ('VNMLS<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 0, D, 0, 1, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),
    ('VNMLS<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 0, D, 0, 1, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),
    ('VNMUL<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 0, D, 1, 0, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),
    ('VNMUL<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 0, D, 1, 0, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),
    ('VMUL<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 0, D, 1, 0, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),
    ('VMUL<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 0, D, 1, 0, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),
    ('VADD<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 0, D, 1, 1, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),    
    ('VADD<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 0, D, 1, 1, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),    
    ('VSUB<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 0, D, 1, 1, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),    
    ('VSUB<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 0, D, 1, 1, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),    
    ('VDIV<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 1, D, 0, 0, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),    
    ('VDIV<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 1, D, 0, 0, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),    
    ('VFNMA<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 1, D, 0, 1, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),    
    ('VFNMA<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 1, D, 0, 1, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),
    ('VFNMS<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 1, D, 0, 1, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),    
    ('VFNMS<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 1, D, 0, 1, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),
    ('VFMA<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 0, Dn, Dd, 1, 0, 1, 1, N, 0, M, 0, Dm),    
    ('VFMA<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 0, Sn, Sd, 1, 0, 1, 0, N, 0, M, 0, Sm),
    ('VFMS<c>.F64 <Dd>, <Dn>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 0, Dn, Dd, 1, 0, 1, 1, N, 1, M, 0, Dm),    
    ('VFMS<c>.F32 <Sd>, <Sn>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 0, Sn, Sd, 1, 0, 1, 0, N, 1, M, 0, Sm),
    ('VABS<c>.F64 <Dd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 0, Dd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VABS<c>.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 0, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VNEG<c>.F64 <Dd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 1, Dd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VNEG<c>.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 1, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VSQRT<c>.F64 <Dd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 1, Dd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VSQRT<c>.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 1, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCVTB<c>.F32.F16 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 1, 0, Sd, 1, 0, 1, (0), 0, 1, M, 0, Dm),
    ('VCVTB<c>.F16.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 1, 1, Sd, 1, 0, 1, (0), 0, 1, M, 0, Sm),
    ('VCVTT<c>.F32.F16 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 1, 0, Sd, 1, 0, 1, (0), 1, 1, M, 0, Dm),
    ('VCVTT<c>.F16.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 1, 1, Sd, 1, 0, 1, (0), 1, 1, M, 0, Sm),
    ('VCMP<c>.F64 <Dd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 0, Dd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VCMP<c>.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 0, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VCMPE<c>.F64 <Dd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 0, Dd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VCMPE<c>.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 0, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCMP<c>.F64 <Dd>, #0.0', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 1, Dd, 1, 0, 1, 1, 0, 1, (0), 0, (0), (0), (0), (0)),
    ('VCMP<c>.F32 <Sd>, #0.0', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 1, Sd, 1, 0, 1, 0, 0, 1, (0), 0, (0), (0), (0), (0)),
    ('VCMPE<c>.F64 <Dd>, #0.0', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 1, Dd, 1, 0, 1, 1, 1, 1, (0), 0, (0), (0), (0), (0)),
    ('VCMPE<c>.F32 <Sd>, #0.0', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 0, 1, Sd, 1, 0, 1, 0, 1, 1, (0), 0, (0), (0), (0), (0)),
    ('VCVT<c>.F64.F32 <Dd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 1, 1, Dd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCVT<c>.F32.F64 <Sd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 1, 1, 1, Dd, 1, 0, 1, 1, 1, 1, M, 0, Sm),
    ('VCVTR<c>.S32.F64 <Sd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VCVTR<c>.S32.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VCVTR<c>.U32.F64 <Sd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 0, Sd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VCVTR<c>.U32.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 0, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VCVT<c>.S32.F64 <Sd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VCVT<c>.S32.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCVT<c>.U32.F64 <Sd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 0, Sd, 1, 0, 1, 1, 1, 1, M, 0, Dm),
    ('VCVT<c>.U32.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 0, 0, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCVT<c>.F64.S32 <Dd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 0, 0, Dd, 1, 0, 1, 1, 1, 1, M, 0, Sm),
    ('VCVT<c>.F32.S32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 0, 0, Sd, 1, 0, 1, 0, 1, 1, M, 0, Sm),
    ('VCVT<c>.F64.U32 <Dd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 0, 0, Dd, 1, 0, 1, 1, 0, 1, M, 0, Sm),
    ('VCVT<c>.F32.U32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 0, 0, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VCVT<c>.S16.F64 <Dd>, <Dd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 0, Dd, 1, 0, 1, 1, 0, 1, i, 0, imm4),
    ('VCVT<c>.U16.F64 <Dd>, <Dd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 1, Dd, 1, 0, 1, 1, 0, 1, i, 0, imm4),
    ('VCVT<c>.S32.F64 <Dd>, <Dd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 0, Dd, 1, 0, 1, 1, 1, 1, i, 0, imm4),
    ('VCVT<c>.U32.F64 <Dd>, <Dd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 1, Dd, 1, 0, 1, 1, 1, 1, i, 0, imm4),
    ('VCVT<c>.S16.F32 <Sd>, <Sd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 0, Sd, 1, 0, 1, 0, 0, 1, i, 0, imm4),
    ('VCVT<c>.U16.F32 <Sd>, <Sd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 1, Sd, 1, 0, 1, 0, 0, 1, i, 0, imm4),
    ('VCVT<c>.S32.F32 <Sd>, <Sd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 0, Sd, 1, 0, 1, 0, 1, 1, i, 0, imm4),
    ('VCVT<c>.U32.F32 <Sd>, <Sd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 1, 1, 1, Sd, 1, 0, 1, 0, 1, 1, i, 0, imm4),
    ('VCVT<c>.F64.S16 <Dd>, <Dd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 0, Dd, 1, 0, 1, 1, 0, 1, i, 0, imm4),
    ('VCVT<c>.F64.U16 <Dd>, <Dd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 1, Dd, 1, 0, 1, 1, 0, 1, i, 0, imm4),
    ('VCVT<c>.F64.S32 <Dd>, <Dd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 0, Dd, 1, 0, 1, 1, 1, 1, i, 0, imm4),
    ('VCVT<c>.F64.U32 <Dd>, <Dd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 1, Dd, 1, 0, 1, 1, 1, 1, i, 0, imm4),
    ('VCVT<c>.F32.S16 <Sd>, <Sd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 0, Sd, 1, 0, 1, 0, 0, 1, i, 0, imm4),
    ('VCVT<c>.F32.U16 <Sd>, <Sd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 1, Sd, 1, 0, 1, 0, 0, 1, i, 0, imm4),
    ('VCVT<c>.F32.S32 <Sd>, <Sd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 0, Sd, 1, 0, 1, 0, 1, 1, i, 0, imm4),
    ('VCVT<c>.F32.U32 <Sd>, <Sd>, #<fbits>', cond, 1, 1, 1, 0, 1, D, 1, 1, 1, 0, 1, 1, Sd, 1, 0, 1, 0, 1, 1, i, 0, imm4),

    ('VSTMIA<c>.64 <Rn>, <list>' , cond, 1, 1, 0, 0, 1, D, 0, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTMIA<c>.32 <Rn>, <list>' , cond, 1, 1, 0, 0, 1, D, 0, 0, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VSTMIA<c>.64 <Rn>!, <list>', cond, 1, 1, 0, 0, 1, D, 1, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTMIA<c>.32 <Rn>!, <list>', cond, 1, 1, 0, 0, 1, D, 1, 0, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VSTMDB<c>.64 <Rn>!, <list>', cond, 1, 1, 0, 1, 0, D, 1, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTMDB<c>.32 <Rn>!, <list>', cond, 1, 1, 0, 1, 0, D, 1, 0, Rn, Sd, 1, 0, 1, 0, imm8),

    ('VSTR<c>.64 <Dd>, [<Rn>,#+<imm>]', cond, 1, 1, 0, 1, 1, D, 0, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTR<c>.64 <Dd>, [<Rn>,#-<imm>]', cond, 1, 1, 0, 1, 0, D, 0, 0, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VSTR<c>.32 <Sd>, [<Rn>,#+<imm>]', cond, 1, 1, 0, 1, 1, D, 0, 0, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VSTR<c>.32 <Sd>, [<Rn>,#-<imm>]', cond, 1, 1, 0, 1, 0, D, 0, 0, Rn, Sd, 1, 0, 1, 0, imm8),


    ('VLDMIA<c>.64 <Rn>, <list>',  cond, 1, 1, 0, 0, 1, D, 0, 1, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VLDMIA<c>.32 <Rn>, <list>',  cond, 1, 1, 0, 0, 1, D, 0, 1, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VLDMIA<c>.64 <Rn>!, <list>', cond, 1, 1, 0, 0, 1, D, 1, 1, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VLDMIA<c>.32 <Rn>!, <list>', cond, 1, 1, 0, 0, 1, D, 1, 1, Rn, Sd, 1, 0, 1, 0, imm8),
    ('VLDMDB<c>.64 <Rn>!, <list>', cond, 1, 1, 0, 1, 0, D, 1, 1, Rn, Dd, 1, 0, 1, 1, imm8),
    ('VLDMDB<c>.32 <Rn>!, <list>', cond, 1, 1, 0, 1, 0, D, 1, 1, Rn, Sd, 1, 0, 1, 0, imm8),\

    ## TODO: distinguish between these two VPOP
    ('VPOP<c>.64 <list>', cond, 1, 1, 0, 0, 1, D, 1, 1, 1, 1, 0, 1, Dd, 1, 0, 1, 1, imm8),
    ('VPOP<c>.32 <list>', cond, 1, 1, 0, 0, 1, D, 1, 1, 1, 1, 0, 1, Sd, 1, 0, 1, 0, imm8),

    ('VPUSH<c>.64 <list>', cond, 1, 1, 0, 1, 0, D, 1, 0, 1, 1, 0, 1, Dd, 1, 0, 1, 1, imm8),
    ('VPUSH<c>.32 <list>', cond, 1, 1, 0, 1, 0, D, 1, 0, 1, 1, 0, 1, Sd, 1, 0, 1, 0, imm8),

    ('VLDR<c>.64 <Dd>, [<Rn>,#+<imm>]', cond, 1, 1, 0, 1, 1, D, 0, 1, Rn, Dd, 1, 0, 1, 1, imm(8, {'m': 4})),
    ('VLDR<c>.64 <Dd>, [<Rn>,#-<imm>]', cond, 1, 1, 0, 1, 0, D, 0, 1, Rn, Dd, 1, 0, 1, 1, imm(8, {'m': -4})),
    ('VLDR<c>.32 <Sd>, [<Rn>,#+<imm>]', cond, 1, 1, 0, 1, 1, D, 0, 1, Rn, Sd, 1, 0, 1, 0, imm(8, {'m': 4})),
    ('VLDR<c>.32 <Sd>, [<Rn>,#-<imm>]', cond, 1, 1, 0, 1, 0, D, 0, 1, Rn, Sd, 1, 0, 1, 0, imm(8, {'m': -4})),
    #('VLDR<c> <Dd>, <label>', cond, 1, 1, 0, 1, U, D, 0, 1, Rn, Vd, 1, 0, 1, 1, imm8), FIXME U depends on value of label
    #('VLDR<c> <Dd>, [PC, #-0]', cond, 1, 1, 0, 1, U, D, 0, 1, Rn, Vd, 1, 0, 1, 1, imm8),

    ('VMOV<c>.F64 <Dd>, #<imm>', cond, 1, 1, 1, 0, 1, D, 1, 1, imm4H, Dd, 1, 0, 1, 1, (0), 0, (0), 0, imm4L),
    ('VMOV<c>.F32 <Sd>, #<imm>', cond, 1, 1, 1, 0, 1, D, 1, 1, imm4H, Sd, 1, 0, 1, 0, (0), 0, (0), 0, imm4L),
    ('VMOV<c>.F64 <Dd>, <Dm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 0, Dd, 1, 0, 1, 1, 0, 1, M, 0, Dm),
    ('VMOV<c>.F32 <Sd>, <Sm>', cond, 1, 1, 1, 0, 1, D, 1, 1, 0, 0, 0, 0, Sd, 1, 0, 1, 0, 0, 1, M, 0, Sm),
    ('VMOV<c> <Sm>, <Sm1>, <Rt>, <Rt2>', cond, 1, 1, 0, 0, 0, 1, 0, 0, Rt2, Rt, 1, 0, 1, 0, 0, 0, M, 1, Sm),
    ('VMOV<c> <Rt>, <Rt2>, <Sm>, <Sm1>', cond, 1, 1, 0, 0, 0, 1, 0, 1, Rt2, Rt, 1, 0, 1, 0, 0, 0, M, 1, Sm),
    ('VMOV<c> <Dm>, <Rt>, <Rt2>', cond, 1, 1, 0, 0, 0, 1, 0, 0, Rt2, Rt, 1, 0, 1, 1, 0, 0, M, 1, Dm),
    ('VMOV<c> <Rt>, <Rt2>, <Dm>', cond, 1, 1, 0, 0, 0, 1, 0, 1, Rt2, Rt, 1, 0, 1, 1, 0, 0, M, 1, Dm),
    ('VMOV<c> <Sn>, <Rt>', cond, 1, 1, 1, 0, 0, 0, 0, 0, Sn, Rt, 1, 0, 1, 0, N, (0), (0), 1, (0), (0), (0), (0)),
    ('VMOV<c> <Rt>, <Sn>', cond, 1, 1, 1, 0, 0, 0, 0, 1, Sn, Rt, 1, 0, 1, 0, N, (0), (0), 1, (0), (0), (0), (0)),
    ('VMOV<c>.32 <Dd[x]>, <Rt>', cond, 1, 1, 1, 0, 0, 0, 0, 0, Dd, Rt, 1, 0, 1, 1, D, 0, 0, 1, (0), (0), (0), (0)),
    ('VMOV<c>.32 <Rt>, <Dn[x]>', cond, 1, 1, 1, 0, 0, 0, 0, 1, Dn, Rt, 1, 0, 1, 1, N, 0, 0, 1, (0), (0), (0), (0)),

    ('VMSR<c> FPSCR, <Rt>', cond, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMSR<c> FPSID, <Rt>', cond, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMSR<c> FPEXC, <Rt>', cond, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMRS<c> <Rt>, FPSID', cond, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMRS<c> <Rt>, FPSCR', cond, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMRS<c> <Rt>, MVFR1', cond, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMRS<c> <Rt>, MVFR0', cond, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),
    ('VMRS<c> <Rt>, FPEXC', cond, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, Rt, 1, 0, 1, 0, (0), (0), (0), 1, (0), (0), (0), (0)),


]


if __name__ == '__main__':
    num = 0
    for description in thumbvfp:
        instr = description[0]
        bits = description[1:]

        bits = [1 if type(x) == int else x.bitsize for x in bits]
        if sum(bits) != 32:
            print(instr, bits, sum(bits))
        num += 1
    print "Verified " + str(num) + " 32-bit thumb vfp instructions"

    num = 0
    for description in armvfp:
        instr = description[0]
        bits = description[1:]

        bits = [1 if type(x) == int else x.bitsize for x in bits]
        if sum(bits) != 32:
            print(instr, bits, sum(bits))
        num += 1
    print "Verified " + str(num) + " 32-bit arm vfp instructions"
