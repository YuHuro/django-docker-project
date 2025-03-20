from django.shortcuts import redirect


class RedirectToMenuMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверка, если путь - это главная страница
        if request.path == '/':
            return redirect('/menu/menu/')

        response = self.get_response(request)
        return response