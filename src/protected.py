import json
import os
from typing import Optional, Union

from fastapi import APIRouter, Request, HTTPException

from src.commons import settings, data

router = APIRouter()


@router.post('/upload-repo', status_code=201)
async def upload_repository(submitted_repo_conf: Request, overwrite: Union[bool, None] = False):
    content_type = submitted_repo_conf.headers['Content-Type']
    if content_type != 'application/json':
        raise HTTPException(status_code=400, detail=f'Content type {content_type} not supported')

    repo_conf_json = await submitted_repo_conf.json()
    repo_name = repo_conf_json['name']
    if repo_name is None:
        raise HTTPException(status_code=500, detail=f'Invalid repository configuration. No "name" found')


    if not overwrite and repo_name in data:
        raise HTTPException(status_code=400, detail=f'Repository Configuration "{repo_name}" exist. '
                                                    f'You can use "/upload-repo?overwrite=true"')
    with open(os.path.join(settings.repositories_conf_dir, f'{repo_name}.json'), mode="w") as file:
            file.write(json.dumps(repo_conf_json))
    data.update({repo_name: repo_conf_json})

    return {"saved-conf": repo_name}


@router.delete("/delete-repo/{name}")
def delete_repository(name: str):
    if name not in data:
        raise HTTPException(status_code=404, detail=f"'{name}' not found.")

    for repo_conf_filename in os.listdir(settings.repositories_conf_dir):
        repo_conf_file = os.path.join(settings.repositories_conf_dir, repo_conf_filename)
        with open(repo_conf_file, "r") as f:
            repo_conf_json = json.loads(f.read())
            if repo_conf_json['name'] == name:
                os.remove(repo_conf_json)
                data.pop(name)
                return {"deleted":name}