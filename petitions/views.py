from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Petition, Vote
from .forms import PetitionForm


def index(request):
    """Display all active petitions"""
    petitions = Petition.objects.filter(is_active=True)
    
    template_data = {
        'title': 'Movie Petitions - Movies Store',
        'petitions': petitions
    }
    
    return render(request, 'petitions/index.html', {'template_data': template_data})


@login_required
def create_petition(request):
    """Create a new petition"""
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, f'Your petition for "{petition.movie_title}" has been created successfully!')
            return redirect('petitions.index')
    else:
        form = PetitionForm()
    
    template_data = {
        'title': 'Create Movie Petition - Movies Store',
        'form': form
    }
    
    return render(request, 'petitions/create.html', {'template_data': template_data})


def petition_detail(request, petition_id):
    """Display petition details"""
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    user_vote = None
    
    if request.user.is_authenticated:
        user_vote = petition.get_user_vote(request.user)
    
    template_data = {
        'title': f'Petition: {petition.movie_title} - Movies Store',
        'petition': petition,
        'user_vote': user_vote,
        'yes_votes': petition.get_yes_votes(),
        'no_votes': petition.get_no_votes(),
        'total_votes': petition.get_total_votes(),
    }
    
    return render(request, 'petitions/detail.html', {'template_data': template_data})


@login_required
@require_POST
def vote_petition(request, petition_id):
    """Handle voting on a petition"""
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    
    try:
        data = json.loads(request.body)
        vote_type = data.get('vote_type')
        
        if vote_type not in ['yes', 'no']:
            return JsonResponse({'success': False, 'message': 'Invalid vote type'})
        
        # Check if user has already voted
        existing_vote = Vote.objects.filter(petition=petition, user=request.user).first()
        
        if existing_vote:
            # Update existing vote
            existing_vote.vote_type = vote_type
            existing_vote.save()
            message = f'Your vote has been updated to "{vote_type.upper()}"'
        else:
            # Create new vote
            Vote.objects.create(
                petition=petition,
                user=request.user,
                vote_type=vote_type
            )
            message = f'Your "{vote_type.upper()}" vote has been recorded'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'yes_votes': petition.get_yes_votes(),
            'no_votes': petition.get_no_votes(),
            'total_votes': petition.get_total_votes(),
            'user_vote': vote_type
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid data format'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred while processing your vote'})


@login_required
def my_petitions(request):
    """Display user's own petitions"""
    petitions = Petition.objects.filter(created_by=request.user)
    
    template_data = {
        'title': 'My Petitions - Movies Store',
        'petitions': petitions
    }
    
    return render(request, 'petitions/my_petitions.html', {'template_data': template_data})