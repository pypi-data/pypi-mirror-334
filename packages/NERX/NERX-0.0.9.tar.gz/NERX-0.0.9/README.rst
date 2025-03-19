Usage Sample
''''''''''''

.. code:: python

        import torch
        from transformers import AutoTokenizer
        from nerx import NER, Collator
        from model_wrapper import ClassifyModelWrapper
        
        model = NER('hlf/rb3', num_classes=8)
        tokenizer = AutoTokenizer.from_pretrained('hlf/rb3')
        wrapper = ClassifyModelWrapper(model)
        history = wrapper.train(train_set, val_set, 
                                collate_fn=Collator(tokenizer, label_padding_id=7))
