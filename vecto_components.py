from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component, secret
from vecto.schema import LookupResult, VectoIngestData
from typing import Union, List
from vecto import Vecto
from pprint import pprint
from dotenv import load_dotenv

import os, io
load_dotenv()

@xai_component
class VectoClient(Component):
    '''Component to initialize a Vecto client. 
    The client is set to the [ctx] so users do not need to pass the client around.

    ### inPorts:
    - token (secret): vecto token. If not provided, will check `vecto_token` from env.
    - vecto_base_url (str): vecto base url. Default: 'https://api.vecto.ai'
    - vector_space_id (int): vector space id. If not provided, will check from env.

    ### outPorts:
    - vecto_client: Vecto client object.
    '''
    token: InArg[secret]
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


@xai_component
class VectoLookup(Component):
    '''A component to search on Vecto, based on the lookup item.

    ### inPorts:
    - vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
    - query (IO): A IO file-like object. 
                    You can use open(path, 'rb') for IMAGE queries and io.StringIO(text) for TEXT queries.
    - modality (str): The type of the file - "IMAGE" or "TEXT"
    - top_k (int): The number of results to return. Default 5.
    - ids (list): A list of vector ids to search on aka subset of vectors, defaults to None
    - **kwargs: Other keyword arguments for clients other than `requests`

    ### outPorts:
    - LookupResponse: named tuple that contains a list of LookupResult named tuples.            
        where LookResult is named tuple with `data`, `id`, and `similarity` keys.
    '''

    vecto_client: InArg[any]
    query: InCompArg[any] #IO
    modality: InCompArg[str]
    top_k: InArg[int]

    LookupResponse: OutArg[LookupResult]

    def __init__(self):
        super().__init__()
        self.top_k.value = 5

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        
        f = ''

        if self.modality.value == 'TEXT':
            f = io.StringIO(self.query.value)

        elif self.modality.value == 'IMAGE':
            f = open(self.query.value, 'rb')

        self.LookupResponse.value = vecto_client.lookup(f, self.modality.value, self.top_k.value)
        # pprint(self.LookupResponse.value)


@xai_component
class VectoIngest(Component):
    '''''
    A component to ingest data into Vecto. 
                
    ### InPorts:
    - vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
    - ingest_data (VectoIngestData or list of VectoIngestData): you can also provide a dict, but ensure that it complies with VectoIngestData.
    - modality (str): 'IMAGE' or 'TEXT'

    ### outPorts:
    - IngestResponse: named tuple that contains the list of index of ingested objects.
    '''
    vecto_client: InArg[any]
    ingest_data: InCompArg[any] #Union[VectoIngestData, List[VectoIngestData]]
    modality: InCompArg[str]

    ingestResponse : OutArg[any] #IngestResponse

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']

        data = self.ingest_data.value
        if len(data) >= 100:
            chunk_size = 100
            chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

            i = 0
            for chunk in chunks:
                self.ingestResponse.value = vecto_client.ingest(chunk, self.modality.value)
                print(f"ingest {(i / len(data)) * 100}% complete.")
        else:
            self.ingestResponse.value = vecto_client.ingest(self.ingest_data.value, self.modality.value)
        # pprint(self.ingestResponse.value)


@xai_component
class VectoComputeAnalogy(Component):
    '''A component to compute an analogy using Vecto.
    It is also possible to do multiple analogies in one request body.
    The computed analogy is not stored in Vecto.

    ### inPorts:
    - query (IO): query in the form of an IO object query.
    - analogy_start_end (VectoAnalogyStartEnd or list of VectoAnalogyStartEnd): start and end analogy to be computed.
    - Use open(path, 'rb') for IMAGE or io.StringIO(text) for TEXT analogies.
    - top_k (int): The number of results to return. Default 5.
    - modality (str): The type of the file, 'IMAGE' or 'TEXT'

    ### outPorts:
    - LookupResponse: named tuple that contains a list of LookupResult named tuples.
        where LookResult is named tuple with `data`, `id`, and `similarity` keys.
    '''

    vecto_client: InArg[any]

    query: InCompArg[any] #IO
    analogy_start_end: InCompArg[any] #Union[VectoAnalogyStartEnd, List[VectoAnalogyStartEnd]]
    top_k: InArg[int]
    modality: InCompArg[str]

    LookupResponse: OutArg[LookupResult]

    def __init__(self):
        super().__init__()
        self.top_k.value = 5

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.LookupResponse.value = vecto_client.compute_analogy(self.query.value,
                                                           self.analogy_start_end.value, 
                                                           self.top_k.value, 
                                                           self.modality.value)
        # pprint(self.LookupResponse.value)
        


@xai_component
class VectoUpdateVectorEmbeddings(Component):
    '''A component to update current vector embeddings with new one.

    ### inPorts:
    - vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
    - embedding_data (VectoEmbeddingData or list of VectoEmbeddingData): data that contains the embedding data to be updated. 
    - modality (str): The type of the file - "IMAGE" or "TEXT"

    ### outPorts:
    - dict: Client response body
    '''
    vecto_client: InArg[any]
    embedding_data: InCompArg[any] #Union[VectoEmbeddingData, List[VectoEmbeddingData]]
    modality: InCompArg[str]

    response : OutArg[any]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.response.value = vecto_client.update_vector_embeddings(self.embedding_data.value, self.modality.value)


@xai_component
class VectoUpdateVectorAttribute(Component):
    '''A component to update current vector attribute with new one.

    ### inPorts:
    - vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
    - update_attribute (VectoAttribute or list of VectoAttribute) : attribute to be updated.

    '''
    vecto_client: InArg[any]
    update_attribute: InCompArg[any] #Union[VectoAttribute, List[VectoAttribute]]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        vecto_client.update_vector_attribute(self.update_attribute.value)



@xai_component
class VectoDeleteVectorEmbeddings(Component):
    '''A component to delete vector embeddings that is stored in Vecto.

    ### inPorts:
    - vecto_client: VectoClient object. If not provided, will check whether VectoClient already exists in ctx.
    - vector_ids (list): A list of vector ids to be deleted

    ### outPorts:
    - dict: Client response body
    '''
    vecto_client: InArg[any]
    vector_ids: InCompArg[list] 

    response: OutArg[any]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.response.value = vecto_client.delete_vector_embeddings(self.vector_ids.value)


@xai_component
class VectoDeleteVectorSpaceEntries(Component):
    '''A component to delete the current vector space in Vecto. 
    All ingested entries will be deleted as well.

    ### outPort:
    - response: Client response body
    '''

    vecto_client: InArg[any]
    response: OutArg[any]

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        self.response.value = vecto_client.delete_vector_space_entries()


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
        self.ingestResponse.value = vecto_client.ingest_image(self.batch_path_list.value, self.attribute_list.value)
        # pprint(self.ingestResponse.value)



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
        self.ingestResponse.value = vecto_client.ingest_all_images(self.path_list.value, self.attribute_list.value, self.batch_size.value)


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
        self.IngestResponse.value = vecto_client.ingest_text(self.batch_text_list.value, self.attribute_list.value)
        # pprint(self.IngestResponse.value)


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
        self.ingestResponse.value = vecto_client.ingest_all_text(self.path_list.value, self.attribute_list.value, self.batch_size.value)
        # pprint(self.ingestResponse.value)


