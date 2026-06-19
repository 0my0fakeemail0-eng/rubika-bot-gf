from pyrubi import Client

app = Client("gf_account")

print(app.get_me())
