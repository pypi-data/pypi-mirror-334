#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
export_model.py
Authors: zhoubohan(zhoubohan@baidu.com)
Date:    2025/03/10
"""
import os
import shutil
import traceback
from argparse import ArgumentParser
from typing import Dict, Any, List

import bcelogger as logger
from jobv1.client.job_api_event import EventKind
from jobv1.client.job_api_job import (
    parse_job_name,
    UpdateJobRequest,
    GetJobRequest,
    JobName,
)
from jobv1.client.job_api_metric import (
    MetricLocalName,
    MetricKind,
    CounterKind,
    DataType,
)
from jobv1.client.job_api_task import UpdateTaskRequest
from jobv1.client.job_client import JobClient
from jobv1.tracker.tracker import Tracker
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import parse_model_name

EXPORT_MODEL_TASK_DISPLAY_NAME = "模型导出"
EXPORT_SKILL_JOB_KIND = "Export/Skill"


def parse_args() -> Any:
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--artifact_names", required=False, type=str, default=None)
    parser.add_argument("--dest_uri", required=False, type=str, default=None)
    parser.add_argument("--source_uri", required=False, type=str, default=".")

    args, _ = parser.parse_known_args()
    return args


def report_job_success(
    job_client: JobClient,
    job_name: JobName,
    dest_uri: str,
    tags: Dict[str, str],
) -> None:
    """
    repo job success things.
    """
    if not dest_uri:
        return

    file_name = os.path.basename(dest_uri)
    tags["outputFileName"] = file_name
    tags["outputFileFormat"] = (
        os.path.splitext(file_name)[1][1:] if "." in file_name else ""
    )
    tags["outputUri"] = dest_uri

    job_client.update_job(
        UpdateJobRequest(
            workspace_id=job_name.workspace_id,
            local_name=job_name.local_name,
            tags=tags,
        )
    )


def clean_resource(source_uri: str) -> None:
    """
    clean resource.
    """
    files_to_remove: List[str] = [
        os.path.join(source_uri, "artifact.txt"),
        os.path.join(source_uri, "log.lock"),
    ]

    for file_path in files_to_remove:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except (OSError, IOError) as e:
            logger.error(f"Delete file failed {file_path}: {e}")

    log_path: str = os.path.join(source_uri, "log")
    try:
        if os.path.isdir(log_path):
            shutil.rmtree(log_path)
    except (OSError, IOError) as e:
        logger.error(f"Delete log dir failed {log_path}: {e}")


def run() -> None:
    """
    export model.
    """
    org_id = os.getenv("ORG_ID")
    user_id = os.getenv("USER_ID")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT")
    job_name = os.getenv("JOB_NAME")
    task_name = os.getenv("PF_STEP_NAME")

    args = parse_args()

    job_success = True
    context = {"OrgID": org_id, "UserID": user_id}

    windmill_client = WindmillClient(endpoint=windmill_endpoint, context=context)
    job_client = JobClient(endpoint=windmill_endpoint, context=context)

    parsed_job_name = parse_job_name(job_name)
    workspace_id = parsed_job_name.workspace_id
    local_job_name = parsed_job_name.local_name

    tracker = Tracker(
        client=job_client,
        job_name=local_job_name,
        workspace_id=workspace_id,
        task_name=task_name,
    )

    job_client.update_task(
        UpdateTaskRequest(
            workspace_id=workspace_id,
            job_name=local_job_name,
            local_name=task_name,
            display_name=EXPORT_MODEL_TASK_DISPLAY_NAME,
        )
    )

    job_detail = job_client.get_job(
        GetJobRequest(
            workspace_id=workspace_id,
            local_name=local_job_name,
        )
    )

    job_kind = job_detail.kind
    job_tags = job_detail.tags or {}

    # 对于技能导出作业，尝试从文件读取工件名称
    if job_kind == EXPORT_SKILL_JOB_KIND:
        artifact_name_path = os.path.join(args.source_uri, "artifact.txt")
        if os.path.exists(artifact_name_path):
            with open(artifact_name_path, "r") as f:
                args.artifact_names = f.read()
        else:
            job_success = False

    if job_success:
        logger.info(f"{job_name} Exporting model args: {args}")

        # 处理技能无模型情况
        if args.artifact_names == "" and job_kind == EXPORT_SKILL_JOB_KIND:
            report_job_success(job_client, parsed_job_name, args.dest_uri, job_tags)
            return

        if not args.artifact_names:
            logger.error(f"{job_name} Artifact names empty: {args}")
            raise ValueError("artifact_names为空")

        artifact_names = args.artifact_names.split(",")
        # 记录模型任务总数
        tracker.log_metric(
            local_name=MetricLocalName.Total,
            kind=MetricKind.Counter,
            counter_kind=CounterKind.Cumulative,
            data_type=DataType.Int,
            value=[str(len(artifact_names))],
        )

        for a_name in artifact_names:
            try:
                if not a_name:
                    continue

                artifact_name = parse_artifact_name(a_name)
                model_name = parse_model_name(artifact_name.object_name)
                logger.info(f"{job_name} Exporting artifact name: {a_name}")
                windmill_client.dump_models(
                    artifact_name=a_name, output_uri=args.source_uri
                )

                if not os.path.exists(os.path.join(args.source_uri, "apply.yaml")):
                    logger.info(
                        f"{job_name} Export model {a_name} failed: apply.yaml file does not exist"
                    )
                    raise ValueError(f"模型导出失败({a_name})：apply.yaml未生成！")

                # 更新标签
                model_list = windmill_client.get_model_manifest(
                    model_name.workspace_id,
                    model_name.model_store_name,
                    model_name.local_name,
                    artifact_name.version,
                )

                for item in model_list.subModels:
                    key = f"{model_name.local_name}.{item['localName']}"
                    job_tags[key] = str(item["artifact"]["version"])

            except Exception as e:
                error_msg = str(e)
                logger.error(
                    f"Export model {job_name} failed: {traceback.format_exc()}"
                )

                tracker.log_metric(
                    local_name=MetricLocalName.Failed,
                    kind=MetricKind.Counter,
                    counter_kind=CounterKind.Monotonic,
                    data_type=DataType.Int,
                    value=[str(1)],
                )

                tracker.log_event(
                    kind=EventKind.Failed,
                    reason=f"系统错误:模型({model_name.local_name}_{artifact_name.version})导出失败",
                    message=error_msg[:500],
                )

                if job_kind == EXPORT_SKILL_JOB_KIND:
                    tracker.log_event(
                        kind=EventKind.Failed,
                        reason=f"系统错误:模型({model_name.local_name}_{artifact_name.version})导出失败",
                        message=error_msg[:500],
                        task_name="",
                    )
                    tracker.log_metric(
                        local_name=MetricLocalName.Failed,
                        kind=MetricKind.Counter,
                        counter_kind=CounterKind.Cumulative,
                        data_type=DataType.Int,
                        value=[str(1)],
                        task_name="",
                    )

                clean_resource(args.source_uri)
                raise ValueError(f"模型导出失败({a_name})：{error_msg[:500]}")

            # 记录模型任务成功
            tracker.log_metric(
                local_name=MetricLocalName.Success,
                kind=MetricKind.Counter,
                counter_kind=CounterKind.Monotonic,
                data_type=DataType.Int,
                value=[str(1)],
            )

        clean_resource(args.source_uri)
        if job_success:
            report_job_success(job_client, parsed_job_name, args.dest_uri, job_tags)


if __name__ == "__main__":
    run()
