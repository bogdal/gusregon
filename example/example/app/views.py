from django.shortcuts import render

from .forms import MyForm


def home(request):
    info = None

    form = MyForm(data=request.POST or None)
    if form.is_valid():
        gus = form.cleaned_data.get('gus')
        info = gus.search(form.cleaned_data.get('nip'))

    return render(request, 'app/home.html', {'form': form, 'info': info})

