from re import I
from django.shortcuts import render, redirect
from .models import Issue
from .forms import IssueForm

# Create your views here.
def support(request):
    if request.method == "POST":
        form = IssueForm(request.POST)
        if(form.is_valid):
            issue = form.save(commit=False)
            issue.save()
            return redirect('support_submitted')
    else:
        form = IssueForm()
    return render(request, 'support/support.html', {'form': form})

def support_submitted(request):
    return render(request, 'support/support_submitted.html')