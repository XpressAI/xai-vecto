from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
import requests
from IPython.display import Image, display, HTML
import io
import json
import re

@xai_component(color="#00D7F2")
class VectoLogin(Component):
    """A component to initialize the Vecto API end-point and pass your Vector Space ID and authentication token into Vector Space. 
    It's required at the start of every Vecto process. 
    
    **Please note that the Vector Space ID and token are unique for every Vector Space.**
    
    ##### inPorts:
    - token: The Vector Space authentication. Must be filled.
    - vecto_base_url: The main Vecto base URL. Default for public is http://api.vecto.ai/api/v0
    - vector_space_id: The Vector Space ID. Must be filled.
    """
    token: InCompArg[str]
    vecto_base_url: InArg[str]
    vector_space_id: InCompArg[int]
    
    def __init__(self):

        self.done = False
        self.token = InCompArg.empty()
        self.vecto_base_url = InArg.empty()
        self.vector_space_id = InCompArg.empty()

    def execute(self, ctx) -> None:
        
        vecto_setup_dict = {
            "vecto" : {
                "token" : self.token.value,
                "vecto_base_url" : self.vecto_base_url.value if self.vecto_base_url.value else 'http://api.vecto.ai/api/v0',
                "vector_space_id" : self.vector_space_id.value
                }
        }
        ctx.update(vecto_setup_dict)
        self.done = True

@xai_component(color="#00D7F2")
class GetFlipkartDataset(Component):
    """A component that return a customized list of product's dataset from a raw CSV file.
    It's custom made for [E-commerce recommendations using Vecto](https://docs.vecto.ai/docs/tutorial/tutorial_ecommerce/#dataset)
    This component will get the CSV from the given path. Then, it'll concatenate text from product_name_header and description_header columns into new variable for vectorizing.

    ##### inPorts:
    - folder_path: The dataset's path from base directory.
    - product_name_header: The title/header of the product's name. Default header is 'product_name'.
    - description_header: The title/header of the product's description. Default header is 'description'.
    
    ##### outPorts:
    - dataset_text: The customized list of the product's dataset ready for vectorizing.
    """
    folder_path: InCompArg[str]
    product_name_header: InArg[str]
    description_header: InArg[str]
    dataset_text: OutArg[list]

    def __init__(self):

        self.done = False
        self.folder_path = InCompArg.empty()
        self.product_name_header = InArg.empty()
        self.description_header = InArg.empty()
        self.dataset_text = OutArg.empty()

    def execute(self, ctx) -> None:
        
        import pandas as pd
        
        text_folder_path = self.folder_path.value
        product_name = self.product_name_header.value if self.product_name_header.value else 'product_name'
        description = self.description_header.value if self.description_header.value else 'description'
        text_data = pd.read_csv(text_folder_path).dropna(subset=[product_name,description])
        text_data['product_details'] = text_data[product_name].astype(str) +" "+ text_data[description].astype(str) 
        raw_text_list = text_data['product_details'].tolist()
        index_list = text_data.index.tolist()
        text_data["image"] = text_data["image"].apply(lambda x: json.loads(x) if type(x) == str else [])
        
        text_list = []
        for i in raw_text_list:
            text = (i.rstrip('\n')).replace('\n','')
            text = (text.rstrip('\t')).replace('\t','')
            text = re.sub('[^\w]',' ', text)
            text = re.sub('\s+',' ',text)
            text_list.append(text)
        
        list_of_data = {'data':text_data,'metadata': index_list}
        ctx.update(list_of_data)
        self.dataset_text.value = text_list
        self.done = True

@xai_component(color="#00D7F2")
class GetDataFromCSV(Component):
    """A component that return lists of data and metadata list from a raw CSV file based on the given data_column and metadata_column. 
    It's a carbon copy of GetFlipkartDataset component but for general purpose. 
    It's also recommended that the dataset already 'clean' before ingesting.

    ##### inPorts:
    - folder_path: The dataset's path from base directory.
    - data_column: The title/header of the data column. 
    - metadata_column: The title/header of the metadata column. 
    
    ##### outPorts:
    - data: Return the column of data_column as a list
    - metadata: Return the column of metadata_column as a list
    """
    folder_path: InCompArg[str]
    data_column: InCompArg[str]
    metadata_column: InCompArg[str]
    data: OutArg[list]
    metadata: OutArg[list]

    def __init__(self):

        self.done = False
        self.folder_path = InCompArg.empty()
        self.data_column = InCompArg.empty()
        self.metadata_column = InCompArg.empty()
        self.data = OutArg.empty()
        self.metadata = OutArg.empty()

    def execute(self, ctx) -> None:
        
        import pandas as pd
        
        text_folder_path = self.folder_path.value
        data_column = self.data_column.value 
        metadata_column = self.metadata_column.value
        csv_data = pd.read_csv(text_folder_path)
        data_list = csv_data[data_column].tolist()
        metadata_list = csv_data[metadata_column].tolist()
        
        list_of_data = {'data':data_list,'metadata': metadata_list}
        ctx.update(list_of_data)
        self.data.value = data_list
        self.metadata.value = metadata_list
        self.done = True
        
@xai_component(color="#00D7F2")
class GetImagesDataset(Component):
    """A component that return a list of images given a folder's path.

    ##### inPorts:
    - folder_path: The images dataset's path from base directory.
    - images_type: What is the images type? (e.g jpg, png and etc)
    
    ##### outPorts:
    - dataset_images: The list of images from the given folder path.
    """
    folder_path: InCompArg[str]
    images_type: InCompArg[str]
    dataset_images: OutArg[list]

    def __init__(self):

        self.done = False
        self.folder_path = InCompArg.empty()
        self.images_type = InCompArg.empty()
        self.dataset_images = OutArg.empty()

    def execute(self, ctx) -> None:
        
        import pathlib
        
        images_folder_path = self.folder_path.value
        images_type = self.images_type.value
        base_dir = pathlib.Path().absolute()
        dataset_path = base_dir.joinpath(images_folder_path)
        dataset_images = list(dataset_path.glob("**/*.%s" % images_type))
        images_data = {'data':dataset_path, 'are_data_images': True}
        ctx.update(images_data)
        self.dataset_images.value = dataset_images
        self.done = True

@xai_component(color="#00D7F2")
class IngestData(Component):
    """A component that will send datas by batch into Vector Space for vectorization.

    ##### Pre-requisite components:
    - VectoLogin
    - GetFlipkartDataset(Custom)/GetDataFromCSV(General)/GetImagesDataset(Images)
    
    ##### inPorts:
    - batch_size: Batch size determines the number of data ingested in each batch. Default is 64.
    - dataset: The customized dataset to ingest. Tip: Use GetFlipkartDataset/GetDataFromCSV component.
    - are_data_images: Are the dataset's images? Default is False.
    - delete_ingested: Should the previous ingested data be deleted before running ingestion process?. If false, it'll append the ingest data. Default is True.
    - skip_ingested: This will skipped the ingestion process.
    
    """
    batch_size: InArg[int]
    dataset: InCompArg[list]
    are_data_images: InArg[bool]
    delete_ingested: InArg[bool]
    skip_ingested: InArg[bool]

    def __init__(self):
        self.done = False
        self.batch_size = InArg.empty()
        self.dataset = InCompArg.empty()
        self.are_data_images = InArg.empty()
        self.delete_ingested = InArg.empty()
        self.skip_ingested = InArg.empty()
    
    def execute(self, ctx) -> None:
        
        from requests_toolbelt import MultipartEncoder
        from tqdm import tqdm
        import math
        
        self.done = True
        batch_size = self.batch_size.value
        dataset_list = self.dataset.value
        are_data_images = self.are_data_images.value
        delete_ingested = self.delete_ingested.value if self.delete_ingested.value else True
        skip_ingested = self.skip_ingested.value
        token = ctx['vecto']['token']
        vecto_base_url = ctx['vecto']['vecto_base_url']
        vector_space_id = ctx['vecto']['vector_space_id']
        
        
        def delete_all():
            payload = MultipartEncoder({'vector_space_id': str(vector_space_id)})
            results = requests.post("%s/delete_all" % vecto_base_url,
                          data=payload,
                          headers={"Authorization":"Bearer %s" % token, 'Content-Type': payload.content_type})
            print("Delete_all status:", results.status_code)
        
        def ingest_image_batch(batch_path_list):
            data = {'vector_space_id': vector_space_id, 'data': [], 'modality': 'IMAGE'}
            files = []
            for path in batch_path_list:
                relative = "%s/%s" % (path.parent.name, path.name)
                data['data'].append(relative)
                files.append(open(path, 'rb'))

            results = requests.post("%s/index" % vecto_base_url,
                          data=data,
                          files=[('input', ('dont_care', f, 'application/octet-stream')) for f in files],
                          headers={"Authorization":"Bearer %s" % token})
            if results.status_code != 200:
                print('Failed to Ingest: ', results)
                return
            for f in files:
                f.close()
    
        def ingest_all_images(path_list, batch_size=64):
            batch_count = math.ceil(len(path_list) / batch_size)
            batches = [path_list[i * batch_size: (i + 1) * batch_size] for i in range(batch_count)]
            for batch in tqdm(batches):
                ingest_image_batch(batch)
        
        def ingest_text_batch(batch_path_list,batch_text_list):
            data = {'vector_space_id': vector_space_id, 'data': [], 'modality': 'TEXT'}
            files = []
            for path in batch_path_list:
                data['data'].append(path)
            requests.post("%s/index" % vecto_base_url,
                          data=data,
                          files=[('input', ('dont_care', f, 'application/octet-stream')) for f in batch_text_list],
                          headers={"Authorization":"Bearer %s" %token})
            for f in files:
                f.close()
        
        def ingest_all_text(path_list, text_list, batch_size=64):
            batch_count = math.ceil(len(path_list) / batch_size)
            batches_path = [path_list[i * batch_size: (i + 1) * batch_size] for i in range(batch_count)]
            batches_text = [text_list[i * batch_size: (i + 1) * batch_size] for i in range(batch_count)]
            for batch,text in tqdm(zip(batches_path,batches_text), total = len(batches_path)):
                ingest_text_batch(batch,text)
        
        if skip_ingested:
            pass
        elif delete_ingested:
            delete_all()
        
        if skip_ingested:
            pass
        elif are_data_images:
            ingest_all_images(dataset_list, batch_size)
        else:
            index_list = ctx['metadata']
            ingest_all_text(index_list, dataset_list, batch_size)

@xai_component(color="#00D7F2")
class VectoSearch(Component):
    """A component that will use search query to find similarities to the query vector against the whole Vector Space.

    ##### Pre-requisite component:
    - VectoLogin
    
    ##### Suggestion for next component:
    - DisplayVectoResult

    ##### inPorts:
    - query: The input that we want to vectorize/search. If query an image, provide its path.
    - top_k: How many similarities you want. Default is 10.
    - is_query_image: Is the query an image? Default is False.
    
    ##### outPorts:
    - results: The output with the highest similarity.
    
    """
    query: InCompArg[str]
    top_k: InArg[int]
    is_query_image: InArg[bool]
    results: OutArg[any]

    def __init__(self):
        self.done = False
        self.query = InArg.empty()
        self.top_k = InArg.empty()
        self.is_query_image = InArg.empty()
        self.results = OutArg.empty()

    def execute(self, ctx) -> None:
        
        token = ctx['vecto']['token']
        vecto_base_url = ctx['vecto']['vecto_base_url']
        vector_space_id = ctx['vecto']['vector_space_id']
        query = self.query.value
        top_k = self.top_k.value
        is_query_image = self.is_query_image.value if self.is_query_image.value else False
        
        def lookup(f, modality, top_k):
            result = requests.post("%s/lookup" % vecto_base_url,
                                   data={'vector_space_id': vector_space_id, 'modality': modality, 'top_k': top_k,},
                                   files={'query': f},
                                   headers={"Authorization":"Bearer %s" % token})
            print(result)
            results = result.json()['results']
            self.results.value = results

        def text_query(query, top_k=10):
            f = io.StringIO(query)
            lookup(f, 'TEXT', top_k)

        def image_query(query, top_k=10):
            with open(query, "rb") as image:
                f = image.read()
                f = io.BytesIO(f)
            lookup(f, 'IMAGE', top_k)
        
        if is_query_image:
            image_query(query, top_k)
        else:
            text_query(query, top_k)
        self.done = True
        
@xai_component(color="#00D7F2")
class VectoSearchAnalogy(Component):
    """A component that use analogies with vector arithmetic to do more advanced Vecto Search. 
    Analogy completion via vector arithmetic has become a common means of demonstrating the compositionality of embeddings. 
    
    ##### Pre-requisite component:
    - VectoLogin
    
    ##### Suggestion for next component:
    - DisplayVectoResult
    
    ##### inPorts:
    - query: The query to apply the analogy on. If query an image, provide its path.
    - start: The start of the analogy.
    - end: The end of the analogy.
    - top_k: How many similarities you want. Default is 10.
    - is_query_image: Is the query an image? Default is False.
    
    ##### outPorts:
    - results: The output with the highest similarity.
    
    """
    
    query: InCompArg[str]
    start: InCompArg[str]
    end: InCompArg[str]
    top_k: InArg[int]
    is_query_image: InArg[bool]
    results: OutArg[any]

    def __init__(self):

        self.done = False
        self.query =  InCompArg.empty()
        self.start =  InCompArg.empty()
        self.end =  InCompArg.empty()
        self.top_k  =  InArg.empty()
        self.is_query_image = InArg.empty()
        self.results = OutArg.empty()

    def execute(self, ctx) -> None:

        self.done = True
        token = ctx['vecto']['token']
        vecto_base_url = ctx['vecto']['vecto_base_url']
        vector_space_id = ctx['vecto']['vector_space_id']
        query = self.query.value
        start = self.start.value
        end = self.end.value
        top_k = self.top_k.value
        is_query_image = self.is_query_image.value if self.is_query_image.value else False
        
        def analogy(query, start, end, modality, top_k):
            result = requests.post("%s/analogy" % vecto_base_url,
                                   data={'vector_space_id': vector_space_id, 'modality': modality, 'top_k': top_k},
                                   files={'query': query, 'from': start, 'to': end},
                                   headers={"Authorization":"Bearer %s" %token})

            results = result.json()['results']
            self.results.value = results
            
        def text_analogy(query, start, end, top_k=10):
            analogy(io.StringIO(query), io.StringIO(start), io.StringIO(end), 'TEXT', top_k)

        def image_analogy(query, start, end, top_k=10):
            with open(query, "rb") as image:
                f = image.read()
                main_query = io.BytesIO(f)
            with open(start, "rb") as image:
                f = image.read()
                start_analogy = io.BytesIO(f)
            with open(end, "rb") as image:
                f = image.read()
                end_analogy = io.BytesIO(f)
            analogy(
                main_query,
                start_analogy,
                end_analogy,
                'IMAGE',
                top_k
            )
        
        if is_query_image:
            image_analogy(query, start, end, top_k)
        else:
            text_analogy(query, start, end, top_k)

@xai_component(color="#00D7F2")
class DisplayVectoResult(Component):
    """A component that will display the Vecto search results.

    ##### Pre-requisite component:
    - GetFlipkartDataset(Custom)/GetDataFromCSV(General)/GetImagesDataset(Images)
    - VectoSearch / VectoSearchAnalogy

    ##### inPorts:
    - results: The Vecto Search output that you want to display. Either from VectoSearch or VectoSearchAnalogy components.
    
    """
    results: InArg[any]

    def __init__(self):
        self.done = False
        self.results = InArg.empty()

    def execute(self, ctx) -> None:
        results = self.results.value
        data = ctx['data']
        print(data)
        try:
            are_data_images = ctx['are_data_images'] 
        except:
            are_data_images = False
        def display_results(results):
            output = []
            for result in results:
                output.append("Similarity: %s" % result['similarity'])
                if are_data_images:
                    output.append(Image(data.joinpath(result['data'])))
                else:
                    image = data['image'][int(result['data'])][0]
                    image = HTML('<img src=%s width="300" height="500">'% image)
                    output.append(image)
                    text = data['product_details'][int(result['data'])]
                    output.append(text)
            display(*output)
        try:
            display_results(results)
        except Exception as e:
            print("Something wrong in displaying the Vecto Search result.")
            print(e)
        self.done = True