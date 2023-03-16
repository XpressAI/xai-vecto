from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component

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

    IngestData: OutArg[any] #Union[VectoIngestData, List[VectoIngestData]]

    def __init__(self):
        super().__init__()
        self.delimiter.value = ","

    def execute(self, ctx) -> None:

        import csv

        data = []

        with open(self.csv_path.value, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter.value)
            
            for row in reader:
                data.append({'data': row[self.data_str.value], 'attributes': row[self.attribute_str.value]})

        self.IngestData.value = data