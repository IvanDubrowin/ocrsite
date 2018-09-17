from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.models import Session
from .forms import UploadForm
from .models import ImageUpload, UserQuery


class IndexView(View):

    template_name = 'index.html'

    def get(self, request):
        request.session.set_expiry(7*24*60*60)
        request.session['sessionid'] = True
        form = UploadForm()
        args = {"form": form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = UploadForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            text = instance.image_to_text()
            args = {"text": text,
                    "form": form}
            save_text = UserQuery(
                    session = Session.objects.get(session_key=request.COOKIES.get('sessionid')),
                    text = text
                    )
            if len(save_text.text) > 0:
                save_text.save()
            else:
                args = {"text": 'Не удалось разпознать изображение',
                        "form": form}
            instance.delete()
            return render(request, self.template_name, args)
        return render(request, self.template_name, {"form": form})


class QueryView(View):

    template_name = 'query.html'

    def get(self, request, page_number):
        query = UserQuery.objects.filter(session=request.COOKIES.get('sessionid')).order_by('-date')
        if query.count() != 0:
            query_page = Paginator(query, 3)
            try:
                pages = query_page.page(page_number)
            except PageNotAnInteger:
                pages = query_page.page(1)
            except EmptyPage:
                pages = query_page.page(query_page.num_pages)
            args = {"query": pages}
        else:
            args = {"none": "Нет записей"}
        return render(request, self.template_name, args)


class InfoView(View):

    template_name = 'info.html'

    def get(self, request):
        return render(request, self.template_name)


def handler404(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html')
    response.status_code = 500
    return response
