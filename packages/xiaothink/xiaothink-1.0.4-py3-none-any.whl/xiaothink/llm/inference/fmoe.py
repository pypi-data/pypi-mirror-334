import os
import json
import pandas as pd
import re
from tqdm import tqdm
import random
import time
import requests
from xiaothink.llm.inference.test_formal import *
model=QianyanModel(MT=40.23101,
                   ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_test_40_23101_tiny_moe_dish',
                   vocab=r'E:\小思框架\论文\ganskchat\vocab_lx3.txt'
                   )

def chat_x(inp,temp=0.3):
    return model.chat_SingleTurn(inp,temp=temp,loop=True)#



