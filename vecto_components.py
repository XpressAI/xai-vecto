from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
from vecto import Vecto, vecto_toolbelt
import os, io

@xai_component
class VectoClient(Component):

    token: InArg[str]
    vecto_base_url: InArg[str]
    vector_space_id: InArg[int]

    vecto_client: OutArg[any]
    
    def __init__(self):

        self.done = False

        self.token = InArg.empty()
        self.vecto_base_url = InArg.empty()
        self.vector_space_id = InArg.empty()

        self.vecto_client = OutArg.empty()

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

    vecto_client: InArg[any]
    search_query: InCompArg[any]
    modality: InCompArg[str]
    top_k: InArg[int]
    
    
    def __init__(self):

        self.done = False

        self.vecto_client = InArg.empty()
        self.search_query = InCompArg.empty()
        self.modality = InCompArg.empty()
        self.top_k = InArg(100)

        self.vecto_client = OutArg.empty()

    def execute(self, ctx) -> None:

        vecto_client = self.vecto_client.value if self.vecto_client.value else ctx['vecto_client']
        
        f = ''

        if self.modality.value == 'TEXT':
            f = io.StringIO(self.search_query.value)

        elif self.modality.value == 'IMAGE':
            f = open(self.search_query.value, 'rb')

        lookup_response = vecto_client.lookup(f, self.modality.value, self.top_k.value)
        print(lookup_response)
        self.done = True

