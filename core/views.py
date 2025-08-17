from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, Market, Outcome, Wager, Transaction, Profile
from .forms import CustomUserCreationForm, BetForm, DepositForm, WithdrawForm


# -----------------------------
# HOME & TERMS
# -----------------------------
def home(request):
    return render(request, 'core/home.html')


def terms_privacy(request):
    return render(request, 'core/terms_privacy.html')


# -----------------------------
# AUTHENTICATION
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure a profile is created
            Profile.objects.create(user=user, balance=0)
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('core:dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You’ve been logged out.")
    return redirect('core:login')


# -----------------------------
# DASHBOARD
# -----------------------------
@login_required
def dashboard(request):
    events = Event.objects.filter(status__in=['upcoming', 'live']).order_by('start_time')
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'core/dashboard.html', {
        'events': events,
        'balance': profile.balance,
    })


# -----------------------------
# BETTING
# -----------------------------
@login_required
def place_bet(request, outcome_id):
    outcome = get_object_or_404(Outcome, id=outcome_id)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            stake = form.cleaned_data['stake']
            if profile.balance < stake:
                messages.error(request, 'Insufficient balance.')
            else:
                # Create wager and deduct stake
                Wager.objects.create(
                    profile=profile,
                    outcome=outcome,
                    stake=stake,
                    potential_payout=outcome.potential_payout(stake)
                )
                profile.balance -= stake
                profile.save(update_fields=['balance'])
                messages.success(request, f'Bet placed: {outcome.name} @ {outcome.decimal_odds}')
            return redirect('core:dashboard')
    else:
        form = BetForm()

    return render(request, 'core/place_bet.html', {
        'outcome': outcome,
        'form': form
    })


# -----------------------------
# PROFILE & HISTORY
# -----------------------------
@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    bets = Wager.objects.filter(profile=profile).order_by('-created_at')
    transactions = Transaction.objects.filter(profile=profile).order_by('-created_at')
    return render(request, 'core/profile.html', {
        'profile': profile,
        'bets': bets,
        'transactions': transactions
    })


# -----------------------------
# DEPOSIT & WITHDRAW
# -----------------------------
@login_required
def deposit_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            profile.deposit(amount)
            messages.success(request, f'Deposited ₵{amount} successfully!')
            return redirect('core:profile')
    else:
        form = DepositForm()
    return render(request, 'core/deposit.html', {'form': form})


@login_required
def withdraw_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
                profile.withdraw(amount)
                messages.success(request, f'Withdrew ₵{amount} successfully!')
            except ValueError as e:
                messages.error(request, str(e))
            return redirect('core:profile')
    else:
        form = WithdrawForm()
    return render(request, 'core/withdraw.html', {'form': form})


def sports(request):
    """
    Display a page of upcoming sports events.
    """
    # Get all upcoming events (assuming 'upcoming' status)
    events = Event.objects.filter(status='upcoming').order_by('start_time')

    return render(request, 'core/sports.html', {
        'events': events,
        'page_title': 'Sports',
    })

def live(request):
    return render(request, 'core/live.html')

def win_games(request):
    return render(request, 'core/win_games.html')

def casino(request):
    return render(request, 'core/casino.html')

def live_casino(request):
    return render(request, 'core/live_casino.html')

def more(request):
    return render(request, 'core/more.html')

def about_us(request):
    """
    Renders the about us page.
    """
    return render(request, 'core/about_us.html')