# from apache_atlas.client.base_client import AtlasClient
# # from apache_atlas.auth import BasicAuth

# def test_atlas_connection():
#     # auth = BasicAuth(username="admin", password="admin")
#     client = AtlasClient("http://localhost:21000", auth=("admin", "admin"))
#     try:
        
#         print(client.admin.get_metrics())
#         print("Connection to Atlas successful")
#     except Exception as e:
#         print(f"Failed to connect to Atlas: {e}")

# test_atlas_connection()

from atlasclient.client import Atlas

client = Atlas('http://localhost', port=21000, username='admin', password='admin')

for t in client.typedefs:
    for e in t.enumDefs:
        for el in e.elementDefs:
            print(el.value)