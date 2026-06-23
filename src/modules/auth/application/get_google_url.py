from src.modules.auth.domain.ports import GoogleOAuthPort

class GetGoogleAuthUrl:

    def __init__(self, google_oauth: GoogleOAuthPort):
        self.google_oauth = google_oauth

    async def execute(self) -> str:
        return self.google_oauth.build_auth_url()