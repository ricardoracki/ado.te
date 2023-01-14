from django.shortcuts import render
from django.contrib.messages import add_message, constants
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('nome')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        confirm_password = request.POST.get('confirmar_senha')

        if len(username) == 0 or len(email) == 0 or len(password) == 0:
            add_message(request, constants.ERROR, 'Preencha todos os campos')
            return render(request, "cadastro.html")

        if password != confirm_password:
            add_message(request, constants.ERROR, 'Digite senhas iguais')
            return render(request, "cadastro.html")

        try:
            user = User.objects.create_user(
                username=username,  email=email, password=password)
            add_message(request, constants.SUCCESS,
                        "Usuário cadastrado com sucesso")
            return render(request, 'cadastro.html')
        except Exception as e:
            print(e)
            add_message(request, constants.ERROR, "Erro no sistema")
            return render(request, "cadastro.html")


def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get("nome")
        password = request.POST.get("senha")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user=user)
            return redirect('novo_pet')

        add_message(request, constants.ERROR,
                    "Nome de usuário ou senha incorretos")
        return render(request, 'login.html')


def deslogar(request):
    logout(request)
    return redirect("login")
