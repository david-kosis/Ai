import requests
class XClient:
    def __init__(self,access_token): self.access_token=access_token
    def create_post(self,text):
        if not self.access_token: raise RuntimeError('X_ACCESS_TOKEN is not configured')
        r=requests.post('https://api.x.com/2/tweets',headers={'Authorization':f'Bearer {self.access_token}','Content-Type':'application/json'},json={'text':text},timeout=20)
        r.raise_for_status(); return r.json()
