from generator import Onto_generator
from reader import PDFSentenceExtractor
from rag_implemention import RAG, Retriever
import config
import util

extractor = PDFSentenceExtractor(pdf_name='Effects of Defects on Thermal Transport.pdf')
sentence_list = extractor.extractor()
rag_retriver = Retriever(onto_file="MatOnto.owl")
ontology_generator = Onto_generator(model_name=config.model_name, load_type="simple_model", token="")
tokenizer = ontology_generator.tokenizer

out = []
for sentence in sentence_list:
    sentence_similarity = rag_retriver.retrieve(query=sentence, top_k=3)
    if sentence_similarity[0][2] < 0.2:
        continue
    else:
        context = '\n'.join(sentence_similarity[0][1])
        prompt = util.prompt_filler(
                    promt_template=config.ds_prompt,
                    instruction=config.instruction,
                    text=context,
                    sentence=sentence,
                    tokenizer=tokenizer
                )
        out.append(ontology_generator.onto_generate(prompt))