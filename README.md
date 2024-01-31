# RDF2vec Update

RDF2vec Update consists of three Python scripts for updating <a href="http://rdf2vec.org/">RDF2Vec</a> embeddings:

- find_new.py
- generate_walks.py
- update_model.py

## Usage Example

Find the new triples in a knowledge graph from two snapshots:

```bash
python3 find_new.py --old kg_old.ttl --new kg_new.ttl --path ./output 
```

Extract update walks from the new snapshot using the new triples:

```bash
python3 generate_walks.py --triples ./output/new_triples.txt --graph kg_new.ttl --depth 4 --walks 10 -p ./output 
```

Continue training a pre-trained <a href="https://github.com/dwslab/jRDF2Vec/">RDF2vec model</a> on the update walks:

```bash
python3 update_model.py --walks ./output/walks.txt --model ./pretrained/model
```

