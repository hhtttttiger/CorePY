from azure.storage.blob import BlobServiceClient
from utils.config.config import load_config

class AzureStorage:
    def __init__(self, connection_string = None):
        """
        初始化 Azure 存储服务。
        
        Args:
            connection_string (str, optional): Azure 存储账户的连接字符串。如果未提供，则使用默认的连接字符串。
        """
        if(connection_string is None):
            config = load_config()
            connection_string = config["storage_account_connect_string"]
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    

    def get_container_client(self, container_name):
        return self.blob_service_client.get_container_client(container_name)
    

    def upload_file_from_path(self, container_name, file_path, blob_name):
        """
        从本地文件路径上传文件到指定的 Blob 容器。
        
        Args:
            container_name (str): Blob 容器名称。
            file_path (str): 本地文件的路径。
            blob_name (str): 要上传到 Blob 容器的 Blob 名称。
        """
        container_client = self.get_container_client(container_name)
        with open(file_path, "rb") as data:
            container_client.upload_blob(blob_name, data, overwrite=True)
    

    def upload_file_from_stream(self, container_name, file_stream, blob_name):
        """
        从文件流上传文件到指定的 Blob 容器。
        
        Args:
            container_name (str): Blob 容器名称。
            file_stream (file-like object): 文件流对象。
            blob_name (str): 要上传到 Blob 容器的 Blob 名称。
        """
        container_client = self.get_container_client(container_name)
        container_client.upload_blob(blob_name, file_stream, overwrite=True)


    def get_blob(self, container_name, blob_name):
        """
        获取 Blob 的文件流。
        
        Args:
            container_name (str): Blob 容器名称。
            blob_name (str): 要获取信息的 Blob 名称。
        
        Returns:
            dict: 文件流。
        """
        container_client = self.get_container_client(container_name)
        try:
            blob_client = container_client.get_blob_client(blob_name)
            blob_data = blob_client.download_blob()
            file_stream = blob_data.readall()  # 获取文件流
            return file_stream
        except Exception as e:
            print(f"Error getting blob info for '{blob_name}': {e}")
            return None
