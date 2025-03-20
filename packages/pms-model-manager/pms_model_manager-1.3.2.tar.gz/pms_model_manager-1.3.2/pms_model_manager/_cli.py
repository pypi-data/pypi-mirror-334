import os
import pathlib
from typing import Annotated, List, Literal
import typer
import sys
from enum import Enum

MODEL_NAME = "model"
NONE_ALIASES = ["unknown-latest"]
ONNX_ALIASES = ["onnx-latest"]
PLAN_ALIASES = ["plan-latest"]
PACKAGE_DIR = os.path.dirname(os.path.dirname(__file__))
if PACKAGE_DIR not in os.environ["PATH"].split(":"):
    sys.path.append(PACKAGE_DIR)
import pms_model_manager as pmm


class ExtensionType(str, Enum):
    none = "none"
    onnx = "onnx"
    plan = "plan"


app = typer.Typer()


def get_file_in_dir(target_dir: pathlib.Path) -> List[pathlib.Path]:
    assert target_dir.is_dir(), f"ERROR, target_dir is not directory."
    p = pathlib.Path(target_dir).glob("**/*")
    files = [x.absolute() for x in p if x.is_file()]
    return files


def split_and_update_tags(tags: dict, _tags_str: str):
    if len(_tags_str) == 0:
        return
    _tag_pairs = _tags_str.split(",")
    print(_tag_pairs)
    assert len(_tag_pairs) > 0, f"ERROR, Theare are not tag pairs. {_tag_pairs}"
    new_tags = {}
    for pair in _tag_pairs:
        key, value = pair.split(":")
        new_tags[key] = value
    tags.update(new_tags)


def split_and_update_aliase(aliase: list, _aliase_str: str):
    if len(_aliase_str) == 0:
        return
    _aliase = _aliase_str.split(",")
    assert len(_aliase) > 0, f"ERROR, Theare are not aliase. {_aliase}"
    for a in _aliase:
        aliase.append(a)


@app.command()
def remote_ls() -> None:
    manager = pmm.ModelManager(os.path.dirname(__file__))
    typer.echo("Remote model list")
    for m in manager.remote_models:
        typer.echo(f"- {m}")


@app.command()
def local_ls(directory: str):
    manager = pmm.ModelManager(directory)
    typer.echo("Local model list")
    for meta in manager.local_metadatas:
        typer.echo(meta)


@app.command()
def remote_cat(model_name: str):
    manager = pmm.ModelManager(os.path.dirname(__file__))
    mi = manager.remote_models[model_name]
    typer.echo(f" * {model_name} Info * ")
    for m in mi:
        typer.echo(m)


@app.command()
def up(
    model_name: str,
    model_directory: str,
    ext: ExtensionType = ExtensionType.none,
    _tags: Annotated[str, typer.Option("--tag")] = "",
    _aliase: Annotated[str, typer.Option("--alias")] = "",
    force_yes: Annotated[bool, typer.Option("--force")] = False,
):
    tags = {}
    aliase: List[str] = []
    model_path = os.path.join(model_directory, f"{MODEL_NAME}.{ext.name}")
    assert os.path.exists(model_path), f"ERROR, model file is not exist({model_path})"

    # apply tag, aliase from args
    split_and_update_aliase(aliase, _aliase)
    split_and_update_tags(tags, _tags)

    # check model path is valid.
    model_dir = pathlib.Path(model_directory)
    assert model_dir.exists(), f"ERROR, the file is not exist."
    assert model_dir.is_dir(), f"ERROR, the path({model_dir}) is NOT directory."

    # confirm upload
    typer.echo(f"Model[{model_name}] files")
    files = get_file_in_dir(model_dir)
    max_file_name_length = max([len(f.name) for f in files])
    for path in files:
        typer.echo(
            f" - name: {path.name:{max_file_name_length}} | local[{path}] --> remote[models://{model_name}/{path.name}]"
        )

    # extract tags and set aliase
    if ext == ExtensionType.onnx:
        tags.update(pmm.extract_onnx_tag(model_path))
        aliase += ONNX_ALIASES
    else:
        typer.echo("The extension is not provided. skip extracting tags from the file.")
        aliase += NONE_ALIASES

    # echo tags
    typer.echo(f"Model[{model_name}] tags")
    for tag in tags.items():
        typer.echo(f" - tag[{tag[0]}]: {tag[1]}")

    # check force_yes
    if force_yes is True:
        typer.echo("Skip confirm.")
    else:
        is_upload = typer.confirm("Are you sure you want to upload it?")
        if is_upload is not True:
            typer.echo("Upload canceled.")
            return

    # upload onnx
    typer.echo("Upload start")
    manager = pmm.ModelManager(model_directory)
    res = manager.upload(
        model_name=model_name,
        model_dir=model_directory,
        aliases=aliase,
        tag=tags,
    )
    assert res, f"ERROR, Fail to upload the model files."
    typer.echo("Upload end")


@app.command()
def down(model_name: str, model_directory: str, alias: str):
    model_manager = pmm.ModelManager(directory=model_directory)
    model_manager.download(model_name=model_name, alias=alias)


def main():
    app()


if __name__ == "__main__":
    main()
