from .base import APIMethod
from clearfacts.models.users import UserInfo, Administrations
from clearfacts.models.base import Error
from clearfacts.constants.errors import APIError

class UserMethods(APIMethod):

    def get_info(self):
        status, headers, response = self.api.get('userinfo', base=self.api.oauth2_server_url)
        if status != 200:
            raise APIError(Error().parse(response))
        return UserInfo().parse(response)
    
    def get_available_administrations(self):

        query = """query admins {
            administrations {
                name, 
                companyNumber, 
                emails {
                type,
                emailAddress
                }
                companyType,
                address {
                streetAddress, 
                country {
                    iso2,
                    name
                }
                },
                accountManager
            }
        }"""

        data = {
            "query": query
        }

        status, headers, response = self.api.post(data=data)

        if status != 200:
            raise APIError(Error().parse(response))
        return Administrations().parse(response.get("data", {}).get("administrations"))