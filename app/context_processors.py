from app.models import Subscription


def check_subscription(request):
    subscription = None
    if request.user.is_authenticated:
        subscription = Subscription.objects.filter(user=request.user).first()
    return {'check_subscription': subscription}
