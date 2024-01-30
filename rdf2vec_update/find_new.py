from argparse import ArgumentParser
import pathlib


parser = ArgumentParser(description='Find')
parser.add_argument('-d', '--delimiter', nargs='?', const=1, default=' ', dest='delimiter', help='delimiter')
parser.add_argument('-p', '--path', dest='path', required=True, help='output path')
parser.add_argument('-o', '--old', dest='old_graph', required=True, help='old graph')
parser.add_argument('-n', '--new', dest='new_graph', required=True, help='new graph')
args = parser.parse_args()

delimiter = args.delimiter

triples_graph_old = []
entities_graph_old = []
with open(args.old_graph, 'r', encoding='UTF-8') as file:
    for line in file:
        line = line.replace(' .', '').replace('<', '').replace('>', '').rstrip('\n')
        triples_graph_old.append(line)
        elements = line.split(delimiter)
        del elements[1]
        entities_graph_old.extend(elements)

triples_graph_new = []
entities_graph_new = []
with open(args.new_graph, 'r', encoding='UTF-8') as file:
    for line in file:
        line = line.replace(' .', '').replace('<', '').replace('>', '').rstrip('\n')
        triples_graph_new.append(line)
        elements = line.split(delimiter)
        del elements[1]
        entities_graph_new.extend(elements)

new_triples = list(set(triples_graph_new) - set(triples_graph_old))
entities_graph_old = set(entities_graph_old)
entities_graph_new = set(entities_graph_new)
new_entities = list(entities_graph_new - entities_graph_old)

print('Computing new triples involving old entities')
new_triples_old_entities = []
for triple in new_triples:
    v_start, _, v_end = triple.split(' ')
    if v_start in entities_graph_old and v_end in entities_graph_old:
        new_triples_old_entities.append(triple)

pathlib.Path(f'{args.path}').mkdir(parents=True, exist_ok=True) 
with open(f'{args.path}/new_entities.txt', 'w') as f:
    for entity in new_entities:
        f.write(f'{entity}\n')

with open(f'{args.path}/new_triples.txt', 'w') as f:
    for triple in new_triples:
        f.write(f'{triple}\n')

with open(f'{args.path}/new_triples_old_entities.txt', 'w') as f:
    for triple in new_triples_old_entities:
        f.write(f'{triple}\n')

print(f'Saved new_entities and new_triples under {args.path}')

print(f'Number of triples in old graph: {len(triples_graph_old)}')
print(f'Number of triples in new graph: {len(triples_graph_new)}')
print(f'Number of new triples: {len(new_triples)}')
print(f'Number of new triples with only entities from old graph: {len(new_triples_old_entities)}')

print(f'Number of entities in old graph: {len(entities_graph_old)}')
print(f'Number of entities in new graph: {len(entities_graph_new)}')
print(f'Number of new entities: {len(new_entities)}')
