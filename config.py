from pathlib import Path

PATH_DATA = Path('data')
ABS_PATH_DATA = PATH_DATA.resolve()

PDF_AI = ABS_PATH_DATA / 'study_plan_AI.pdf'
PDF_PRODUCT = ABS_PATH_DATA / 'study_plan_PRODUCT.pdf'

URL_AI = 'https://abit.itmo.ru/program/master/ai'
URL_PRODUCT = 'https://abit.itmo.ru/program/master/ai_product'


XLSX_AI = ABS_PATH_DATA / 'product.xlsx'
XLSX_PRODUCT = ABS_PATH_DATA / 'ai.xlsx'