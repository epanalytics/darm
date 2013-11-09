#ifndef __DARM_LOOKUPS__
#define __DARM_LOOKUPS__
// thumb_vfp_ldst 0b00000001101100000000000100000000
#define THUMB_VFP_LDST(__v) ((GETBT(__v, 8, 1)) | (GETBT(__v, 20, 2) << 1) | (GETBT(__v, 23, 2) << 3))
#define THUMB_VFP_LDST_LOOKUP(__v) (thumb_vfp_ldst_lookup[THUMB_VFP_LDST(__v)])
// thumb_vfp_dpi 0b00000000101111110000000111000000
#define THUMB_VFP_DPI(__v) ((GETBT(__v, 6, 3)) | (GETBT(__v, 16, 6) << 3) | (GETBT(__v, 23, 1) << 9))
#define THUMB_VFP_DPI_LOOKUP(__v) (thumb_vfp_dpi_lookup[THUMB_VFP_DPI(__v)])
// thumb_neon_ldst 0b00000000001000000000110111110010
#define THUMB_NEON_LDST(__v) ((GETBT(__v, 1, 1)) | (GETBT(__v, 4, 5) << 1) | (GETBT(__v, 10, 2) << 6) | (GETBT(__v, 21, 1) << 8))
#define THUMB_NEON_LDST_LOOKUP(__v) (thumb_neon_ldst_lookup[THUMB_NEON_LDST(__v)])
// thumb_neon_dpi 0b00010000001100000000010101010000
#define THUMB_NEON_DPI(__v) ((GETBT(__v, 4, 1)) | (GETBT(__v, 6, 1) << 1) | (GETBT(__v, 8, 1) << 2) | (GETBT(__v, 10, 1) << 3) | (GETBT(__v, 20, 2) << 4) | (GETBT(__v, 28, 1) << 6))
#define THUMB_NEON_DPI_LOOKUP(__v) (thumb_neon_dpi_lookup[THUMB_NEON_DPI(__v)])
// arm_vfp_ldst 0b00000001101100000000000100000000
#define ARM_VFP_LDST(__v) ((GETBT(__v, 8, 1)) | (GETBT(__v, 20, 2) << 1) | (GETBT(__v, 23, 2) << 3))
#define ARM_VFP_LDST_LOOKUP(__v) (arm_vfp_ldst_lookup[ARM_VFP_LDST(__v)])
// arm_vfp_dpi 0b00000000101111110000000111000000
#define ARM_VFP_DPI(__v) ((GETBT(__v, 6, 3)) | (GETBT(__v, 16, 6) << 3) | (GETBT(__v, 23, 1) << 9))
#define ARM_VFP_DPI_LOOKUP(__v) (arm_vfp_dpi_lookup[ARM_VFP_DPI(__v)])
// arm_neon_ldst 0b00000000101000000000111111110010
#define ARM_NEON_LDST(__v) ((GETBT(__v, 1, 1)) | (GETBT(__v, 4, 8) << 1) | (GETBT(__v, 21, 1) << 9) | (GETBT(__v, 23, 1) << 10))
#define ARM_NEON_LDST_LOOKUP(__v) (arm_neon_ldst_lookup[ARM_NEON_LDST(__v)])
// arm_neon_dpi 0b00000001101111110000111111010000
#define ARM_NEON_DPI(__v) ((GETBT(__v, 4, 1)) | (GETBT(__v, 6, 6) << 1) | (GETBT(__v, 16, 6) << 7) | (GETBT(__v, 23, 2) << 13))
#define ARM_NEON_DPI_LOOKUP(__v) (arm_neon_dpi_lookup[ARM_NEON_DPI(__v)])

#endif
