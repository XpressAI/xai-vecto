from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
from vecto import Vecto, vecto_toolbelt
from vecto.vecto_requests import ( VectoIngestData, VectoEmbeddingData, VectoAttribute, 
                   VectoAnalogyStartEnd, IngestResponse, LookupResult, 
                   LookupResponse )
import os, io
from typing import IO, List, Union, NamedTuple

@xai_component
class VectoIngestImage(Component):
    """A component that accepts a str or list of image paths and their attribute, formats it 
    in a list of dicts to be accepted by the ingest function. 

    ### inPorts:
    - batch_path_list (str or list): Str or list of image paths.
    - attribute_list (str or list): Str or list of image attribute.

    ### outPorts:
    - IngestResponse: named tuple that contains the list of index of ingested objects.
    """

    vecto_client: InArg[any]
    batch_path_list: InCompArg[any] # Union[str, list]
    attribute_list: InCompArg[str] # Union[str, list]
    
    ingestResponse: OutArg[any]
    
    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.ingestResponse.value = vecto_toolbelt.ingest_image(vecto_client, self.batch_path_list.value, self.attribute_list.value)

        self.done = True


@xai_component
class VectoIngestAllImages(Component):
    """A component that accepts a list of image paths and their attribute, then send them
    to the ingest_image function in batches.

    ### inPorts:
    - path_list (list): List of image paths.
    - attribute_list (list): List of image attribute.
    - batch_size (int): batch size of images to be sent at one request. Default 64.

    ### outPorts:
    - IngestResponse: named tuple that contains the list of index of ingested objects.
    """

    vecto_client: InArg[any]
    path_list: InCompArg[list]
    attribute_list: InCompArg[list]
    batch_size: InArg[int]

    ingestResponse: OutArg[any]
    
    def __init__(self):
        super().__init__()
        self.batch_size.value = 64

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.ingestResponse.value = vecto_toolbelt.ingest_all_images(vecto_client, self.path_list.value, self.attribute_list.value, self.batch_size.value)

        self.done = True

@xai_component
class VectoIngestText(Component):
    """A component that accepts a str or list of text and their attribute, formats it 
    in a list of dicts to be accepted by the ingest function. 

    ### inPorts:
    - batch_text_list (str or list): Str or list of text.
    - attribute_list (str or list): Str or list of the text attribute.

    ### outPorts:
    - IngestResponse: named tuple that contains the list of index of ingested objects.
    """
    vecto_client: InArg[any]
    batch_text_list: InCompArg[any] # Union[str, list]
    attribute_list: InCompArg[str]

    IngestResponse: OutArg[any]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.IngestResponse.value = vecto_toolbelt.ingest_text(vecto_client, self.batch_text_list.value, self.attribute_list.value)

        self.done = True

@xai_component
class VectoIngestAllText(Component):
    """A component that accepts a list of text and their attribute, then send them
    to the ingest_text function in batches.

    ### inPorts:
    - batch_text_list (list): List of image paths.
    - attribute_list (list): List of image attribute.
    - batch_size (int): batch size of images to be sent at one request. Default 64.
    - **kwargs: Other keyword arguments for clients other than `requests`

    ### outPorts:
    - IngestResponse: named tuple that contains the list of index of ingested objects.
    """

    vecto_client: InArg[any]
    path_list: InCompArg[list]
    attribute_list: InCompArg[list]
    batch_size: InArg[int]

    ingestResponse: OutArg[any]
    
    def __init__(self):
        super().__init__()
        self.batch_size.value = 64

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.ingestResponse.value = vecto_toolbelt.ingest_all_text(vecto_client, self.path_list.value, self.attribute_list.value, self.batch_size.value)

        self.done = True

