from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from administrators.models import ParkingLot
from customers.forms import ParkingLotMembership
from users.models import User


def home(request):
    # View for the home page
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Administrators').exists() and \
                request.user.groups.filter(name='Customers').exists() or \
                request.user.groups.filter(name='Administrators').exists():
            return HttpResponseRedirect(reverse_lazy('manage_parking_lots_list'))
        else:
            return HttpResponseRedirect(reverse_lazy('manage_cars_list'))

    return render(request, 'home.html')


# Create your views here.
class ParkingLotListView(TemplateResponseMixin, View):
    """View for the list of parking lots"""
    model = ParkingLot
    template_name = 'parking_lots/parking_lots.html'

    def get(self, request):
        parking_lots = ParkingLot.objects.annotate(total_parking_lots=Count('parking_name'))
        parking_lots = parking_lots.all()

        return self.render_to_response({'parking_lots': parking_lots})


class ParkingLotDetailView(DetailView):
    """ View for parking lot details"""
    model = ParkingLot
    template_name = 'parking_lots/parking_lot_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['membership_form'] = ParkingLotMembership(initial={'parking_lot': self.object})

        return context


class CreatorMixin(object):
    def get_queryset(self):
        """Allows to only display or update the parking lots created"""
        queryset = super().get_queryset()
        return queryset.filter(administrator=self.request.user)


class EditableCreatorMixin(object):
    def form_valid(self, form):
        form.instance.administrator = self.request.user
        return super().form_valid(form)


class CreatorParkingLotMixin(CreatorMixin, LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin):
    model = ParkingLot
    fields = ['parking_name', 'overview', 'street_address', 'city', 'state', 'zip_code', 'phone', 'capacities']
    success_url = reverse_lazy('manage_parking_lots_list')
    success_message = "%(parking_name)s was added successfully"


class EditableCreatorMixinParkingLot(CreatorParkingLotMixin, EditableCreatorMixin):
    template_name = 'administrators/parking/management/form.html'


class ManageParkingLotListView(CreatorParkingLotMixin, ListView):
    template_name = 'administrators/parking/management/list.html'
    permission_required = 'administrators.view_parkinglot'


class CreateParkingLotView(EditableCreatorMixinParkingLot, CreateView):
    permission_required = 'administrators.add_parkinglot'


class UpdateParkingLotView(EditableCreatorMixinParkingLot, UpdateView):
    permission_required = 'administrators.change_parkinglot'
    success_message = "%(parking_name)s was updated successfully"


class DeleteParkingLotView(CreatorParkingLotMixin, DeleteView):
    template_name = 'administrators/parking/management/delete.html'
    permission_required = 'administrators.delete_parkinglot'
    success_message = "The parking was deleted successfully"


class ParkingLotCustomers(ListView):
    """List View of parking lot customers"""
    template_name = 'administrators/parking/customers/list.html'
    model = ParkingLot

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parking_lots = ParkingLot.objects.filter(administrator=self.request.user).all()
        context["parking_lots"] = parking_lots

        return context

