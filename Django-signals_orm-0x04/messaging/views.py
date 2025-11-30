from django.contrib.auth.models import User
from django.shortcuts import redirect

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect("/")
