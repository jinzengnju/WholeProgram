#!/usr/bin/python
# -*- coding:UTF-8 -*-
# .meta文件保存了当前图结构
# .index文件保存了当前参数名
# .data文件保存了当前参数值
# https://www.cnblogs.com/hellcat/p/6925757.html
# https://blog.csdn.net/huachao1001/article/details/78501928
# http://www.voidcn.com/article/p-faybcfqu-bqu.html
# https://blog.csdn.net/sinat_34474705/article/details/78995196
import re
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import tensorflow as tf
from Model.data_utils import *
from Model.model import Model
import json
import os
import yaml
from gensim.models import Word2Vec

tf.app.flags.DEFINE_string("ckpt_dir","checkpoints","Directory to save the model checkpoints")
tf.app.flags.DEFINE_string("vocab_dict","checkpoints","Directory to save the model checkpoints")
tf.app.flags.DEFINE_string("w2v_model","checkpoints","Directory to save the model checkpoints")
tf.app.flags.DEFINE_integer("num_classes","2"," ")
tf.app.flags.DEFINE_string("lda_model","checkpoints","Directory to save the model checkpoints")
tf.app.flags.DEFINE_string("lda_vocab","checkpoints","Directory to save the model checkpoints")
tf.app.flags.DEFINE_float("max_gradient_norm",5.0,"Clip gradients to this norm")
tf.app.flags.DEFINE_integer("batch_size",64,"Batch size to use during training")
tf.app.flags.DEFINE_integer("num_hidden_units",300,"Number of hidden units in each RNN unit")
tf.app.flags.DEFINE_integer("num_layers",2,"NUmber of layers in the model")
tf.app.flags.DEFINE_float("dropout",0.5,"Amount to drop during training")
tf.app.flags.DEFINE_integer("en_vocab_size",10000,"English vocabulary size")
tf.app.flags.DEFINE_integer("pos_weight",3400,'')
tf.app.flags.DEFINE_integer("embedding_size","150",'')

FLAGS=tf.app.flags.FLAGS

def get_EmbeddingMatrix(sorted_word):
    model=Word2Vec.load(FLAGS.w2v_model)
    embedding_matrix=np.random.randn(FLAGS.en_vocab_size,FLAGS.embedding_size)
    for word,index in sorted_word.items():
        try:
            embedding_vector=model[word]
            embedding_matrix[index]=embedding_vector
        except KeyError:
            embedding_vector=embedding_matrix[3]
            embedding_matrix[index]=embedding_vector
    return embedding_matrix

def get_topicVector(dictionary,batch_context,lda):
    batch_text = []
    for text in batch_context:
        #text=bytes.decode(text)
        text = re.sub('[^(\\u4e00-\\u9fa5)]', '', text)
        text = re.sub('(?i)[^a-zA-Z0-9\u4E00-\u9FA5]', '', text)
        batch_text.append([word for word in jieba.cut(text) if len(word) > 1])
    other_corpus = [dictionary.doc2bow(text) for text in batch_text]
    topic_vector=[]
    for temp in other_corpus:
        temp_vector=lda[temp]
        topic_vector.append([list(t) for t in zip(*temp_vector)][1])
    return np.array(topic_vector)


def create_model(sess,FLAGS,embedding_matrix):
    text_model=Model(FLAGS,embedding_matrix)
    ckpt=tf.train.get_checkpoint_state(FLAGS.ckpt_dir)
    if ckpt and ckpt.model_checkpoint_path:
        print("Restoring old model parameters from %s"%ckpt.model_checkpoint_path)
        text_model.saver.restore(sess,ckpt.model_checkpoint_path)
    return text_model

def build_graph():
    traincofig = TrainConfig()
    preprocess = PreProcess(traincofig)
    vocab_dict = preprocess.before_train()
    lda = LdaModel.load(FLAGS.lda_model)
    dictionary = Dictionary.load(FLAGS.lda_vocab)
    lda.__setattr__("minimum_probability", 0)
    embedding_matrix = get_EmbeddingMatrix(vocab_dict)
    # 模型的y中有用到placeholder，在sess.run()
    # 的时候肯定要feed对应的数据，因此还要根据具体placeholder的名字，从graph中使用get_operation_by_name方法获取。
    with tf.Graph().as_default():
        sess=tf.Session()
        model = create_model(sess, FLAGS, embedding_matrix)
    return model,sess,lda,dictionary,vocab_dict

def predict(model,sess,message,dictionary,lda,vocab_dict):
    train_fact_v=[]
    train_fact_v.append(message)
    train_law_v=[[]]
    train_topic_vector=get_topicVector(dictionary, train_fact_v, lda)
    train_fact_val,train_seq_lens=get_X_with_word_index(train_fact_v,vocab_dict,1000)
    valid_predict = model.step(sess, train_fact_val, train_seq_lens, train_law_v,
                                                          train_topic_vector, dropout=1.0,
                                                                forward_only=True)
    result=valid_predict[1]
    return result[0]

class TrainConfig:
    def __init__(self):
        path=os.path.abspath('.')
        f = open(os.path.join(path,'Model\config.yaml'), encoding='utf-8')
        self.configs_dict = yaml.load(f)
    def get(self,name):
        return self.configs_dict.get(name)

class PreProcess:
    def __init__(self,trainconfig):
        FLAGS.ckpt_dir=trainconfig.get("ckpt_dir")
        FLAGS.w2v_model=trainconfig.get("w2v_model")
        FLAGS.vocab_dict=trainconfig.get("vocab_dict")
        FLAGS.lda_model=trainconfig.get("lda_model")
        FLAGS.lda_vocab=trainconfig.get("lda_vocab")
        FLAGS.max_gradient_norm = trainconfig.get("max_gradient_norm")
        FLAGS.batch_size = trainconfig.get("batch_size")
        FLAGS.num_hidden_units = trainconfig.get("num_hidden_units")
        FLAGS.num_layers = trainconfig.get("num_layers")
        FLAGS.dropout = trainconfig.get("dropout")
        FLAGS.en_vocab_size = trainconfig.get("en_vocab_size")
        FLAGS.pos_weight = trainconfig.get("pos_weight")
        FLAGS.embedding_size = trainconfig.get("embedding_size")
    def before_train(self):
        law_num = getClassNum("law")
        FLAGS.num_classes=law_num
        f_read1 = open(FLAGS.vocab_dict, 'r',encoding='utf-8')
        vocab_dict = json.load(f_read1)
        f_read1.close()
        return vocab_dict

if __name__=='__main__':    
    model, sess, lda, dictionary, vocab_dict = build_graph()
    fin=open("D:\WorkFile\竞赛\cail_0518\data_test.json",'r',encoding='utf8')
    line=fin.readline()
    while line:
        d=json.loads(line)
        message=d['fact']
        res = predict(model, sess, message, dictionary, lda, vocab_dict)
        print("推荐结果：")
        print(res)
        print("真实：")
        print([law[str(e)] for e in d['meta']['relevant_articles']])
        line=fin.readline()