from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
from vecto import Vecto, vecto_toolbelt
from vecto import ( VectoIngestData, VectoEmbeddingData, VectoMetadata, 
                   VectoAnalogyStartEnd, IngestResponse, LookupResult, 
                   LookupResponse )
import os, io
from typing import IO, List, Union, NamedTuple

@xai_component
class VectoIngestImage(Component):

    vecto_client: InArg[any]
    image_path: InCompArg[str]
    metadata: InCompArg[str]
    
    
    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']

        vecto_toolbelt.ingest_image(vecto_client, self.image_path.value, self.metadata.value)

        self.done = True


@xai_component
class VectoIngestText(Component):

    vecto_client: InArg[any]
    image_path: InCompArg[str]
    metadata: InCompArg[str]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        vecto_toolbelt.ingest_text(vecto_client, self.image_path.value, self.metadata.value)

        self.done = True
