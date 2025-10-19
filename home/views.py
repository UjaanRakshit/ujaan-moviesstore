from django.shortcuts import render
def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {
        'template_data': template_data})
def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request,
                  'home/about.html',
                  {'template_data': template_data})

def local_popularity_map(request):
    template_data = {}
    template_data['title'] = 'Local Popularity Map'
    # Example country popularity data keyed by ISO A3 code
    # In production, compute these values from your models (e.g., count of local interactions per country)
    country_popularity = {
        'USA': 120,  # demo: highlight United States
    }

    # Pass JSON-serializable data to template; template will render into window.COUNTRY_POPULARITY
    return render(request,
                  'home/local_popularity_map.html',
                  {
                      'template_data': template_data,
                      'country_popularity': country_popularity,
                  })