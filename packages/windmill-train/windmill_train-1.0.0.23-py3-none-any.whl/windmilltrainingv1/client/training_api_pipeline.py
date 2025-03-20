#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/3/15 12:17
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : training_api_pipeline.py
# @Software: PyCharm
"""
import re
from typing import Optional
from pydantic import BaseModel

pipeline_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/projects/(?P<project_name>.+?)/pipelines/(?P<local_name>.+?)$"
)


class PipelineName(BaseModel):
    """
    The name of pipeline.
    """

    workspace_id: str
    project_name: str
    local_name: str

    def get_name(self):
        """
        get name
        :return:
        """
        return f"workspaces/{self.workspace_id}/projects/{self.project_name}/pipelines/{self.local_name}"


def parse_pipeline_name(name: str) -> Optional[PipelineName]:
    """
    Get workspace id, project name and dataset pipeline from pipeline name.
    """
    m = pipeline_name_regex.match(name)
    if m is None:
        return None
    return PipelineName(
        workspace_id=m.group("workspace_id"),
        project_name=m.group("project_name"),
        local_name=m.group("local_name"),
    )
