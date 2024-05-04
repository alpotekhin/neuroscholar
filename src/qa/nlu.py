from transformers import RobertaTokenizerFast, RobertaForSequenceClassification, TextClassificationPipeline

def get_intent_classifier(hf_path="bespin-global/klue-roberta-small-3i4k-intent-classification"):
    loaded_tokenizer = RobertaTokenizerFast.from_pretrained(hf_path)
    loaded_model = RobertaForSequenceClassification.from_pretrained(hf_path)
    
    text_classifier = TextClassificationPipeline(
        tokenizer=loaded_tokenizer, 
        model=loaded_model, 
        return_all_scores=True
    )
    
    return text_classifier

class HuggingFaceModelSingleton:
    _instance = None

    @classmethod
    def get_instance(cls, hf_path="bespin-global/klue-roberta-small-3i4k-intent-classification"):
        """Create or return the already created Hugging Face model instance"""
        if not cls._instance:
                loaded_tokenizer = RobertaTokenizerFast.from_pretrained(hf_path)
                loaded_model = RobertaForSequenceClassification.from_pretrained(hf_path)
                
                cls._instance = TextClassificationPipeline(
                    tokenizer=loaded_tokenizer, 
                    model=loaded_model, 
                    return_all_scores=True
                )
                
        return cls._instance

def classify_message(message):
    classifier = HuggingFaceModelSingleton.get_instance()
    preds_list = classifier(message)[0]
    label_score_dict = {item['label']: item['score'] for item in preds_list}
    
    return label_score_dict
    



