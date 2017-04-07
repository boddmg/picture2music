#coding=gb18030
import mxnet as mx
import numpy as np
import random
import bisect
# set up logging
import logging
reload(logging)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')


from lstm import lstm_unroll, lstm_inference_symbol
from bucket_io import BucketSentenceIter
from rnn_model import LSTMInferenceModel
# Read from doc
def read_content(path):
    with open(path) as ins:
        content = ins.read().decode('gb18030')
        return content

# Build a vocabulary of what char we have in the content
def build_vocab(path):
    content = read_content(path)
    content = list(content)
    idx = 1 # 0 is left for zero-padding
    the_vocab = {}
    for word in content:
        if len(word) == 0:
            continue
        if not word in the_vocab:
            the_vocab[word] = idx
            idx += 1
    return the_vocab

# We will assign each char with a special numerical id
def text2id(sentence, the_vocab):
    words_before = list(sentence)
    words = []
    for w in words_before:
        words.append(the_vocab[w])
    return words
# Evaluation
def Perplexity(label, pred):
    label = label.T.reshape((-1,))
    loss = 0.
    for i in range(pred.shape[0]):
        loss += -np.log(max(1e-10, pred[i][int(label[i])]))
    return np.exp(loss / label.size)
# The batch size for training
batch_size = 32
# We can support various length input
# For this problem, we cut each input sentence to length of 129
# So we only need fix length bucket
buckets = [150]
# hidden unit in LSTM cell
num_hidden = 1024
# embedding dimension, which is, map a char to a 256 dim vector
num_embed = 256
# number of lstm layer
num_lstm_layer = 4
# we will show a quick demo in 2 epoch
# and we will see result by training 75 epoch
num_epoch = 100
# learning rate
learning_rate = 0.01
# we will use pure sgd without momentum
momentum = 0.1
# we can select multi-gpu for training
# for this demo we only use one
devs = [mx.context.gpu(i) for i in range(1)]

# build char vocabluary from input
vocab = build_vocab("./gulong.txt")


# generate symbol for a length
def sym_gen(seq_len):
    return lstm_unroll(num_lstm_layer, seq_len, len(vocab) + 1,
                       num_hidden=num_hidden, num_embed=num_embed,
                       num_label=len(vocab) + 1, dropout=0.2)

# initalize states for LSTM
init_c = [('l%d_init_c'%l, (batch_size, num_hidden)) for l in range(num_lstm_layer)]
init_h = [('l%d_init_h'%l, (batch_size, num_hidden)) for l in range(num_lstm_layer)]
init_states = init_c + init_h

# we can build an iterator for text
data_train = BucketSentenceIter("./gulong.txt", vocab, buckets, batch_size,
                                init_states, seperate_char='\n',
                                text2id=text2id, read_content=read_content)
# the network symbol
symbol = sym_gen(buckets[0])

# Train a LSTM network as simple as feedforward network
model = mx.model.FeedForward(ctx=devs,
                             symbol=symbol,
                             num_epoch=num_epoch,
                             learning_rate=learning_rate,
                             momentum=momentum,
                             wd=0.0001,
                             initializer=mx.init.Xavier(factor_type="in", magnitude=2.34))
# _, arg_params, __ = mx.model.load_checkpoint("model", 40)
# model.arg_params = arg_params
# Fit
# model.fit(X=data_train,
#           eval_metric = mx.metric.np(Perplexity),
#           batch_end_callback=mx.callback.Speedometer(batch_size, 50),
#           epoch_end_callback=mx.callback.do_checkpoint("model"))

# helper strcuture for prediction
def MakeRevertVocab(vocab):
    dic = {}
    for k, v in vocab.items():
        dic[v] = k
    return dic

# make input from char
def MakeInput(char, vocab, arr):
    idx = vocab[char]
    tmp = np.zeros((1,))
    tmp[0] = idx
    arr[:] = tmp

# helper function for random sample
def _cdf(weights):
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

def _choice(population, weights):
    assert len(population) == len(weights)
    cdf_vals = _cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)
    return population[idx]

# we can use random output or fixed output by choosing largest probability
def MakeOutput(prob, vocab, sample=False, temperature=1.):
    if sample == False:
        idx = np.argmax(prob, axis=1)[0]
    else:
        fix_dict = [""] + [vocab[i] for i in range(1, len(vocab) + 1)]
        scale_prob = np.clip(prob, 1e-6, 1 - 1e-6)
        rescale = np.exp(np.log(scale_prob) / temperature)
        rescale[:] /= rescale.sum()
        return _choice(fix_dict, rescale[0, :])
    try:
        char = vocab[idx]
    except:
        char = ''
    return char

# load from check-point
_, arg_params, __ = mx.model.load_checkpoint("model", 40)

# build an inference model
model = LSTMInferenceModel(num_lstm_layer, len(vocab) + 1,
                           num_hidden=num_hidden, num_embed=num_embed,
                           num_label=len(vocab) + 1, arg_params=arg_params, ctx=mx.gpu(), dropout=0.2)

# generate a sequence of 1200 chars

seq_length = 1200
input_ndarray = mx.nd.zeros((1,))
revert_vocab = MakeRevertVocab(vocab)
# Feel free to change the starter sentence
output ="客松为云空间的黑客马拉松活动，本次事主题为智慧城市生活服务及人文关怀体验，将于月日早晨，以拜单车别样的户外方式开始。并在接下来二十四小时内，疯狂头脑风暴、设计和编码，创造自己的作品。欢迎设计师、产品经理、开发者们来参体验，超级大奖等待着最优秀的客团队。本次黑客马拉松由团队特别支持".decode("gb18030")
random_sample = True
new_sentence = True

ignore_length = len(output)

print(vocab)

for i in range(seq_length):
    if i <= ignore_length - 1:
        MakeInput(output[i], vocab, input_ndarray)
    else:
        MakeInput(output[-1], vocab, input_ndarray)
    prob = model.forward(input_ndarray, new_sentence)
    new_sentence = False
    next_char = MakeOutput(prob, revert_vocab, random_sample)
    if next_char == '':
        new_sentence = True
    if i >= ignore_length - 1:
        output += next_char

print(output)

