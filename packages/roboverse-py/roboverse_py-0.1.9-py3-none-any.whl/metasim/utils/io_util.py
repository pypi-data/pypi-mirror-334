import os

from huggingface_hub import HfApi, HfFileSystem, hf_hub_download
from loguru import logger as log

REPO_ID = "RoboVerseOrg/roboverse_data"
LOCAL_DIR = "roboverse_data"

hf_api = HfApi()
hf_fs = HfFileSystem()


def _check_repo_access():
    if not hf_api.repo_exists(REPO_ID, repo_type="dataset", token=True):
        raise Exception(
            "Cannot access the huggingface repository. Please check your token is correctly set and try again."
            "\nTo generate a token, go to https://huggingface.co/settings/tokens. A token with read access is"
            " enough."
            "\nTo set your token, run `huggingface-cli login` or `export HF_TOKEN=<your_token>`."
            "\nIf one way doesn't work, please try the other way. It is very likely a huggingface bug."
        )


def check_and_download(filepath: str):
    """
    Args:
        filepath: the filepath to check and download. It should a existing file in the local directory. It should start with `LOCAL_DIR`.
    """
    local_exists = os.path.exists(filepath)
    hf_exists = hf_fs.exists(os.path.join("datasets", REPO_ID, os.path.relpath(filepath, LOCAL_DIR)))

    if local_exists:
        ## In this case, the runner is a developer who has the file in their local machine.
        if hf_exists:
            return
        else:
            _check_repo_access()
            log.warning(f"Please upload the file {filepath} to the huggingface dataset!")
            return
    else:
        ## In this case, we didn't find the file in the local directory, the circumstance is complicated.

        ## First, make sure we have the access to the repo
        _check_repo_access()

        ## Then, make sure the file exists in the huggingface dataset.
        if not hf_exists:
            raise Exception(
                f"File {filepath} neither exists in the local directory nor exists in the huggingface dataset. Please"
                " report this issue to the developers."
            )

        ## Also, we need to exclude a circumstance that a developer forgot to update the submodule.
        using_hf_git = os.path.exists(os.path.join(LOCAL_DIR, ".git"))
        if using_hf_git:
            raise Exception(
                "Please update the roboverse_data to the latest version, by running `cd roboverse_data && git pull`."
            )

        ## Finally, download the file from the huggingface dataset.
        try:
            hf_hub_download(
                repo_id=REPO_ID,
                filename=os.path.relpath(filepath, LOCAL_DIR),
                repo_type="dataset",
                token=True,
                local_dir=LOCAL_DIR,
            )
        except Exception as e:
            raise e
