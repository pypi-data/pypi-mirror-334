import json
import os
import requests

from .base import APIMethod
from clearfacts.models.invoices import InvoiceUploaded
from clearfacts.models.base import Errors
from clearfacts.constants.errors import APIError

class InvoiceMethods(APIMethod):

    def upload(self, vat_number: str, file_name: str, invoice_type: str, local_file_path: str):
        """
            Upload an invoice file using the GraphQL mutation.

            :param vat_number: The VAT number for the upload.
            :param file_name: The file name to be used in the upload.
            :param invoice_type: The type of invoice (e.g., "SALE").
            :param local_file_path: The local path to the file to be uploaded.
            :return: The response content from the API.
        """

        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"File not found at path: {local_file_path}")
        
        query = """mutation upload($vatnumber: String!, $filename: String!, $invoicetype: InvoiceTypeArgument!) {
        uploadFile(vatnumber: $vatnumber, filename: $filename, invoicetype: $invoicetype) { 
            uuid,
            amountOfPages
            } 
        }"""

        variables = {
            "vatnumber": vat_number,
            "filename": file_name,
            "invoicetype": "SALE"
        }

        files = {
            'file': open(local_file_path, 'rb')
        }

        data = {
            "query": query,
            "variables": json.dumps(variables)
        }

        status, headers, response = self.api.post(data=data, files=files)

        if status != 200:
            raise APIError(Errors().parse(response))
        return InvoiceUploaded().parse(response.get("data", {}).get("uploadFile"))