import yaml
import typing
import asyncio
from pathlib import Path
from typing import Literal
from divr_diagnosis import DiagnosisMap

from .audio_loader import AudioLoader
from .task import Task
from ..logger import Logger
from ..download import Download
from ..task_generator import generator_map

VERSIONS = Literal["v1"]
versions = typing.get_args(VERSIONS)
task_generator_maps = {"v1": generator_map["v1"]}


class Benchmark:
    def __init__(
        self,
        storage_path: str | Path,
        version: VERSIONS,
        quiet: bool = False,
        sample_rate: int = 16000,
    ) -> None:
        self.__quiet = quiet
        if not Path(storage_path).is_dir():
            raise ValueError(
                f"storage_path: ({storage_path}) is not a valid directory."
            )
        if version not in versions:
            raise ValueError(
                f"invalid version ({version}) selected. Choose from: {versions}"
            )
        module_path = Path(__file__).parent.parent.resolve()
        self.__logger = Logger(log_path=f"{storage_path}/logs", key=f"{version}")
        self.__data_path = Path(f"{storage_path}/data")
        self.__audio_loader = AudioLoader(version, self.__data_path, sample_rate)
        self.__downloader = Download(
            database_path=self.__data_path, logger=self.__logger
        )
        self.__tasks_path = f"{module_path}/tasks/{version}"
        self.__task_generator = task_generator_maps[version]
        self.__ensure_datasets(tasks_path=self.__tasks_path)

    async def generate_task(
        self,
        filter_func,
        task_path: Path,
        diagnosis_map: DiagnosisMap,
        allow_incomplete_classification: bool,
    ) -> None:
        await self.__task_generator.generate_task(
            source_path=self.__data_path,
            filter_func=filter_func,
            task_path=task_path,
            diagnosis_map=diagnosis_map,
            allow_incomplete_classification=allow_incomplete_classification,
        )

    def load_task(
        self,
        task_path: Path,
        diag_level: int | None,
        diagnosis_map: DiagnosisMap,
        load_audios: bool = True,
    ) -> Task:
        if not task_path.is_dir():
            raise ValueError("Invalid task selected")
        return Task(
            diagnosis_map=diagnosis_map,
            audio_loader=self.__audio_loader,
            train=Path(f"{task_path}/train.yml"),
            val=Path(f"{task_path}/val.yml"),
            test=Path(f"{task_path}/test.yml"),
            quiet=self.__quiet,
            diag_level=diag_level,
            load_audios=load_audios,
        )

    def __ensure_datasets(self, tasks_path: str) -> None:
        datasets_file = f"{tasks_path}/datasets.yml"
        with open(datasets_file, "r") as df:
            datasets = yaml.load(df, Loader=yaml.FullLoader)

        to_download = []
        for dataset in datasets:
            dataset_path = Path(f"{self.__data_path}/{dataset}")
            if dataset_path.is_dir():
                self.__logger.info(f"{dataset} already exists at {dataset_path}")
            else:
                self.__logger.info(
                    f"{dataset} does not exist. Will create at {dataset_path}"
                )
                to_download.append(dataset)
        coro = self.__downloader.selected(datasets=to_download)
        try:
            loop = asyncio.get_running_loop()
            asyncio.run_coroutine_threadsafe(coro=coro, loop=loop)
        except RuntimeError:
            asyncio.run(coro)
