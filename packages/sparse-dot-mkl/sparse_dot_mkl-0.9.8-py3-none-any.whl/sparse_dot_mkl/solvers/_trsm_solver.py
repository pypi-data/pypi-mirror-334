from sparse_dot_mkl._mkl_interface import (
    MKL,
    _create_mkl_sparse,
    _destroy_mkl_handle,
    matrix_descr,
    _get_numpy_layout,
    _check_return_value,
    LAYOUT_CODE_C,
    _out_matrix,
    _mkl_scalar,
    SPARSE_MATRIX_TYPE_SYMMETRIC,
    SPARSE_DIAG_NON_UNIT,
    SPARSE_FILL_MODE_LOWER,
    SPARSE_OPERATION_NON_TRANSPOSE
)

# Dict keyed by ('double_precision_bool', 'complex_bool')
_mkl_sp_mm_funcs = {
    (False, False): MKL._mkl_sparse_s_trsm,
    (True, False): MKL._mkl_sparse_d_trsm,
    (False, True): MKL._mkl_sparse_c_trsm,
    (True, True): MKL._mkl_sparse_z_trsm,
}


def trsm(
    A,
    X,
    alpha=1.0,
    out=None,
    sparse_operation_t=SPARSE_OPERATION_NON_TRANSPOSE,
    sparse_matrix_type_t=SPARSE_MATRIX_TYPE_SYMMETRIC,
    sparse_fill_mode_t=0,
    sparse_diag_type_t=0
):

    _mkl_handles = []

    if A.dtype != X.dtype:
        raise ValueError(
            f'Matrix A ({A.dtype}) type is not the same as '
            f'Matrix X ({X.dtype})'
        )

    try:
        mkl_A, dbl, cplx = _create_mkl_sparse(A)
        _mkl_handles.append(mkl_A)

        layout_x, ld_x = _get_numpy_layout(X)

        out = _out_matrix(
            X.shape,
            X.dtype,
            "C" if layout_x == LAYOUT_CODE_C else "F",
            out_arr=out
        )

        func = _mkl_sp_mm_funcs[(dbl, cplx)]

        ret_val = func(
            sparse_operation_t,
            _mkl_scalar(alpha, cplx, dbl),
            mkl_A,
            matrix_descr(
                sparse_matrix_type_t,
                sparse_fill_mode_t,
                sparse_diag_type_t
            ),
            layout_x,
            X,
            out.shape[1],
            ld_x,
            out
        )

        _check_return_value(ret_val, func.__name__)

        return out

    finally:
        for _mhandle in _mkl_handles:
            _destroy_mkl_handle(_mhandle)
