from argparse import ArgumentParser
from gensim.models import Word2Vec
import time

"""
This script updates a pretrained RDF2vec model.
Required inputs: RDF2vec model, walks
"""

parser = ArgumentParser(description='Update KGEs')
parser.add_argument('-w', '--walks', dest='walk_path', required=True, help='path to walks file')
parser.add_argument('-m', '--model', dest='model_path', required=True, help='path to model file')
args = parser.parse_args()

print(f'Updating KGEs with {args.walk_path} ...')

# Get walks from txt file
walks = []
with open(f'{args.walk_path}', 'r', encoding='UTF-8') as file:
    for line in file:
        line = line.rstrip('\n')
        walk = line.split(' ')
        walks.append(walk)

# Update model and save updated model separately
model_updated = Word2Vec.load(f'{args.model_path}')
start_time = time.time()
model_updated.build_vocab(walks, update=True)
model_updated.train(walks, total_examples=len(walks), epochs=5)
end_time = time.time()
model_updated.save(f'{args.model_path}/model_updated')

print(f'Number of walks: {len(walks)}')

sec = end_time - start_time
sec = sec % (24 * 3600)
hour = sec // 3600
sec %= 3600
min = sec // 60
sec %= 60

print('Training time: %02d:%02d:%02d' % (hour, min, sec))
