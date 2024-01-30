from argparse import ArgumentParser
from gensim.models import Word2Vec
import time


parser = ArgumentParser(description='Update KGEs')
parser.add_argument('-w', '--walk-dir', dest='walk_dir', required=True, help='walk directory')
args = parser.parse_args()

print(f'Updating KGEs with {args.walk_dir} ...')

walks = []
with open(f'{args.walk_dir}', 'r', encoding='UTF-8') as file:
    for line in file:
        line = line.rstrip('\n')
        walk = line.split(' ')
        walks.append(walk)

model_dir = args.walk_dir.rsplit('/',1)[0]
model_updated = Word2Vec.load(f'{model_dir}/model')
start_time = time.time()
model_updated.build_vocab(walks, update=True)
model_updated.train(walks, total_examples=len(walks), epochs=5)
end_time = time.time()
model_updated.save(f'{args.walk_dir}/model_updated')

print(f'Number of walks: {len(walks)}')

sec = end_time - start_time
sec = sec % (24 * 3600)
hour = sec // 3600
sec %= 3600
min = sec // 60
sec %= 60

print('Training time: %02d:%02d:%02d' % (hour, min, sec))
