import xml.etree.ElementTree as ET

def get_item(attrib, item):
    try:
        return attrib[item]
    except:
        return None

class Layer:
    def __init__(self, attrib) -> None:
        # attrib={'id': '7362', 'name': 'Constant_239524', 'type': 'Convert', 'version': 'opset1'}
        self.id=get_item(attrib,'id')
        self.name=get_item(attrib,'name')
        self.type=get_item(attrib,'type')
        self.version=get_item(attrib,'version')
        # data
        self.data=None
        # input
        self.input=[]
        # output
        self.output=[]

    def add_data(self, shape=None, element_type=None):
        pass
    def add_input_output(self, shape, element_type, id, is_input=True):
        if is_input:
            self.input.append({"shape":shape, "element_type":element_type, "id":id})
        else:
            self.output.append({"shape":shape, "element_type":element_type, "id":id})

class Edge:
    def __init__(self, attrib) -> None:
        self.from_layer=attrib['from-layer']
        self.to_layer=attrib['to-layer']
        self.from_port=attrib['from-port']
        self.to_port=attrib['to-port']
        pass

def parse_input_output(sub_layer, my_layer, is_input=True):
    # <input ... or <output ...
    for port in sub_layer:
        # <dim ...
        my_dims=[]
        my_element_type=port.attrib['precision']
        my_id=port.attrib['id']
        for dim in port:
            my_dims.append(dim.text)
        # print("dims=", my_dims)
        my_layer.add_input_output(shape=my_dims, element_type=my_element_type, id=my_id, is_input=is_input)

class OV_IR:
    def __init__(self, xml_fn):
        self.xml_fn = xml_fn
        self.my_layers=[]
        self.my_edges=[]
        
        print("Start to read xml:" + self.xml_fn)
        tree = ET.parse(self.xml_fn)
        
        # getting the parent tag of the xml document
        root = tree.getroot()

        for net in root:
            if net.tag == 'layers':
                layers=net
                # ==================================
                for layer in layers:
                    # print(layer.attrib)
                    my_layer = Layer(layer.attrib)
                    
                    for sub_layer in layer:
                        # ===========================
                        # <input ...>
                        if sub_layer.tag == 'input':
                            # <port id=...
                            parse_input_output(sub_layer, my_layer, is_input=True)
                        # ===========================
                        # <data ...>
                        if sub_layer.tag == 'data':
                            pass

                        if sub_layer.tag == 'output':
                            # <port id=...
                            parse_input_output(sub_layer, my_layer, is_input=False)
                    self.my_layers.append(my_layer)
            elif net.tag == 'edges':
                edges = net
                # ==================================
                for edge in edges:
                    my_edge=Edge(edge.attrib)
                    self.my_edges.append(my_edge)

    # Get all parent id based on current layer id.
    def get_parent_ids(self, layer_id):
        parent_layers=[]
        for edge in self.my_edges:
            if edge.to_layer == layer_id:
                parent_layers.append(edge.from_layer)
        return parent_layers

    def get_son_edgs(self, layer_id):
        son_layers=[]
        for edge in self.my_edges:
            if edge.from_layer == layer_id:
                son_layers.append(edge.to_layer)
        return son_layers
    
    def get_layer_num(self):
        return len(self.my_layers)

    def get_layers(self) -> list:
        return self.my_layers

    def get_layer(self, layer_id) -> Layer:
        for layer in self.my_layers:
            if layer.id == layer_id:
                return layer
        return None
