from typing import List, Tuple
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from .crf import CRF
from transformers import AutoModel, AutoConfig

from .collator import Collator

__all__ = ['NER', 'Collator']

class NER(nn.Module):
    
    def __init__(self, pretrained_path, num_classes, bidirectional=True, num_train_layers=0, rnn=nn.GRU):
        """
        初始化模型
        :param pretrained_path: 预训练模型路径
        :param num_classes: 类别数量
        :param bidirectional: RNN是否双向，默认为True
        :param num_train_layers (int): 需要训练的预训练模型层数量，默认为0，表示不训练任何层。
        """
        super().__init__()
        # 从预训练路径加载配置
        config = AutoConfig.from_pretrained(pretrained_path)
        # 加载预训练模型
        self.pretrained = AutoModel.from_pretrained(pretrained_path)
        # 定义RNN层
        self.rnn = rnn(config.hidden_size, config.hidden_size, bidirectional=bidirectional, batch_first=True)
        # 定义全连接层
        self.fc = nn.Linear(config.hidden_size << 1 if bidirectional else config.hidden_size, num_classes)
        # 定义CRF层
        self.crf = CRF(num_classes, batch_first=True)
        # 存储类别数量
        self.num_classes = num_classes
        # 冻结预训练模型部分参数
        if num_train_layers <= 0:
            for param in self.pretrained.parameters():
                param.requires_grad_(False)
        else:
            parameters = list(self.pretrained.parameters())
            if num_train_layers < len(parameters):
                for param in parameters[:num_train_layers]:
                    param.requires_grad_(False)
                for param in parameters[num_train_layers:]:
                    param.requires_grad_(True)
            else:
                for param in parameters:
                    param.requires_grad_(True)
                
    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor, 
                token_type_ids: torch.Tensor = None) -> List[List[int]]:
        """
        前向传播
        :param tokenizies: 分词后的输入数据
        :return: 解码后的结果
        """
        # 获取发射分数
        emissions = self._do_forward(input_ids, attention_mask, token_type_ids)
        mask = attention_mask.new_ones(attention_mask.shape, dtype=torch.uint8)
        for i in range(mask.shape[0]):
            length = attention_mask[i].sum() - 2
            mask[i][length:] = 0
        return self.crf.decode(emissions, mask.bool())

    def fit(self, input_ids: torch.Tensor, attention_mask: torch.Tensor, labels: torch.Tensor, 
            token_type_ids: torch.Tensor = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        训练模型
        :param tokenizies: 分词后的输入数据
        :param labels: 标签
        :return: 损失和解码后的结果
        """
        emissions = self._do_forward(input_ids, attention_mask, token_type_ids)
        # 创建掩码，忽略padding部分
        mask = labels < self.num_classes
        # 计算CRF损失
        loss = -self.crf(emissions, labels, mask=mask)
        return loss, torch.tensor(self.crf.decode(emissions, mask), dtype=torch.long)
    
    def _do_forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor, 
                token_type_ids: torch.Tensor = None) -> torch.Tensor: 
        """
        :param tokenizies: 分词后的输入数据
        """
        self.rnn.flatten_parameters()

        lengths = [m.sum() for m in attention_mask.cpu()]
        lengths = torch.stack(lengths)
        # 获取预训练模型的输出
        outputs = self.pretrained(nput_ids=input_ids, attention_mask=attention_mask, 
                                token_type_ids=token_type_ids, output_hidden_states=True)

        # 通过RNN处理输出
        outputs = pack_padded_sequence(outputs.last_hidden_state, lengths, batch_first=True, enforce_sorted=False)
        outputs, _ = self.rnn(outputs)
        outputs, _ = pad_packed_sequence(outputs, batch_first=True)
            
        # 通过全连接层处理输出
        return self.fc(outputs)
    