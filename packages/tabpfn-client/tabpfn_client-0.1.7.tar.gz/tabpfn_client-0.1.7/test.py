import tabpfn_client
from tabpfn_client.client import ServiceClient


access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiMjYyYjcyMWEtNmYwMC00YzJiLThlZTMtM2VhYmZiYzgyMTU5IiwiZXhwIjoxNzY3MTg2ODg3fQ.GlLZj4z2k2nWsygzf-n9pbhLd4bJWkymUWX50k-gYps"

tabpfn_client.set_access_token(access_token)

print(tabpfn_client.get_access_token())

print(ServiceClient.validate_email("new_user@gmail.com"))
