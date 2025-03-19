Usage Sample
''''''''''''

.. code:: python

        import torch
        from nerx import NER
        from model_wrapper import ClassifyModelWrapper
        
        model = NER('hlf/rb3', num_classes=8)
        wrapper = ClassifyModelWrapper(model)
        history = wrapper.train(train_set, val_set, collate_fn=collate_fn)
