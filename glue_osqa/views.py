from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect, render_to_response


def question_page(request):
    return render(request, 'glue_osqa/question_main.html')

def question_ask(request):
    return render(request, 'glue_osqa/question_askpage.html')