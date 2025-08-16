from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError

# =========================
#  CONSTANTS
# =========================
CURRENCY_CHOICES = [
    ('GHS', 'Ghanaian Cedi'),
    ('USD', 'US Dollar'),
]

STATUS_CHOICES = [
    ('upcoming', 'Upcoming'),
    ('live', 'Live'),
    ('settled', 'Settled'),
    ('cancelled', 'Cancelled'),
]

MARKET_TYPE_CHOICES = [
    ('win_draw_win', '1X2'),
    ('over_under', 'Over/Under'),
    ('moneyline', 'Moneyline'),
    ('spread', 'Spread'),
    ('custom', 'Custom'),
]

TRANSACTION_TYPE_CHOICES = [
    ('deposit', 'Deposit'),
    ('withdrawal', 'Withdrawal'),
    ('payout', 'Payout'),
    ('refund', 'Refund'),
    ('stake', 'Stake hold'),
    ('stake_release', 'Stake release'),
]

WAGER_STATUS_CHOICES = [
    ('open', 'Open'),
    ('won', 'Won'),
    ('lost', 'Lost'),
    ('cancelled', 'Cancelled'),
    ('pending', 'Pending'),
]

# =========================
#  HELPERS
# =========================
def quantize_currency(amount):
    """Helper to quantize Decimal to 2 places (currency)."""
    if amount is None:
        return Decimal('0.00')
    return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


# =========================
#  PROFILE
# =========================
class Profile(models.Model):
    """
    Extended user profile for balance & user metadata.
    One-to-one with Django's User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GHS')
    is_verified = models.BooleanField(default=False)
    display_name = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def deposit(self, amount, reference=None):
        """Create a deposit transaction and increase balance."""
        amount = quantize_currency(Decimal(amount))
        if amount <= 0:
            raise ValidationError("Deposit amount must be positive.")
        txn = Transaction.objects.create(
            profile=self,
            txn_type='deposit',
            amount=amount,
            reference=reference or f"DEP-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        )
        self.balance = quantize_currency(self.balance + amount)
        self.save(update_fields=['balance'])
        return txn

    def withdraw(self, amount, reference=None):
        """Create a withdrawal transaction and decrease balance (simulated)."""
        amount = quantize_currency(Decimal(amount))
        if amount <= 0:
            raise ValidationError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValidationError("Insufficient balance.")
        txn = Transaction.objects.create(
            profile=self,
            txn_type='withdrawal',
            amount=amount,
            reference=reference or f"WDL-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        )
        self.balance = quantize_currency(self.balance - amount)
        self.save(update_fields=['balance'])
        return txn

    def __str__(self):
        return f"{self.user.username} ({self.currency}) - {self.balance}"


# =========================
#  EVENT
# =========================
class Event(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='upcoming')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=128, blank=True, null=True, help_text="ID from external provider")

    class Meta:
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['status', 'start_time']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def is_active(self):
        return self.status in ('upcoming', 'live')

    def settle_event(self):
        """Mark event as settled and trigger settlement on linked markets/outcomes."""
        if self.status == 'settled':
            return
        self.status = 'settled'
        self.save(update_fields=['status', 'updated_at'])
        for market in self.markets.all():
            market.settle_market()


# =========================
#  MARKET
# =========================
class Market(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='markets')
    name = models.CharField(max_length=200)
    market_type = models.CharField(max_length=32, choices=MARKET_TYPE_CHOICES, default='custom')
    params = models.JSONField(blank=True, null=True)
    is_settled = models.BooleanField(default=False)
    settled_outcome = models.ForeignKey('Outcome', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        unique_together = ('event', 'name')

    def __str__(self):
        return f"{self.event.title} — {self.name}"

    def settle_market(self, winning_outcome_id=None):
        """Settle this market and all linked wagers."""
        if self.is_settled:
            return
        if winning_outcome_id:
            try:
                winner = self.outcomes.get(pk=winning_outcome_id)
            except Outcome.DoesNotExist:
                raise ValidationError("Winning outcome not found in market.")
            self.settled_outcome = winner
        if not self.settled_outcome:
            raise ValidationError("No outcome specified for settlement.")
        self.is_settled = True
        self.save(update_fields=['is_settled', 'settled_outcome'])
        for outcome in self.outcomes.all():
            outcome.settle_outcome(outcome == self.settled_outcome)


# =========================
#  OUTCOME
# =========================
class Outcome(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='outcomes')
    name = models.CharField(max_length=200)
    decimal_odds = models.DecimalField(max_digits=6, decimal_places=3)
    is_winner = models.BooleanField(default=False)

    class Meta:
        unique_together = ('market', 'name')

    def __str__(self):
        return f"{self.market} — {self.name} @ {self.decimal_odds}"

    def potential_payout(self, stake_amount):
        stake = quantize_currency(Decimal(stake_amount))
        payout = quantize_currency(stake * self.decimal_odds)
        return payout

    def settle_outcome(self, did_win):
        self.is_winner = did_win
        self.save(update_fields=['is_winner'])
        for wager in self.wagers.filter(status='open'):
            if did_win:
                wager.settle(win=True)
            else:
                wager.settle(win=False)
# =========================
#  WAGER
# =========================
class Wager(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='wagers')
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE, related_name='wagers')
    stake = models.DecimalField(max_digits=12, decimal_places=2)
    potential_payout = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=16, choices=WAGER_STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Wager {self.id}: {self.profile.user.username} on {self.outcome.name}"

    def save(self, *args, **kwargs):
        if not self.potential_payout:
            self.potential_payout = quantize_currency(self.stake * self.outcome.decimal_odds)
        super().save(*args, **kwargs)

    def settle(self, win):
        if self.status != 'open':
            return
        self.status = 'won' if win else 'lost'
        self.save(update_fields=['status', 'updated_at'])
        if win:
            self.profile.balance = quantize_currency(self.profile.balance + self.potential_payout)
            self.profile.save(update_fields=['balance'])


# =========================
#  TRANSACTION
# =========================
class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='transactions')
    txn_type = models.CharField(max_length=16, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.txn_type.title()} of {self.amount} for {self.profile.user.username}"
