#ifndef __DARM_EXT_TBL__
#define __DARM_EXT_TBL__
#include <stdint.h>
#include "darm-tbl.h"
extern darm_fieldloader_t thumb_vfp_ldst_lookup[32];
extern darm_fieldloader_t thumb_vfp_dpi_lookup[1024];
extern darm_fieldloader_t thumb_neon_ldst_lookup[512];
extern darm_fieldloader_t thumb_neon_dpi_lookup[128];
extern darm_fieldloader_t arm_vfp_ldst_lookup[32];
extern darm_fieldloader_t arm_vfp_dpi_lookup[1024];
extern darm_fieldloader_t arm_neon_ldst_lookup[2048];
extern darm_fieldloader_t arm_neon_dpi_lookup[32768];

#endif
