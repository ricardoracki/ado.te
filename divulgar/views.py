from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, constants
from django.views.decorators.csrf import csrf_exempt
from adotar.models import PedidoAdocao
from .models import Raca, Tag, Pet
from django.http import JsonResponse


@login_required
def novo_pet(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        racas = Raca.objects.all()

        return render(request, "novo_pet.html", {"racas": racas, "tags": tags})

    elif request.method == "POST":
        foto = request.FILES.get("foto")
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        pet = Pet(usuario=request.user,
                  foto=foto, nome=nome,
                  descricao=descricao,
                  estado=estado,
                  cidade=cidade,
                  telefone=telefone,
                  raca_id=raca)

        pet.save()

        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            pet.tags.add(tag)

        pet.save()
        add_message(request, constants.SUCCESS, 'Pet aqdicionado com sucesso')
        return redirect('seus_pets')


@login_required
def seus_pets(request):
    if request.method == 'GET':
        pets = Pet.objects.filter(usuario=request.user)
        return render(request, "seus_pets.html", {"pets": pets})


@login_required
def remover_pet(request, id):
    pet = Pet.objects.get(id=id)

    if pet.usuario == request.user:
        pet.delete()
        add_message(request, constants.SUCCESS, "Pet removido com sucesso")
    else:
        add_message(request, constants.ERROR, "O pet não é seu")

    return redirect("seus_pets")


@login_required
def ver_pet(request, id):
    if request.method == "GET":
        pet = Pet.objects.get(id=id)
        return render(request, "ver_pet.html", {"pet": pet})


@login_required
def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(
            usuario=request.user, status="AG")
        return render(request, "ver_pedido_adocao.html", {"pedidos": pedidos})


@login_required
def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')


@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()
    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).count()
        qtd_adocoes.append(adocoes)

    racas = [raca.raca for raca in racas]
    data = {"qtd_adocoes": qtd_adocoes, "labels": racas}

    return JsonResponse(data)
