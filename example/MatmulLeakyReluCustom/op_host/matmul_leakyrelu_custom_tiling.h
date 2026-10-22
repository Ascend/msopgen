/* -------------------------------------------------------------------------
 * This file is part of the MindStudio project.
 * Copyright (c) 2026 Huawei Technologies Co.,Ltd.
 *
 * MindStudio is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *
 *          http://license.coscl.org.cn/MulanPSL2
 *
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 * ------------------------------------------------------------------------- */

#ifndef MATMUL_LEAKYRELU_CUSTOM_TILING_H
#define MATMUL_LEAKYRELU_CUSTOM_TILING_H

#include "register/tilingdata_base.h"
#include "tiling/tiling_api.h"

namespace optiling
{
BEGIN_TILING_DATA_DEF(MatmulLeakyreluCustomTilingData)
TILING_DATA_FIELD_DEF(float, alpha);
TILING_DATA_FIELD_DEF_STRUCT(TCubeTiling, cubeTilingData);
END_TILING_DATA_DEF;

REGISTER_TILING_DATA_CLASS(MatmulLeakyreluCustom, MatmulLeakyreluCustomTilingData)
}  // namespace optiling

#endif  // MATMUL_LEAKYRELU_CUSTOM_TILING_H
