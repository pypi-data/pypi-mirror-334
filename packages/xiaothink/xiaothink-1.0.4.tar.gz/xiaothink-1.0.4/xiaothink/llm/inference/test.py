import tensorflow as tf
import time
import numpy as np
import os
import time
try:from build_model import *
except ImportError:
    from xiaothink.llm.inference.build_model import *

from tensorflow.keras.layers import Input, Embedding, GRU, Dense, Dropout  
from tensorflow.keras.models import Model  
from tensorflow.keras.layers import Multiply,Attention
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import LayerNormalization
from tensorflow.keras.layers import Add,MultiHeadAttention
import gc
def ct():
    gc.collect()
#tf.config.run_functions_eagerly(True)

from tensorflow.keras.layers import Embedding, GRU, Dropout, Dense, AdditiveAttention, LayerNormalization

dic={
40.231:[int(1024),{'rnn_units':int(2048),'embed_q':0.6,}, 128],#512],#推理时需要500M内存
40.23101:[int(512),{'rnn_units':int(512), 'embed_q':0.4,}, 512],

40.31:[int(512),{'rnn_units':int(512), 'embed_q':0.4,'router_units':256,'n_layer':1,
            'maxlen':130,'trans_layers':5,'dff_factor':4,'trans_window':100}, 256],#1200#512

40.3101:[int(128),{'rnn_units':int(128), 'embed_q':0.4,'router_units':64,'n_layer':1,
            'maxlen':130,'trans_layers':3,'dff_factor':2,'trans_window':100}, 128],#1200#512
40.31666:[int(512),{'rnn_units':int(512), 'embed_q':0.4,'router_units':256,'n_layer':1,
            'maxlen':130,'trans_layers':5,'dff_factor':4,'trans_window':100}, 1200],#1200#512

}

import tensorflow as tf
from tensorflow.keras import layers




ms=0
def load(ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_novel_en',
         vocab=r'E:\小思框架\论文\ganskchat\vocab_lx4.txt',
         BATCH_SIZE = 1,
         model_type=3,
         print_out=True,
         ):
    global dic, ms
    with open(vocab,'r',encoding='utf-8') as f:
        vocab=eval(f.read())
    char2idx = {u:i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)
    
    # 词集的长度
    vocab_size = len(vocab)
    '''
    dic={1:[int(256*4*2*0.7),int(1024*4*2*0.7),512],
         2:[int(1024*2*1),int(1024*4*2),128],
         2.2:[int(1024*2*1),int(1024*4*2),128],
         3:[int(512),int(1024),128],
         2.3:[int(1024*2*1),int(1024*3),128],
         0.1:[128,256,32],
         0.2:[1024,int(1024*5.5),128],
         0.01:[512,int(1024*2.5),128],
         0.02:[int(1024*1),int(1024*4*2.75),128],
         0.022:[int(1024*9),int(1024*4*1.2),128],
         0.023:[int(1024*16),int(1024*4*0.55),128],
         0.024:[int(1024*16),int(1024*4*0.6),64],
         0.025:[int(1024*16),int(1024*4*0.6),64],
         0.0252:[int(1024*16),int(1024*4*0.6),64],
         0.0253:[int(1024*16),int(1024*4*0.6),64],
         0.0254:[int(1024*5),int(1024*2),64],#int(1024*2.414),64],
         0.0255:[int(1024*5),int(1024*2),64],
         }
    '''

    seq_length=dic[model_type][2]
    
    # 嵌入的维度
    embedding_dim = dic[model_type][0]

    # RNN 的单元数量
    rnn_units = dic[model_type][1]
    window= dic[model_type][2]
    
    checkpoint_dir=ckpt_dir

    checkpoint_path = tf.train.latest_checkpoint(checkpoint_dir)



    # 假设 build_model 是一个定义并返回模型的函数
    model = build_model(vocab_size, embedding_dim, rnn_units, batch_size=BATCH_SIZE,
                        mt=model_type,window=window)
    try:
        if print_out:model.summary()
    except:
        ms=1
        if print_out:print('Model Summary Error')
    
    if print_out:print(checkpoint_path)
    # 直接加载权重到模型中
    model.load_weights(checkpoint_path)
    
    return model,[char2idx,idx2char]



# 评估步骤（用学习过的模型生成文本）
#@tf.function
def generate_texts(model,
                   vocabdata,
                  start_string,
                  num_generate = 512,
                  temperature = 0.6,
                  every=None,#每写一个字执行的函数
                  pass_char=[],
                  ):
  t1=time.time()
  char2idx,idx2char=vocabdata[0],vocabdata[1]
  
  # 将起始字符串转换为数字（向量化）
  input_eval = tf.convert_to_tensor([int(char2idx.get(s, char2idx['▩'])) for s in start_string], dtype=tf.int32)
  input_eval = tf.expand_dims(input_eval, 0)

  # 空字符串用于存储结果
  text_generated = []

  # 低温度会生成更可预测的文本
  # 较高温度会生成更令人惊讶的文本
  # 可以通过试验以找到最好的设定
  #print(input_eval.shape)

  # 这里批大小为 1
  try:model.reset_states()
  except:print('model rest error')
  #cnt=0
  f=1
  for i in range(num_generate):
      
      predictions = model.predict(input_eval,verbose=0)#model(input_eval)#model.predict(input_eval,verbose=0)
      # 删除批次的维度
      predictions = tf.squeeze(predictions, 0)

      # 用分类分布预测模型返回的字符
      predictions = predictions / temperature
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
      while idx2char[predicted_id] in pass_char:
                predictions = model.predict(input_eval,verbose=0)#model(input_eval)#model.predict(input_eval,verbose=0)
                # 删除批次的维度
                predictions = tf.squeeze(predictions, 0)

                # 用分类分布预测模型返回的字符
                predictions = predictions / temperature
                predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()



      input_eval = tf.expand_dims([predicted_id], 0)
      text_generated.append(idx2char[predicted_id])
      if every!= None:every(idx2char[predicted_id])
      
      
      '''
      cnt+=1
      if time.time()-t1>1 and f:
          print(time.time()-t1,cnt)
          f=0
      '''
          
      '''
      # 把预测字符和前面的隐藏状态一起传递给模型作为下一个输入
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])
      if every!= None:every(idx2char[predicted_id])
      '''
  del model,vocabdata
  ct()
  return ''.join(text_generated)#(start_string + ''.join(text_generated))


def generate_texts_untilstr(model,
                   vocabdata,
                  start_string,
                  num_generate = 512,
                  temperature = 0.6,
                  every=None,#每写一个字执行的函数
                  stop_c='\n问：',
                  ):
  #print('every',every)
  char2idx,idx2char=vocabdata[0],vocabdata[1]
  
  # 将起始字符串转换为数字（向量化）
  input_eval = [char2idx[s] for s in start_string]
  input_eval = tf.expand_dims(input_eval, 0)

  # 空字符串用于存储结果
  text_generated = []

  # 低温度会生成更可预测的文本
  # 较高温度会生成更令人惊讶的文本
  # 可以通过试验以找到最好的设定
  #print(input_eval.shape)

  # 这里批大小为 1
  try:model.reset_states()
  except:print('model rest error')
  for i in range(num_generate):
      
      predictions = model.predict(input_eval,verbose=0)#model(input_eval)#model.predict(input_eval,verbose=0)
      # 删除批次的维度
      predictions = tf.squeeze(predictions, 0)

      # 用分类分布预测模型返回的字符
      predictions = predictions / temperature
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

      if 1:#not idx2char[predicted_id] in ['，','。']:
          input_eval = tf.expand_dims([predicted_id], 0)
          text_generated.append(idx2char[predicted_id])
          if every!= None:every(idx2char[predicted_id])
      if type(stop_c)==str:
          if stop_c in ''.join(text_generated):
              return ''.join(text_generated)[:-len(stop_c)]
      elif type(stop_c)==list:
          for ii in stop_c:
              if ii in ''.join(text_generated):
                  return ''.join(text_generated)[:-len(ii)]
      '''
      # 把预测字符和前面的隐藏状态一起传递给模型作为下一个输入
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])
      if every!= None:every(idx2char[predicted_id])
      '''
  del model,vocabdata
  ct()
  return ''.join(text_generated)#(start_string + ''.join(text_generated))


'''
def generate_texts_batch(model,
                         vocabdata,
                         start_strings,
                         num_generate = 512,
                         temperature = 0.6,
                         every=None,
                         batch_size=1):
    char2idx, idx2char = vocabdata[0], vocabdata[1]

    # 将所有起始字符串转换为数字（向量化）
    input_evals = [[char2idx[s] for s in start_str] for start_str in start_strings]
    input_evals = tf.keras.preprocessing.sequence.pad_sequences(input_evals, maxlen=num_generate, padding='pre')
    input_evals = tf.expand_dims(input_evals, axis=1)

    # 初始化存储结果的列表
    text_generated = [[] for _ in start_strings]

    model.reset_states()
    for i in range(num_generate):
        # 对整个批次进行预测
        predictions = model.predict(input_evals[:, :i, :], verbose=0)

        # 平滑分布并抽样
        predictions /= temperature
        predicted_ids = tf.random.categorical(predictions, num_samples=1)
        predicted_ids = tf.squeeze(predicted_ids, axis=-1).numpy()

        # 更新每个起始字符串对应的生成序列
        for j in range(len(start_strings)):
            text_generated[j].append(idx2char[predicted_ids[j]])

            if every is not None and (i % batch_size == 0 or i == num_generate - 1):
                every(idx2char[predicted_ids[j]], start_strings[j])

        # 将预测字符添加到下一轮输入
        input_evals = tf.concat([input_evals[:, i:i+1], tf.expand_dims(predicted_ids, axis=1)], axis=1)

    return [start_str + ''.join(text_seq) for start_str, text_seq in zip(start_strings, text_generated)]
'''


def generate_texts_faster(model, vocabdata, start_string,
                          num_generate=512, temperature=0.6,
                          every=None, utf=False, rest=True):
    char2idx, idx2char = vocabdata
    input_eval = tf.convert_to_tensor([int(char2idx.get(s, char2idx['▩'])) for s in start_string], dtype=tf.int32)
    input_eval = tf.expand_dims(input_eval, 0)

    # 预分配内存以提升效率
    text_generated = np.empty(num_generate, dtype=np.int32)

    if rest:model.reset_states()

    for i in range(num_generate):
        # 获取预测
        predictions = model.predict(input_eval, verbose=0)
        predictions = tf.squeeze(predictions, 0)

        # 用分类分布预测模型返回的字符
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        # 更新input_eval 和 text_generated
        input_eval = tf.expand_dims([predicted_id], 0)
        text_generated[i] = predicted_id

        # 如果需要，执行外部函数
        if every is not None:
            every(idx2char[predicted_id])

    # 转换为字符串并拼接起始字符串
    return ''.join(idx2char[text_generated.tolist()])



def generate_texts_np(model,
                   vocabdata,
                   start_string,
                   num_generate=512,
                   top_n=1,  # 选取概率最高的前n个字符
                   every=None):  # 每写一个字执行的函数
    char2idx, idx2char = vocabdata[0], vocabdata[1]

    # 将起始字符串转换为数字（向量化）
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # 空字符串用于存储结果
    text_generated = []

    # 这里批大小为 1
    #model.reset_states()
    for i in range(num_generate):
        predictions = model.predict(input_eval, verbose=0)
        # 删除批次的维度
        predictions = tf.squeeze(predictions, 0)

        # 找到概率最高的前n个预测
        top_n_probs, top_n_indices = tf.nn.top_k(predictions, k=top_n)
        # 从最高的n个预测中随机选择一个
        predicted_id = np.random.choice(top_n_indices.numpy()[0])

        # 把预测字符和前面的隐藏状态一起传递给模型作为下一个输入
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])
        if every is not None:
            every(idx2char[predicted_id])

    return start_string + ''.join(text_generated)


# 评估步骤（用学习过的模型生成文本）
@tf.function
def generate_texts_fast_core(model,
                   vocabdata,
                  start_string,
                  num_generate = 512,
                  temperature = 1.0,
                  every=None,#每写一个字执行的函数
                  ):
  char2idx,idx2char=vocabdata[0],vocabdata[1]
  
  # 将起始字符串转换为数字（向量化）
  input_eval = [char2idx[s] for s in start_string]
  input_eval = tf.expand_dims(input_eval, 0)
  #print('ie',input_eval)
  # 空字符串用于存储结果
  text_generated = []

  # 低温度会生成更可预测的文本
  # 较高温度会生成更令人惊讶的文本
  # 可以通过试验以找到最好的设定
  

  # 这里批大小为 1
  model.reset_states()
  for i in range(num_generate):
      
      predictions = model(input_eval)
      # 删除批次的维度
      try:
          predictions = tf.squeeze(predictions, 0)

          # 用分类分布预测模型返回的字符
          '''
          predictions = predictions / temperature
          predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
            '''
          predicted_id = tf.random.categorical(predictions / temperature, num_samples=1)[0, 0]
      except tf.python.framework.errors_impl.InvalidArgumentError:
          predictions = tf.expand_dims(predictions, axis=0) 
          predicted_id = tf.random.categorical(predictions / temperature, num_samples=1)[0, 0]

      # 把预测字符和前面的隐藏状态一起传递给模型作为下一个输入
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])
      if every!= None:every(idx2char[predicted_id])

  del model, vocabdata
  return text_generated


def generate_texts_fast(model,
                   vocabdata,
                  start_string,
                  num_generate = 512,
                  temperature =1.0,
                  every=None,#每写一个字执行的函数
                  ret_ori=True):
    li=generate_texts_fast_core(model=model,
                   vocabdata= vocabdata,
                  start_string=start_string,
                  num_generate = num_generate ,
                  temperature = temperature,
                  every=every,
                  )
    str_=''
    for i in li:
        str_+=i.numpy().decode('utf-8')
    del model, vocabdata
    if ret_ori:return (start_string + str_)
    else:return str_

def generate_texts_add(model,
                       model2,
                   vocabdata,
                  start_string,
                  num_generate = 512,
                  temperature = 0.6,
                  every=None,#每写一个字执行的函数
                       q=[0.5,0.5],
                  ):
  q1,q2=q
  char2idx,idx2char=vocabdata[0],vocabdata[1]
  
  # 将起始字符串转换为数字（向量化）
  input_eval = [char2idx[s] for s in start_string]
  input_eval = tf.expand_dims(input_eval, 0)

  # 空字符串用于存储结果
  text_generated = []

  # 低温度会生成更可预测的文本
  # 较高温度会生成更令人惊讶的文本
  # 可以通过试验以找到最好的设定
  #print(input_eval.shape)

  # 这里批大小为 1
  #model.reset_states()
  for i in range(num_generate):
      
      predictions = model(input_eval)*q1+model2(input_eval)*q2#model.predict(input_eval,verbose=0)
      # 删除批次的维度
      predictions = tf.squeeze(predictions, 0)

      # 用分类分布预测模型返回的字符
      predictions = predictions / temperature
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

      if 1:#not idx2char[predicted_id] in ['，','。']:
          input_eval = tf.expand_dims([predicted_id], 0)
          text_generated.append(idx2char[predicted_id])
          if every!= None:every(idx2char[predicted_id])
      '''
      # 把预测字符和前面的隐藏状态一起传递给模型作为下一个输入
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])
      if every!= None:every(idx2char[predicted_id])
      '''
  del model,vocabdata
  ct()
  return ''.join(text_generated)#(start_string + ''.join(text_generated))


def generate_texts_mask(model,
                       model2,
                   vocabdata,
                  start_string,
                  num_generate = 512,
                  temperature = 0.6,
                  every=None,#每写一个字执行的函数
                       #q=[0.5,0.5],
                  ):
  #q1,q2=q
  char2idx,idx2char=vocabdata[0],vocabdata[1]
  
  # 将起始字符串转换为数字（向量化）
  input_eval = [char2idx[s] for s in start_string]
  input_eval = tf.expand_dims(input_eval, 0)

  # 空字符串用于存储结果
  text_generated = []

  # 低温度会生成更可预测的文本
  # 较高温度会生成更令人惊讶的文本
  # 可以通过试验以找到最好的设定
  #print(input_eval.shape)

  # 这里批大小为 1
  #model.reset_states()
  for i in range(num_generate):
      mean=np.mean((model2(input_eval)))
      predictions = (model(input_eval))#model.predict(input_eval,verbose=0)
      predictions2=predictions
      
      # 创建一个布尔数组，其中matrix中的元素大于threshold的位置为True，否则为False
      bool_mask = predictions2 > mean*0.

      # 使用布尔数组对matrix进行索引，并将True位置的值设为1，False位置的值设为0
      booln = np.where(bool_mask, 1, 0)

      predictions+=mean*booln
      #print(predictions)

      
      # 删除批次的维度
      predictions = tf.squeeze(predictions, 0)

      # 用分类分布预测模型返回的字符
      predictions = predictions / temperature
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

      if 1:#not idx2char[predicted_id] in ['，','。']:
          input_eval = tf.expand_dims([predicted_id], 0)
          text_generated.append(idx2char[predicted_id])
          if every!= None:every(idx2char[predicted_id])
      '''
      # 把预测字符和前面的隐藏状态一起传递给模型作为下一个输入
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])
      if every!= None:every(idx2char[predicted_id])
      '''
  del model,vocabdata
  ct()
  return ''.join(text_generated)#(start_string + ''.join(text_generated))


def fill(inp,n,pad_char=' ',cut=False):
    if len(inp)>=n:
        if not cut:return inp
        else:
            return inp[-n:]
    elif len(inp)<n:
        return pad_char*(n-len(inp))+inp

def generate_texts_loop(m, d, inp_m, num_generate=100,
                             every=lambda a:print(a,end='',flush=True),
                             temperature=0.7,#0.5#0.8
                       window=128,
                       pass_char=['▩']
                             ):
    out=''
    for i in range(num_generate):
          out+=generate_texts(m, d, fill(inp_m+out,window,cut=True),num_generate=1,
                             every=every,
                             temperature=temperature,#0.5#0.8
                             pass_char=pass_char
                       #      utf=False,
                               #q=[0.6,0.4]
                       #     rest=False,
                                )
    return out

def generate_texts_untilstr_loop(model,
                   vocabdata,
                  start_string,
                  num_generate = 512,
                  temperature = 0.6,
                  every=None,#每写一个字执行的函数
                  stop_c='\n问：',
                  window=128,
                  pass_char=[],
                  ):
  #print('every',every)
  char2idx,idx2char=vocabdata[0],vocabdata[1]
  
  # 将起始字符串转换为数字（向量化）
  input_eval = [char2idx[s] for s in start_string]
  input_eval = tf.expand_dims(input_eval, 0)

  # 空字符串用于存储结果
  text_generated = list(start_string)#[]
  ou=[]
  # 低温度会生成更可预测的文本
  # 较高温度会生成更令人惊讶的文本
  # 可以通过试验以找到最好的设定
  #print(input_eval.shape)

  # 这里批大小为 1
  try:model.reset_states()
  except:print('model rest error')
  for i in range(num_generate):
      

      g=generate_texts(model, vocabdata, fill(''.join(text_generated),window,
                                              cut=True),num_generate=1,
                             every=every,
                             temperature=temperature,#0.5#0.8
                       pass_char=pass_char,
                       #      utf=False,
                               #q=[0.6,0.4]
                       #     rest=False,
                                )
      if 1:#not idx2char[predicted_id] in ['，','。']:
          
          text_generated.append(g)
          ou.append(g)
          
      #if every!= None:every(idx2char[predicted_id])
      if type(stop_c)==str:
          if stop_c in ''.join(ou):
              return ''.join(ou)[:-len(stop_c)]
      elif type(stop_c)==list:
          for ii in stop_c:
              if ii in ''.join(ou):
                  return ''.join(ou)[:-len(ii)]
      '''
      # 把预测字符和前面的隐藏状态一起传递给模型作为下一个输入
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])
      if every!= None:every(idx2char[predicted_id])
      '''
  del model,vocabdata
  ct()
  return ''.join(ou)#(start_string + ''.join(text_generated))


      
import numpy as np

if __name__=='__main__' and 0:
    m,d=load(ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_chat')
    aa,bb=0,0
    for i in range(10):
        print(i)
        t1=time.time()
        generate_texts(m,d,'hello! I ',num_generate=10)
        aa+=(time.time()-t1)
    for i in range(10):
        print(i)
        t1=time.time()
        generate_texts_fast(m,d,'hello! I ',num_generate=10)
        bb+=(time.time()-t1)
    print(aa,bb)
elif __name__=='__main__':
  if 1:
      #import moti.run_text as rt
      
      MT=40.231#20.4121#0.01#20.35
      m,d=load(ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_test_40_2_3_1_formal_open',#ckpt_test_20_4121',#r'E:\小思框架\论文\ganskchat\ckpt_novel_zh_mini_t2_chat',
               model_type=MT,
               vocab=r'E:\小思框架\论文\ganskchat\vocab_lx3.txt',
               
               )#(ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_novel_en_2.2',model_type=2.2)
      #m2,d=load(ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_formal_zh_mini_t1',#r'E:\小思框架\论文\ganskchat\ckpt_formal_zh_common_t3_0255',
      #         model_type=0.01)
      
      hlm='一语未了，只听后院中有人笑声，说：“我来迟了，不曾迎接远客!”黛玉纳罕道：“这些人个个皆 敛声屏气，恭肃严整如此，这来者系谁，这样放诞无礼?”心下想时，只见一群媳妇丫鬟围拥着一个人从后房门进来。这个人'
      yw='她声线原本偏软，此时却染上了一抹沙哑，意外的有种'
      yw2='一语未了，只听后院中有人笑声，说：“'
      yw_en='Dave Darrin \'s Second Year At Annapolis\n\nOr\n\nTwo Midshipmen As Naval Academy " Youngsters "\n\nBy\n\nH. Irving Hancock\n\n\n\nChapter I\n\nA'
      wen='你是谁？\n'#'你吃了吗？'#'杨大哥，你在干什么？'
      quest=f'南枝问道：“{wen}\n”\n    杨大哥说到：“'
      chat='你好！\r\n'#'不知可否作曲一首？\n'
      json='{"prompt": "二氧化碳有害吗？", "answer": "'
      mpt='{"prompt": "我想买一辆新汽车，请问燃油车和电动车哪个好一些？", "answer": "'
      luxun='人。这草\r\r\n案的深意就在这里：叫民众看见是民权，而民族祖宗看见是忠\r\r\n孝——忠于固有科举的民族，孝于制定科举的祖宗。此外，像\r\r\n上海已经实现的民权，是 纳税的方有权选举和被选，使偌大上\r\r\n海只剩四千四百六十五个大市民。这虽是捐班——有钱的\r\r\n为主，然'
      xyj='   诗曰：\n\n    混沌未分天地乱，茫茫渺渺无人见。\n\n    自从盘古破鸿蒙，开辟从兹清浊辨。\n\n    覆载群生仰至仁，发'
      novel='的房间，相宜清醒过来时，听到了一个低沉戏谑的男声。\r\n\r\n\xa0\xa0\xa0\xa0大脑一片眩晕，她眯着眼睛打量周围环境。\r\n\r\n\xa0\xa0\xa0\xa0大约是酒店'
      rzb='{\n    "instruction": "只剩一个心脏了还能活吗？",\n    "output": "'
      dldl='就不懂了吧。\n快说拉，为什么啊\n水系的女孩子很多哦，基本上没有什么男生，我可以欺负她们，还可以抢她们的好吃的，嘿嘿\n这么小你就这么坏啊，我回去告诉你爸。\n 你也和我学水系吧\n不了，你只要以后把弄来的好吃的分我一点我就不告诉你爸，好不好\n好，没问题，谁叫咱们好呢\n到学校了，快跑，要迟到拉\n还好没迟到，要不老巫婆又要让咱俩罚站了\n别说了，老巫婆来来了。（老巫婆当然就是我们的班主任，50多岁的火系高级魔法师林老师喽，她可是很严厉的，长的又没什么吸引力，所以我们几个要好的小伙伴就给她起了个老巫婆的外号）\n同学们好\n老师'
      '''
      ret=generate_texts_fast(m,d, yw_en,num_generate=10)
      print(len(ret),ret)
      '''
      llama3_zhihu='{"conversation": [{"human": "海洋中为什么使用海里这一单位？对比日常使用的公制单位，海里和节有何便利之处？", "assistant": "'
      aljshn='别哭了，已经十分钟了。\n我难受，今天延长时间。\n\n女人准则，十分钟\n跟你的 妹妹一起滚远点儿！\n\n洛枳，你的电脑开着呢吧，能放段音乐吗？没声音，光我在这里哭好没气氛。\n静物素描\n\n吃了吗，来一口？康师傅，就是这个味儿！\n\n没关系的时候，他已经转身朝付款处走去了。她连他道歉的声音都没听清楚，只是凭逻辑判断那应该是一句对不起\n\n他手指微凉，拂过我手背时有干爽的触觉\n\n鬼打墙\n\n'
      chatbot='你吃苹果吗？\n'#'你什么星座\r\n'#'qq群号：1750555975这是什么群？\n'#'你好\n你好啊\n你叫什么？\n'
      print('loaded')
      en2='Hello! '
      alis='q1:莫妮卡·贝鲁奇的代表作？\r\n\
select ?x where { <莫妮卡·贝鲁奇> <代表作品> ?x. }\r\n<西西里的美丽\
传说>\t\r\n\r\nq2:《湖上草》是谁的诗？\r\nselect ?x where { ?x <主要\
作品> <湖上草>. }\r\n<柳如是_（明末“秦淮八艳”之一）>\t\r\n\r\nq3:龙卷风\
的英文名是什么？\r\nselect ?x where { <龙卷风_（一种自然天气现象）> <外\
文名> ?x. }\r\n"Tornado"\t\r\n\r\nq4:新加坡的水域率是多少？\r\nselect ?x w\
here { '
      alis='q1:莫妮卡·贝鲁奇的代表作？\r\n\
select ?x where { <莫妮卡·贝鲁奇> <代表作品> ?x. }\r\n<西西里的美丽\
传说>\t\r\n\r\nq2:《湖上草》是谁的诗？\r\nselect ?x where { ?x <主要\
作品> <湖上草>. }\r\n<柳如是_（明末“秦淮八艳”之一）>\t\r\n\r\nq3:龙卷风\
的英文名是什么？\r\n'
      belle='{"instruction": "请告诉我如何制作披萨。\n我想学做牛肉披萨。", "input": "", "output": "'
      belle2='{"instruction": "我最近经常感到喉咙痛，尤其是在吞咽时，这是为什么？", "input": "", "output": "'
      novel_2='啧”了声，“你怎么知道我一定会选封口费？\r\n”\r\n\xa0\xa0\xa0\xa0相宜懒得和他废话，报上了一串地址，“想结婚去联系我家管家。\r\n”她声线原本偏软，此时却染上了一抹沙哑，意外的有种让人骨头发软的感觉，“叨扰，借过。\r\n”\r\n\xa0\xa0\xa0\xa0她一把拉开了窗帘，还没来得及侧身避开'
      ad='李九宫北京市回城门那种做那个老大汉做我自己睡觉的时候老大就是一里边修两次来我一来兴趣大做饭现在他给找一个做母做饭的然后我能抽货我也也也会做牛羊动物动物动物是牛羊不累呢叫冬月人老虎四日大象犀牛狗猫鹤马长发鹿四条腿都是中国人长发鹿老虎四日狗熊鹅萝卜韭菜胡萝卜欧香菜白菜原白菜青菜窝瓜嚼瓜南瓜好吃 | '
      sklm1='问：你叫什么？\r\n答：我是清韵千言大模型，有问题欢迎\
问我！\r\n\r\n问：计算152*46\r\n答：调用模型[计算152*46]\r\n返回：结果\
是6992\r\n答：结果是6992\r\n\r\n 问：今天天气怎么样？\r\n答：调用模型[查询\
今天的天气]\r\n返回：今天是晴天，最高温'
      sklm1_chat='问：计算一下179*5428\r\n答：'#'问：计算152*46\r\n答：'#'问：你叫什么？\r\n答：'
      sklm1_tool='问：中国的首都是哪个城市？\r\r\n答：调用模型[中国的首都是哪个城市？]\r\r\n返回：北京\r\r\n\r\r\n问：世界上最高的山是哪座？\r\r\n答：调用模型[世界上最高的山是哪座？]\r\r\n返回：珠穆朗玛峰\r\r\n\r\r\n问：太阳系中最大的行星是什么？\r\r\n答：'
      sklm1_wenyi='''问：“红尘多可笑，痴情最无聊。”可为何，我对你的情意，却如此难以割舍？
答：红尘滚滚，世人皆笑痴，殊不知情之深，爱之切。李清照曾言：“此情无计可消除，才下眉头，却上心头。”情之一字，最是磨人，却也最是动人。你我的情缘，纵使旁人不解，其中甘苦，唯有自知，这份痴情，正是人间最真挚的写照。

问：“众里寻他千百度，蓦然回首，那人却在，灯火阑珊处。”你是否相信，命中注定的相遇？
答：世间万般寻觅，只为那一瞬的回眸。辛弃疾所描绘的那份惊喜与宿命，恰如你我相遇。是的，我信那灯火阑珊处的奇迹，正如我信你我相遇非偶然，一切冥冥之中自有安排。无论千百度的寻找，终将在最合适的时间，遇见最对的人，共谱一曲不朽的情缘。

问：嘿，如果...如果我能为你做一顿饭，你最想尝尝什么？
答：我'''
      
      geci='也见不到\n我不能就这样失去你的微笑\n口红待在桌脚而你我找不到\n若角色对调你说好不好\n说了再见才发现再也见不到\n能不能就这样忍着痛泪不掉\n说好陪我到老永恒往 哪里找\n再次拥抱一分一秒都好\n天凉了雨下了你走了\n清楚了我爱的遗失了\n落叶飘在湖面上睡着了\n想要放放不掉'
      alis2='\r\n\r\nq9:被誉为万岛之国的是哪个国家？\r\n'
      cped='''1,01_001,01_001_001,童文洁,你孩子也在这上学,female,middle-aged,high,high,low,low,high,other-venue,0_0,0_0,neutral,neutral,question
1,01_001,01_001_002,刘静,'''
      doct='''问：最近我经常恶心想吐，怎么回事？
答：'''
      hqylr='''　　怪不得君之他们扔了高危信号上去，这到底是个什么地方啊！
　　不过这些水猴子也很奇怪，她在很多地理杂志的期刊上都看过，这种生物，其实是一种水生物的变异体，传说'''
      #生成一份食谱，包括食材清单和烹饪步骤，介绍如何做一道甜品。\\n请生成一份甜品食谱，包括所需的食材和烹饪步骤，尽可能详细地描述每一步骤。\\n
      #请生成一首关于秋天的五言诗。\\n秋天的景色、气息或情感的描述
      hobby='''Unpopularity:3,Loss of interest:2,Reliability:1,Classical music:3,Opera:5,Metal or Hardrock:5,Mood swings:3,Height:secondary school,Gardening:3,Music:5,Small - big dogs:3,Art exhibitions:5,Romantic:3,Gender:block of flats,Healthy eating:3,Empathy:2,Waiting:2,Darkness:1,Workaholism:3,Musical instruments:1,Spending on healthy eating:male,Economy Management:3,Daily events:1,Law:5,Thriller:3,Theatre:2,Flying:2,Rock:5,Country:2,Judgment calls:5,Elections:2,Dreams:3, Ska":4,Knowing the right people:4,Getting up:2,Responding to a serious letter:4,Snakes:never smoked,Politics:4,Decision making:4,"Countryside:5,Assertiveness:3,Animated:5,Friends versus money:5,Shopping:2,New environment:2,War:2,Mathematics:1,Thinking ahead:2,Questionnaires or polls:3,Action:2,Religion:1,Internet usage:1,Hypochondria:5,Alternative:3,Public speaking:4,Internet:4,Spending on looks:77,Writing:2,Number of friends:3,Lying:4,Fake:4,Heights:1,Final judgement:3,"Reggae:4,Branded clothing:20,Energy levels:5,Age:right handed,Charity:4,Self-criticism:3, Jazz":3,Cars:1,Cheating in school:2,Science and technology:3,"Hiphop:4,Sci-fi:3,Documentary:3,Slow songs or fast songs:3,God:only to avoid hurting someone,Alcohol:3,Chemistry:4,Compassion to animals:3,"Techno:5,Rock n roll:1,Passive sport:3,Comedy:4,Finances:4,Socializing:3,Criminal damage:1,Giving:3,Musical:3,Rats:never,Health:3,Dancing:2,Smoking:3,Active sport:1,Spiders:3,Shopping centres:4,"Swing:5,Latino:5,Physics:4,History:3,Funniness:4,Getting angry:3,Keeping promises:4,Children:4,Western:4,Horror:3,Finding lost valuables:few hours a day,Parents' advice:3,Entertainment spending:186,Writing notes:4,Dance:2,Adrenaline sports:2,Celebrities:3,Eating to survive:4,Prioritising workload:3,Punk:3,Number of siblings:city,Pets:1,Movies:2, Rap":3, Trance":5,PC:3,Ageing:2,Fantasy/Fairy tales:4,Fear of public speaking:2,Reading:3,Appearence and gestures:4,Medicine:2,Foreign languages:2,Borrowed stuff:3,Changing the past:i am often early,Fun with friends:2,Geography:5,Dangerous dogs:2, outdoors":4,Weight:no,Achievements:4,Biology:4,Personality:4,Pop:2,Loneliness:3,Storm:2,Folk:3,Life struggles:3,Interests or hobbies:3,Psychology:4,Spending on gadgets:1,Happiness in life:3,Punctuality:'''
      gpt4='''{"instruction": "Russia Finishes Building Iran Nuclear Plant  MOSCOW (Reuters) - Russia and Iran said Thursday they had  finished construction of an atomic power plant in the Islamic  Republic -- a project the United States fears Tehran could use  to make nuclear arms. \nIs this a piece of news regarding world politics, sports, business, or science and technology? ", "input": "", "output": "'''
      #答案是.....:3
      geci='''{ "_id" : { "▩oid" : "5bbdf280831b976\
548aa14e8" }, "singer" : "张雨生", "s\
ong" : "玫瑰的名字", "geci" : [ "玫瑰的颜色 '''

      gw='''故意露出一些破绽，以引诱敌人深入我方，乘机切断他的后援和前应，最终陷他于死地。|假之以便，唆之使前，断其援应，陷之死地。
这就如《易经》 噬嗑 卦中说的，咬坚硬的腊肉而伤了牙齿一样，敌人为贪求不应得的利益，必招致后患。|遇毒，位不当也。
宁肯装作无知而不采取行动，不可装作假聪明而轻易妄动。|宁伪作不知不为，不伪作假知妄为。
要在心里暗暗谋划计策，外表不露任何声色，就像迅猛激烈的云雷在冬时隐藏地下一样地平静。|静不露机，云雷屯也。
多次变动敌人的阵容，把他的兵力调开，等待他自己败阵，然后用谋进攻他，好比拖住了车轮，车子就不能运行了。|'''
      pg='''With Murray seemingly happy to just keep the ball in play in the early moments, Federer then stepped in with aggressive winners off the backhand and forehand sides to break for 2-0.\t在穆雷似乎乐于在前几局保持球路的情况下，费德勒随后以极具攻击性的反手和正手制胜球取得2-0的破发。\t'''
      belle3='{"instruction": "判断给定的文章是否符合语法规则。如果不符合，请提供修改建议。\\n下面是一篇文章的开头: \\"为了探讨这个主题，本文将提供一系列数据和实例，以证明这一观点。\\"\\n", "input": "", "output": "'
      yishi='''{  
    "instruction": "<用户展示新发型>看我新剪的头发，怎么样？",  
    "link": "'''
      zhz='{\n        "instruction": "小姐，别的秀女都在求中选，唯有咱们小姐想被撂牌子，菩萨一定记得真真儿的——",\n        "input": "",\n        "output": "'
      belle_fy_en='I want to play football.'#'I want to do this.'#'The quick brown fox jumps over the lazy dog.'
      belle_fy='{"instruction": "给定一个英文文本，生成与之相关的中文翻译。\\n文本：“{belle_fy_en}”\n", "input": "", "output": "'.replace('{belle_fy_en}',belle_fy_en)
      b_chat={0:'麒麟芯片是什么？',
          1:'给定一个数字列表，找出其中的最大值和最小值。\\n数字列表：[3, 9, 2, 7, 5, 1, 8, 4, 6, 0]',
          2:'请生成一段关于“春风”为主题的短故事，提供完整的答案。\n',
          3:'请回答下列问题：“什么是全球变暖？”\n',
          4:'请创建一个简单的Python程序，用于计算两数乘积\n',
          5:'创建一个简单的计算器，并提供任何必需的数学原理。\n',
          6:'根据给定的单词，生成与该单词相关的五个同义词。\n单词：友谊\n',
          7:'创作一首简短的诗歌，内容为“春天的晚，风”和自然的诗歌。\n',
          8:'给定一个数字列表，找出其中的最大值和最小值。\\n数字列表：[3, 9, 2, 7, 5, 1, 8, 4, 6, 0]',
          9:'请描述一下如何制造一个蛋糕。\n',
          10:'请从社会学、人口学和环境科学的维度分析人口老龄化对环境可持续发展的影响。综合考察并阐述老年人口增加对自然资源消耗、城市规划、交通系统和医疗保健需求的影响。分析人口老龄化趋势在不同国家和地区的差异性，以及这些差异如何反映不同社会政策和经济发展水平。进一步预测，随着全球人口老龄化问题的加剧，可持续发展目标如何调整以适应这一挑战，并讨论相关政策制定者如何在保障老年人福祉和推动环境可持续性之间找到平衡。请在您的答案中考虑最新的研究和数据支持您的观点。',
          11:'请设计实验证明煤油中含有碳元素并完成实验报告。\n实验步骤：\n实验现象：\n实验结论：',
          12:'请撰写一份300-500字的个人介绍，用于一位科学家申请加入国际环保组织的个人简历。介绍中需要包含科学家的基本资料、教育背景、研究领域，并特别强调在环境保护方面所做的贡献或发明。分享至少一个与环保研究相关的真实案例故事，并展现其解决环境问题的能力。请确保文本具有多样化的语言风格，结构清晰，每个段落都有明确的主题。',
          13:'你需要撰写一篇不少于300字的演讲稿，目的是说服听众支持并参与当地的植树造林活动。演讲稿应以一个引人深思的引言开头，提出至少三个鼓励植树的论点（如提升空气质量、促进生物多样性、增加城市绿化地带），对抗可能的反对论点（例如土地使用冲突或资金问题），并以一段鼓舞人心的结论结束。文章中需使用拟人、排比等多种修辞手法，并包含丰富的词汇，从而提升演讲的感染力和说服力，保证思路连贯和结构完整。',
          14:'请在原有文本基础上，增加3-4个有创造性的细节或描述，并构造一个简单的情节发展，使得文本达到至少400字，并且与原文内容紧密相关。原文内容为：“午后的咖啡馆里，窗外细雨纷飞。一位女士静静坐在角落，手中的情书微微发抖。她的眼神中透露出一丝期待，而她等待的人即将出现。',
          15:'华为海思的麒麟芯片是什么？',
              16:'创作一首简短的古代古诗，内容为“春花秋月何时了”。\n',
              17:'太阳系中最大的天体是是什么？',
              18:'计算15*84',
              19:'分类以下单词，并将它们分为动物、植物、水果或其他。\n狗、猫、猴子、熊猫',
            20:'生成一段代码，基于tensorflow实现深度学习文本分类。\n',
              21:'根据给定的文本，对其进行分类，归纳出其主要观点。\n文本：这场比赛我赢了',
              22:'回答以下问题：什么是机器学习？',
              23:"请你概括题下内容：摘要：当地时间1月25日上午，意大利米兰附近一列火车脱轨，造成至少5人死亡，数10人受伤。据悉，该辆通勤列车满载乘客，目前有5名伤者伤势严重，还有不少乘客被困在车厢中。 现 场图（图片来源：《每日快报》）现场图（图片来源：《每日快报》）脱轨的列车图（图片来源：《每日邮报》）海外网1月25日电 综合路透社、《每日快报》报道，当地时间1月25日上午，意大利米兰附近一列火车脱轨，造成至少5人死亡，数10人受伤。据悉，该辆通勤列车满载乘客，目前有5名伤者伤势严重，还有不少乘客被困在车厢中。事故发生的原因尚不清楚，救援人员目前已赶到现场。路透社联系 到当地国营火车公司Ferrovie Dello Stato的发言人证实，在距离米兰约40公里的皮奥尔泰洛（Pioltello）路段发生了一起列车脱轨事 故，但没有提供可能的伤亡细节。央视新闻援引意大利警方通报，事故造成的伤亡人数可能会进一步上升。事故发生后，意大利北部米兰至威尼斯段火车运营全线延误。（海外网 张敏）本文系版权作品，未经授权严禁转载。海外视野，中国立场，登陆人民日报海外版官网——海外网www.haiwainet.cn或“海客”客户端，领先一步获取权威资讯。 责编：张敏、朱惠悦 31246145,.意大利米兰一列火车脱轨 致5人 死多人伤,.2018-01-25 16:00:18,.204317,.张敏、朱惠悦\\n意大利米兰郊区一火车脱轨 已致5人死逾百人受伤 原标题：意大利米兰郊 区一火车脱轨 已致5人死逾百人受伤 中新网1月25日电 综合外媒报道，意大利米兰郊区一列火车当地时间25日早高峰时段发生脱轨事故 ，目前死亡人数已升至至少5人，事故还造成逾100人受伤。 报道称，这列火车在位于意大利米兰约40公里远的郊区路段发生脱轨事故。 当时火车上满载了通勤人员。 报道称，这列火车在位于意大利米兰约40公里远的郊区路段发生脱轨事故。当时火车上满载了通勤人员。 路透社援引当地消防官员最新消息称，事故已造成至少5人死亡。此前报道的死亡数字是2人。 事故发生后，当场警报响起，大批救援车 辆介入救援，包括几十辆救护车、汽车和救援直升机。现场还有消防人员和宪兵等。 为了方便救援，铁路路堤的混凝土栏杆已被移除， 护士和消防队员帮助把受伤的乘客带到安全的地方。 为了方便救援，铁路路堤的混凝土栏杆已被移除，护士和消防队员帮助把受伤的乘 客带到安全的地方。 事故原因目前尚不可知。\\n中新网1月25日电 综合外媒报道，意大利米兰郊区一列火车当地时间25日早高峰时段发生脱轨事故，已造成至少2人死亡，10人重伤，约100人轻伤。报道称，这列火车在位于意大利米兰约40公里远的郊区路段发生脱轨事故。当时火车上满载了通勤人员。事故发生后，当场警报响起，大批救援车辆介入救援，包括几十辆救护车、汽车和救援直升机。现场还有消防人员和宪兵等。为了方便救援，铁路路堤的混凝土栏杆已被移除，护士和消防队 员帮助把受伤的乘客带到安全的地方。事故原因目前尚不可知。（原题为《意大利米兰郊区火车脱轨致2死逾百伤 救援进行中》）\\n原 标题：意大利列车脱轨逾百伤亡 或因道岔机械装置故障 中新网1月25日电 据俄罗斯卫星网报道，意大利米兰附近列车脱轨事件的初步原因是道岔机械装置故障。 当地时间1月25日，意大利米兰郊区一列火车在早高峰时段发生脱轨事故，已造成至少2人死亡，10人重伤，约100人轻伤。 意大利Rainews24电视频道报道，火车头和列车四节中的第一节车厢能够通过前往米兰方向的铁轨连接处，但道岔机械装置偏离中心线后，接下来的两节车厢脱轨。 当地时间25日早上7时，一辆从克雷莫纳发往米兰的列车发生脱轨，其上乘客主要是前往米兰上班的人。 据报道，这起事故至少造成多人死亡，逾百人受伤。 大量急救车、救援人员、宪兵、铁路警察正在事故现场进行工作。 责任编 辑：张岩\\n中新网2月1日电 据欧联网援引欧联通讯社报道，1月25日意大利米兰近郊发生的列车脱轨事故，造成3人死亡46人受伤。近日，米兰检察院经调查，决定将分别以涉嫌渎职、过失杀人等刑事罪名，对4名铁路高管进行立案调查。 据报道，1月25日，载有350名乘客的10452次列车，行驶到米兰省塞格拉泰市和皮奥尔泰洛市路段脱轨。期间，部分列车车厢从脱轨点到列车侧翻时，脱轨行驶了长达2公里，以至于救援人员不得不对挤压在一起的车厢进行切割，才能救出被困车厢内的乘客。 资料图：当地时间1月25日，意大利米兰郊区一列火车在早高峰时段发生脱轨事故。 报道称，米兰检察院指派了3名高级检察官组成专案调查组，全面对事件展开调查。检察院专案组经调查认为，意大利铁路公司首席执行官简迪雷、公司生产部经理雷博鲁托，以及意大利北方铁路公司首席执行官法利赛、运营总监米诺亚4 位铁路高管，对事故负有不可推卸的责任。因此近日米兰检察院决定，对4名铁路高管进行立案调查。 据检察院专案组在前几天的事故调查中发现，事故列车脱轨路段轨道使用的木质枕木破损严重。因铁路部门管理人员不作为，没有及时更换铁轨枕木，导致了事故的发生。但意大利铁路公司则声明称，公司技术条例并非完全要求废弃使用木质枕木，除特殊路段仍在延续使用木质材料的枕木外，意大利全国铁路的主干线已经基本不再使用木质枕木。 然而检察院专案组认为，该声明显然是将事故责任，直接推给了负责检修铁路的一线员工。事 实上，正是铁路高层决策人物忽略了对铁路危险路段的检修和维护，才造成了列车脱轨的重大交通事故。 目前，意大利检方专案调查组 仍在对米兰列车脱轨事件做进一步调查，检方将很快对涉嫌渎职的铁路高管提起司法诉讼。(博源)",
           }[21]
      qychat='p1 : 你 的 歌声 真 美妙 ， 离 你 很远 都 听见 了 。\np2 : 我 以为 没 人 呢 ， 被 我 的 歌声 吓 到 了 吗 ？\np1 : 没有 ， 唱 的 太 好听 了 ， 我 都 没 听 够 。\np2 : 我 是 我们 部队 里 歌唱 组 的 领唱 ， 以前 就 唱唱 军歌 。\np1 : 你 是 一名 军人 吗 ， 看着 很 年轻 的 小伙子 。\np2 : 是 的 ， 我 高中 毕业后 参 军 了 ， 今天 和 我们 班长 请假 出来 回家 看看 。\np1 : 在 部队 里 请 个 假 不容易 ， 就 不能 经常 回家 看望 亲人 。\np2 : 对 ， 我 母亲 最近 生病 了 ， 我 要 回家 来 照顾 她 ， 母亲 是 我 最 重要 的 人 。\np1 : 你 真 有 孝心 ， 我 也 好久 没 回家 了 ， 忙于 工作 。\np2 : 你 是 苏州 人 吧 ， 你 在 这 住 多少年 了 呀 ？\np1 : 从小 就 住在 这 ， 不过 我 会 在 两个月 内 搬去 上海 ， 在 上海 定居 。\np2 : '
      qychat2='p1 : 我 好 无聊 。\np2 : '
      moti='''{"instruction": "请问图片中的图形颜色：[img 'test_dataset/img_2_aaa.jpg']", "input": "", "output": "'''

      belle_chat='{"instruction": "{b_chat}", "input": "", "output": "'.replace('{b_chat}',b_chat)
      inp_m=belle_chat#qychat2#novel#chatbot#novel#luxun.replace('\r\r\n','')#yw#luxun#chatbot#xyj#hlm#xyj
      #rt.replace_img_tags(moti)#
      is_fill=0
      if is_fill:
          inp_m=fill(inp_m,128,cut=True)
      #window=128
      #fwindow=0#8
      #inp_m=rw(inp_m,window-fwindow)
      #inp_m=rw(inp_m,window-fwindow)#' '*(96-len(inp_m))+inp_m
      print('原文：',inp_m,'\n续写：')
      #print('问题：',chatbot,'\n回答：',end='')
      ti=time.time()
      out=''
      #art: 0.65
      #print(444)
      if is_fill:#
          for i in range(1000):
              out+=generate_texts(m, d, fill(inp_m+out,128,cut=True),
                                  num_generate=1,
                                 every=lambda a:print(a,end='',flush=True),
                                 temperature=0.72,#0.5#0.8
                                 pass_char=['▩']
                           #      utf=False,
                                   #q=[0.6,0.4]
                           #     rest=False,
                                    )
      else:
          for i in range(1000):
              out+=generate_texts(m, d, (inp_m+out)[-128:],
                                  num_generate=1,
                                 every=lambda a:print(a,end='',flush=True),
                                 temperature=0.4,#0.5#0.8
                                 pass_char=['▩']
                           #      utf=False,
                                   #q=[0.6,0.4]
                           #     rest=False,
                                    )
      if ms:
          pass#m.summmary()
      
      #aaa=input('img:')
      #print(rt.extract_and_save_images(aaa))
      #                         batch_size=512)
      print(len(out),'\n\nSpeed (Tokens/s) :',len(out)/(time.time()-ti))

      
  else:
      m,d=load(ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_test_40_2_3',
               #r'E:\小思框架\论文\ganskchat\ckpt_formal_zh_mini_t2',#r'E:\小思框架\论文\ganskchat\ckpt_formal_zh_common_t3_0255',
                vocab=r'E:\小思框架\论文\ganskchat\vocab_lx3.txt',
               model_type=40.23)
      while True:
        wen=input('我：')
        quest=f'南枝问道：“{wen}\n”\n    杨大哥说到：“'
        q2=f'''　　小姑娘也说：“{wen}”
　　高行接着她的话往下：“'''#_loop
        ret=generate_texts_loop(m,d,quest,num_generate=15,
                                temperature=0.55
                                )
        if '”' in ret:
          ret=ret[:ret.index('”')]
        if '“' in ret:
          ret=ret[ret.index('“')+1:]
        print('\nAI：',ret)
