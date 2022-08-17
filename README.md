# Xircuits Vecto Components Library

## Requirements

PyCaret is tested and supported on the following 64-bit systems:
- Python 3.6 – 3.8
- Python 3.9 for Ubuntu only
- Ubuntu 16.04 or later
- Windows 7 or later

Ensure you have the right Python version before installing.

--- 

This library consists of Vecto components that allow a minimum Vecto implementation in Xircuits:

1. [VectoLogin](#vectologin)
2. [GetFlipkartDataset](#getflipkartdataset)
3. [GetDataFromCSV](#getdatafromcsv)
4. [GetImagesDataset](#getimagesdataset)
5. [IngestData](#ingestdata)
6. [VectoSearch](#vectosearch)
7. [VectoSearchAnalogy](#vectosearchanalogy)
8. [DisplayVectoResult](#displayvectoresult)

Below is a description of each components and its ports in Xircuits:

## Description
### VectoLogin

A component to initialize the Vecto API end-point and pass our Vector Space ID and authentication token into Vector Space. It's required at the start of every Vecto process.

**Please note that the Vector Space ID and token are unique for every Vector Space.**

##### inPorts:
- token: The Vector Space authentication. Must be filled.
- vecto_base_url: The main Vecto base URL. Default for public is http://api.vecto.ai/api/v0
- vector_space_id: The Vector Space ID. Must be filled.

### GetFlipkartDataset

A component that return a customized list of product's dataset from a raw CSV file.
It's custom made for [E-commerce recommendations using Vecto](https://docs.vecto.ai/docs/tutorial/tutorial_ecommerce/#dataset)
This component will get the CSV from the given path. Then, it'll concatenate text from product_name_header and description_header columns into new variable for vectorizing.

##### inPorts:
- folder_path: The dataset's path from base directory.
- product_name_header: The title/header of the product's name. Default header is 'product_name'.
- description_header: The title/header of the product's description. Default header is 'description'.

##### outPorts:
- dataset_text: The customized list of the product's dataset ready for vectorizing.

### GetDataFromCSV

A component that return lists of data and metadata list from a raw CSV file based on the given data_column and metadata_column. 
It's a carbon copy of GetFlipkartDataset component but for general purpose. 
It's also recommended that the dataset already 'clean' before ingesting.

##### inPorts:
- folder_path: The dataset's path from base directory.
- data_column: The title/header of the data column. 
- metadata_column: The title/header of the metadata column. 

##### outPorts:
- data: Return the column of data_column as a list
- metadata: Return the column of metadata_column as a list

### GetImagesDataset

A component that return a list of images given a folder's path.

##### inPorts:
- folder_path: The images dataset's path from base directory.
- images_type: What is the images type? (e.g jpg, png and etc)

##### outPorts:
- dataset_images: The list of images from the given folder path.

### IngestData

A component that will send datas by batch into Vector Space for vectorization.

##### Pre-requisite components:
- VectoLogin
- GetFlipkartDataset(Custom)/GetDataFromCSV(General)/GetImagesDataset(Images)

##### inPorts:
- batch_size: Batch size determines the number of data ingested in each batch. Default is 64.
- dataset: The customized dataset to ingest. Tip: Use GetFlipkartDataset/GetDataFromCSV component.
- are_data_images: Are the dataset's images? Default is False.
- delete_ingested: Should the previous ingested data be deleted before running ingestion process?. If false, it'll append the ingest data. Default is True.
- skip_ingested: This will skipped the ingestion process.

### VectoSearch

A component that will use search query to find similarities to the query vector against the whole Vector Space.

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

### VectoSearchAnalogy

A component that use analogies with vector arithmetic to do more advanced Vecto Search. 
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

### DisplayVectoResult

A component that will display the Vecto search results.

##### Pre-requisite component:
- GetFlipkartDataset(Custom)/GetDataFromCSV(General)/GetImagesDataset(Images)
- VectoSearch / VectoSearchAnalogy

##### inPorts:
- results: The Vecto Search output that you want to display. Either from VectoSearch or VectoSearchAnalogy components.

## Example

There a couple of template-like-example that already connected to run a simple Vecto Search using an **images dataset**. 

1. ingest_images.py - For ingesting images dataset.
2. vecto_search_images - To quering a vecto search and display the similarities.

It just missing  its `inPorts`. Before that, make sure you already create your [Vector Space](https://docs.vecto.ai/docs/tutorial/hello_world#make-a-vector-space) and you've your own images dataset.
