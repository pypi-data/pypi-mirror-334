from typing import Mapping, Tuple, List
import numpy as np
import torch

class Collator:
    """
    用于将数据样本转换为模型可处理的格式。
    
    初始化时接收一个tokenizer和一个可选的最大长度参数。
    调用时，接收一个包含文本和标签的示例列表，将文本转换为token，并将标签转换为张量。
    """

    def __init__(self, tokenizer, label_padding_id, max_length: int = 512):
        """
        初始化Collator。
        
        :param tokenizer: 用于将文本转换为token的tokenizer。
        :param max_length: 文本的最大长度，默认为512。
        """
        self.tokenizer = tokenizer
        self.label_padding_id = label_padding_id
        self.max_length = max_length
    
    def __call__(self, samples: List[Tuple[str, int]]) -> Tuple[Mapping, torch.Tensor]:
        """
        调用Collator时执行的操作。
        
        :param examples: 一个包含文本和标签的元组列表。
        :return: 一个包含token和对应标签的元组。
        """
        # 分离文本和标签
        texts, labels = zip(*samples)
        
        # 使用tokenizer将文本批量化编码为tokens
        tokens = self.tokenizer.batch_encode_plus(texts,
                                                max_length=self.max_length,
                                                padding=True,
                                                truncation=True,
                                                return_tensors='pt',
                                                return_token_type_ids=False,
                                                is_split_into_words=True)
        
        length = tokens['input_ids'].shape[1]
        for label in labels:
            label_len = len(label)
            if label_len < length:
                label += [self.label_padding_id] * (length - label_len)
            elif label_len > length:
                label = label[:length]
            
        # 将标签转换为LongTensor
        labels = torch.LongTensor(np.array(labels))
        # 确保labels的长度与input_ids一致
        return tokens, labels[:, :tokens['input_ids'].shape[1]]   
    