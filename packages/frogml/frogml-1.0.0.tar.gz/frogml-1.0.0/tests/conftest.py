import os
from pathlib import Path
from platform import python_version

import pytest
from _pytest.fixtures import fixture
from transformers import DistilBertModel, DistilBertTokenizer

from tests.frogml.utils.test_files_tools import given_full_path_to_file


@pytest.fixture
def resource_folder() -> str:
    resource_path: str = "../../../tests/resources"

    return os.path.abspath(resource_path)


@pytest.fixture(scope="session")
def jf_project() -> str:
    return "tests-project"


@fixture(scope="session")
def repository_in_project(jf_project: str) -> str:
    return f"{jf_project}-test-ml-repo2"


@fixture(scope="session")
def repository_not_in_project() -> str:
    return "test-ml-repo3"


@pytest.fixture
def given_resource_path() -> str:
    return given_full_path_to_file("../../../tests/resources/models")


@pytest.fixture
def given_runtime_version() -> str:
    return python_version()


@pytest.fixture
def given_huggingface_model_path(tmp_path: Path) -> Path:
    """
    Fixture to create a Hugging Face model, save it to a temporary directory,
    return the path to the directory.
    """
    model = DistilBertModel.from_pretrained("distilbert-base-uncased")
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    model_path = os.path.join(tmp_path, "distilbert_model")

    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)

    return tmp_path


@pytest.fixture(scope="session")
def resource_dir_path() -> str:
    return os.path.abspath(Path(__file__).resolve().parent / "resources")


@pytest.fixture(scope="session")
def models_resources_dir_path(resource_dir_path: str) -> str:
    return os.path.join(resource_dir_path, "models")
