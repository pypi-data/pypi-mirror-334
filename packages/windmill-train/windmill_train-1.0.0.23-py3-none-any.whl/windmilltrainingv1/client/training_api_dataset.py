#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/6
# @Author  : yanxiaodong
# @File    : training_api_dataset.py.py
"""
import re
from typing import Optional
from pydantic import BaseModel

dataset_name_regex = re.compile(
    "^workspaces/(?P<workspace_id>.+?)/projects/(?P<project_name>.+?)/datasets/(?P<local_name>.+?)$"
)

ANNOTATION_FORMAT_COCO = "COCO"
ANNOTATION_FORMAT_IMAGENET = "ImageNet"
ANNOTATION_FORMAT_CITYSCAPES = "Cityscapes"

ANNOTATION_FORMAT_PADDLEOCR = "PaddleOCR"
ANNOTATION_FORMAT_PADDLECLAS = "PaddleClas"
ANNOTATION_FORMAT_PADDLESEG = "PaddleSeg"

ANNOTATION_FORMAT_MULTI_ATTRIBUTE_DATASET = "MultiAttributeDataset"

ANNOTATION_FORMAT_MS_SWIFT = "ms-swift"


class DatasetName(BaseModel):
    """
    The name of dataset.
    """

    workspace_id: str
    project_name: str
    local_name: str

    def get_name(self):
        """
        get name
        :return:
        """
        return f"workspaces/{self.workspace_id}/projects/{self.project_name}/datasets/{self.local_name}"


def parse_dataset_name(name: str) -> Optional[DatasetName]:
    """
    Get workspace id, project name and dataset name from dataset name.
    """
    m = dataset_name_regex.match(name)
    if m is None:
        return None
    return DatasetName(
        workspace_id=m.group("workspace_id"),
        project_name=m.group("project_name"),
        local_name=m.group("local_name"),
    )
