#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/10 19:21
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : training_client.py
# @Software: PyCharm
"""
import json
from typing import Optional
from multidict import MultiDict
from baidubce.http import http_methods
from baidubce.http import http_content_types
from baidubce.bce_client_configuration import BceClientConfiguration
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from bceinternalsdk.client.paging import PagingRequest
from windmillartifactv1.client.artifact_api_artifact import ArtifactContent


class TrainingClient(BceInternalClient):
    """
    A client class for interacting with the Training service. Initializes with default configuration.

    This client provides an interface to send requests to the BceService for training-related operations.
    """

    """
    job api
    """

    def create_job(
        self,
        workspace_id: str,
        project_name: str,
        local_name: str,
        display_name: Optional[str] = "",
        description: Optional[str] = "",
        kind: Optional[str] = "Train",
        spec_kind: Optional[str] = "PaddleFlow",
        spec_name: Optional[str] = "",
        experiment_name: Optional[str] = "",
        create_if_not_exist: Optional[bool] = False,
        compute_name: Optional[str] = "",
        filesystem_name: Optional[str] = "",
        resource_tips: Optional[dict] = None,
        spec_raw: Optional[str] = "",
        parameters: Optional[dict] = None,
        config: Optional[dict] = None,
        tags: Optional[dict] = None,
        datasets: Optional[list] = None,
    ):
        """
        Create a new training job.

        Args:
            workspace_id (str): 工作区id，example:"ws01"
            project_name (str): project localname. example:"project01"
            local_name (str): 作业名称 example:"job01"
            display_name (str): 作业中文名 example:"作业1"
            description (str): 作业描述 example:"job description"
            kind (str): 作业类型, default:"Train"
            spec_kind (str): spec 类型: Pod, PaddleFlow, Argo.
            spec_name (str): 部署作业的物料
            experiment_name (str): 实验名称
            create_if_not_exist (bool): 是否自动创建 experiment 实验
            compute_name (str):  计算资源名称
            filesystem_name (str): 文件系统资源名称
            resource_tips (list): 影响Suggest的过滤和排序的因素 比如 training
            spec_raw (bytes): spec 文件内容
            parameters (dict): spec 文件参数, 如 pipeline 模板文件参数, {"train.flavour": "flavourgpu1"}
            config (dict): 配置文件参数
            tags (dict): 标签
            datasets (list): 训练用的数据集

        Returns:
            dict: The response from the server.
        """
        body = {
            "workspaceID": workspace_id,
            "projectName": project_name,
            "localName": local_name,
            "displayName": display_name,
            "description": description,
            "kind": kind,
            "specKind": spec_kind,
            "specName": spec_name,
            "experimentName": experiment_name,
            "createIfNotExist": create_if_not_exist,
            "computeName": compute_name,
            "fileSystemName": filesystem_name,
            "tips": resource_tips,
            "specRaw": spec_raw,
            "parameters": parameters,
            "config": config,
            "tags": tags,
            "datasets": datasets,
        }

        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/jobs",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def list_job(
        self,
        workspace_id: str,
        project_name: str,
        experiment_name: Optional[str] = "",
        status: Optional[str] = "",
        filter_param: Optional[str] = "",
        tags: Optional[list] = None,
        page_request: Optional[PagingRequest] = PagingRequest(),
    ):
        """
        List jobs based on specified criteria.

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localName
            experiment_name (str): experiment localName
            status (str): job状态
            tags (list, optional): tags 过滤
            filter_param (str):the search keyword, search by localName, nameCN and description is supported.
            page_request (PagingRequest): Object containing paging request details.

        Returns:
            dict: The response from the server.
        """
        params = {
            "pageNo": str(page_request.get_page_no()),
            "pageSize": str(page_request.get_page_size()),
            "order": page_request.order,
            "orderBy": page_request.orderby,
            "filter": filter_param,
        }
        body = {}
        if tags:
            body["tags"] = tags

        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/jobs",
                encoding="utf-8",
            ),
            body=json.dumps(body),
            params=params,
        )

    def get_job(
        self,
        workspace_id: str,
        project_name: str,
        local_name: str,
        naming_kind: str = None,
    ):
        """
        Get details of a specific job.

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localname
            local_name (str): job名称
            naming_kind (str):

        Returns:
            dict: The response from the server.
        """
        params = MultiDict()
        params.add("namingKind", naming_kind)
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/jobs/"
                + local_name,
                encoding="utf-8",
            ),
            params=params,
        )

    def update_job(
        self,
        workspace_id: str,
        project_name: str,
        local_name: str,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[dict] = None,
        experiment_runs: Optional[dict] = None,
    ):
        """
        Update the details of a specific job.

        Args:
            workspace_id (str): ID of the workspace containing the job.
            project_name (str): Name of the project containing the job.
            local_name (str): Local name of the job.
            display_name(str): New display name for the job.
            description (str): New description for the job.
            tags (dict): New tags to associate with the job.
            experiment_runs (dict): New experiment name to associate with the job.

        Returns:
            dict: The response from the server.
        """
        body = {
            "workspaceID": workspace_id,
            "projectName": project_name,
            "localName": local_name,
            "displayName": display_name,
            "description": description,
            "tags": tags,
            "experimentRuns": experiment_runs,
        }
        return self._send_request(
            http_method=http_methods.PUT,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/jobs/"
                + local_name,
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def delete_job(self, workspace_id: str, project_name: str, local_name: str):
        """
        Delete a specific job.

        Args:
            workspace_id (str): 工作区id.
            project_name (str): project localname
            local_name (str): Local name of the job.

        Returns:
            dict: The response from the server.
        """
        return self._send_request(
            http_method=http_methods.DELETE,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/jobs/"
                + local_name,
                encoding="utf-8",
            ),
        )

    def stop_job(self, workspace_id: str, project_name: str, local_name: str):
        """
        Stop the execution of a specific job.

        Args:
            workspace_id (str): ID of the workspace containing the job.
            project_name (str): Name of the project containing the job.
            local_name (str): Local name of the job.

        Returns:
            dict: The response from the server.
        """
        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/jobs/"
                + local_name
                + "/stop",
                encoding="utf-8",
            ),
        )

    """
    dataset api
    """

    def create_dataset(
        self,
        workspace_id: str,
        project_name: str,
        category: str,
        local_name: str,
        artifact_uri: str,
        description: Optional[str] = "",
        display_name: Optional[str] = "",
        data_type: Optional[str] = "",
        annotation_type: Optional[str] = "",
        file_format: Optional[str] = "File",
        annotation_format: Optional[str] = "Coco",
        artifact_description: Optional[str] = "",
        artifact_alias: Optional[list] = None,
        artifact_tags: Optional[dict] = None,
        artifact_metadata: Optional[dict] = None,
    ):
        """
        Create a new dataset

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localname
            local_name (str): 数据集名称
            category (str): 数据集分类，用 "/" 表示级别
            description (str): 数据集描述
            display_name (str): 数据集中文名
            data_type (str): 数据集类型 image video
            annotation_type (str): Type of annotations.
            file_format (str): 数据集文件格式: Zip, File, Folder ...
            annotation_format (str): 数据集标注格式: Coco
            artifact_uri (str): 数据集版本文件路径. example:"s3://aiqa/store/workspaces/projects/default/datasets/default/versions/1"
            artifact_description (str): 数据集版本描述
            artifact_alias (list): 数据集版本别名，如default
            artifact_tags (dict): 数据集版本标签 [key:value]
            artifact_metadata (dict): 数据集版本基本信息

        Returns:
            dict: The response from the server.
        """
        artifact_content = {
            "uri": artifact_uri,
            "description": artifact_description,
            "alias": artifact_alias,
            "tags": artifact_tags,
            "metadata": artifact_metadata,
        }
        body = {
            "workspaceID": workspace_id,
            "projectName": project_name,
            "localName": local_name,
            "displayName": display_name,
            "description": description,
            "category": category,
            "fileFormat": file_format,
            "annotationFormat": annotation_format,
            "artifact": artifact_content,
        }

        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/datasets",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def list_dataset(
        self,
        workspace_id: str,
        project_name: str,
        categories: Optional[list] = None,
        tags: Optional[dict] = None,
        filter_param: Optional[str] = "",
        page_request: Optional[PagingRequest] = PagingRequest(),
    ):
        """
        List the datasets

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localname
            categories (list): 数据集分类，用 "/" 表示级别
            tags (dict): 数据集标签 [key:value]
            filter_param (str):the search keyword, search by localName, displayName and description is supported.
            page_request (PagingRequest): Parameters for the pagination request.
        Returns:
            dict: The response from the server.
        """

        params = MultiDict()
        params.add("pageNo", str(page_request.get_page_no()))
        params.add("pageSize", str(page_request.get_page_size()))
        params.add("order", page_request.order)
        params.add("orderBy", page_request.orderby)
        params.add("filter", filter_param)
        if categories:
            for i in categories:
                params.add("categories", i)
        if tags:
            for i in tags:
                params.add("tags", i)
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/datasets",
                encoding="utf-8",
            ),
            params=params,
        )

    def get_dataset(self, workspace_id: str, project_name: str, local_name: str):
        """
        get the specific dataset by local name

        Args:
            workspace_id (str): 工作区id
            project_name (str): project local name
            local_name (str): 数据集名称
        Returns:
            dict: The response from the server.
        """
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/datasets/"
                + local_name,
                encoding="utf-8",
            ),
        )

    def update_dataset(
        self,
        workspace_id: str,
        project_name: str,
        local_name: str,
        category: Optional[str],
        display_name: Optional[str] = "",
        description: Optional[str] = "",
        annotation_format: Optional[str] = "Coco",
    ):
        """
        update a dataset by localname

        Args:
            workspace_id (str): 工作区id
            project_name (str): project local name
            local_name (str): 数据集名称
            category (str): 数据集分类
            display_name (str): 数据集中文名
            description (str): 数据集描述
            annotation_format (str): 数据集标注格式: Coco...
        Returns:
            dict: The response from the server.
        """
        body = {
            "displayName": display_name,
            "description": description,
            "category": category,
            "annotationFormat": annotation_format,
        }
        return self._send_request(
            http_method=http_methods.PUT,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/datasets/"
                + local_name,
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def delete_dataset(self, workspace_id: str, project_name: str, local_name: str):
        """
        delete a dataset by local name

        Args:
            workspace_id(str): 工作区id
            project_name(str): project local name
            local_name(str): 数据集名称
        Returns:
            dict: The response from the server.
        """
        return self._send_request(
            http_method=http_methods.DELETE,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/datasets/"
                + local_name,
                encoding="utf-8",
            ),
        )

    """
    pipeline api
    """

    def create_pipeline(
        self,
        workspace_id: str,
        project_name: str,
        local_name: str,
        display_name: Optional[str] = "",
        description: Optional[str] = "",
        category: Optional[str] = "",
        kind: Optional[str] = "",
        artifact: Optional[ArtifactContent] = None,
    ):
        """
        create a pipeline by localname

        args：
            workspace_id (str): 工作区id
            project_name(str): project local name
            display_nam(str): pipeline 中文名
            local_name(str): pipeline名称
            description(str): pipeline描述
            category (str): pipeline分类
            kind(str): pipeline类型
            artifact(ArtifactContent): pipeline版本内容
        """
        body = {
            "workspaceID": workspace_id,
            "projectName": project_name,
            "localName": local_name,
            "displayName": display_name,
            "category": category,
            "description": description,
            "kind": kind,
            "artifact": {
                "uri": artifact.uri,
                "description": artifact.description,
                "alias": artifact.alias,
                "tags": artifact.tags,
                "metadata": artifact.metadata,
            },
        }

        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/pipelines",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def get_pipeline(self, workspace_id: str, project_name: str, local_name: str):
        """
        get the specific pipeline by local name

        Args:
            workspace_id(str): 工作区id
            project_name(str): project local name
            local_name(str): pipeline名称
        Returns:
            dict: The response from the server
        """
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/pipelines/"
                + local_name,
                encoding="utf-8",
            ),
        )

    def list_pipeline(
        self,
        workspace_id: str,
        project_name: str,
        categories: Optional[list] = None,
        tags: Optional[dict] = None,
        filter_param: Optional[str] = "",
        page_request: Optional[PagingRequest] = PagingRequest(),
    ):
        """
        List the pipeline

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localname
            categories (list): 产线分类，用 "/" 表示级别
            tags (dict):产线标签 [key:value]
            filter_param (str):the search keyword, search by localName, displayName and description is supported.
            page_request (PagingRequest): Parameters for the pagination request.
        Returns:
            dict: The response from the server.
        """
        params = MultiDict()
        params.add("pageNo", str(page_request.get_page_no()))
        params.add("pageSize", str(page_request.get_page_size()))
        params.add("order", page_request.order)
        params.add("orderBy", page_request.orderby)
        params.add("filter", filter_param)
        if categories:
            for i in categories:
                params.add("categories", i)
        if tags:
            for i in tags:
                params.add("tags", i)
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/pipelines",
                encoding="utf-8",
            ),
            params=params,
        )

    """
    project_api
    """

    def create_project(self,
                       workspace_id: str,
                       local_name: str,
                       display_name: Optional[str] = None,
                       description: Optional[str] = None,
                       compute_name: Optional[str] = None,
                       file_system_name: Optional[str] = None,
                       tags: Optional[dict] = None):
        """
        Create project
        """
        body = {
            "localName": local_name,
            "displayName": display_name,
            "description": description,
            "computeName": compute_name,
            "fileSystemName": file_system_name,
            "tags": tags,
        }
        return self._send_request(
            http_method=http_methods.POST,
            path=bytes("/v1/workspaces/" + workspace_id + "/projects", encoding="utf-8"),
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body))

    def list_project(
        self,
        workspace_id: str,
        f: Optional[str] = "",
        page_request: Optional[PagingRequest] = PagingRequest(),
    ):
        """
        List project by workspace_id

        args：
            workspace_id (str): 工作区id
            f:  filter
            page_request (PagingRequest): Parameters for the pagination request.
        """
        params = MultiDict()
        params.add("pageNo", str(page_request.get_page_no()))
        params.add("pageSize", str(page_request.get_page_size()))
        params.add("order", page_request.order)
        params.add("orderBy", page_request.orderby)
        params.add("filter", f)
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/" + workspace_id + "/projects", encoding="utf-8"
            ),
            params=params,
        )

    def get_project(self, workspace_id: str, project_name: str):
        """
        Get project by workspace_id and project_name
        Args:
            workspace_id (str): 工作区id
            project_name (str): project local name
        Returns:
            dict: The response from the server.
        """
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/" + workspace_id + "/projects/" + project_name,
                encoding="utf-8",
            ),
        )

    """
    experiment_api
    """

    def create_experiment(
        self,
        workspace_id: str,
        project_name: str,
        local_name: str,
        display_name: Optional[str] = "",
        description: Optional[str] = "",
        kind: Optional[str] = "Aim",
        tags: Optional[dict] = None,
        extra_data: Optional[dict] = None,
    ):
        """
        create experiment
        Args:
            workspace_id (str): 工作区id
            project_name (str): project local name
            local_name (str): experiment local name
            display_name (str): display name, example:"实验1"
            description (str): description
            kind (str): kind, oneof=MLFlow Aim default:"Aim" example:"MLFlow"
            tags (dict): tags, `json:"tags" binding:"tags" example:"k:v"`
            extra_data (dict): 依赖的外部系统的额外信息
        Returns:
            dict: The response from the server.
        """
        body = {
            "workspaceID": workspace_id,
            "projectName": project_name,
            "localName": local_name,
            "displayName": display_name,
            "description": description,
            "kind": kind,
            "tags": tags,
        }
        if extra_data:
            body.update({"extraData": extra_data})

        return self._send_request(
            http_method=http_methods.POST,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/experiments",
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def list_experiment(
        self,
        workspace_id: str,
        project_name: str,
        f: Optional[str] = "",
        page_request: Optional[PagingRequest] = PagingRequest(),
    ):
        """
        List experiment by workspace_id and project_name
        Args:
            workspace_id (str): 工作区id
            project_name (str): project local name
            f:  filter
            page_request (PagingRequest): Parameters for the pagination request.
        """
        params = MultiDict()
        params.add("pageNo", str(page_request.get_page_no()))
        params.add("pageSize", str(page_request.get_page_size()))
        params.add("order", page_request.order)
        params.add("orderBy", page_request.orderby)
        params.add("filter", f)
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/"
                + workspace_id
                + "/projects/"
                + project_name
                + "/experiments",
                encoding="utf-8",
            ),
            params=params,
        )
