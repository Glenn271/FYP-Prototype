from django.shortcuts import render

locations = [
    {
        'author': 'CoreyMS',
        'title': 'location 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'location 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]


def home(request):
    context = {
        'locations': locations
    }
    return render(request, 'world/home.html', context)


def about(request):
    return render(request, 'world/about.html', {'title': 'About'})


