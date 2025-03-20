Usage Sample
''''''''''''

.. code:: python

        import torch
        from torch.utils.data import Dataset
        from transformers import AutoTokenizer
        from nerx import NER, Collator
        from model_wrapper import ClassifyModelWrapper

        pretrained_path = "nghuyong/ernie-3.0-base-zh"
        classes = ['O', 'B-PER', 'I-PER', 'B-ORG', 'I-ORG', 'B-LOC', 'I-LOC', 'padding']

        def f(data):
                return 5 < len(data['tokens']) <= 512 - 2

        class PairDataset(Dataset):

                def __init__(self, dataset):
                        self.dataset = dataset

                def __getitem__(self, index):
                        data = self.dataset[index]
                        return data['tokens'], data['ner_tags']

                def __len__(self):
                        return len(self.dataset)

        dataset_dict = load_from_disk('/kaggle/input/peoples-daily-ner-data/peoples_daily_ner')
        train_set = dataset_dict['train'].remove_columns(['id']).filter(f, cache_file_name='/kaggle/working/train.cache')
        val_set = dataset_dict['validation'].remove_columns(['id']).filter(f, cache_file_name='/kaggle/working/val.cache')
        test_set = dataset_dict['test'].remove_columns(['id']).filter(f, cache_file_name='/kaggle/working/test.cache')

        train_set = PairDataset(train_set)
        val_set = PairDataset(val_set)
        
        model = NER(pretrained_path, num_classes=8, num_train_layers=2)
        wrapper = ClassifyModelWrapper(model)
        tokenizer = AutoTokenizer.from_pretrained(pretrained_path)
        history = wrapper.train(train_set, val_set, collate_fn=Collator(tokenizer, label_padding_id=7))
        wrapper.save_state_dict(mode='best')

        def display(tags, text, classes):
                padding_idx = len(classes) - 1
                start_index, start_tag = -1, -1
                for i, tag in enumerate(tags):
                        if tag == padding_idx:
                        if start_index != -1:
                                print(f"{start_index}-{i}", ' ', classes[start_tag].split('-')[1], ' ', ''.join(text[start_index:i]))
                        break

                        if 0 < tag:
                        if start_index == -1 and 0 < tag:
                                start_index, start_tag = i, tag
                                continue
                                
                        if start_tag != tag - 1 and start_tag != tag:
                                print(f"{start_index}-{i}", ' ', classes[start_tag].split('-')[1], ' ', ''.join(text[start_index:i]))
                                start_index, start_tag = i, tag 
                        else:
                        if start_index > -1:
                                print(f"{start_index}-{i}", ' ', classes[start_tag].split('-')[1], ' ', ''.join(text[start_index:i]))
                                start_index, start_tag = -1, -1

        def test(data, model):
                M, N = 40, 30
                text, label = data['tokens'], data['ner_tags']
                tokens = tokenizer.batch_encode_plus([text],
                                                max_length=256,
                                                padding=True,
                                                truncation=True,
                                                return_tensors='pt',
                                                return_token_type_ids=False,
                                                is_split_into_words=True)
                model.eval()
                with torch.no_grad():
                        result = model(tokens)[0]
                print('=' * M, "原文", '=' * M)
                print(''.join(text))
                print('-' * N, "标注",'-' * N)
                display(label, text, classes)
                print('-' * N, "预测",'-' * N)
                display(result, text, classes)

        for i in range(20):
                test(test_set[i], model)
