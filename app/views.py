from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from app.forms import AddPublicationForm, SubscriptionForm
from app.models import Publication, Subscription
from django.db.models import Q

from app.services import create_stripe_price, create_stripe_session, create_stripe_items
from users.utils import subscribe


class PublicationListView(ListView, PermissionRequiredMixin):
    model = Publication
    template_name = 'app/publication_list.html'
    context_object_name = 'publications'

    def get_queryset(self):
        if self.request.user.has_perm('app.view_publication'):
            return self.model.objects.filter(is_published='published')
        return self.model.objects.filter(Q(is_published='published') & Q(is_paid='free'))


class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    login_url = reverse_lazy('users:login')
    form_class = AddPublicationForm
    success_url = reverse_lazy('app:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_name'] = self.request.user
        return context


class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'app/publication_detail.html'

    def get_object(self, queryset=None):
        return self.model.objects.filter(slug=self.kwargs['slug']).first()


class PublicationDeleteView(DeleteView, PermissionRequiredMixin):
    model = Publication
    success_url = reverse_lazy('app:index')
    permission_required = 'app.delete_publication'


class PublicationUpdateView(UpdateView, PermissionRequiredMixin):
    model = Publication
    success_url = reverse_lazy('app:update')
    fields = '__all__'
    permission_required = 'app.change_publication'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)


class SubscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Subscription
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('app:index')
    form_class = SubscriptionForm
    queryset = Publication.objects.filter(Q(is_published='published') & Q(is_paid='paid'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    @staticmethod
    def change_title_in_stripe_page(products_names):
        if len(products_names) >= 1:
            products_names = 'Оплата подписки'
            return products_names
        try:
            return f'Оплата публикации: {products_names[0]}'
        except IndexError:
            return 'Оплата подписки'

    def form_valid(self, form):
        payment = form.save(commit=False)
        payment.user = self.request.user
        publications = self.get_queryset()
        products_name = create_stripe_items([publication.title for publication in publications])
        stripe_price_id = create_stripe_price(payment.price, self.change_title_in_stripe_page(products_name))
        payment.payment_link, payment.payment_id = create_stripe_session(stripe_price_id)
        payment.save()
        payment.paid_publication.set(publications)
        subscribe(payment.user.phone_number)
        return redirect(payment.payment_link)
