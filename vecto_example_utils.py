from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
from vecto.schema import LookupResult, VectoIngestData
from typing import Union, List

@xai_component
class CSV2VectoIngest(Component):
    '''Component that tran a csv file into list of VectoIngestData.

    ### inPorts:
    - csv_path (str): path of the csv file. 
    - data_str (str): data to be ingested.
    - attribute_str (str): The attribute of the data.
    - delimiter (str): csv data delimiter. Default ",".

    ### outPorts:
    - IngestData: data in VectoIngestData format for VectoIngest.
    '''
    csv_path: InCompArg[str]
    data_str: InCompArg[str]
    attribute_str: InCompArg[str]

    delimiter: InArg[str]

    IngestData: OutArg[Union[VectoIngestData, List[VectoIngestData]]]

    def __init__(self):
        super().__init__()
        self.delimiter.value = ","

    def execute(self, ctx) -> None:

        import csv

        data = []

        with open(self.csv_path.value, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter.value)
            
            for row in reader:
                if ',' in self.attribute_str.value:
                    data.append({
                        'data': row[self.data_str.value],
                        'attributes': {attr: row[attr] for attr in self.attribute_str.value.split(',')}
                    })
                else:
                    data.append({'data': row[self.data_str.value], 'attributes': row[self.attribute_str.value]})

        self.IngestData.value = data
        
@xai_component
class PrettyPrint(Component):
    msg: InArg[any]
    
    def execute(self, ctx) -> None:
        from pprint import pprint
        pprint(self.msg.value)


@xai_component
class VectoResultUnpacker(Component):
    """
    A component to unpack a LookupResult into its individual components: attributes, id, and similarity.
    
    ### InPorts:
    - lookup_result: The LookupResult named tuple to be unpacked.

    ### OutPorts:
    - attributes: The attributes part of the LookupResult.
    - id: The id part of the LookupResult.
    - similarity: The similarity score part of the LookupResult.
    """
    lookup_result: InCompArg[LookupResult]

    attributes: OutArg[object]
    id: OutArg[int]
    similarity: OutArg[float]

    def execute(self, ctx) -> None:
        self.attributes.value = self.lookup_result.value.attributes
        self.id.value = self.lookup_result.value.id
        self.similarity.value = self.lookup_result.value.similarity

