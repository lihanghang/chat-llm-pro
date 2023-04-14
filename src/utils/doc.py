import hashlib
import json

import openai
import requests
import zipfile
import io
import time
import gzip
import os
import logging

from tqdm import tqdm

from web import api_server
from src.utils.doc_enum import DocField

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def request_api(base_url, endpoint, filename, output_dir, params=None, _async='flase', output_format='pdf'):
    """
    Send a request to the API endpoint and return the result.
    :param endpoint: The API endpoint URL.
    :param input_dir: The input file path.
    :param output_dir: The output directory path.
    :param _async: Whether to use asynchronous request (default is True).
    :return: The result of the API call.
    """
    headers = {'Content-Type': 'application/octet-stream'}
    if params:
        query = {}
        query.update(params)
    with open(filename, 'rb') as f:
        res = requests.post(url=base_url+endpoint,
                            headers=headers,
                            data=f,
                            params=query
                            )
        res.raise_for_status()
    if res.status_code == 200:
        return get_result(endpoint, res, output_dir, _async, output_format)


def get_result(endpoint, res, output_dir, _async, ouput_format):
    """
    Get the result of the API call.

    :param endpoint: The API endpoint URL.
    :param res: The API response.
    :param output_dir: The output directory path.
    :param _async: Whether the request was asynchronous (default is True).
    :return: The result of the API call.
    """
    if _async == 'true':
        while True:
            task_id = res.json()['data']['task']['id']
            parse_res = requests.get(url=endpoint + f'?task_id={task_id}')
            parse_res.raise_for_status()  # Raise an exception if the response status code is not 200.
            error = parse_res.headers.get('x-api-status')
            if error and parse_res.json()['error']['code'] in ['running', 'waiting']:
                time.sleep(1)
            else:
                # 返回解析结果，格式为zip包
                return save_result(parse_res, output_dir)
    else:
        return save_result(res, output_dir, ouput_format)


def save_result(res, output_dir, output_format='pdf'):
    """
    Save the result to a zip file and extract it to the output directory.

    :param res: The API response.
    :param output_dir: The output directory path.
    """
    if output_format in ['pdf', 'json']:
        with open(output_dir, 'wb') as fp:
            fp.write(res.content)
    else:
        filename = os.path.join(output_dir, 'result.zip')
        with io.BytesIO(res.content) as fp:
            with zipfile.ZipFile(fp) as zf:
                zf.extractall(output_dir)
        with gzip.open(filename, 'wb') as file_out:
            for chunk in res.iter_content(chunk_size=8192):
                file_out.write(chunk)


def parser_doc(input_file_path, store_origin_file_dir):
    """
    解析文档
    Args:
        store_origin_file_dir: 解析输出目录
        input_file_path:  输入文件路径
    Returns:

    """
    base_url = api_server
    docx2pdf, pdf2doc = 'docx2pdf', 'pdf2doc'
    ext, _ = get_file_ext_size(input_file_path)
    _, doc_name = get_file_name(input_file_path)
    try:
        if ext in ['.doc', '.docx']:
            convert_pdf_dir = f'{store_origin_file_dir}/{doc_name}.pdf'

            # docx2pdf
            query = {"table-border": None, 'output-format': 'pdf'}
            request_api(base_url=base_url, endpoint=docx2pdf, filename=input_file_path, params=query,
                        output_dir=convert_pdf_dir, _async='false')

            # pdf2doc
            query = {'text': 'true', 'output-format': 'zip', 'html': 'true'}
            request_api(base_url=base_url, endpoint=pdf2doc, filename=convert_pdf_dir, params=query,
                        output_dir=store_origin_file_dir, output_format='zip')
            return f'{store_origin_file_dir}/table.txt'
        elif ext in ['.pdf']:
            # pdf2doc 生成文本内容
            query = {'text': 'true', 'output-format': 'zip', 'html': 'true'}
            request_api(base_url=base_url, endpoint=pdf2doc, filename=input_file_path, params=query,
                        output_dir=store_origin_file_dir, output_format='zip')
            return f'{store_origin_file_dir}/table.txt'
        else:
            # 直接文本文件
            return input_file_path

    except Exception as e:
        logging.error(e)


def hashcode_with_file(file_path):
    with open(file_path, 'rb') as f:
        file_hashcode = hashlib.md5(f.read()).hexdigest()
    return file_hashcode


def get_file_ext_size(file_path):
    (_, ext) = os.path.splitext(file_path)  # /xx/xx/xxx  .xx
    file_size = os.path.getsize(file_path)  # bytes

    return ext, file_size


def get_file_name(file_path):
    file_dir, filename = os.path.split(file_path)
    return file_dir, filename


def read_file(file_path):
    with open(file_path, 'r') as fp:
        contents = fp.readlines()
        contents = [content.strip() for content in contents if content.strip()]
        return contents


def create_embedding(file_name):
    """
    Generate file embedding.
    Args:
        file_name:

    Returns:

    """
    result = []

    def get_embedding(input_slice):
        embedding = openai.Embedding.create(engine="text-embedding-ada-002", input=input_slice)
        return [(text, data.embedding) for text, data in zip(input_slice, embedding.data)], embedding.usage.total_tokens

    # TODO：解析doc.json 保留页码信息
    contents = read_file(file_name)
        
    lens = [len(text) for text in contents]
    query_len = 0
    start_index = 0
    tokens = 0
    if sum(lens) <= 4096:
        ebd, tk = get_embedding(contents[start_index:len(lens)-1])
        result.extend(ebd)
        return result
    else:
        for index, l in tqdm(enumerate(lens)):
            query_len += l
            if query_len > 4096:
                ebd, tk = get_embedding(contents[start_index:index + 1])
                query_len = 0
                start_index = index + 1
                tokens += tk
                result.extend(ebd)
        logging.info(f"doc2vector. tokens={tokens}")
        return result


class DocContent:
    def __init__(self, text_type, page_number, text):
        self.text_type = text_type
        self.page = page_number
        self.text = text
        self.embedding = None


if __name__ == '__main__':
    doc_json = 'data/store/da9b6be2f0fd7eaa506e2266a9100918/doc.json'
    with open(doc_json, 'r', encoding='utf-8') as f:
        doc_obj = json.loads(f.read())

    doc_result = []
    for item in doc_obj[DocField.ITEMS.value]:
        doc_result.append(DocContent(item[DocField.TYPE.value], item[DocField.PAGE_NUMBER.value], item[DocField.TEXT.value]))

    print(doc_result[0].text)
