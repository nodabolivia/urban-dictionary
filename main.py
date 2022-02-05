from utils import OptycalCharacterRecognizer

ocr = OptycalCharacterRecognizer('chat.png')
# NORMAL
result = ocr.process(2)
# WITH API OCR
#result = ocr.process(2)

ocr.definition_term(result)
#ocr.definition_term2(result)
