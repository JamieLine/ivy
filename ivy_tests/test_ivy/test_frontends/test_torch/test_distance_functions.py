# global
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
import ivy.functional.backends.torch as ivy_torch
import ivy.functional.backends.numpy as ivy_np
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


@handle_cmd_line_args
@given(
    dtype_and_x=helpers.dtype_and_values(
        available_dtypes=tuple(
            set(ivy_np.valid_float_dtypes).intersection(
                set(ivy_torch.valid_float_dtypes)
            )
        ),
        num_arrays=2,
    ),
    # dtype_and_x2=helpers.dtype_and_values(
    #    available_dtypes=tuple(
    #        set(ivy_np.valid_float_dtypes).intersection(
    #            set(ivy_torch.valid_float_dtypes)
    #        )
    #    ),
    #    # TODO: Find a better way to make sure that x1 and x2 are the same size
    #    # This does ensure that, but it also ensures that they are always 3x3 matrices
    #    min_num_dims=2,
    #    max_num_dims=2,
    #    min_dim_size=3,
    #    max_dim_size=3,
    # ),
    # The following bounds are arbitrary
    # (other than min_value = 0 for p,
    # and a max_value = 10 for p causes overflow issues.)
    p=helpers.floats(
        min_value=0, max_value=3.0, allow_nan=False, allow_inf=False, exclude_min=True
    ),
    eps=helpers.floats(
        min_value=1e-8, max_value=1e-4, allow_nan=False, allow_inf=False
    ),
    keepdims=st.booleans(),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.nn.functional.pairwise_distance"
    ),
    as_variable=st.booleans(),
    native_array=st.booleans(),
)
def test_torch_pairwise_distance(
    dtype_and_x,
    # dtype_and_x2,
    p,
    eps,
    keepdims,
    as_variable,
    num_positional_args,
    native_array,
    fw,
):
    dtype, x = dtype_and_x
    x1 = (np.asarray(x[0], dtype=dtype[0]),)
    x2 = (np.asarray(x[1], dtype=dtype[1]),)
    helpers.test_frontend_function(
        input_dtypes=dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="pairwise_distance",
        # These repeated calls look redundant, but
        # they remove an issue where lists are passed
        # into the frontend function.
        x1=np.asarray(x1, dtype=dtype[0]),
        x2=np.asarray(x2, dtype=dtype[1]),
        p=p,
        eps=eps,
        keepdim=keepdims,
    )
