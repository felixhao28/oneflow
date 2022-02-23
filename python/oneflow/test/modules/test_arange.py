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

import unittest
from collections import OrderedDict

import numpy as np
from test_util import GenArgList

import oneflow as flow
import oneflow.unittest

from oneflow.test_utils.automated_test_util import *


def _test_arange(test_case, device):
    np_out = np.arange(13, dtype=np.float32)
    of_out = flow.arange(13, device=device, dtype=flow.float32)
    test_case.assertTrue(np.allclose(of_out.numpy(), np_out, 1e-05, 1e-05))


def _test_arange_step_prarm(test_case, device):
    np_out = np.arange(0, 20, 2)
    of_out = flow.arange(0, 20, step=2, device=device)
    test_case.assertTrue(np.allclose(of_out.numpy(), np_out, 1e-05, 1e-05))


def _test_arange_more_params(test_case, device):
    np_out = np.arange(0, 100, 3)
    of_out = flow.arange(start=0, end=100, step=3, device=device)
    test_case.assertTrue(np.allclose(of_out.numpy(), np_out, 1e-05, 1e-05))


def _test_arange_backward(test_case, device):
    np_out = np.arange(13)
    x = flow.arange(13, dtype=flow.float32, device=device)
    x.requires_grad = True
    y = x.sum()
    y.backward()
    test_case.assertTrue(np.allclose(x.grad.numpy(), np.ones(13), 1e-05, 1e-05))


@flow.unittest.skip_unless_1n1d()
class TestArange(flow.unittest.TestCase):
    def test_arange(test_case):
        arg_dict = OrderedDict()
        arg_dict["function_test"] = [
            _test_arange,
            _test_arange_step_prarm,
            _test_arange_more_params,
            _test_arange_backward,
        ]
        arg_dict["device"] = ["cpu", "cuda"]
        for arg in GenArgList(arg_dict):
            arg[0](test_case, *arg[1:])

    @autotest(n=30, auto_backward=False, rtol=1e-5, atol=1e-5, check_graph=True)
    def test_arange_with_random_data(test_case):
        start = random().to(int)
        end = start + random().to(int)
        step = random(0, end - start).to(int)
        x = torch.arange(start=start, end=end, step=step)
        device = random_device()
        x.to(device)
        return x

    @autotest(n=5, auto_backward=False, rtol=1e-5, atol=1e-5, check_graph=True)
    def test_arange_with_float_delta(test_case):
        start = random().to(int)
        end = start + random().to(int)
        step = random(0, end - start).to(float)
        x = torch.arange(start=start, end=end, step=step)
        device = random_device()
        x.to(device)
        return x

    def test_global_naive(test_case):
        placement = flow.placement("cpu", ranks=[0])
        sbp = (flow.sbp.broadcast,)
        x = flow.arange(start=0, end=10, step=1, placement=placement, sbp=sbp)
        test_case.assertEqual(x.sbp, sbp)
        test_case.assertEqual(x.placement, placement)


def _test_consistent_arange(test_case, start, end, step, placement, sbp):
    x = flow.arange(start, end, step, placement=placement, sbp=sbp)
    test_case.assertEqual(x.sbp, sbp)
    test_case.assertEqual(x.placement, placement)


def _test_consistent_arange_graph(test_case, start, end, step, placement, sbp):
    class ConsistentArangeGraph(flow.nn.Graph):
        def __init__(self,):
            super().__init__()

        def build(self):
            x = flow.arange(start, end, step, placement=placement, sbp=sbp)
            return x

    c_arange_g = ConsistentArangeGraph()
    x = c_arange_g()
    test_case.assertEqual(x.sbp, sbp)
    test_case.assertEqual(x.placement, placement)


@unittest.skipIf(os.getenv("ONEFLOW_TEST_CPU_ONLY"), "only test cpu cases")
@flow.unittest.skip_unless_1n2d()
class TestArangeConsistent(flow.unittest.TestCase):
    def test_arange_consistent(test_case):
        arg_dict = OrderedDict()
        arg_dict["test_fun"] = [_test_consistent_arange, _test_consistent_arange_graph]
        arg_dict["start"] = [i for i in range(1, 5, 1)]
        arg_dict["end"] = [i for i in range(10, 50, 10)]
        arg_dict["step"] = [i for i in range(1, 5, 1)]
        arg_dict["placement"] = [
            # 1d
            flow.placement("cpu", ranks=[0, 1]),
            flow.placement("cuda", ranks=[0, 1]),
            # 2d
            flow.placement("cpu", ranks=[[0, 1],]),
            flow.placement("cuda", ranks=[[0, 1],]),
        ]
        arg_dict["sbp"] = [(flow.sbp.broadcast,), (flow.sbp.split(0),)]
        for arg in GenArgList(arg_dict):
            arg[0](test_case, *arg[1:])


if __name__ == "__main__":
    unittest.main()
