import argparse
import tensorflow as tf

CONFIG_GENERAL = ['cell', 'latent_size', 'batch_size', 'weight_loss', 'num_epochs', \
                 'learning_rate', 'print_step']
CONFIG_ENCODER = ['name', 'max_num', 'max_length', 'rnn_units', 'tile', 'pretrained_embed']
CONFIG_DECODER = ['rnn_units', 'max_ast_depth']
CONFIG_CHARS_VOCAB = ['chars', 'vocab', 'vocab_size']

C0 = 'CLASS0'
UNK = '_UNK_'
CHILD_EDGE = 'V'
SIBLING_EDGE = 'H'

def length(tensor):
    elems = tf.sign(tf.reduce_max(tensor, axis=2))
    return tf.reduce_sum(elems, axis=1)

import bayou.core.evidence

# convert JSON to config
def read_config(js, clargs):
    config = argparse.Namespace()

    for attr in CONFIG_GENERAL:
        config.__setattr__(attr, js[attr])
    
    config.evidence = bayou.core.evidence.Evidence.read_config(js['evidence'], clargs)

    attrs = CONFIG_DECODER + (CONFIG_CHARS_VOCAB if clargs.continue_from else [])
    config.decoder = argparse.Namespace()
    for attr in attrs:
        config.decoder.__setattr__(attr, js['decoder'][attr])

    return config

# convert config to JSON
def dump_config(config):
    js = {}

    for attr in CONFIG_GENERAL:
        js[attr] = config.__getattribute__(attr)

    js['evidence'] = [ev.dump_config() for ev in config.evidence]

    attrs = CONFIG_DECODER + CONFIG_CHARS_VOCAB
    js['decoder'] = { attr: config.decoder.__getattribute__(attr) for attr in attrs }

    return js