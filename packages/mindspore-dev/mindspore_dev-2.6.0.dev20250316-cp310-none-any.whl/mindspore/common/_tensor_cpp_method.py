# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Add tensor cpp methods for stub tensor"""

tensor_cpp_methods = ['log', 'exp', 'narrow', 'bitwise_or', '__or__', 'cosh', 'scatter', 'dot', 'sin', 'argsort', 'cos', 'unique', 'div_', '__itruediv__', 'nan_to_num', 'copy_', 'type_as', 'sigmoid', 'less_equal', 'le', 'triu', 'prod', 'index_add', 'chunk', 'unsqueeze', 'kthvalue', 'isneginf', 'less', 'lt', 'topk', 'acos', 'arccos', 'erf', 'logsumexp', 'hardshrink', 'bitwise_xor', '__xor__', 'take', 'put_', 'mm', 'clone', 'log10', 'flatten', 'masked_fill_', 'sum', 'gather', 'mul', 'isclose', 'diag', 'allclose', 'round', 'bitwise_and', '__and__', 'repeat_interleave', 'mul_', '__imul__', 'add', '__add__', 'erfc', 'logaddexp2', 'floor', 'square', 'tan', 'logical_and', 'mean', 'addbmm', 'split', 'histc', 'neg', 'negative', 'new_ones', 'isinf', 'tile', 'isfinite', 'eq', 'tanh', 'nansum', 'clamp', 'clip', 'asinh', 'arcsinh', 't', 'minimum', 'roll', 'atanh', 'arctanh', 'exp_', 'lerp', 'argmin', 'inverse', 'scatter_', 'addmm', 'fmod', 'log_', 'sub', '__sub__', 'sqrt', 'greater_equal', 'ge', 'where', 'rsqrt', 'pow', '__pow__', 'bincount', 'sub_', '__isub__', 'logical_xor', 'add_', '__iadd__', 'all', 'logical_or', 'count_nonzero', 'addmv', 'asin', 'arcsin', 'select', 'view_as', 'transpose', 'expand_as', 'sinh', 'abs', '__abs__', 'absolute', 'outer', 'reciprocal', 'logical_not', 'reshape', 'atan2', 'arctan2', '_to', 'sort', 'argmax', 'remainder', 'true_divide', 'acosh', 'arccosh', 'floor_divide', 'std', 'unbind', 'max', 'subtract', 'not_equal', 'ne', 'min', 'masked_fill', 'floor_divide_', '__ifloordiv__', 'trunc', 'scatter_add', 'masked_select', 'tril', 'new_zeros', 'fill_', 'log2', 'baddbmm', 'frac', 'ceil', 'fill_diagonal_', 'median', 'div', 'divide', 'xlogy', 'gcd', 'log1p', 'var', 'index_select', 'repeat', 'maximum', 'atan', 'arctan', 'logaddexp', 'expm1', 'addcdiv', 'matmul', 'cumsum', 'bitwise_not', 'sinc', 'greater', 'gt', 'any']
