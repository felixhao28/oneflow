"""
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import oneflow
from oneflow.framework.docstr.utils import add_docstr

add_docstr(
    oneflow.tensor,
    r"""
    Constructs a tensor with data, return a global tensor if placement and sbp are in kwargs,
       otherwise return a local tensor.

    Arguments:
        data: Initial data for the tensor. Can be a list, tuple, NumPy ndarray, scalar or tensor.
    Keyword Arguments:
        dtype (oneflow.dtype, optional) – the desired data type of returned tensor.
            Default: if None, infers data type from data.
        device (oneflow.device, optional): the desired device of returned tensor. If placement
            and sbp is None, uses the current cpu for the default tensor type.
        placement (oneflow.placement, optional): the desired placement of returned tensor.
        sbp (oneflow.sbp or tuple of oneflow.sbp, optional): the desired sbp of returned tensor.
        requires_grad (bool, optional): If autograd should record operations on the returned tensor. Default: False

    Note:
        The Keyword Argument device is mutually exclusive with placement and sbp.


    For example:

    .. code-block:: python

        >>> import oneflow as flow

        >>> x = flow.tensor([1,2,3])
        >>> x
        tensor([1, 2, 3], dtype=oneflow.int64)

    """,
)

add_docstr(
    oneflow.from_numpy,
    r"""
    Creates a ``Tensor`` from a ``numpy.ndarray``.

    The returned tensor and ndarray share the same memory. Modifications to the tensor
    will be reflected in the ndarray and vice versa.

    It currently accepts ndarray with dtypes of numpy.float64, numpy.float32, numpy.float16,
    numpy.int64, numpy.int32, numpy.int8, numpy.uint8.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np
        >>> np_arr = np.arange(6).reshape(2, 3)
        >>> t = flow.from_numpy(np_arr)
        >>> t
        tensor([[0, 1, 2],
                [3, 4, 5]], dtype=oneflow.int64)
        >>> np_arr[0, 0] = -1
        >>> t
        tensor([[-1,  1,  2],
                [ 3,  4,  5]], dtype=oneflow.int64)
    """,
)


add_docstr(
    oneflow.Tensor.device,
    r"""
    The documentation is referenced from:
    https://pytorch.org/docs/stable/generated/torch.Tensor.device.html#torch.Tensor.device
    
    Is the :class:`oneflow.device` where this Tensor is, which is invalid for global tensor.
    """,
)

add_docstr(
    oneflow.Tensor.placement,
    r"""
    Is the :class:`oneflow.placement` where this Tensor is, which is invalid for local tensor.
    """,
)

add_docstr(
    oneflow.Tensor.sbp,
    r"""
    Is the ``oneflow.sbp`` representing that how the data of the global tensor is distributed, which is invalid for local tensor.
    """,
)

add_docstr(
    oneflow.Tensor.is_global,
    r"""
    Return whether this Tensor is a global tensor.
    """,
)

add_docstr(
    oneflow.Tensor.atan2,
    r"""
    See :func:`oneflow.atan2`
    """,
)

add_docstr(
    oneflow.Tensor.expand,
    """
    Tensor.expand() -> Tensor

    See :func:`oneflow.expand`
    """,
)

add_docstr(
    oneflow.Tensor.expand_as,
    """
    expand_as(other) -> Tensor

    Expand this tensor to the same size as :attr:`other`.
    ``self.expand_as(other)`` is equivalent to ``self.expand(other.size())``.

    Please see :meth:`~Tensor.expand` for more information about ``expand``.

    Args:
        other (:class:`oneflow.Tensor`): The result tensor has the same size
            as :attr:`other`.
    """,
)

add_docstr(
    oneflow.Tensor.flatten,
    """
    See :func:`oneflow.flatten`
    """,
)

add_docstr(
    oneflow.Tensor.floor,
    """
    See :func:`oneflow.floor`
    """,
)

add_docstr(
    oneflow.Tensor.flip,
    """
    See :func:`oneflow.flip`
    """,
)

add_docstr(
    oneflow.Tensor.in_top_k,
    """
    Tensor.in_top_k(targets, predictions, k) -> Tensor

    See :func:`oneflow.in_top_k`
    """,
)

add_docstr(
    oneflow.Tensor.index_select,
    """
    Tensor.index_select(dim, index) -> Tensor

    See :func:`oneflow.index_select`
    """,
)

add_docstr(
    oneflow.Tensor.numel,
    """
    See :func:`oneflow.numel`
    """,
)

add_docstr(
    oneflow.Tensor.new_ones,
    """
    Tensor.new_ones() -> Tensor

    See :func:`oneflow.new_ones`
    """,
)

add_docstr(
    oneflow.Tensor.to_global,
    """
    Tensor.to_global(placement=None, sbp=None, grad_sbp=None) -> Tensor

    Creates a global tensor if this tensor is a local tensor, otherwise performs Tensor placement and/or sbp conversion.

    Note:
        This tensor can be local tensor or global tensor.

        - For local tensor

          Both placement and sbp are required.

          The returned global tensor takes this tensor as its local component in the current rank.

          There is no data communication usually, but when sbp is ``oneflow.sbp.broadcast``, the data on rank 0 will be broadcast to other ranks.

        - For global tensor

          At least one of placement and sbp is required.

          If placement and sbp are all the same as this tensor's own placement and sbp, then returns this tensor own.
    
    Args:
        placement (flow.placement, optional): the desired placement of returned global tensor. Default: None
        sbp (flow.sbp.sbp or tuple of flow.sbp.sbp, optional): the desired sbp of returned global tensor. Default: None
        grad_sbp (flow.sbp.sbp or tuple of flow.sbp.sbp, optional): manually specify the sbp of this tensor's grad tensor in the backward pass. If None, the grad tensor sbp will be infered automatically. It is only used if this tensor is a global tensor. Default: None

    For local tensor:

    .. code-block:: python

        >>> # Run on 2 ranks respectively
        >>> import oneflow as flow
        >>> input = flow.tensor([0., 1.], dtype=flow.float32) # doctest: +SKIP
        >>> output = input.to_global(placement=flow.placement("cpu", ranks=[0, 1]), sbp=[flow.sbp.split(0)]) # doctest: +SKIP
        >>> print(output.size()) # doctest: +SKIP
        >>> print(output) # doctest: +SKIP

    .. code-block:: python

        >>> # results on rank 0
        oneflow.Size([4])
        tensor([0., 1., 0., 1.], placement=oneflow.placement(type="cpu", ranks=[0, 1]), sbp=(oneflow.sbp.split(axis=0),), dtype=oneflow.float32) 
 
    .. code-block:: python

        >>> # results on rank 1
        oneflow.Size([4])
        tensor([0., 1., 0., 1.], placement=oneflow.placement(type="cpu", ranks=[0, 1]), sbp=(oneflow.sbp.split(axis=0),), dtype=oneflow.float32)

    For global tensor:

    .. code-block:: python

        >>> # Run on 2 ranks respectively
        >>> import oneflow as flow
        >>> input = flow.tensor([0., 1.], dtype=flow.float32, placement=flow.placement("cpu", ranks=[0, 1]), sbp=[flow.sbp.broadcast]) # doctest: +SKIP
        >>> output = input.to_global(placement=flow.placement("cpu", ranks=[0, 1]), sbp=[flow.sbp.split(0)]) # doctest: +SKIP
        >>> print(output.size()) # doctest: +SKIP
        >>> print(output) # doctest: +SKIP

    .. code-block:: python

        >>> # results on rank 0
        oneflow.Size([2])
        tensor([0., 1.], placement=oneflow.placement(type="cpu", ranks=[0, 1]), sbp=(oneflow.sbp.split(axis=0),), dtype=oneflow.float32)

    .. code-block:: python

        >>> # results on rank 1
        oneflow.Size([2])
        tensor([0., 1.], placement=oneflow.placement(type="cpu", ranks=[0, 1]), sbp=(oneflow.sbp.split(axis=0),), dtype=oneflow.float32)
    """,
)

add_docstr(
    oneflow.Tensor.to_consistent,
    """
    This interface is no longer available, please use :func:`oneflow.Tensor.to_global` instead.
    """,
)

add_docstr(
    oneflow.Tensor.to_local,
    """
    Tensor.to_local() -> Tensor

    Returns the local component of this global tensor in the current rank.

    Note:
        This tensor should be a global tensor, and it returns a empty tensor if there is no local component in the current rank.

        No copy occurred in this operation.

    For example:

    .. code-block:: python

        >>> # Run on 2 ranks respectively
        >>> import oneflow as flow
        >>> x = flow.tensor([0., 1.], dtype=flow.float32, placement=flow.placement("cpu", ranks=[0, 1]), sbp=[flow.sbp.split(0)]) # doctest: +SKIP
        >>> y = x.to_local() # doctest: +SKIP
        >>> print(y.size()) # doctest: +SKIP
        >>> print(y) # doctest: +SKIP

    .. code-block:: python

        >>> # results on rank 0
        oneflow.Size([1])
        tensor([0.], dtype=oneflow.float32)

    .. code-block:: python

        >>> # results on rank 1
        oneflow.Size([1])
        tensor([1.], dtype=oneflow.float32)
    """,
)

add_docstr(
    oneflow.Tensor.transpose,
    """
    See :func:`oneflow.transpose`
    """,
)

add_docstr(
    oneflow.Tensor.logical_not,
    """
    logical_not() -> Tensor
    See :func:`oneflow.logical_not`
    """,
)

add_docstr(
    oneflow.Tensor.std,
    """
    See :func:`oneflow.std`
    """,
)

add_docstr(
    oneflow.Tensor.var,
    """
    See :func:`oneflow.var`
    """,
)

add_docstr(
    oneflow.Tensor.squeeze,
    """
    See :func:`oneflow.squeeze`
    """,
)

add_docstr(
    oneflow.Tensor.unfold,
    """
    The interface is consistent with PyTorch.
    The documentation is referenced from: https://pytorch.org/docs/stable/generated/torch.Tensor.unfold.html#torch.Tensor.unfold.

    Returns a view of the original tensor which contains all slices of `size` size from `self`
    tensor in the dimension `dimension`.

    Step between two slices is given by `step`.

    If sizedim is the size of dimension `dimension` for `self`, the size of dimension dimension in the
    returned tensor will be (sizedim - size) / step + 1.

    An additional dimension of size `size` is appended in the returned tensor.

    Args:
        dimension (int): dimension in which unfolding happens
        size (int): the size of each slice that is unfolded
        step (int): the step between each slice

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow

        >>> x = flow.arange(1., 8)
        >>> x
        tensor([1, 2, 3, 4, 5, 6, 7], dtype=oneflow.int64)
        >>> x.unfold(0, 2, 1)
        tensor([[1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7]], dtype=oneflow.int64)
        >>> x.unfold(0, 2, 2)
        tensor([[1, 2],
                [3, 4],
                [5, 6]], dtype=oneflow.int64)
    """,
)

add_docstr(
    oneflow.Tensor.matmul,
    """
    See :func:`oneflow.matmul`
    """,
)

add_docstr(
    oneflow.Tensor.narrow,
    """
    See :func:`oneflow.narrow`
    """,
)

add_docstr(
    oneflow.Tensor.unsqueeze,
    """
    See :func:`oneflow.unsqueeze`
    """,
)

add_docstr(
    oneflow.Tensor.permute,
    """
    See :func:`oneflow.permute`
    """,
)

add_docstr(
    oneflow.Tensor.abs,
    """
    See :func:`oneflow.abs`
    """,
)

add_docstr(
    oneflow.Tensor.acos,
    """
    See :func:`oneflow.acos`
    """,
)

add_docstr(
    oneflow.Tensor.arccos,
    """
    See :func:`oneflow.arccos`
    """,
)

add_docstr(
    oneflow.Tensor.acosh,
    """
    See :func:`oneflow.acosh`
    """,
)

add_docstr(
    oneflow.Tensor.arccosh,
    """
    See :func:`oneflow.arccosh`
    """,
)

add_docstr(
    oneflow.Tensor.arctanh,
    """
    See :func:`oneflow.arctanh`
    """,
)

add_docstr(
    oneflow.Tensor.argmax,
    """
    See :func:`oneflow.argmax`
    """,
)

add_docstr(
    oneflow.Tensor.argmin,
    """
    See :func:`oneflow.argmin`
    """,
)

add_docstr(
    oneflow.Tensor.argsort,
    """
    See :func:`oneflow.argsort`
    """,
)

add_docstr(
    oneflow.Tensor.argwhere,
    """
    See :func:`oneflow.argwhere`
    """,
)

add_docstr(
    oneflow.Tensor.atanh,
    """
    See :func:`oneflow.atanh`
    """,
)

add_docstr(
    oneflow.Tensor.backward,
    """
    The interface is consistent with PyTorch.
    The documentation is referenced from: https://pytorch.org/docs/stable/generated/torch.Tensor.backward.html#torch.Tensor.backward.

    Computes the gradient of current tensor w.r.t. graph leaves.

    The graph is differentiated using the chain rule. If the tensor is non-scalar (i.e. its data has more than one element) and requires gradient, the function additionally requires specifying gradient. It should be a tensor of matching type and location, that contains the gradient of the differentiated function w.r.t. self.

    This function accumulates gradients in the leaves - you might need to zero .grad attributes or set them to None before calling it. See Default gradient layouts for details on the memory layout of accumulated gradients.

    Note:
        If you run any forward ops, create gradient, and/or call backward in a user-specified CUDA stream context, see Stream semantics of backward passes.
    Note:
        When inputs are provided and a given input is not a leaf, the current implementation will call its grad_fn (though it is not strictly needed to get this gradients). It is an implementation detail on which the user should not rely. See https://github.com/pytorch/pytorch/pull/60521#issuecomment-867061780 for more details.

    Args:
        gradient (Tensor or None): Gradient w.r.t. the tensor. If it is a tensor, it will be automatically converted to a Tensor that does not require grad unless create_graph is True. None values can be specified for scalar Tensors or ones that don’t require grad. If a None value would be acceptable then this argument is optional.

        retain_graph (bool, optional): If False, the graph used to compute the grads will be freed. Note that in nearly all cases setting this option to True is not needed and often can be worked around in a much more efficient way. Defaults to the value of create_graph.

        create_graph (bool, optional): If True, graph of the derivative will be constructed, allowing to compute higher order derivative products. Defaults to False.
    """,
)

add_docstr(
    oneflow.Tensor.bmm,
    """
    See :func:`oneflow.bmm`
    """,
)

add_docstr(
    oneflow.Tensor.chunk,
    """
    See :func:`oneflow.chunk`
    """,
)

add_docstr(
    oneflow.Tensor.split,
    """
    See :func:`oneflow.split`
    """,
)

add_docstr(
    oneflow.Tensor.swapaxes,
    """
    See :func:`oneflow.swapaxes`
    """,
)

add_docstr(
    oneflow.Tensor.cast,
    """
    See :func:`oneflow.cast`
    """,
)

add_docstr(
    oneflow.Tensor.diag,
    """
    See :func:`oneflow.diag`
    """,
)

add_docstr(
    oneflow.Tensor.dim,
    """
    Tensor.dim() → int

    Returns the number of dimensions of self tensor.
    """,
)

add_docstr(
    oneflow.Tensor.element_size,
    """
    Tensor.element_size() → int

    Returns the size in bytes of an individual element.

    """,
)

add_docstr(
    oneflow.Tensor.exp,
    """
    See :func:`oneflow.exp`
    """,
)

add_docstr(
    oneflow.Tensor.erf,
    """
    Tensor.erf() -> Tensor

    See :func:`oneflow.erf`
    """,
)

add_docstr(
    oneflow.Tensor.erfc,
    """
    Tensor.erfc() -> Tensor

    See :func:`oneflow.erfc`
    """,
)

add_docstr(
    oneflow.Tensor.erfinv,
    """
    See :func:`oneflow.erfinv`
    """,
)

add_docstr(
    oneflow.Tensor.erfinv_,
    """
    Inplace version of :func:`oneflow.erfinv`
    """,
)

add_docstr(
    oneflow.Tensor.eq,
    """
    See :func:`oneflow.eq`
    """,
)

add_docstr(
    oneflow.Tensor.lt,
    """
    See :func:`oneflow.lt`
    """,
)

add_docstr(
    oneflow.Tensor.le,
    """
    See :func:`oneflow.le`
    """,
)

add_docstr(
    oneflow.Tensor.ne,
    """
    See :func:`oneflow.ne`
    """,
)

add_docstr(
    oneflow.Tensor.fill_,
    """
    Tensor.fill_(value) → Tensor

    Fills self tensor with the specified value.
    """,
)

add_docstr(
    oneflow.Tensor.ge,
    """
    See :func:`oneflow.ge`
    """,
)

add_docstr(
    oneflow.Tensor.gelu,
    """
    See :func:`oneflow.gelu`
    """,
)

add_docstr(
    oneflow.Tensor.get_device,
    """
    Tensor.get_device() -> Device ordinal (Integer)

    For CUDA tensors, this function returns the device ordinal of the GPU on which the tensor resides. For CPU tensors, an error is thrown.


    """,
)

add_docstr(
    oneflow.Tensor.gt,
    """
    See :func:`oneflow.gt`
    """,
)

add_docstr(
    oneflow.Tensor.log1p,
    """
    See :func:`oneflow.log1p`
    """,
)

add_docstr(
    oneflow.Tensor.mish,
    """
    See :func:`oneflow.mish`
    """,
)

add_docstr(
    oneflow.Tensor.mul,
    """Tensor.mul(value) -> Tensor
    See :func:`oneflow.mul`
    """,
)

add_docstr(
    oneflow.Tensor.mul_,
    """Tensor.mul_(value) -> Tensor

    In-place version of :func:`oneflow.Tensor.mul`.
    """,
)

add_docstr(
    oneflow.Tensor.div_,
    """Tensor.div_(value) -> Tensor
    In-place version of :func:`oneflow.Tensor.div`.
    """,
)

add_docstr(
    oneflow.Tensor.sub_,
    """Tensor.sub_(value) -> Tensor
    In-place version of :func:`oneflow.Tensor.sub`.
    """,
)

add_docstr(
    oneflow.Tensor.negative,
    """
    See :func:`oneflow.negative`
    """,
)

add_docstr(
    oneflow.Tensor.nelement,
    """
    Tensor.nelement() → int

    Alias for numel()
    """,
)

add_docstr(
    oneflow.Tensor.floor_,
    r"""
    In-place version of :func:`oneflow.floor`

    """,
)

add_docstr(
    oneflow.Tensor.normal_,
    """
    normal_(mean=0, std=1, *, generator=None) -> Tensor

    Fills :attr:`self` tensor with elements samples from the normal distribution parameterized by :attr:`mean` and :attr:`std`.
    """,
)

add_docstr(
    oneflow.Tensor.numpy,
    """
    Tensor.numpy() → numpy.ndarray

    Returns self tensor as a NumPy ndarray. This tensor and the returned ndarray share the same underlying storage. Changes to
     self tensor will be reflected in the ndarray and vice versa.
    """,
)

add_docstr(
    oneflow.Tensor.pow,
    """
    See :func:`oneflow.pow`
    """,
)

add_docstr(
    oneflow.Tensor.relu,
    """
    See :func:`oneflow.relu`
    """,
)

add_docstr(
    oneflow.Tensor.roll,
    """
    See :func:`oneflow.roll`
    """,
)

add_docstr(
    oneflow.Tensor.round,
    """
    See :func:`oneflow.round`
    """,
)

add_docstr(
    oneflow.Tensor.reciprocal,
    """
    See :func:`oneflow.reciprocal`
    """,
)

add_docstr(
    oneflow.Tensor.add,
    """
    See :func:`oneflow.add`
    """,
)

add_docstr(
    oneflow.Tensor.add_,
    """
    In-place version of :func:`oneflow.Tensor.add`.
    """,
)

add_docstr(
    oneflow.Tensor.asin,
    """
    See :func:`oneflow.asin`
    """,
)

add_docstr(
    oneflow.Tensor.arcsin,
    """
    See :func:`oneflow.arcsin`
    """,
)

add_docstr(
    oneflow.Tensor.arcsinh,
    """
    See :func:`oneflow.arcsinh`
    """,
)

add_docstr(
    oneflow.Tensor.sin,
    """
    sin() -> Tensor

    See :func:`oneflow.sin`
    """,
)

add_docstr(
    oneflow.Tensor.cos,
    """
    See :func:`oneflow.cos`
    """,
)

add_docstr(
    oneflow.Tensor.atan,
    """
    See :func:`oneflow.atan`
    """,
)

add_docstr(
    oneflow.Tensor.arctan,
    """
    See :func:`oneflow.arctan`
    """,
)

add_docstr(
    oneflow.Tensor.selu,
    """
    See :func:`oneflow.selu`
    """,
)

add_docstr(
    oneflow.Tensor.sigmoid,
    """
    See :func:`oneflow.sigmoid`
    """,
)

add_docstr(
    oneflow.Tensor.sign,
    """
    See :func:`oneflow.sign`
    """,
)

add_docstr(
    oneflow.Tensor.silu,
    """
    See :func:`oneflow.silu`
    """,
)

add_docstr(
    oneflow.Tensor.sinh,
    """
    See :func:`oneflow.sinh`
    """,
)

add_docstr(
    oneflow.Tensor.size,
    """
    The interface is consistent with PyTorch.

    Returns the size of the self tensor. If dim is not specified, the returned value is a oneflow.Size, a subclass of tuple. If dim is specified, returns an int holding the size of that dimension.

    Args:
        idx (int, optional): The dimension for which to retrieve the size.


    """,
)

add_docstr(
    oneflow.Tensor.softmax,
    """
    See :func:`oneflow.softmax`
    """,
)

add_docstr(
    oneflow.Tensor.softplus,
    """
    See :func:`oneflow.softplus`
    """,
)

add_docstr(
    oneflow.Tensor.softsign,
    """
    See :func:`oneflow.softsign`
    """,
)

add_docstr(
    oneflow.Tensor.tan,
    """
    See :func:`oneflow.tan`
    """,
)

add_docstr(
    oneflow.Tensor.tanh,
    """
    See :func:`oneflow.tanh`
    """,
)

add_docstr(
    oneflow.Tensor.tril,
    """
    See :func:`oneflow.tril`
    """,
)

add_docstr(
    oneflow.Tensor.triu,
    """
    See :func:`oneflow.triu`
    """,
)

add_docstr(
    oneflow.Tensor.uniform_,
    """
    Tensor.uniform_(from=0, to=1) → Tensor

    Fills self tensor with numbers sampled from the continuous uniform distribution:

    .. math::
        P(x)=1/(to-from)

    """,
)

add_docstr(
    oneflow.Tensor.copy_,
    """
    The interface is consistent with PyTorch.

    Tensor.copy_(src, non_blocking=False) → Tensor

    Copies the elements from src into self tensor and returns self.

    The src tensor must be broadcastable with the self tensor. It may be of a different data type or reside on a different device.

    Args:

        src (Tensor): the source tensor to copy from

        non_blocking (bool): if True and this copy is between CPU and GPU, the copy may occur asynchronously with respect to the host. For other cases, this argument has no effect.
    """,
)

add_docstr(
    oneflow.Tensor.to,
    """Performs Tensor dtype and/or device conversion.
        A flow.dtype and flow.device are inferred from the arguments of `input.to(*args, **kwargs)`.

    .. note::
        If the ``input`` Tensor already
        has the correct :class:`flow.dtype` and :class:`flow.device`, then ``input`` is returned.
        Otherwise, the returned tensor is a copy of ``input`` with the desired.

    Args:
        input (oneflow.Tensor): An input tensor.
        *args (oneflow.Tensor or oneflow.device or oneflow.dtype): Positional arguments
        **kwargs (oneflow.device or oneflow.dtype) : Key-value arguments

    Returns:
        oneflow.Tensor: A Tensor.

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow

        >>> arr = np.random.randint(1, 9, size=(1, 2, 3, 4))
        >>> input = flow.Tensor(arr)
        >>> output = input.to(dtype=flow.float32)
        >>> np.array_equal(arr.astype(np.float32), output.numpy())
        True

    """,
)

add_docstr(
    oneflow.Tensor.gather,
    """
    oneflow.Tensor.gather(dim, index) -> Tensor

    See :func:`oneflow.gather`

    """,
)

add_docstr(
    oneflow.Tensor.clamp,
    """
    See :func:`oneflow.clamp`.
    """,
)

add_docstr(
    oneflow.Tensor.clamp_,
    """
    Inplace version of :func:`oneflow.Tensor.clamp`.
    """,
)

add_docstr(
    oneflow.Tensor.clip,
    """
    Alias for :func:`oneflow.Tensor.clamp`.
    """,
)

add_docstr(
    oneflow.Tensor.clip_,
    """
    Alias for :func:`oneflow.Tensor.clamp_`.
    """,
)

add_docstr(
    oneflow.Tensor.cpu,
    r"""Returns a copy of this object in CPU memory.
    If this object is already in CPU memory and on the correct device, then no copy is performed and the original object is returned.

    For example:

    .. code-block:: python

        >>> import oneflow as flow

        >>> input = flow.tensor([1, 2, 3, 4, 5], device=flow.device("cuda"))
        >>> output = input.cpu()
        >>> output.device
        device(type='cpu', index=0)
    """,
)

add_docstr(
    oneflow.Tensor.cuda,
    r"""Returns a copy of this object in CUDA memory.
    If this object is already in CUDA memory and on the correct device, then no copy is performed and the original object is returned.

    Args:
        device  (flow.device): The destination GPU device. Defaults to the current CUDA device.

    For example:

    .. code-block:: python

        >>> import oneflow as flow

        >>> input = flow.Tensor([1, 2, 3, 4, 5])
        >>> output = input.cuda()
        >>> output.device
        device(type='cuda', index=0)
    """,
)


add_docstr(
    oneflow.Tensor.repeat,
    """
    Tensor.repeat(*size) -> Tensor

    See :func:`oneflow.repeat`
    """,
)

add_docstr(
    oneflow.Tensor.t,
    """
    Tensor.t() → Tensor

    See :func:`oneflow.t`
    """,
)

add_docstr(
    oneflow.Tensor.tile,
    """
    Tensor.tile(*dims) -> Tensor

    See :func:`oneflow.tile`
    """,
)

add_docstr(
    oneflow.Tensor.T,
    """
    Is this Tensor with its dimensions reversed.

    If `n` is the number of dimensions in `x`, `x.T` is equivalent to `x.permute(n-1, n-2, ..., 0)`.
    """,
)

add_docstr(
    oneflow.Tensor.fmod,
    """
    Tensor.fmod(other) -> Tensor

    See :func:`oneflow.fmod`

    """,
)

add_docstr(
    oneflow.Tensor.logical_and,
    """
    logical_and() -> Tensor

    See :func:`oneflow.logical_and`

    """,
)

add_docstr(
    oneflow.Tensor.logical_or,
    """

    logical_or() -> Tensor

    See :func:`oneflow.logical_or`

    """,
)

add_docstr(
    oneflow.Tensor.logical_xor,
    """
    logical_xor() -> Tensor

    See :func:`oneflow.logical_xor`

    """,
)

add_docstr(
    oneflow.Tensor.masked_fill,
    """
    See :func:`oneflow.masked_fill`
    """,
)

add_docstr(
    oneflow.Tensor.masked_select,
    """
    See :func:`oneflow.masked_select`
    """,
)

add_docstr(
    oneflow.Tensor.sub,
    """
    See :func:`oneflow.sub`
    """,
)

add_docstr(
    oneflow.Tensor.div,
    """
    See :func:`oneflow.div`

    """,
)

add_docstr(
    oneflow.Tensor.ceil,
    """
    See :func:`oneflow.ceil`
    """,
)

add_docstr(
    oneflow.Tensor.expm1,
    """
    See :func:`oneflow.expm1`
    """,
)

add_docstr(
    oneflow.Tensor.topk,
    """
    See :func:`oneflow.topk`
    """,
)

add_docstr(
    oneflow.Tensor.nms,
    """
    See :func:`oneflow.nms`
    """,
)

add_docstr(
    oneflow.Tensor.nonzero,
    """
    nonzero(input, as_tuple=False) -> Tensor

    See :func:`oneflow.nonzero`
    """,
)

add_docstr(
    oneflow.Tensor.max,
    """
    input.max(dim, index) -> Tensor

    See :func:`oneflow.max`
    """,
)

add_docstr(
    oneflow.Tensor.min,
    """
    input.min(dim, index) -> Tensor

    See :func:`oneflow.min`
    """,
)

add_docstr(
    oneflow.Tensor.sum,
    """
    input.sum(dim, index) -> Tensor

    See :func:`oneflow.sum`
    """,
)

add_docstr(
    oneflow.Tensor.mean,
    """
    input.mean(dim, index) -> Tensor

    See :func:`oneflow.mean`
    """,
)

add_docstr(
    oneflow.Tensor.prod,
    """
    input.prod(dim, index) -> Tensor

    See :func:`oneflow.prod`
    """,
)

add_docstr(
    oneflow.Tensor.reshape,
    """
    See :func:`oneflow.reshape`
    """,
)

add_docstr(
    oneflow.Tensor.view,
    """
    The interface is consistent with PyTorch.
    The documentation is referenced from: https://pytorch.org/docs/stable/generated/torch.Tensor.view.html

    Returns a new tensor with the same data as the :attr:`self` tensor but of a
    different :attr:`shape`.

    The returned tensor shares the same data and must have the same number
    of elements, but may have a different size. For a tensor to be viewed, the new
    view size must be compatible with its original size and stride, i.e., each new
    view dimension must either be a subspace of an original dimension, or only span
    across original dimensions :math:`d, d+1, \\dots, d+k` that satisfy the following
    contiguity-like condition that :math:`\\forall i = d, \\dots, d+k-1`,

    .. math::

      \\text{stride}[i] = \\text{stride}[i+1] \\times \\text{size}[i+1]

    Otherwise, it will not be possible to view :attr:`self` tensor as :attr:`shape`
    without copying it (e.g., via :meth:`contiguous`). When it is unclear whether a
    :meth:`view` can be performed, it is advisable to use :meth:`reshape`, which
    returns a view if the shapes are compatible, and copies (equivalent to calling
    :meth:`contiguous`) otherwise.

    Args:
        input: A Tensor.
        *shape: flow.Size or int...
    Returns:
        A Tensor has the same type as `input`.

    For example:

    .. code-block:: python

        >>> import numpy as np
        >>> import oneflow as flow

        >>> x = np.array(
        ...    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        ... ).astype(np.float32)
        >>> input = flow.Tensor(x)

        >>> y = input.view(2, 2, 2, -1).numpy().shape
        >>> y
        (2, 2, 2, 2)
    """,
)

add_docstr(
    oneflow.Tensor.sort,
    """
    See :func:`oneflow.sort`
    """,
)

add_docstr(
    oneflow.Tensor.type_as,
    r"""Returns this tensor cast to the type of the given tensor.
        This is a no-op if the tensor is already of the correct type.

    Args:
        input  (Tensor): the input tensor.
        target (Tensor): the tensor which has the desired type.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np

        >>> input = flow.tensor(np.random.randn(1, 2, 3), dtype=flow.float32)
        >>> target = flow.tensor(np.random.randn(4, 5, 6), dtype = flow.int32)
        >>> input = input.type_as(target)
        >>> input.dtype
        oneflow.int32
    """,
)

add_docstr(
    oneflow.Tensor.int,
    r"""`Tensor.int()` is equivalent to `Tensor.to(flow.int32)`. See to().

    Args:
        input  (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np

        >>> input = flow.tensor(np.random.randn(1, 2, 3), dtype=flow.float32)
        >>> input = input.int()
        >>> input.dtype
        oneflow.int32
    """,
)

add_docstr(
    oneflow.Tensor.long,
    r"""`Tensor.long()` is equivalent to `Tensor.to(flow.int64)`. See to().

    Args:
        input  (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np

        >>> input = flow.tensor(np.random.randn(1, 2, 3), dtype=flow.float32)
        >>> input = input.long()
        >>> input.dtype
        oneflow.int64
    """,
)

add_docstr(
    oneflow.Tensor.float,
    r"""`Tensor.float()` is equivalent to `Tensor.to(flow.float32)`. See to().

    Args:
        input  (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np

        >>> input = flow.tensor(np.random.randn(1, 2, 3), dtype=flow.int)
        >>> input = input.float()
        >>> input.dtype
        oneflow.float32
    """,
)

add_docstr(
    oneflow.Tensor.double,
    r"""`Tensor.double()` is equivalent to `Tensor.to(flow.float64)`. See to().

    Args:
        input  (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> import numpy as np

        >>> input = flow.tensor(np.random.randn(1, 2, 3), dtype=flow.int)
        >>> input = input.double()
        >>> input.dtype
        oneflow.float64
    """,
)

add_docstr(
    oneflow.Tensor.is_floating_point,
    """
    See :func:`oneflow.is_floating_point`
    """,
)

add_docstr(
    oneflow.Tensor.item,
    r"""Returns the value of this tensor as a standard Python number. This only works for tensors with one element.
    For other cases, see tolist().

    This operation is not differentiable.

    Args:
        input  (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> x = flow.tensor([1.0])
        >>> x.item()
        1.0
    """,
)

add_docstr(
    oneflow.Tensor.tolist,
    r"""Returns the tensor as a (nested) list. For scalars, a standard Python number is returned,
    just like with `item()`. Tensors are automatically moved to the CPU first if necessary.

    This operation is not differentiable.

    Args:
        input  (Tensor): the input tensor.

    For example:

    .. code-block:: python

        >>> import oneflow as flow
        >>> input = flow.tensor([[1,2,3], [4,5,6]])
        >>> input.tolist()
        [[1, 2, 3], [4, 5, 6]]
    """,
)

add_docstr(
    oneflow.Tensor.where,
    """
    See :func:`oneflow.where`
    """,
)

add_docstr(
    oneflow.Tensor.storage_offset,
    """
    storage_offset() -> int

    Returns self tensor’s offset in the underlying storage in terms of number of storage elements (not bytes).

    For example:

    .. code-block:: python

        >>> import oneflow as flow

        >>> x = flow.tensor([1, 2, 3, 4, 5])
        >>> x.storage_offset()
        0
    """,
)
