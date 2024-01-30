from argparse import ArgumentParser
import time
import random
import pathlib

        
parser = ArgumentParser(description='Generate RDF2vec Update walks from triples and/or entities')
parser.add_argument('-d', '--depth', nargs='?', type=int, default=4, dest='depth', help='walk depth (here depth = hops between entities)')
parser.add_argument('-n', '--walks', nargs='?', type=int, default=10, dest='walks_per_entity', help='walks per entity or triple')
parser.add_argument('-g', '--graph', dest='graph', required=True, help='graph path')
parser.add_argument('-e', '--entities', dest='input_entities', default=None, required=False, help='input triples path')
parser.add_argument('-t', '--triples', dest='input_triples', default=None, required=False, help='input triples path')
parser.add_argument('-p', '--path', dest='path', required=True, help='output path')
args = parser.parse_args()

start_time = time.time()

graph = []
with open(args.graph, 'r', encoding='UTF-8') as file:
    for line in file:
        line = line.replace(' .', '').replace('<', '').replace('>', '').rstrip('\n')
        graph.append(line)
print(f'Number of triples in graph: {len(graph)}')

_pred = [x.rsplit(' ',1) for x in graph]
_succ = [x.split(' ',1) for x in graph]

pred_dict= {}
for v, k in _pred:
    pred_dict.setdefault(k, []).append(v)

succ_dict= {}
for k, v in _succ:
    succ_dict.setdefault(k, []).append(v)

d = args.depth
n = args.walks_per_entity

# Walks for RDF2vec Update 
if args.input_triples:
    triples = []
    with open(args.input_triples, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.rstrip('\n')
            triples.append(line)
    print(f'Number of new triples: {len(triples)}')

    update_walks = []
    for triple in triples:
        for _ in range(n):
            w = triple
            v_start, _, v_end = w.split(' ')
            if v_start in pred_dict:
                pred = pred_dict[v_start]
            else:
                pred = []
            if v_end in succ_dict:
                succ = succ_dict[v_end]
            else:
                succ = []
            while len(w.split(' '))/2 < d:
                cand = pred + succ
                if not cand:
                    break
                else:
                    elem = random.choice(cand)
                    if elem in pred:
                        w = elem + ' ' + w
                        v_start = elem.split(' ')[0]
                        if v_start in pred_dict:
                            pred = pred_dict[elem.split(' ')[0]]
                        else:
                            pred = []
                    else:
                        w = w + ' ' + elem
                        v_end = elem.split(' ')[1]
                        if v_end in succ_dict:
                            succ = succ_dict[elem.split(' ')[1]]
                        else:
                            succ = []
            update_walks.append(w)

if args.input_entities:
    entities = []
    with open(args.input_entities, 'r', encoding='UTF-8') as file:
        for line in file:
            line = line.rstrip('\n')
            entities.append(line)
    print(f'Number of new entities: {len(entities)}')

    update_walks_input_entities = []
    for entity in entities:
        for _ in range(n):
            w = entity
            if entity in pred_dict:
                pred = pred_dict[entity]
            else:
                pred = []
            if entity in succ_dict:
                succ = succ_dict[entity]
            else:
                succ = []
            while len(w.split(' '))/2 < d:
                cand = pred + succ
                if not cand:
                    break
                else:
                    elem = random.choice(cand)
                    if elem in pred:
                        w = elem + ' ' + w
                        v_start = elem.split(' ')[0]
                        if v_start in pred_dict:
                            pred = pred_dict[elem.split(' ')[0]]
                        else:
                            pred = []
                    else:
                        w = w + ' ' + elem
                        v_end = elem.split(' ')[1]
                        if v_end in succ_dict:
                            succ = succ_dict[elem.split(' ')[1]]
                        else:
                            succ = []
            update_walks_input_entities.append(w)

end_time = time.time()

pathlib.Path(f'{args.path}').mkdir(parents=True, exist_ok=True)
with open(f'{args.path}/walks.txt', 'w') as f:
    if args.input_triples and not args.input_entities:
        for walk in update_walks:
            f.write(f'{walk}\n')
    if args.input_entities and not args.input_triples:
        for walk in update_walks_input_entities:
            f.write(f'{walk}\n')
    if args.input_triples and args.input_entities:
        for walk in update_walks + update_walks_input_entities:
                f.write(f'{walk}\n')

sec = end_time - start_time
sec = sec % (24 * 3600)
hour = sec // 3600
sec %= 3600
min = sec // 60
sec %= 60

print('Walk generation time: %02d:%02d:%02d' % (hour, min, sec))
print(f'Saved walks under {args.path}')
