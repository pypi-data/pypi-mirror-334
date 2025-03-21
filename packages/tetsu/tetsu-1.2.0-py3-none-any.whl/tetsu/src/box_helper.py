# Box helper script

"""
This class will provide common functionalities with
the Box API specifically with the JWTAuth method

*** ---------------------- IMPORTANT ---------------------- ***

THIS CLASS REQUIRES THE LOG HELPER SCRIPT TO ALSO BE PRESENT IN YOUR PROJECT WRKDIR.
CHANGE THE IMPORT STATEMENT AS NEEDED TO CORRECTLY IMPORT LOG_HELPER OR REMOVE THE LOGGER
FROM THE CLASS
"""

import pandas as pd
from boxsdk import Client, JWTAuth
from boxsdk.exception import BoxAPIException

from tetsu.src.log_helper import logger

logger = logger(name=__name__, handler="console")


class BoxHelper:
    def __init__(
        self,
        path: str = None,
        manual_auth: bool = False,
        manual_auth_config: dict = None,
    ):
        """
        Initialization function for the BOXHelper class
        :param path: The local path to the JWTAuth JSON file. *** Not needed if manual_auth = True ***
        :param manual_auth: If True, JWTAuth JSON file content must be passed through a config dict. Default = False
        :param manual_auth_config: If manual_auth = True, pass a dictionary with the following structure...
                                   {'client_id': '***YOUR_CLIENT_ID***',
                                    'client_secret': '***YOUR_CLIENT_SECRET***',
                                    'enterprise_id': '***YOUR_ENTERPRISE_ID***',
                                    'jwt_key_id': '***YOUR_JWT_KEY_ID***',
                                    'rsa_private_key_passphrase': '***YOUR_RSA_PRIVATE_KEY_PASSPHRASE***',
                                    'rsa_private_key_data': b'***YOUR_RSA_PRIVATE_KEY_DATA***'}
                                    * NOTE * : The keys of the dictionary must be
                                               exactly as the ones shown in the example
        """
        keys = [
            "client_id",
            "client_secret",
            "enterprise_id",
            "jwt_key_id",
            "rsa_private_key_passphrase",
            "rsa_private_key_data",
        ]

        if manual_auth:
            for key in keys:
                if key not in manual_auth_config.keys():
                    raise RuntimeError(
                        "The manual_auth_config parameter must contain the following keys: client_id, "
                        "client_secret, enterprise_id, jwt_key_id, rsa_private_key_passphrase, "
                        "rsa_private_key_data"
                    )
        self.path = path
        try:
            if manual_auth:
                self.client = Client(
                    JWTAuth(
                        client_id=manual_auth_config["client_id"],
                        client_secret=manual_auth_config["client_secret"],
                        enterprise_id=manual_auth_config["enterprise_id"],
                        jwt_key_id=manual_auth_config["jwt_key_id"],
                        rsa_private_key_passphrase=manual_auth_config[
                            "rsa_private_key_passphrase"
                        ],
                        rsa_private_key_data=manual_auth_config["rsa_private_key_data"],
                    )
                )
            else:
                self.client = Client(JWTAuth.from_settings_file(f"{path}"))
        except Exception as e:
            logger.exception(f"Could not authorize using JWTAuth method due to: {e}")
        else:
            logger.info("Box instance has been authorized...")

    def download_file(self, file_id: str, file_name: str) -> None:
        try:
            with open(file_name, "wb") as open_file:
                self.client.file(file_id).download_to(open_file)
                open_file.close()
        except Exception as e:
            logger.exception(f"Could not download file to local directory due to {e}")
        else:
            logger.info(
                f"{file_name} has successfully been downloaded to the local directory"
            )

    def download_file_as_df(
        self, file_id: str, file_type: str = "xlsx"
    ) -> pd.DataFrame:
        """
        Downloads a specified file from box. Currently, supports .xlsx, .csv, or .pkl
        :param file_id: A string of the ID of the file to be downloaded from box
        :param file_type: A string of the type of file. Currently, supports xlsx, csv, or pkl. Default = xlsx
        :return: The contents of the file
        """
        try:
            content = self.client.file(file_id=file_id).get_download_url()
        except Exception as e:
            logger.exception(f"Could not download file from box due to {e}")
        else:
            logger.info(f"File #{file_id} has been downloaded as a dataframe...")
            if file_type == "xlsx":
                return pd.read_excel(content)
            if file_type == "csv":
                return pd.read_csv(content)
            if file_type == "pkl":
                return pd.read_pickle(content)

    def upload_file(self, path: str, folder_id: str) -> None:
        """
        Uploads a specified file to a specified box folder

        :param path: A string of the local path to the file that will be uploaded
        :param folder_id: A string of the folder ID the file will be uploaded to
        """
        try:
            self.client.folder(folder_id).upload(path)
        except BoxAPIException as be:
            logger.exception(f"Could not upload file due to {be}")
        else:
            logger.info("File uploaded successfully...")

    def update_file(self, path: str, file_id: str) -> None:
        """
        Uploads a specified file to a specified box folder

        :param path: A string of the local path to the file that will be uploaded
        :param file_id: A string of the file ID for the updated file
        """
        try:
            self.client.file(file_id).update_contents(path)
        except BoxAPIException as be:
            logger.exception(f"Could not update file #{file_id} due to {be}")
        else:
            logger.info(f"File #{file_id} updated successfully...")

    def upload_df(
        self, data: pd.DataFrame, path: str, folder_id: str, file_type: str = "xlsx"
    ):
        """
        Uploads a specified pandas dataframe to a specified box folder

        :param data: The dataframe that will be uploaded
        :param path: A string with the path to the location where
                     the file should be saved *** MUST ALSO INCLUDE FILE NAME ***
        :param folder_id: A string with the folder ID for the specified box folder
        :param file_type: A string of the type of file the df should end up in.
                          Currently, supports xlsx, csv, or pkl. Default = xlsx
        """
        try:
            if file_type == "xlsx":
                data.to_excel(path)
            if file_type == "csv":
                data.to_csv(path)
            if file_type == "pkl":
                data.to_pickle(path)
        except BoxAPIException as be:
            logger.exception(
                f"Could not save data locally to initiate upload process due to {be}"
            )
        else:
            self.upload_file(path=path, folder_id=folder_id)
