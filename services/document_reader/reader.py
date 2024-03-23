from datetime import datetime
from io import BytesIO, StringIO
from fastapi import UploadFile
import mammoth
import markdownify
import shutil
import os
from db.database import Database
from pypdf import PdfReader
from utils.azure_storage import AzureStorage
from utils.snowflake_id import SnowflakeUtil
import utils.file_utils
import fitz
import pandas as pd
import uuid


class FileInfo:
    def __init__(self, id, workspace_id, path, container_name, name):
        self.id = id
        self.workspace_id = workspace_id
        self.file_path = path
        self.container_name = container_name
        self.file_name = name

FileID = None
async def reader(file: UploadFile):
    file_type = utils.file_utils.get_file_extension(file.file_name)
    text = choose_branch(file_type)(file.file, file.file_name)

    return text

def choose_branch(file_type):
    branches = {
        'pdf': fitz_pdf_handle,
        'docx': docx_handle,
        'xlsx': xlsx_hadle
    }
    return branches.get(file_type)


def pypdf_handle(file_stream, file_info):
    """
        这个方法会提取pdf里面的图片保存
    """
    text = ""
    count = 0
    image_list = []

    # 创建临时目录存储图片
    root_directory = str(file_info.id)
    if not os.path.exists(root_directory):     
        os.makedirs(root_directory)

    with BytesIO(file_stream) as f:
        reader = PdfReader(f)  

        for page in reader.pages:
            count += 1
            text += page.extract_text()

            page.ex
            for image_file_object in page.images:
                file_name = f'page_{str(count)}{image_file_object.name}'
                file_path = os.path.join(root_directory, file_name)
                with open(file_path, "wb") as fp:
                    fp.write(image_file_object.data)

                file = assemble_file(file_name, root_directory, file_path)
                image_list.append(file)
                text += f'[{file["Id"]}]'

    upload_file(root_directory)
    save_file(image_list)
    shutil.rmtree(root_directory)

    return text


def fitz_pdf_handle(file_stream, file_info,):
    """
        这个方法会将带图片的那一页转换为图片
    """
    text = ""
    page_image_list = []
    # 创建临时目录存储图片
    root_directory = str(file_info.id)
    if not os.path.exists(root_directory):     
        os.makedirs(root_directory)

    with BytesIO(file_stream) as f:
        reader = fitz.open(stream= f)
    
        for page in reader:
            text += page.get_text()
            image_list = page.get_images()
            if image_list:
                file_name = "page-%i.png" % page.number
                file_path = os.path.join(root_directory, file_name)
                page.get_pixmap().save(file_path)

                file = assemble_file(file_name, root_directory, file_path)
                page_image_list.append(file)
                text += f'[{file["Id"]}]'

    upload_file(root_directory)
    if(page_image_list):
        save_file(page_image_list)
    shutil.rmtree(root_directory)

    return text


def docx_handle(file_stream, file_info):
    root_directory = str(file_info.id)
    page_image_list = []
    if not os.path.exists(root_directory):     
        os.makedirs(root_directory)

    # 转存 docx 文档内的图片
    def docx_convert_image(image):
        with image.open() as image_bytes:
            file_suffix = image.content_type.split("/")[1]

            file_name = f"image{uuid.uuid1()}.{file_suffix}"
            path_file = f"./{root_directory}/{file_name}"
            with open(path_file, 'wb') as f:
                f.write(image_bytes.read())
            
            page_image_list.append(assemble_file(file_name, root_directory, path_file))

        return {"src":path_file}

    # docx转htm
    with BytesIO(file_stream) as f:
        result = mammoth.convert_to_html(f, convert_image=mammoth.images.img_element(docx_convert_image))
        html = result.value
        # html转md
        md = markdownify.markdownify(html,heading_style="ATX")

    upload_file(root_directory)
    if(page_image_list):
        save_file(page_image_list)

    shutil.rmtree(root_directory)

    return md

def xlsx_hadle(file_stream, file_info):
    string_builder = StringIO()
    with BytesIO(file_stream) as f:
        excel_file = pd.ExcelFile(f)
        # 读取Excel文件中的第一个表格
        with pd.ExcelFile(f) as excel_file:
            df = pd.read_excel(excel_file, sheet_name=excel_file.sheet_names[0])

        # 获取表头
        header_str = list_to_md_table(df.columns.tolist())

        split_str = '|'
        for _ in range(df.columns.size):
            split_str += ' --- |'

        header_len = len(header_str)

        new_table = True
        current_length = header_len
        for _, row in df.iterrows():
            if new_table:
                new_table = False
                string_builder.write(f'{header_str}\n')
                string_builder.write(f'{split_str}\n')
            row_str = ' | '.join([str(item) for item in row])
            row_length = len(row_str)
            string_builder.write(f'| {row_str} |\n')

            current_length += row_length
            # 如果当前行加上表头超过了 1024 个字符，则保存当前小表格并重新开始
            if current_length > 1024:
                current_length = header_len
                new_table = True

    result = string_builder.getvalue()
    string_builder.close()

    return result

def list_to_md_table(list):
    builder = StringIO()
    for item in list:
        builder.write('|' + item)
    builder.write(' |')
    
    result = builder.getvalue()
    builder.close()
    
    return result

# 文件上传
def upload_file(directory: str, azure_storage: AzureStorage):
    pass

# 文件持久化
def save_file(file_list: list):
    pass

def assemble_file(file_name: str, root_directory: str, file_path: str):
    utc_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    image_id = SnowflakeUtil.generate_id(machine_id=1)
    return {
                "Id": image_id, 
                "FileName": file_name,
                "ExtensionName": "." + utils.file_utils.get_file_extension(file_name),
                "FilePath": "/" + root_directory,
                "Size": os.path.getsize(file_path),
                "ContainerName": "",
                "OriginalName": file_name,
                "FileMd5": utils.file_utils.calculate_file_md5(file_path),
                "Modified": utc_now,
                "Created": utc_now
            }