#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/6
# @Author  : yanxiaodong
# @File    : training_api_project.py
"""
import re
from pydantic import BaseModel
from typing import Optional

project_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/projects/(?P<local_name>.+?)$"
)


class ProjectName(BaseModel):
    """
    The name of project.
    """

    workspace_id: str
    local_name: str

    def get_name(self):
        """
        get name
        :return:
        """
        return f"workspaces/{self.workspace_id}/projects/{self.local_name}"


def parse_project_name(name: str) -> Optional[ProjectName]:
    """
    Get workspace id, project local name from project name.
    """
    m = project_name_regex.match(name)
    if m is None:
        return None
    return ProjectName(
        workspace_id=m.group("workspace_id"), local_name=m.group("local_name")
    )
