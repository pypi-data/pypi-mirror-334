#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/14
# @Author  : yanxiaodong
# @File    : training_api_job.py
"""
import re

from typing import Optional
from pydantic import BaseModel

job_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/projects/(?P<project_name>.+?)/jobs/(?P<local_name>.+?)$"
)


class JobName(BaseModel):
    """
    The name of job.
    """

    workspace_id: str
    project_name: str
    local_name: str

    def get_name(self):
        """
        get name
        :return:
        """
        return f"workspaces/{self.workspace_id}/projects/{self.project_name}/jobs/{self.local_name}"


def parse_job_name(name: str) -> Optional[JobName]:
    """
    Get workspace id, project name and job local name from job name.
    """
    m = job_name_regex.match(name)
    if m is None:
        return None
    return JobName(
        workspace_id=m.group("workspace_id"),
        project_name=m.group("project_name"),
        local_name=m.group("local_name"),
    )
