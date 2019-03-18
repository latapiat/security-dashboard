import yaml

def generate_visjs_graph(service_file):
    service_dict = yaml.load(service_file)

    nodes = [{"id": service, "label": service, "group": "service"}
             for service in service_dict['services']]

    nodes.append({"id": "public", "label": "public", "group": "public"})

    edges = [{"from": a, "to": b, "arrows": "to"}
             for a in service_dict['services']
             for b in service_dict['services']
             if b in service_dict['services'][a].get('depends_on',[])]

    return nodes, edges
