from __future__ import absolute_import

import oneflow.core.job.job_pb2 as job_util

class FunctionAttribute(object):
  pass

class FunctionDesc(object):
    def __init__(self, job_func=None, job_config_proto=None, function_attribute=None):
        if job_config_proto is None: job_config_proto=job_util.JobConfigProto()
        if function_attribute is None: function_attribute=FunctionAttribute()
        self.job_func = job_func
        self.job_config_proto = job_config_proto
        self.function_attribute = function_attribute
