from sentence_transformers import SentenceTransformer, util
import torch
from summarizer.sbert import SBertSummarizer

model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
embedder = SentenceTransformer('all-mpnet-base-v2')



def check_news(new_body, new_header, records):
    return True
    new_text_sum = model(new_body, num_sentences=4)
    news_text_all = embedder.encode(new_header, convert_to_tensor=True) + \
                    embedder.encode(new_body, convert_to_tensor=True) + \
                    embedder.encode(new_text_sum, convert_to_tensor=True)
    for record in records:
        text_in_base_header = record[0]
        text_in_base_text = record[1]
        text_in_base_sum = model(text_in_base_text, num_sentences=4)
        text_in_base_all = embedder.encode(text_in_base_header, convert_to_tensor=True) + embedder.encode(
            text_in_base_text, convert_to_tensor=True) + embedder.encode(text_in_base_sum,
                                                                         convert_to_tensor=True)
        cos_scores = util.cos_sim(news_text_all, text_in_base_all)[0]
        if cos_scores > 0.79:
            print(cos_scores)
            return False
    return True