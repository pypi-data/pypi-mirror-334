from sinatools.DataDownload import downloader
import os
from sinatools.ner.helpers import load_object
import pickle
import os
import torch
import pickle
import json
from argparse import Namespace

tagger = None
tag_vocab = None
train_config = None
print("ner started")
filename = 'Wj27012000.tar'
path =downloader.get_appdatadir()
model_path = os.path.join(path, filename)

_path = os.path.join(model_path, "tag_vocab.pkl")

with open(_path, "rb") as fh:
    tag_vocab = pickle.load(fh)
print("tag_vocab loaded")

train_config = Namespace()
args_path = os.path.join(model_path, "args.json")
print("args loaded")
with open(args_path, "r") as fh:
    train_config.__dict__ = json.load(fh)
print("steps 1")
model = load_object(train_config.network_config["fn"], train_config.network_config["kwargs"])
model = torch.nn.DataParallel(model)
print("steps 2")
if torch.cuda.is_available():
    model = model.cuda()
print("steps 3")
train_config.trainer_config["kwargs"]["model"] = model
tagger = load_object(train_config.trainer_config["fn"], train_config.trainer_config["kwargs"])
tagger.load(os.path.join(model_path,"checkpoints"))
print("steps 4")