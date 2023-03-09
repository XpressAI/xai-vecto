from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
from vecto import Vecto, vecto_toolbelt
from vecto.vecto_requests import ( VectoIngestData, VectoEmbeddingData, VectoMetadata, 
                   VectoAnalogyStartEnd, IngestResponse, LookupResult, 
                   LookupResponse )
import os, io
from typing import IO, List, Union, NamedTuple

@xai_component
class VectoClient(Component):

    token: InArg[str]
    vecto_base_url: InArg[str]
    vector_space_id: InArg[int]

    vecto_client: OutArg[any]

    def execute(self, ctx) -> None:

        token = self.token.value if self.token.value else os.environ['user_token']

        vecto_base_url = ''
        if self.vecto_base_url.value:
            vecto_base_url = self.vecto_base_url.value
        elif os.environ.get('vecto_base_url') is not None:
            vecto_base_url = os.environ['vecto_base_url']
        else:
            vecto_base_url = 'https://api.vecto.ai'

        vector_space_id = self.vector_space_id.value if self.vector_space_id.value else os.environ['vector_space_id']

        vecto_client = Vecto(token, vector_space_id, vecto_base_url=vecto_base_url)

        ctx.update({'vecto_client': vecto_client})
        self.done = True

@xai_component
class VectoLookup(Component):
    '''A component to search on Vecto, based on the lookup item.

    inPorts:
        vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
        query (IO): A IO file-like object. 
                    You can use open(path, 'rb') for IMAGE queries and io.StringIO(text) for TEXT queries.
        modality (str): The type of the file - "IMAGE" or "TEXT"
        top_k (int): The number of results to return
        ids (list): A list of vector ids to search on aka subset of vectors, defaults to None
        **kwargs: Other keyword arguments for clients other than `requests`

    outPorts:
        LookupResponse: named tuple that contains a list of LookupResult named tuples.            
        where LookResult is named tuple with `data`, `id`, and `similarity` keys.
    '''

    vecto_client: InArg[any]
    query: InCompArg[any]
    modality: InCompArg[str]
    top_k: InArg[int]

    def __init__(self):
        super().__init__()
        self.top_k.value = 100

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        
        f = ''

        if self.modality.value == 'TEXT':
            f = io.StringIO(self.query.value)

        elif self.modality.value == 'IMAGE':
            f = open(self.query.value, 'rb')

        lookup_response = vecto_client.lookup(f, self.modality.value, self.top_k.value)
        print(lookup_response)
        self.done = True


@xai_component
class VectoIngest(Component):
    '''''
    A component to ingest data into Vecto. 
                
    InPorts:
        vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
        ingest_data (VectoIngestData or list of VectoIngestData): you can also provide a dict, but ensure that it complies with VectoIngestData.
        modality (str): 'IMAGE' or 'TEXT'

    outPorts:
        IngestResponse: named tuple that contains the list of index of ingested objects.
    '''
    vecto_client: InArg[any]
    ingest_data: InCompArg[any] #Union[VectoIngestData, List[VectoIngestData]]
    modality: InCompArg[str]

    ingestResponse : OutArg[IngestResponse]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.ingestResponse.value = vecto_client.ingest(self.ingest_data.value, self.modality.value)

        self.done = True


@xai_component
class VectoUpdateVectorEmbeddings(Component):
    '''A component to update current vector embeddings with new one.

    inPorts:
        vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
        embedding_data (VectoEmbeddingData or list of VectoEmbeddingData): data that contains the embedding data to be updated. 
        modality (str): The type of the file - "IMAGE" or "TEXT"
        **kwargs: Other keyword arguments for clients other than `requests`

    outPorts:
        dict: Client response body
    '''
    vecto_client: InArg[any]
    embedding_data: InCompArg[any] #Union[VectoEmbeddingData, List[VectoEmbeddingData]]
    modality: InCompArg[str]

    response : OutArg[any]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.response.value = vecto_client.update_vector_embeddings(self.embedding_data.value, self.modality.value)

        self.done = True


@xai_component
class VectoUpdateVectorMetadata(Component):
    '''A component to update current vector metadata with new one.

    inPorts:
        vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
        update_metadata (VectoMetadata or list of VectoMetadata) : metadata to be updated.

    '''
    vecto_client: InArg[any]
    update_metadata: InCompArg[any] #Union[VectoMetadata, List[VectoMetadata]]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        vecto_client.update_vector_metadata(self.update_metadata.value)

        self.done = True


@xai_component
class VectoDeleteVectorEmbeddings(Component):
    '''A component to delete vector embeddings that is stored in Vecto.

    inPorts:
        vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
        vector_ids (list): A list of vector ids to be deleted

    outPorts:
        dict: Client response body
    '''
    vecto_client: InArg[any]
    vector_ids: InCompArg[list] 

    response: OutArg[any]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.response.value = vecto_client.delete_vector_embeddings(self.vector_ids.value)

        self.done = True

@xai_component
class VectoDeleteVectorSpaceEntries(Component):
    '''A component to delete the current vector space in Vecto. 
    All ingested entries will be deleted as well.

    outPort:
        dict: Client response body
    '''

    vecto_client: InArg[any]
    response: OutArg[any]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.response.value = vecto_client.delete_vector_space_entries()

        self.done = True
