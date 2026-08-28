import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]


#admin client (관리자 클라)
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

#anon client (익명 클라)
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
def get_anon_client()-> Client:
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
