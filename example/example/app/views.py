from django.shortcuts import render
from gusregon.gus import GUS

from .forms import MyForm


def home(request):
    info = None
    form = MyForm(data=request.POST or None)
    if form.is_valid():
        gus = GUS()
        info = gus.search(form.cleaned_data.get('nip'))
    return render(request, 'app/home.html', {'form': form, 'info': info})
