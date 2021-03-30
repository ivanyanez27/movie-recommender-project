from ..models import ApiMovie, AuthUser

user = AuthUser.objects.filter(id=10533)

def run():
    print(user)