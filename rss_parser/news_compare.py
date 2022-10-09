from transformers import pipeline

emotional_coloring_classifier = pipeline("zero-shot-classification",
                                         model="cointegrated/rubert-base-cased-nli-threeway")


def emotional_classification(sequence_to_classify):
    candidate_labels = ['хорошо', 'плохо', 'нейтрально']
    """
    Выдаст строку
    """
    return emotional_coloring_classifier(sequence_to_classify, candidate_labels)['labels'][0]


tag_dict = {
    'налог': 1,
    'выплата': 2,
    'пенсия': 3,
    'другое': 4,
    'война': 5,
    'утечка данных': 6,
    'компьютер': 7,
    'нейросеть': 8
}
classifier = pipeline("zero-shot-classification", model="cointegrated/rubert-base-cased-nli-threeway")


def news_tagger(news,
                labels=['налог', 'выплата', 'пенсия', 'другое', 'война', 'утечка данных', 'компьютер', 'нейросеть']):
    answer = classifier(news, labels)
    tag = answer['labels'][0]
    tag_score = answer['scores'][0]
    return tag_dict[tag], tag_score


"""
Выдача именованных сущностей
"""

from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsNERTagger, Doc


def ner_tagger(news):
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()
    ner_tagger = NewsNERTagger(emb)
    doc = Doc(news)
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)
    for span in doc.spans:
        span.normalize(morph_vocab)
    normal = []
    for i in doc.spans:
        normal.append(f'{i.normal} -- {i.type}')

    for info in set(normal):
        info_sp = info.split(' -- ')
        yield (info_sp[0], info_sp[1])
    """
    ЛНР -- LOC
    Starlink -- ORG
    ДНР -- LOC
    Financial Times -- ORG
    Илону Маску -- PER
    Херсонской -- LOC
    Харькова -- LOC
    Запорожской областей -- LOC

    """
    return '', ''
