# src/atc2txt/lib/download_model.py

import os
import subprocess
import sys


def download_model(model_url: str) -> None:
    models_dir = "models"
    repo_name = model_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(models_dir, repo_name)

    if os.path.exists(repo_path):
        print(
            f"Error: The repository '{repo_name}' already exists in '{models_dir}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    os.makedirs(models_dir, exist_ok=True)
    print("Download model:", model_url)
    subprocess.run(
        ["git", "clone", "--depth", "1", model_url], cwd=models_dir, check=True
    )
