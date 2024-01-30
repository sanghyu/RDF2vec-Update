from argparse import ArgumentParser
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_predict, StratifiedKFold 


parser = ArgumentParser(description='Classification with split accuracy')
parser.add_argument('-d', '--datasets', dest='datasets_dir', default=None, required=True, help='path of geval datasets')
parser.add_argument('-c', '--classic-vectors', dest='classic_vectors', default=None, required=True, help='path of classic vectors')
parser.add_argument('-u', '--update-vectors', dest='update_vectors', default=None, required=True, help='path of update vectors')
parser.add_argument('-e', '--entities', dest='new_entities', default=None, required=True, help='path of new entities')
parser.add_argument('-n', '--vector-size', nargs='?', type=int, default=200, dest='vector_size', help='vector size')
args = parser.parse_args()

print(f'Input:\n vector_size: {args.vector_size}')
print(f'Classic vectors: {args.classic_vectors}')
print(f'Update vectors: {args.update_vectors}')
print(f'New entities: {args.new_entities}\n')

datasets = ['Forbes', 'MetacriticAlbums', 'MetacriticMovies']
vector_size = args.vector_size
headers = ['name']
for i in range(0, vector_size):
    headers.append(i)

entities_classic = []
with open(args.classic_vectors, 'r', encoding='UTF-8') as file:
    for line in file:
        line = line.rstrip('\n')
        entity = line.split(' ')[0]
        entities_classic.append(entity)

entities_new = []
with open(args.new_entities, 'r', encoding='UTF-8') as file:
    for line in file:
        line = line.rstrip('\n')
        entities_new.append(line)

vectors = pd.read_csv(args.update_vectors, sep='\s+', names=headers, encoding='utf-8', index_col=False)

for dataset in datasets:
    gold = pd.read_csv(f'{args.datasets_dir}/{dataset}.tsv', delimiter='\t')
    gold.rename(columns={'DBpedia_URI15': 'name'}, inplace=True)
    gold = gold[['name', 'label']]
    gold.loc[gold['name'].isin(entities_classic), 'membership'] = 'classic'
    gold.loc[gold['name'].isin(entities_new), 'membership'] = 'new'
    gold = gold.loc[gold['membership'] != 'nan']

    data = pd.merge(gold, vectors, on='name', how='inner')
    model = SVC(C=1)
    if dataset == 'MetacriticMovies':
        n_splits = 10
    else:
        n_splits = 5   
    n_samples = data.shape[0]
    
    scores = []
    scores_classic = []
    scores_new = []

    for i in range(10):
        data = data.sample(frac=1, random_state=i).reset_index(drop=True)
        skf = StratifiedKFold(n_splits=n_splits,random_state=i,shuffle=True)
        pred = cross_val_predict(model, data.iloc[:, 3:], data['label'], cv=skf)
        fold_pred = [pred[x] for _, x in skf.split(data.iloc[:, 3:],data['label'])]
        fold_label = [data['label'][x] for _, x in skf.split(data.iloc[:, 3:],data['label'])]
        
        fold_scores = []
        fold_scores_classic= []
        fold_scores_new = []
        for j in range(n_splits):
            results = []
            results_classic = []
            results_new = []
            for k in range(len(fold_label[j])):
                if fold_label[j].tolist()[k] == fold_pred[j].tolist()[k]:
                    results.append(1)
                    if data['membership'].iloc[fold_label[j].index[k]] == 'classic':
                        results_classic.append(1)
                    else:
                        results_new.append(1)
                else:
                    results.append(0)
                    if data['membership'].iloc[fold_label[j].index[k]] == 'classic':
                        results_classic.append(0)
                    else:
                        results_new.append(0)

            fold_scores.append(sum(results)/len(results))
            fold_scores_classic.append(sum(results_classic)/len(results_classic))
            fold_scores_new.append(sum(results_new)/len(results_new))

        scores.append(np.mean(fold_scores))
        scores_classic.append(np.mean(fold_scores_classic))
        scores_new.append(np.mean(fold_scores_new))

    print(f'{dataset} accuracy: {np.mean(scores)}')
    print(f'{dataset} v_classic accuracy: {np.mean(scores_classic)}')
    print(f'{dataset} v_new accuracy: {np.mean(scores_new)}\n')
