from pdfminer import high_level
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()

with open('raw_data/euromar_abstract_books/Euromar_2017_abstracts_p26-28.pdf', 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(),
                       output_type='html', codec=None)
