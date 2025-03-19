'''
try:import test
except ImportError:
    import xiaothink.llm.inference.test as test
'''
import xiaothink.llm.inference.test as test
#form




class QianyanModel:
    def __init__(self,ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_test_40_2_3_qas',
               MT=40.231,
                 vocab=r'E:\小思框架\论文\ganskchat\vocab_lx3.txt'):
        self.model,self.d=test.load(ckpt_dir=ckpt_dir, model_type=MT,
                                    vocab=vocab)
        self.his=''
    #moe lyric:0.72
    def chat_SingleTurn(self,t,temp=0.8,maxlen=1200,form=1,ontime=True,loop=True,stop=None):#0.85
        
        if form==0:
            inp=f'{{"instruction": "{t}", "input": "", "output": "'
            stopc=['"}\r\n',
                   '"}\n\r',
                   '"}\n',
                   '", "input"',
                   '", "i',
                   '"}',
                   ]
        elif form==1:
            inp='{"conversations": [{"role": "user", "content": {inp}}, {"role": "assistant", "content": "'.replace('{inp}',t)
            stopc=[
                    '"}]}',
                    '"}',
                ]
        else:
            print('Err')
            
            return '-1: form error'
        if stop:
            stopc.append(stop)
        funct=None
        if ontime:
            funct=lambda a:print(a,end='',flush=True)
        if loop:
            inf=test.generate_texts_untilstr_loop
        else:
            inf=test.generate_texts_untilstr
            
        #print(funct)
        re=inf(self.model, self.d, inp,num_generate=maxlen,
                                 every=funct,
                                 temperature=temp,#0.8
                                stop_c=stopc
                                    #q=[0.6,0.4]
                                    )
        self.model.reset_states()
        return re
    def chat(self,text,temp=0.8,max_len=150,form=1,ontime=True,loop=False):
        text=text.replace('\n','\\n')
        if form==0:
            if self.his!='':
                self.his+='\\nHuman: '+text+'\\nAssistant:'
            else:
               self.his+='Human: '+text+'\\nAssistant:'
            #print('his',self.his)
            t=self.his
            
            inp=f'{{"instruction": "{t}", "input": "", "output": "'
            stopc=['"}\r\n',
                   '"}\n\r',
                   '"}\n',
                   '", "input"',
                   '", "i',
                   '"}',
                   '\\nHuman:',
                   ]
        elif form==1:
            if self.his!='':
                self.his+=', {"role": "user", "content": "{inp}"}'.replace('{inp}',text)
      
            else:
                self.his='{"role": "user", "content": "{inp}"}'.replace('{inp}',text)


            inp='{"conversations": [{his}, {"role": "assistant", "content": "'.replace('{his}',self.his)
            stopc=[
                    '"}]}',
                    '"}',
                ]
        else:
            print('Err')
            return '-1: form error'
        funct=None
        if ontime:
            funct=lambda a:print(a,end='',flush=True)
            print('\n【实时输出】')
        #print(funct)
        if loop:
            inf=test.generate_texts_untilstr_loop
        else:
            inf=test.generate_texts_untilstr
        re=inf(self.model, self.d, inp,num_generate=max_len,
                                 every=funct,
                                 temperature=temp,#0.8
                                stop_c=stopc
                                    #q=[0.6,0.4]
                                    )
        if form==0:
            self.his+=re
        elif form==1:
            self.his+=', {"role": "assistant", "content": "{inp}"}'.replace('{inp}',re)
      
        return re

    def clean_his(self):
        self.his=''

    def write(self,t,temp=0.85,max_len=150,form=0,ontime=True,onfunc=None):#0.62

        
        if ontime:
            funct=onfunc#lambda a:print(a,end='',flush=True)

        #print(funct)
        re=test.generate_texts_loop(self.model, self.d, t,num_generate=max_len,
                                 every=funct,
                                 temperature=temp,#0.8
                                    #q=[0.6,0.4]
                                    )
        return re
    
#你要写歌词，用神采为题
#用卫星图像显示中国向南海岛屿派歼11战机,已降落在永兴 岛,美菲将讨论中国“挑衅”行为。为题写报道
        
if __name__=='__main__':
    model=QianyanModel()
    while True:
        inp=input('【问】：')
        if inp =='[CLEAN]':
            print('【清空上下文】\n\n')
            model.clean_his()
            continue
        re=model.chat(inp,temp=0.55)#model.chat_SingleTurn(inp)
        print('\n【答】：',re,'\n')
