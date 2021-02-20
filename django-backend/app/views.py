from .models import User
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse


# User object
class UserFunction(View):

    users = User.objects.all()
    output = ''

    for i in range(0, 10):
        user = users[i]
        output += f'This is user {user.user_id}<br>'

    def get(self, request):
        return HttpResponse(self.output)


def test(request):
    users = User.objects.all()

    return render(request, 'temp_1.html', {'users': users})
