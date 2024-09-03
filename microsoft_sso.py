from msal import PublicClientApplication
app = PublicClientApplication(
    "91698855-ba6e-4daf-b8bd-f441f269f570", 
    authority="https://login.microsoftonline.com/af8e89a3-d9ac-422f-ad06-cc4eb4214314",
    client_credential=None
)

scopes = ["https://af8e89a3-d9ac-422f-ad06-cc4eb4214314.onmicrosoft.com/api/read"]

result = app.acquire_token_interactive(scopes=scopes)
print(result["access_token"])

# accounts = app.get_accounts()
# if accounts:
#     print("pick the account you want to proceed:")
#     for a in accounts:
#         print(a["username"])
#     chosen = accounts[0]
#     result = app.acquire_token_silent(["User.Read"], account=chosen)

# if not result:
#     result = app.acquire_token_interactive(scopes=["User.Read"])

# if "access_token" in result:
#     print(result["access_token"])
# else:
#     print(result.get("error"))
#     print(result.get("error_description"))
#     print(result.get("correlation_id"))