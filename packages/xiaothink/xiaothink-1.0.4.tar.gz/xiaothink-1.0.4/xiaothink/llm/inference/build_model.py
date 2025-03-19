import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
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


LR=0.00005

import tensorflow as tf
from tensorflow.keras.layers  import Layer, Dense, Embedding



import tensorflow as tf
from tensorflow.keras import layers

    
def send_matrices_to_server(matrix1, matrix2):
    tf.compat.v1.enable_eager_execution()
    #time1 = time.time()
    return tf.linalg.matmul(matrix1, matrix2)


class CustomGRUCell(tf.keras.layers.Layer):
    def __init__(self, units, recurrent_initializer='glorot_uniform', **kwargs):
        super(CustomGRUCell, self).__init__(**kwargs)
        self.units = units
        self.state_size = units
        self.recurrent_initializer = recurrent_initializer

    def build(self, input_shape):
        self.kernel = self.add_weight(
            shape=(input_shape[-1], 3 * self.units),
            initializer='glorot_uniform',
            name='kernel'
        )
        self.recurrent_kernel = self.add_weight(
            shape=(self.units, 3 * self.units),
            initializer=self.recurrent_initializer,
            name='recurrent_kernel'
        )
        self.bias = self.add_weight(
            shape=(3 * self.units,),
            initializer='zeros',
            name='bias'
        )

    def call(self, inputs, states):
        h_tm1 = states[0]  # previous memory state
        combined_inputs = tf.concat([inputs, h_tm1], axis=-1)

        # Perform the linear transformation and split into three parts
        z_r_h = (
            send_matrices_to_server(inputs, self.kernel) +
            send_matrices_to_server(h_tm1, self.recurrent_kernel) +
            self.bias
        )
        z, r, h_hat = tf.split(z_r_h, num_or_size_splits=3, axis=1)

        # Apply activations
        z = tf.sigmoid(z)
        r = tf.sigmoid(r)
        h_hat = tf.tanh(r * h_hat + (1 - r) * h_tm1)

        # Update hidden state
        h_t = (1 - z) * h_hat + z * h_tm1

        return h_t, [h_t]

    
class CustomGRU(tf.keras.layers.RNN):
    def __init__(self, units, return_sequences=False, stateful=False, recurrent_initializer='glorot_uniform', name=None, trainable=True, **kwargs):
        cell = CustomGRUCell(units, recurrent_initializer=recurrent_initializer, **kwargs)
        super(CustomGRU, self).__init__(
            cell,
            return_sequences=return_sequences,
            stateful=stateful,
            name=name,
            trainable=trainable,
            **kwargs
        )

class CLModel_41_1(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, n=1, his_q=0.75, use_matt=True, att_q=0.4, att_units=None, n_char=3, wd_q=1.0, nh=8, train_deep_layer=True, train_main=True, num_chargru_layer=8, embed_q=0.5, **kwargs):
        super(CLModel_41_1, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q = his_q
        self.use_matt = use_matt
        self.att_q = att_q
        self.att_units = att_units
        self.n_char = n_char
        self.wd_q = wd_q
        self.nh = nh
        self.train_deep_layer = train_deep_layer
        self.train_main = train_main
        self.num_chargru_layer = num_chargru_layer
        self.embed_q = embed_q

        self.next_token_predictor = layers.Dense(vocab_size, trainable=True)
        self.styler = layers.Dense(vocab_size, trainable=True)
        self.dropout = tf.keras.layers.Dropout(0.1)
        self.embedding = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim)

        # Stacked GRU layers
        self.context_encoders = [
            GRU(units, return_sequences=True, stateful=False, recurrent_initializer='glorot_uniform', name=f'gru_{i}', trainable=True) for i in range(n)
        ]

        self.lnl = layers.LayerNormalization(epsilon=1e-6)
        self.lnl0 = layers.LayerNormalization(epsilon=1e-6)
        self.lnl1 = layers.LayerNormalization(epsilon=1e-6)

    def call(self, inputs, training=None, use_teacher_forcing=True):
        # 嵌入层
        embedded_inputs = inputs#self.embedding(inputs)
        embedded_inputs = self.lnl0(embedded_inputs)
        embedded_inputs = self.dropout(embedded_inputs, training=training)

        # 使用GRU进行序列编码
        sequence = embedded_inputs
        for gru_layer in self.context_encoders:
            sequence = gru_layer(sequence, training=training)
            sequence = self.lnl(sequence)


        return sequence

    def get_config(self):
        config = super(CLModel_40_1, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "his_q": self.his_q,
            "use_matt": self.use_matt,
            "att_q": self.att_q,
            "att_units": self.att_units,
            "n_char": self.n_char,
            "wd_q": self.wd_q,
            "nh": self.nh,
            "train_deep_layer": self.train_deep_layer,
            "train_main": self.train_main,
            "num_chargru_layer": self.num_chargru_layer,
            "embed_q": self.embed_q
        })
        return config


class CLModel_40_1_01(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, n=1, his_q=0.75, use_matt=True, att_q=0.4, att_units=None, n_char=3, wd_q=1.0, nh=8, train_deep_layer=True, train_main=True, num_chargru_layer=8, embed_q=0.5, **kwargs):
        super(CLModel_40_1_01, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q = his_q
        self.use_matt = use_matt
        self.att_q = att_q
        self.att_units = att_units
        self.n_char = n_char
        self.wd_q = wd_q
        self.nh = nh
        self.train_deep_layer = train_deep_layer
        self.train_main = train_main
        self.num_chargru_layer = num_chargru_layer
        self.embed_q = embed_q

        self.next_token_predictor = layers.Dense(vocab_size, trainable=True)
        self.styler = layers.Dense(vocab_size, trainable=True)
        self.dropout = tf.keras.layers.Dropout(0.1)
        #self.embedding = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim)

        # Stacked GRU layers
        self.context_encoders = [
            CustomGRU(units, return_sequences=True, stateful=False, recurrent_initializer='glorot_uniform', name=f'gru_{i}', trainable=True) for i in range(n)
        ]

        self.lnl = layers.LayerNormalization(epsilon=1e-6)
        self.lnl0 = layers.LayerNormalization(epsilon=1e-6)
        self.lnl1 = layers.LayerNormalization(epsilon=1e-6)
        self.f_d=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        self.f_d_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)
        self.f_d2=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)

        
        #self.memory= GRUMemoryLayer(input_dim=units, memory_size=units, key_dim=units // 2)


    def call(self, inputs, training=None, use_teacher_forcing=True):
        # 嵌入层
        
        input_shape = tf.shape(inputs)  
        input_dim = input_shape[-1]  
        embedded_inputs = self.f_d(inputs)
        embedded_inputs=self.lnl0(embedded_inputs)
        embedded_inputs = self.f_d2(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        embedded_inputs=self.lnl1(embedded_inputs)
        
        embedded_inputs = self.dropout(embedded_inputs, training=training)
        
        # 使用GRU进行序列编码
        sequence = inputs#(embedded_inputs)
        for gru_layer in self.context_encoders:
            sequence = gru_layer(sequence, training=training)
            sequence = self.lnl(sequence)


        return sequence

    def get_config(self):
        config = super(CLModel_40_1, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "his_q": self.his_q,
            "use_matt": self.use_matt,
            "att_q": self.att_q,
            "att_units": self.att_units,
            "n_char": self.n_char,
            "wd_q": self.wd_q,
            "nh": self.nh,
            "train_deep_layer": self.train_deep_layer,
            "train_main": self.train_main,
            "num_chargru_layer": self.num_chargru_layer,
            "embed_q": self.embed_q
        })
        return config
    
'''
class TokenAndPositionEmbedding_41_01(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding_41_01, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.lstm = layers.LSTM(units=embed_dim, return_sequences=True)
        self.bn = layers.BatchNormalization()

    def call(self, x):
        x = self.token_emb(x)
        residual = x  # 残差连接
        x = self.lstm(x)
        x = self.bn(x)
        x += residual  # 添加残差
        return x   





class TokenAndPositionEmbedding_41_01(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding_41_01, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.lstm1 = layers.GRU(units=embed_dim, return_sequences=True)
        self.dropout1 = layers.Dropout(0.5)
        self.dense = layers.Dense(embed_dim, activation='relu')
        self.bn = layers.BatchNormalization()
        
        # 添加LAuReL模块，这里简化为一个小型网络，实际应用中可以根据需要调整
        self.lau_rel = tf.keras.Sequential([
            layers.Dense(embed_dim // 4, activation='relu'),  # 减少参数量
            layers.Dense(embed_dim)                          # 输出维度与残差一致
        ])

    def call(self, x, training=False):
        x = self.token_emb(x)
        residual = x  # 残差连接
        
        x = self.lstm1(x)
        x = self.dropout1(x, training=training)
        
        x = self.dense(x)
        x = self.bn(x, training=training)
        
        # LAuReL: 在残差连接之前通过一个小网络处理residual
        residual = self.lau_rel(residual)
        
        x += residual  # 添加残差，经过了LAuReL处理
        return x


'''



# 定义MoE模型
class MoEModel_40_2(tf.keras.Model):
    def __init__(self, experts, vocab_size, **kwargs):
        super(MoEModel_40_2, self).__init__(**kwargs)
        self.experts = experts
        #self.router = router
        self.router_outputs=None
        self.rout_dense=layers.Dense(1, activation='softmax')
        self.next_token_predictor = layers.Dense(vocab_size)
       
        
    def router(self,inputs,rout_dense):
        logits = rout_dense(inputs)
        return logits
        

    def call(self, inputs, training=None, mask=None):
        # 路由机制决定输入应该被分配给哪个专家
        #self.router_outputs = self.router(inputs,self.rout_dense)
        #print(self.router_outputs)
        # 将输入分配给不同的专家
        expert_outputs = []
        for i, expert in enumerate(self.experts):
            expert_input = inputs #* tf.expand_dims(self.router_outputs[:, :, i], -1)
            expert_output = expert(expert_input, training=training)
            expert_outputs.append(expert_output)
        
        # 组合所有专家的输出
        combined_output = tf.reduce_sum(tf.stack(expert_outputs, axis=-1), axis=-1)
        next_token_logits = self.next_token_predictor(combined_output)
        return next_token_logits
    


class TokenAndPositionEmbedding_41_01(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding_41_01, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.lstm1 = (layers.GRU(units=embed_dim, return_sequences=True))#layers.Bidirectional
        self.dropout1 = layers.Dropout(0.5)
        self.dense = layers.Dense(embed_dim, activation='relu')
        self.bn = layers.BatchNormalization()

    def call(self, x):
        x = self.token_emb(x)
        residual = x  # 残差连接
        
        x = self.lstm1(x)
        x = self.dropout1(x)
        
        x = self.dense(x)
        x = self.bn(x)
        
        x += residual  # 添加残差
        return x

# 定义路由机制
def create_router(num_experts):
    def router(inputs):
        logits = layers.Dense(num_experts, activation='softmax')(inputs)
        return logits
    return router
def send_matrices_to_server(matrix1, matrix2):
    tf.compat.v1.enable_eager_execution()
    return tf.linalg.matmul(matrix1, matrix2)
    open('tt.bin','wb').write(matrix1_bytes)
    open('tt2.bin','wb').write(matrix2_bytes)
    print('sending requests', len(matrix1_bytes), len(matrix2_bytes))
    #return tf.linalg.matmul(matrix1, matrix2)

    response = requests.post('https://10pz02pw83097.vicp.fun', data={'file1': matrix1_bytes, 'file2': matrix2_bytes})

    if response.status_code == 200:
        print('web mult', time.time() - time1)
        # 解包返回的字节流
        result_matrix = msgpack.unpackb(response.content, raw=False)
        return np.array(result_matrix)
    else:
        print("Error:", response.text)
        return None

class CustomGRUCell(tf.keras.layers.Layer):
    def __init__(self, units, recurrent_initializer='glorot_uniform', **kwargs):
        super(CustomGRUCell, self).__init__(**kwargs)
        self.units = units
        self.state_size = units
        self.recurrent_initializer = recurrent_initializer

    def build(self, input_shape):
        self.kernel = self.add_weight(
            shape=(input_shape[-1], 3 * self.units),
            initializer='glorot_uniform',
            name='kernel'
        )
        self.recurrent_kernel = self.add_weight(
            shape=(self.units, 3 * self.units),
            initializer=self.recurrent_initializer,
            name='recurrent_kernel'
        )
        self.bias = self.add_weight(
            shape=(3 * self.units,),
            initializer='zeros',
            name='bias'
        )

    def call(self, inputs, states):
        h_tm1 = states[0]  # previous memory state
        combined_inputs = tf.concat([inputs, h_tm1], axis=-1)

        # Perform the linear transformation and split into three parts
        z_r_h = (
            send_matrices_to_server(inputs, self.kernel) +
            send_matrices_to_server(h_tm1, self.recurrent_kernel) +
            self.bias
        )
        z, r, h_hat = tf.split(z_r_h, num_or_size_splits=3, axis=1)

        # Apply activations
        z = tf.sigmoid(z)
        r = tf.sigmoid(r)
        h_hat = tf.tanh(r * h_hat + (1 - r) * h_tm1)

        # Update hidden state
        h_t = (1 - z) * h_hat + z * h_tm1

        return h_t, [h_t]

    
class CustomGRU(tf.keras.layers.RNN):
    def __init__(self, units, return_sequences=False, stateful=False, recurrent_initializer='glorot_uniform', name=None, trainable=True, **kwargs):
        cell = CustomGRUCell(units, recurrent_initializer=recurrent_initializer, **kwargs)
        super(CustomGRU, self).__init__(
            cell,
            return_sequences=return_sequences,
            stateful=stateful,
            name=name,
            trainable=trainable,
            **kwargs
        )

    

class CLModel_41_1(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, n=1, his_q=0.75, use_matt=True, att_q=0.4, att_units=None, n_char=3, wd_q=1.0, nh=8, train_deep_layer=True, train_main=True, num_chargru_layer=8, embed_q=0.5, **kwargs):
        super(CLModel_41_1, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q = his_q
        self.use_matt = use_matt
        self.att_q = att_q
        self.att_units = att_units
        self.n_char = n_char
        self.wd_q = wd_q
        self.nh = nh
        self.train_deep_layer = train_deep_layer
        self.train_main = train_main
        self.num_chargru_layer = num_chargru_layer
        self.embed_q = embed_q

        self.next_token_predictor = layers.Dense(vocab_size, trainable=True)
        self.styler = layers.Dense(vocab_size, trainable=True)
        self.dropout = tf.keras.layers.Dropout(0.1)
        self.embedding = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim)

        # Stacked GRU layers
        self.context_encoders = [
            GRU(units, return_sequences=True, stateful=False, recurrent_initializer='glorot_uniform', name=f'gru_{i}', trainable=True) for i in range(n)
        ]

        self.lnl = layers.LayerNormalization(epsilon=1e-6)
        self.lnl0 = layers.LayerNormalization(epsilon=1e-6)
        self.lnl1 = layers.LayerNormalization(epsilon=1e-6)

    def call(self, inputs, training=None, use_teacher_forcing=True):
        # 嵌入层
        embedded_inputs = inputs#self.embedding(inputs)
        embedded_inputs = self.lnl0(embedded_inputs)
        embedded_inputs = self.dropout(embedded_inputs, training=training)

        # 使用GRU进行序列编码
        sequence = embedded_inputs
        for gru_layer in self.context_encoders:
            sequence = gru_layer(sequence, training=training)
            sequence = self.lnl(sequence)


        return sequence

    def get_config(self):
        config = super(CLModel_40_1, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "his_q": self.his_q,
            "use_matt": self.use_matt,
            "att_q": self.att_q,
            "att_units": self.att_units,
            "n_char": self.n_char,
            "wd_q": self.wd_q,
            "nh": self.nh,
            "train_deep_layer": self.train_deep_layer,
            "train_main": self.train_main,
            "num_chargru_layer": self.num_chargru_layer,
            "embed_q": self.embed_q
        })
        return config



class CLModel_40_1_01(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, n=1, tst=False, his_q=0.75, use_matt=True, att_q=0.4, att_units=None, n_char=3, wd_q=1.0, nh=8, train_deep_layer=True, train_main=True, num_chargru_layer=8, embed_q=0.5, **kwargs):
        super(CLModel_40_1_01, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q = his_q
        self.use_matt = use_matt
        self.att_q = att_q
        self.att_units = att_units
        self.n_char = n_char
        self.wd_q = wd_q
        self.nh = nh
        self.train_deep_layer = train_deep_layer
        self.train_main = train_main
        self.num_chargru_layer = num_chargru_layer
        self.embed_q = embed_q

        self.next_token_predictor = layers.Dense(vocab_size, trainable=bool(1-tst))
        self.styler = layers.Dense(vocab_size, trainable=True)
        self.dropout = tf.keras.layers.Dropout(0.1)
        #self.embedding = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim)

        # Stacked GRU layers
        self.context_encoders = [
            CustomGRU(units, return_sequences=True, stateful=False, recurrent_initializer='glorot_uniform', name=f'gru_{i}', trainable=bool(1-tst)) for i in range(n)
        ]

        self.lnl = layers.LayerNormalization(epsilon=1e-6, trainable=bool(1-tst))
        self.lnl0 = layers.LayerNormalization(epsilon=1e-6, trainable=bool(1-tst))
        self.lnl1 = layers.LayerNormalization(epsilon=1e-6, trainable=bool(1-tst))
        self.f_d=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-tst))
        self.f_d_0=tf.keras.layers.Dense(units=self.vocab_size, trainable=bool(1-tst))
        self.f_d2=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-tst))

        
        #self.memory= GRUMemoryLayer(input_dim=units, memory_size=units, key_dim=units // 2)


    def call(self, inputs, training=None, use_teacher_forcing=True):
        # 嵌入层
        
        input_shape = tf.shape(inputs)  
        input_dim = input_shape[-1]  
        embedded_inputs = self.f_d(inputs)
        embedded_inputs=self.lnl0(embedded_inputs)
        embedded_inputs = self.f_d2(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        embedded_inputs=self.lnl1(embedded_inputs)
        
        embedded_inputs = self.dropout(embedded_inputs, training=training)
        
        # 使用GRU进行序列编码
        sequence = inputs#(embedded_inputs)
        for gru_layer in self.context_encoders:
            sequence = gru_layer(sequence, training=training)
            sequence = self.lnl(sequence)


        return sequence

    def get_config(self):
        config = super(CLModel_40_1, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "his_q": self.his_q,
            "use_matt": self.use_matt,
            "att_q": self.att_q,
            "att_units": self.att_units,
            "n_char": self.n_char,
            "wd_q": self.wd_q,
            "nh": self.nh,
            "train_deep_layer": self.train_deep_layer,
            "train_main": self.train_main,
            "num_chargru_layer": self.num_chargru_layer,
            "embed_q": self.embed_q
        })
        return config
    
'''
class TokenAndPositionEmbedding_41_01(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding_41_01, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.lstm = layers.LSTM(units=embed_dim, return_sequences=True)
        self.bn = layers.BatchNormalization()

    def call(self, x):
        x = self.token_emb(x)
        residual = x  # 残差连接
        x = self.lstm(x)
        x = self.bn(x)
        x += residual  # 添加残差
        return x   





class TokenAndPositionEmbedding_41_01(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding_41_01, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.lstm1 = layers.GRU(units=embed_dim, return_sequences=True)
        self.dropout1 = layers.Dropout(0.5)
        self.dense = layers.Dense(embed_dim, activation='relu')
        self.bn = layers.BatchNormalization()
        
        # 添加LAuReL模块，这里简化为一个小型网络，实际应用中可以根据需要调整
        self.lau_rel = tf.keras.Sequential([
            layers.Dense(embed_dim // 4, activation='relu'),  # 减少参数量
            layers.Dense(embed_dim)                          # 输出维度与残差一致
        ])

    def call(self, x, training=False):
        x = self.token_emb(x)
        residual = x  # 残差连接
        
        x = self.lstm1(x)
        x = self.dropout1(x, training=training)
        
        x = self.dense(x)
        x = self.bn(x, training=training)
        
        # LAuReL: 在残差连接之前通过一个小网络处理residual
        residual = self.lau_rel(residual)
        
        x += residual  # 添加残差，经过了LAuReL处理
        return x


'''






class TokenAndPositionEmbedding_41_01(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim, tst=False):
        super(TokenAndPositionEmbedding_41_01, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.lstm1 = (layers.GRU(units=embed_dim, return_sequences=True, trainable=bool(1-tst)))#layers.Bidirectional
        self.dropout1 = layers.Dropout(0.5)
        self.dense = layers.Dense(embed_dim, activation='relu', trainable=bool(1-tst))
        self.bn = layers.BatchNormalization()
        self.bn2 = layers.BatchNormalization()

    def call(self, x):
        x = self.token_emb(x)
        residual = x  # 残差连接
        
        x = self.lstm1(x)
        x = self.dropout1(x)

        #x = self.bn2(x)
        
        x = self.dense(x)
        x = self.bn(x)
        
        x += residual  # 添加残差
        return x



class TokenAndPositionEmbedding_41_01_large(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim, tst=False):
        super(TokenAndPositionEmbedding_41_01_large, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim,trainable=bool(1-tst))
        self.lstm1 = (layers.GRU(units=embed_dim, return_sequences=True,trainable=bool(1-tst)))#layers.Bidirectional
        self.dropout1 = layers.Dropout(0.5)
        self.dense = layers.Dense(embed_dim, activation='relu',trainable=bool(1-tst))
        self.bn = layers.BatchNormalization(trainable=bool(1-tst))
        self.bn2 = layers.BatchNormalization(trainable=bool(1-tst))

    def call(self, x):
        x = self.token_emb(x)
        residual = x  # 残差连接
        
        x = self.lstm1(x)
        x = self.dropout1(x)

        #x = self.bn2(x)
        
        x = self.dense(x)
        x = self.bn(x)
        
        x += residual  # 添加残差
        return x

from tensorflow.keras.layers  import Bidirectional

class CLModel_40_1_01_large(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, n=1, tst=False, his_q=0.75, use_matt=True, att_q=0.4, att_units=None, n_char=3, wd_q=1.0, nh=8, train_deep_layer=True, train_main=True, num_chargru_layer=8, embed_q=0.5, **kwargs):
        super(CLModel_40_1_01_large, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q = his_q
        self.use_matt = use_matt
        self.att_q = att_q
        self.att_units = att_units
        self.n_char = n_char
        self.wd_q = wd_q
        self.nh = nh
        self.train_deep_layer = train_deep_layer
        self.train_main = train_main
        self.num_chargru_layer = num_chargru_layer
        self.embed_q = embed_q

        self.next_token_predictor = layers.Dense(vocab_size, trainable=True)
        self.styler = layers.Dense(vocab_size, trainable=True)
        self.dropout = tf.keras.layers.Dropout(0.1)
        #self.embedding = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim)

        # Stacked GRU layers
        self.context_encoders = [
            CustomGRU(units, return_sequences=True, stateful=False, recurrent_initializer='glorot_uniform', name=f'gru_{i}',trainable=bool(1-tst)) for i in range(n)
        ]

        self.lnl = layers.LayerNormalization(epsilon=1e-6,trainable=bool(1-tst))
        self.lnl0 = layers.LayerNormalization(epsilon=1e-6,trainable=bool(1-tst))
        self.lnl1 = layers.LayerNormalization(epsilon=1e-6,trainable=bool(1-tst))
        self.f_d=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh',trainable=bool(1-tst))
        self.f_d_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=bool(1-tst))
        self.f_d2=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh',trainable=bool(1-tst))

        
        #self.memory= GRUMemoryLayer(input_dim=units, memory_size=units, key_dim=units // 2)


    def call(self, inputs, training=None, use_teacher_forcing=True):
        # 嵌入层
        
        input_shape = tf.shape(inputs)  
        input_dim = input_shape[-1]  
        embedded_inputs = self.f_d(inputs)
        embedded_inputs=self.lnl0(embedded_inputs)
        embedded_inputs = self.f_d2(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        embedded_inputs=self.lnl1(embedded_inputs)
        
        embedded_inputs = self.dropout(embedded_inputs, training=training)
        
        # 使用GRU进行序列编码
        sequence = inputs#(embedded_inputs)
        for gru_layer in self.context_encoders:
            sequence = gru_layer(sequence, training=training)
            sequence = self.lnl(sequence)


        return sequence

    def get_config(self):
        config = super(CLModel_40_1, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "his_q": self.his_q,
            "use_matt": self.use_matt,
            "att_q": self.att_q,
            "att_units": self.att_units,
            "n_char": self.n_char,
            "wd_q": self.wd_q,
            "nh": self.nh,
            "train_deep_layer": self.train_deep_layer,
            "train_main": self.train_main,
            "num_chargru_layer": self.num_chargru_layer,
            "embed_q": self.embed_q
        })
        return config

from tensorflow.keras.layers  import LSTM, Dense, Dropout, LayerNormalization 
 
class ClassicLSTMModel(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, n=1, tst=False, **kwargs):
        super(ClassicLSTMModel, self).__init__(**kwargs)
        self.vocab_size  = vocab_size 
        self.embedding_dim  = embedding_dim 
        self.window  = window 
        self.units  = units 
        self.n = n  # Number of stacked LSTM layers 
 
        # LSTM layers 
        self.lstm_layers  = [
            LSTM(units, return_sequences=True, stateful=False, name=f'lstm_{i}',trainable=bool(1-tst)) for i in range(n)
        ]
        

 
    def call(self, inputs, training=None):
        # 假设输入已经经过嵌入处理，直接传入LSTM 
        sequence = inputs 
        
        # 通过多层LSTM 
        for lstm_layer in self.lstm_layers: 
            sequence = lstm_layer(sequence)

        
        return sequence
 
    def get_config(self):
        config = super(ClassicLSTMModel, self).get_config()
        config.update({ 
            "vocab_size": self.vocab_size, 
            "embedding_dim": self.embedding_dim, 
            "window": self.window, 
            "units": self.units, 
            "n": self.n,
        })
        return config
    
            
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras  import layers

import tensorflow as tf
from tensorflow.keras import layers

class MoEModel_40_1_01_large(tf.keras.Model):
    def __init__(self, experts, vocab_size, num_experts, router_units, tst=False, **kwargs):
        super(MoEModel_40_1_01_large, self).__init__(**kwargs)
        self.experts = experts
        self.num_experts = num_experts
        self.router_units = router_units
        self.vocab_size = vocab_size

        # 定义路由网络（包含GRU辅助分类）
        self.router_gru = layers.GRU(router_units, return_sequences=False,trainable=bool(1-tst))
        self.router_dense = layers.Dense(num_experts, activation='softmax',trainable=bool(1-tst))

        # 定义最终的预测层
        self.next_token_predictor = layers.Dense(vocab_size,trainable=bool(1-tst))
        self.styler = layers.Dense(vocab_size)

    def router(self, inputs):
        gru_out = self.router_gru(inputs)
        expert_weights = self.router_dense(gru_out)
        return expert_weights

    def call(self, inputs, training=None, mask=None):
        expert_weights = self.router(inputs)
        expert_outputs = []
        
        # 首先计算最大序列长度
        max_length = 0
        for i in range(self.num_experts):
            expert_output = self.experts[i](inputs)
            expert_seq_length = tf.shape(expert_output)[1]  # 动态获取序列长度
            max_length = tf.maximum(max_length, expert_seq_length)  # 使用tf.maximum来比较并更新最大长度
        
        # 根据最大长度进行填充
        for i in range(self.num_experts):
            expert_output = self.experts[i](inputs)
            expert_seq_length = tf.shape(expert_output)[1]
            padding_length = max_length - expert_seq_length
            if padding_length > 0:
                padding_shape = [[0, 0], [0, padding_length], [0, 0]]  # 只在第二个维度进行填充
                expert_output = tf.pad(expert_output, padding_shape, 'CONSTANT', constant_values=0)
            expert_outputs.append(expert_output)

        stacked_expert_outputs = tf.stack(expert_outputs, axis=-1)
        expanded_expert_weights = tf.expand_dims(tf.expand_dims(expert_weights, axis=1), axis=1)
        combined_output = tf.reduce_sum(stacked_expert_outputs * expanded_expert_weights, axis=-1)

        next_token_logits = self.next_token_predictor(combined_output)
        next_token_logits = self.styler(next_token_logits)

        return next_token_logits
    

'''
class TransformerEncoder(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, 
                 num_heads=8, num_layers=7, dff_factor=4, **kwargs):
        super(TransformerEncoder, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window  # 序列长度 (time steps)
        self.units = units    # d_model
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.dff = dff_factor * units  # 前馈网络维度

        # 输入投影层（适配embedding_dim到d_model）
        self.input_projection = layers.Dense(units)
        
        # 可学习的位置编码
        self.position_embedding = self.add_weight(
            name="position_embedding",
            shape=(1, self.window, self.units),
            initializer="glorot_uniform",
            trainable=True
        )

        # Transformer编码器堆叠
        self.encoders = [
            TransformerBlock(self.units, self.num_heads, self.dff)
            for _ in range(num_layers)
        ]
        
        # 最终归一化
        self.final_norm = layers.LayerNormalization(epsilon=1e-6)

    def call(self, inputs, training=None):
        # 输入形状转换 (batch_size, window, embedding_dim) -> (batch_size, window, d_model)
        x = self.input_projection(inputs)
        
        # 添加位置编码
        x += self.position_embedding
        
        # 通过编码器堆叠
        for encoder in self.encoders:
            x = encoder(x, training=training)
        
        # 最终归一化
        return self.final_norm(x)

    def get_config(self):
        config = super().get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "window": self.window,
            "units": self.units,
            "num_heads": self.num_heads,
            "num_layers": self.num_layers,
            "dff_factor": self.dff // self.units
        })
        return config

class TransformerBlock(layers.Layer):
    def __init__(self, d_model, num_heads, dff, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.mha = layers.MultiHeadAttention(num_heads, key_dim=d_model//num_heads)
        self.ffn = tf.keras.Sequential([
            layers.Dense(dff, activation='relu'),
            layers.Dense(d_model)
        ])

        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(dropout_rate)
        self.dropout2 = layers.Dropout(dropout_rate)

    def call(self, x, training=None):
        # 多头注意力
        attn_output = self.mha(x, x)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(x + attn_output)

        # 前馈网络
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        out2 = self.layernorm2(out1 + ffn_output)

        return out2
   '''




from tensorflow.keras import layers
import tensorflow as tf

'''
class TransformerEncoder(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, 
                 num_heads=8, num_layers=12, dff_factor=2, max_position=800, **kwargs):
        super(TransformerEncoder, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window  # 最大序列长度
        self.units = units    # d_model
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.dff = dff_factor * units
        self.max_position=max_position

        # 输入投影层（适配任意embedding_dim）
        self.input_projection = layers.Dense(units)
        
        # 可学习的位置编码（支持最大window长度）
        self.position_embedding = self.add_weight(
            name="position_embedding",
            shape=(1, max_position, self.units),  # 保持最大长度
            initializer="glorot_uniform",
            trainable=True
        )

        # 编码器堆叠
        self.encoders = [
            TransformerBlock(self.units, self.num_heads, self.dff)
            for _ in range(num_layers)
        ]
        
        self.final_norm = layers.LayerNormalization(epsilon=1e-6)

    def call(self, inputs, training=None):
        # 动态获取序列长度
        seq_length = tf.shape(inputs)[1]
        
        # 输入投影
        x = self.input_projection(inputs)  # (B, T, D)
        
        # 动态截取位置编码
        position_emb = self.position_embedding[:, :seq_length, :]
        x += position_emb
        
        # 通过编码器堆叠
        for encoder in self.encoders:
            x = encoder(x, training=training)
        
        return self.final_norm(x)

    def get_config(self):
        # 保持与原实现一致
        return super().get_config()

class TransformerBlock(layers.Layer):
    def __init__(self, d_model, num_heads, dff, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.mha = layers.MultiHeadAttention(
            num_heads=num_heads,
            key_dim=d_model//num_heads,
            # 关键设置：支持动态注意力掩码
            attention_axes=(1,)  # 仅在序列维度做注意力
        )
        self.ffn = tf.keras.Sequential([
            layers.Dense(dff, activation='relu'),
            layers.Dense(d_model)
        ])

        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(dropout_rate)
        self.dropout2 = layers.Dropout(dropout_rate)

    def call(self, x, training=None):
        # 自动处理变长序列的注意力掩码
        attn_output = self.mha(x, x)  # 自动处理因果掩码
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(x + attn_output)

        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
'''

import tensorflow as tf
from tensorflow.keras import layers

class TransformerEncoder(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, 
                 num_heads=8, num_layers=12, dff_factor=2,
                 max_position=800, tst=False,**kwargs):
        super(TransformerEncoder, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window  # 最大处理序列长度
        self.units = units    # d_model
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.dff = dff_factor * units
        self.max_position = max_position

        # 确保max_position >= window以支持位置编码
        if max_position < window:
            raise ValueError(f"max_position must be >= window, but got {max_position} < {window}")

        # 输入投影层
        self.input_projection = layers.Dense(units, trainable=bool(1-tst))
        
        # 可学习的位置编码（支持最大max_position长度）
        self.position_embedding = self.add_weight(
            name="position_embedding",
            shape=(1, max_position, self.units),
            initializer="glorot_uniform",
            trainable=bool(1-tst)
        )

        # 编码器堆叠
        self.encoders = [
            TransformerBlock(self.units, self.num_heads, self.dff, tst=tst)
            for _ in range(num_layers)
        ]
        
        self.final_norm = layers.LayerNormalization(epsilon=1e-6)

    def call(self, inputs, training=None):
        # 输入投影
        x = self.input_projection(inputs)  # (B, T, D)
        
        # 截断输入到window长度
        x = x[:, -self.window:, :]
        seq_length = tf.shape(x)[1]  # 实际序列长度（<= window）
        
        # 动态截取位置编码
        position_emb = self.position_embedding[:, :seq_length, :]
        x += position_emb
        
        # 通过编码器堆叠
        for encoder in self.encoders:
            x = encoder(x, training=training)
        
        return self.final_norm(x)

    def get_config(self):
        config = super().get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "window": self.window,
            "units": self.units,
            "num_heads": self.num_heads,
            "num_layers": self.num_layers,
            "dff_factor": self.dff_factor,
            "max_position": self.max_position
        })
        return config

class TransformerBlock(layers.Layer):
    def __init__(self, units, num_heads, dff, tst=False, dropout_rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=units, trainable=bool(1-tst))
        self.ffn = tf.keras.Sequential([
            layers.Dense(dff, activation='relu', trainable=bool(1-tst)),
            layers.Dense(units, trainable=bool(1-tst))
        ])
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(dropout_rate)
        self.dropout2 = layers.Dropout(dropout_rate)

    def call(self, inputs, training=None):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)







if 1:
    def build_model(vocab_size, embedding_dim, rnn_units,
                    batch_size,mt=2.2,window=128,
                    ):
      #global mt
      if mt==40.23:
        # 参数设置
        maxlen = window
        #vocab_size = 20000
        embed_dim = embedding_dim

        num_experts = 1

        # 创建专家
        expert1 = CLModel_40_1(vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    #find_window=rnn_units['find_window'],
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
                    embed_q=rnn_units['embed_q'],
                    
                    )
        
        #TransformerBlock(embed_dim, num_heads, ff_dim)
        experts = [expert1]

        # 创建路由机制
        router = create_router(num_experts)

        # 创建MoE模型
        moe_model = MoEModel_40_2(experts, vocab_size)

        # 输入层
        input_layer = layers.Input(shape=(maxlen,))
        x = TokenAndPositionEmbedding_40_2(maxlen, vocab_size, embed_dim)(input_layer)
        output = moe_model(x)

        # 构建完整模型
        model = tf.keras.Model(inputs=input_layer, outputs=output)
        return model
      elif mt==41.23:
        # 参数设置
        maxlen = window
        #vocab_size = 20000
        embed_dim = embedding_dim

        num_experts = 1

        # 创建专家
        expert1 = CLModel_41_1(vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    #find_window=rnn_units['find_window'],
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
                    embed_q=rnn_units['embed_q'],
                    
                    )
        
        #TransformerBlock(embed_dim, num_heads, ff_dim)
        experts = [expert1]

        # 创建路由机制
        router = create_router(num_experts)

        # 创建MoE模型
        moe_model = MoEModel_40_2(experts, vocab_size)

        # 输入层
        input_layer = layers.Input(shape=(maxlen,))
        x = TokenAndPositionEmbedding_40_2(maxlen, vocab_size, embed_dim)(input_layer)
        output = moe_model(x)

        # 构建完整模型
        model = tf.keras.Model(inputs=input_layer, outputs=output)
        return model
      elif  mt==40.231 or mt==40.232:
        # 参数设置
        maxlen = window
        #vocab_size = 20000
        embed_dim = embedding_dim

        num_experts = 1

        # 创建专家
        expert1 = CLModel_40_1(vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    #find_window=rnn_units['find_window'],
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
                    embed_q=rnn_units['embed_q'],
                    
                    )
        
        #TransformerBlock(embed_dim, num_heads, ff_dim)
        experts = [expert1]

        # 创建路由机制
        router = create_router(num_experts)

        # 创建MoE模型
        moe_model = MoEModel_40_2(experts, vocab_size)

        # 输入层
        input_layer = layers.Input(shape=(None,))
        x = TokenAndPositionEmbedding_40_231(maxlen, vocab_size, embed_dim)(input_layer)
        output = moe_model(x)

        # 构建完整模型
        model = tf.keras.Model(inputs=input_layer, outputs=output)
        return model
      elif mt==40.23101 or mt==40.23101001:
        # 参数设置
        maxlen = window
        #vocab_size = 20000
        embed_dim = embedding_dim

        num_experts = 1

        # 创建专家
        expert1 = CLModel_40_1_01(vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    #find_window=rnn_units['find_window'],
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
                    embed_q=rnn_units['embed_q'],
                    
                    )
        
        #TransformerBlock(embed_dim, num_heads, ff_dim)
        experts = [expert1]

        # 创建路由机制
        router = create_router(num_experts)

        # 创建MoE模型
        moe_model = MoEModel_40_2(experts, vocab_size)

        # 输入层
        input_layer = layers.Input(shape=(None,))
        x = TokenAndPositionEmbedding_41_01(
            maxlen, vocab_size, embed_dim
            )(input_layer)
        output = moe_model(x)

        # 构建完整模型
        model = tf.keras.Model(inputs=input_layer, outputs=output)
        return model
      elif mt==40.31:
        # 参数设置
        maxlen = window
        #vocab_size = 20000
        embed_dim = embedding_dim

        
        
        # 创建专家
        expert1 = [CLModel_40_1_01(vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    #find_window=rnn_units['find_window'],
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
                    embed_q=rnn_units['embed_q'],
                    n=rnn_units['n_layer'])]*1

        
                
        expert2=[ClassicLSTMModel(
            vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
            )]*1

        expert3=[
            TransformerEncoder(
            vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    window=rnn_units['trans_window'],
                    units=rnn_units['rnn_units'],
            max_position=rnn_units['maxlen'],
             num_layers=rnn_units['trans_layers'],
            dff_factor=rnn_units['dff_factor'],
            )]*1
        
        #TransformerBlock(embed_dim, num_heads, ff_dim)
        experts = expert1+expert2+expert3

        # 创建路由机制
        #router = create_router(num_experts)

        # 创建MoE模型
        moe_model = MoEModel_40_1_01_large(experts, vocab_size,
                                  num_experts=3,
                                  router_units=rnn_units['router_units'],
                                           
                                  )

        # 输入层
        input_layer = layers.Input(shape=(None,))
        x = TokenAndPositionEmbedding_41_01(
            maxlen, vocab_size, embed_dim
            )(input_layer)
        #x = layers.BatchNormalization()(x)
        #x = layers.BatchNormalization()(x)
        output = moe_model(x)

        # 构建完整模型
        model = tf.keras.Model(inputs=input_layer, outputs=output)
        return model

      elif mt==40.3101:
        # 参数设置
        maxlen = window
        #vocab_size = 20000
        embed_dim = embedding_dim

        
        
        # 创建专家
        expert1 = [CLModel_40_1_01(vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    #find_window=rnn_units['find_window'],
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
                    embed_q=rnn_units['embed_q'],
                    n=rnn_units['n_layer'])]*1

        
                


        expert3=[
            TransformerEncoder(
            vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    window=rnn_units['trans_window'],
                    units=rnn_units['rnn_units'],
            max_position=rnn_units['maxlen'],
             num_layers=rnn_units['trans_layers'],
            dff_factor=rnn_units['dff_factor'],
            )]*1
        
        #TransformerBlock(embed_dim, num_heads, ff_dim)
        experts = expert1+expert3

        # 创建路由机制
        #router = create_router(num_experts)

        # 创建MoE模型
        moe_model = MoEModel_40_1_01_large(experts, vocab_size,
                                  num_experts=2,
                                  router_units=rnn_units['router_units'],
                                           
                                  )

        # 输入层
        input_layer = layers.Input(shape=(None,))
        x = TokenAndPositionEmbedding_41_01(
            maxlen, vocab_size, embed_dim
            )(input_layer)
        #x = layers.BatchNormalization()(x)
        #x = layers.BatchNormalization()(x)
        output = moe_model(x)

        # 构建完整模型
        model = tf.keras.Model(inputs=input_layer, outputs=output)
        return model
      elif mt==40.31666:
        # 参数设置
        maxlen = window
        #vocab_size = 20000
        embed_dim = embedding_dim

        
        
        # 创建专家
        expert1 = [CLModel_40_1_01(vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    #find_window=rnn_units['find_window'],
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
                    embed_q=rnn_units['embed_q'],
                    n=rnn_units['n_layer'],
                                   tst=True
                                   )]*1

        
                
        expert2=[ClassicLSTMModel(
            vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
            tst=True 
            )]*1

        expert3=[
            TransformerEncoder(
            vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    window=rnn_units['trans_window'],
                    units=rnn_units['rnn_units'],
            max_position=rnn_units['maxlen'],
             num_layers=rnn_units['trans_layers'],
            dff_factor=rnn_units['dff_factor'],
            tst=True 
            )]*1
        
        #TransformerBlock(embed_dim, num_heads, ff_dim)
        experts = expert1+expert2+expert3

        # 创建路由机制
        #router = create_router(num_experts)

        # 创建MoE模型
        moe_model = MoEModel_40_1_01_large(experts, vocab_size,
                                  num_experts=3,
                                  router_units=rnn_units['router_units'],
                                         tst=True  
                                  )

        # 输入层
        input_layer = layers.Input(shape=(None,))
        x = TokenAndPositionEmbedding_41_01(
            maxlen, vocab_size, embed_dim
            )(input_layer)
        #x = layers.BatchNormalization()(x)
        #x = layers.BatchNormalization()(x)
        output = moe_model(x)

        # 构建完整模型
        model = tf.keras.Model(inputs=input_layer, outputs=output)
        return model
    
      else:
            raise Exception('MT Error!')
