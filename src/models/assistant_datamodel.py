from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class TransformedMetadata(BaseModel):
    """
    Represents metadata for a transformed resource.

    Attributes:
    - name (str): The name of the transformed resource.
    - transformer_url (Optional[str]): The URL of the transformer, if applicable.
    - target_dir (str): The target directory for the transformed resource.
    - restricted (Optional[bool]): Indicates if the resource is restricted.
    """
    name: str
    transformer_url: Optional[str] = Field(None, alias='transformer-url')
    target_dir: Optional[str] = Field(None, alias='target-dir')
    restricted: Optional[bool] = None


class Metadata(BaseModel):
    """
    Represents metadata for a repository.

    Attributes:
    - specification (List[str]): A list of specifications associated with the repository.
    - transformed_metadata (List[TransformedMetadata]): A list of transformed metadata instances.
    """
    specification: Optional[List[str]] = None
    transformed_metadata: List[TransformedMetadata] = Field(..., alias='transformed-metadata')


class Input(BaseModel):
    from_target_name: str = Field(default=None, alias='from-target-name')


class Target(BaseModel):
    """
    Represents a target in the repository assistant application.

    Attributes:
        repo_pid (str): A unique identifier for the repository. This field is required.
        repo_name (str): The name of the repository. This field is required.
        repo_display_name (str): The display name of the repository. This field is required.
        bridge_module_class (str): The class name of the bridge module. This field is required.
        base_url (str): The base URL of the repository. This field is required.
        target_url (str): The target URL of the repository. This field is required.
        username (str): The username for authentication. This field is required.
        password (str): The password for authentication. This field is required.
        metadata (Metadata): Metadata associated with the target repository. This field is required.
        initial_release_version (Optional[str]): The initial release version of the repository. This field is optional.
        input (Optional[Input]): Input data for the target. This field is optional.
    """
    repo_pid: str = Field(..., alias='repo-pid')
    repo_name: str = Field(..., alias='repo-name')
    repo_display_name: str = Field(..., alias='repo-display-name')
    bridge_module_class: str = Field(..., alias='bridge-module-class')
    base_url: Optional[str] = Field(default=None, alias='base-url')
    target_url: str = Field(..., alias='target-url')
    target_url_params: Optional[str] = Field(default=None, alias='target-url-params')
    username: Optional[str] = None
    password: Optional[str] = None
    metadata: Optional[Metadata] = None
    initial_release_version: Optional[str] = Field(default=None, alias='initial-release-version')
    input: Optional[Input] = None

class NotificationItem(BaseModel):
    """
    Represents a notification item.

    Attributes:
    - type (str): The type of notification.
    - conf (str): The configuration for the notification.
    """
    type: str
    conf: str


class FileConversion(BaseModel):
    """
    Represents a file conversion process.

    Attributes:
    - id (str): The unique identifier for the file conversion.
    - origin_type (str): The original file type. This field is aliased to 'origin-type'.
    - target_type (str): The target file type. This field is aliased to 'target-type'.
    - conversion_url (str): The URL for the conversion service. This field is aliased to 'conversion-url'.
    - notification (Optional[List[NotificationItem]]): A list of notification items associated with the conversion.
    """
    id: str
    origin_type: str = Field(..., alias='origin-type')
    target_type: str = Field(..., alias='target-type')
    conversion_url: str = Field(..., alias='conversion-url')
    notification: Optional[List[NotificationItem]] = None


class Enrichment(BaseModel):
    """
    Represents an enrichment process.

    Attributes:
    - id (str): The unique identifier for the enrichment.
    - name (str): The name of the enrichment.
    - service_url (str): The URL for the enrichment service. This field is aliased to 'service-url'.
    - result_url (str): The URL where the result of the enrichment can be found. This field is aliased to 'result-url'.
    - notification (Optional[List[NotificationItem]]): A list of notification items associated with the enrichment.
    - permission (Optional[str]): The permission level for the enrichment.
    """
    id: str
    name: str
    service_url: str = Field(..., alias='service-url')
    result_url: str = Field(..., alias='result-url')
    notification: Optional[List[NotificationItem]] = None
    permission: Optional[str] = None


class RepoAssistantDataModel(BaseModel):
    """
    Represents the data model for the repository assistant.

    Attributes:
    - assistant_config_name (str): The name of the assistant configuration. This field is aliased to 'assistant-config-name'.
    - description (str): A description of the repository assistant.
    - app_name (str): The name of the application. This field is aliased to 'app-name'.
    - app_config_url (str): The URL for the application configuration. This field is aliased to 'app-config-url'.
    - targets (List[Target]): A list of target repositories.
    - file_conversions (Optional[List[FileConversion]]): A list of file conversion processes. This field is aliased to 'file-conversions'.
    - enrichments (Optional[List[Enrichment]]): A list of enrichment processes.
    """
    assistant_config_name: str = Field(..., alias='assistant-config-name')
    description: Optional[str] = None
    app_name: str = Field(..., alias='app-name')
    app_config_url: Optional[str] = Field(None, alias='app-config-url')
    targets: List[Target]
    file_conversions: Optional[List[FileConversion]] = Field(None, alias='file-conversions')
    enrichments: Optional[List[Enrichment]] = None

json_rda = '''
{
    "assistant-config-name": "new-local.zenodo.org",
    "description": "",
    "app-name": "rda",
    "app-config-url": "https://",
    "targets": [
        {
            "repo-pid":"PLACE_HOLDER",
            "repo-name": "demo.zenodo.org",
            "repo-display-name": "Zenodo Dev Environment",
            "bridge-module-class": "ZenodoApiDepositor",
            "base-url": "https://zenodo.org",
            "target-url": "https://zenodo.org/api/deposit/depositions",
            "username": "PLACE_HOLDER",
            "password": "PLACE_HOLDER",
            "metadata": {
                "specification": [],
                "transformed-metadata": [
                    {
                        "name": "zenodo-dataset.json",
                        "transformer-url": "http://localhost:1745/transform/rda-form-metadata-to-zenodo-dataset-v1.xsl",
                        "target-dir": ""
                    },
                    {
                        "name": "zenodo-file.json",
                        "transformer-url": "http://localhost:1745/transform/form-metadata-to-dataverse-file-v1.xsl",
                        "target-dir": ""
                    }
                ]
            }
        }
    ],
    "file-conversions": [
        {
            "id": "1",
            "origin-type": "mov",
            "target-type": "mp4",
            "conversion-url": "https://",
            "notification": [
                {
                    "type": "mail",
                    "conf": "file:///path"
                }
            ]
        },
        {
            "id": "2",
            "origin-type": "mp4",
            "target-type": "mp3",
            "conversion-url": "https://"
        }
    ],
    "enrichments": [
        {
            "id": "1",
            "name": "CV",
            "service-url": "https://cv-service.labs.dansdemo.nl",
            "result-url": "file:///path"
        },
        {
            "id": "2",
            "name": "AVG-ML",
            "service-url": "https://avg-service.labs.dansdemo.nl",
            "result-url": "file:///path",
            "notification": [
                {
                    "type": "mail",
                    "conf": "file:///path"
                }
            ]
        },
        {
            "id": "3",
            "name": "TRANSCRIPT",
            "permission":"PUBLIC",
            "service-url": "https://whispers.surf.nl",
            "result-url": "https:/doi.org/doi-numbers"
        }
    ]
}

'''
