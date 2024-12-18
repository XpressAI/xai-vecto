<p align="center">
  <a href="https://github.com/XpressAI/xircuits/tree/master/xai_components#xircuits-component-library-list">Component Libraries</a> •
  <a href="https://github.com/XpressAI/xircuits/tree/master/project-templates#xircuits-project-templates-list">Project Templates</a>
  <br>
  <a href="https://xircuits.io/">Docs</a> •
  <a href="https://xircuits.io/docs/Installation">Install</a> •
  <a href="https://xircuits.io/docs/category/tutorials">Tutorials</a> •
  <a href="https://xircuits.io/docs/category/developer-guide">Developer Guides</a> •
  <a href="https://github.com/XpressAI/xircuits/blob/master/CONTRIBUTING.md">Contribute</a> •
  <a href="https://www.xpress.ai/blog/">Blog</a> •
  <a href="https://discord.com/invite/vgEg2ZtxCw">Discord</a>
</p>

<p align="center">
<a href="https://www.vecto.ai/">
<img src="https://user-images.githubusercontent.com/68586800/192857099-499146bb-5570-4702-a88f-bb4582e940c0.png" width="300"/>
</a>


<p align="center"><i>Xircuits Component Library to interface with Vecto AI! Seamlessly manage vector embeddings and perform advanced vector operations.</i></p>

---
## Xircuits Component Library for Vecto
Integrate Vecto AI into Xircuits workflows for seamless vector embedding management, advanced search, data ingestion, and analogy computation for both text and image data.

## Table of Contents

- [Preview](#preview)
- [Prerequisites](#prerequisites)
- [Main Xircuits Components](#main-xircuits-components)
- [Try the Examples](#try-the-examples)
- [Installation](#installation)

## Preview

### SimpleAnalogy Example:

<img src="https://github.com/user-attachments/assets/61c1e26f-c2c4-4726-a088-a707e8516a27" alt="SimpleAnalogy_example"  />

### SimpleAnalogy Result:

<img src="https://github.com/user-attachments/assets/61eee2c3-083a-4936-a3f9-40206035fbb3" alt="SimpleAnalogy_result" />

<img src="https://github.com/user-attachments/assets/03a85803-5e7b-4cbd-83b2-fa87d1ff3bab" alt="SimpleAnalogy_vecto"  />

## Prerequisites

Before you begin, you will need the following:

1. Python3.9+.
2. Xircuits.
3. Vecto token and space_id

## Main Xircuits Components

### VectoClient Component:
Initializes a Vecto client for managing vector operations and sets it in the context for reuse across workflows.

<img src="https://github.com/user-attachments/assets/21aceacf-a5de-4094-87af-7f6cb274ff13" alt="VectoClient" width="200" height="125" />

### VectoLookup Component:
Performs a lookup operation on Vecto using a query (text or image) and returns the most similar vectors based on the specified modality.

<img src="https://github.com/user-attachments/assets/22e35f4e-ee25-4af7-8e9e-4c4c0297dca3" alt="VectoLookup" width="200" height="150" />

### VectoIngest Component:
Ingests data (text or image) into Vecto's vector space for efficient vector representation and similarity search.

### VectoComputeAnalogy Component:
Calculates analogies between vectors using Vecto for both text and image modalities.

### VectoUpdateVectorEmbeddings Component:
Updates existing vector embeddings in Vecto with new data.

### VectoUpdateVectorAttribute Component:
Modifies attributes of existing vectors in Vecto.

### VectoDeleteVectorEmbeddings Component:
Deletes specified vector embeddings from Vecto's vector space.

### VectoIngestImage Component:
Ingests one or more images into Vecto's vector space, with attributes for metadata.

### VectoIngestText Component:
Ingests one or more text entries into Vecto's vector space, with attributes for metadata.

## Try The Examples

We have provided an example workflow to help you get started with the Vecto component library. Give it a try and see how you can create custom Vecto components for your applications.

### SimpleLookup Example  
Check out the `SimpleLookup.xircuits` workflow. This example demonstrates how to perform a search in Vecto by querying vectors for similarity based on text or image data.

---

### SimpleIngestLookup Example  
Check out the `SimpleIngestLookup.xircuits` workflow. This example shows how to ingest data into Vecto's vector space and perform a lookup to retrieve similar vectors.

---

### SimpleAnalogy Example  
Check out the `SimpleAnalogy.xircuits` workflow. This example highlights how to compute analogies between vectors in Vecto, leveraging the relationships between vector embeddings.

## Installation
To use this component library, ensure that you have an existing [Xircuits setup](https://xircuits.io/docs/main/Installation). You can then install the Vecto library using the [component library interface](https://xircuits.io/docs/component-library/installation#installation-using-the-xircuits-library-interface), or through the CLI using:

```
xircuits install vecto
```
You can also do it manually by cloning and installing it:
```
# base Xircuits directory
git clone https://github.com/XpressAI/xai-vecto xai_components/xai_vecto
pip install -r xai_components/xai_vecto/requirements.txt 
```
### Authentication and Setup for Vecto

To access Vecto services, follow these steps:

1. **Create an Account and Log In**:
   - Visit [app.vecto.ai](https://app.vecto.ai) and register for an account.
   - After registering, log in to your account.

2. **Create a New Vector Space**:
   - Navigate to the dashboard and create a new vector space. Note the `space ID` assigned to it for later use.

3. **Generate a Token**:
   - Click on your account name in the top-right corner of the dashboard.
   - Select **Tokens** from the dropdown menu and create a new token.
   - **Important**: The token will only be displayed once. Save it securely in a safe location.

4. **Start Using Vecto**:
   - With your token and `space ID`, you are ready to use Vecto in your Xircuits workflows.