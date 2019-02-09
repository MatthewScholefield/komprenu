import simplejson as json
from prettyparse import create_parser

from komprenu.model import Model

usage = '''
    Train a new grammar model on the input json data
    
    :data_json str
        Data file to load from

    :model_json str
        Model file to write to
    
    :--latent-len -l int 100
        Number of latent bits in model
    
    :--vocab-size -v int 100
        Number of words in limited grammar dictionary
    
    :--lines -li int 10
        lines to train on
    
    :--iterations -i int 1000
        Number of iterations to train the model
'''


def main():
    args = create_parser(usage).parse_args()

    print('Loading json data...')
    with open(args.data_json) as f:
        conversations = json.load(f)

    print('Creating empty model...')
    model = Model(args.vocab_size, args.latent_len)

    try:
        model.train((j for i in conversations for j in i), args.vocab_size, args.iterations,
                    args.lines)
    finally:
        model.save(args.model_json)
        for i in range(10):
            print(' '.join(model.walk(10)))


if __name__ == '__main__':
    main()
