from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total, derive_region_code
from .models import Order, Item, Feedback
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',
        {'template_data': template_data})
def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')
def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')
@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    # Tag order with best-effort region (query -> session -> Accept-Language)
    order.region_code = derive_region_code(request)
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html', {'template_data': template_data})

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            feedback = Feedback()
            feedback.name = data.get('name', '') or None
            feedback.feedback_text = data.get('feedback_text', '')
            order_id = data.get('order_id')
            
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    feedback.order = order
                except Order.DoesNotExist:
                    pass
            
            if feedback.feedback_text.strip():
                feedback.save()
                return JsonResponse({'success': True, 'message': 'Thank you for your feedback!'})
            else:
                return JsonResponse({'success': False, 'message': 'Feedback text is required.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error saving feedback.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def view_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-date_created')
    template_data = {
        'title': 'Customer Feedback',
        'feedbacks': feedbacks
    }
    return render(request, 'cart/feedback.html', {'template_data': template_data})