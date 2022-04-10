from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from customers.forms import ParkingLotMembership, RegisterCarForm, UpdateParkingCarForm
from customers.models import Car, ParkingHistory
from administrators.models import ParkingLot


# Create your views here.
class CarListView(TemplateResponseMixin, View):
    """View for the list of cars"""
    model = Car
    template_name = 'customers/cars.html'

    def get(self, request):
        cars = Car.objects.annotate(total_cars=Count('make'))
        cars = cars.all()

        return self.render_to_response({'cars': cars})


class CreatorMixin(object):
    def get_queryset(self):
        """Allows to only display or update the cars created"""
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class EditableCreatorMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CreatorCarMixin(CreatorMixin, LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin):
    model = Car
    fields = ['make', 'model', 'license_plate_number', 'state']
    success_url = reverse_lazy('manage_cars_list')
    success_message = "Your car with %(license_plate_number)s was added successfully"


class EditableCreatorMixinCar(CreatorCarMixin, EditableCreatorMixin):
    template_name = 'customers/car/management/form.html'


class ManageCarListView(CreatorCarMixin, ListView):
    template_name = 'customers/car/management/list.html'
    permission_required = 'customers.view_car'


class CreateCarView(EditableCreatorMixinCar, CreateView):
    permission_required = 'customers.add_car'


class UpdateCarView(EditableCreatorMixinCar, UpdateView):
    permission_required = 'customers.change_car'
    success_message = "Your car with %(license_plate_number)s was updated successfully"


class DeleteCarView(CreatorCarMixin, DeleteView):
    template_name = 'customers/car/management/delete.html'
    permission_required = 'customers.delete_car'
    success_message = "Your car was deleted successfully"


class CustomerParkingLotMembershipView(LoginRequiredMixin, FormView):
    """ View of customer parking lot membership which inherits from the LoginRequiredMixin and FormView"""
    parking_lot = None
    form_class = ParkingLotMembership

    def form_valid(self, form):
        """Validation of the form for the parking"""
        self.parking_lot = form.cleaned_data['parking_lot']
        self.parking_lot.customer.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """ Returns the URL that the user will be directed to if the form is successful"""
        return reverse_lazy('customer_parking_lot_details', args=[self.parking_lot.id])


class CustomerParkingLotView(LoginRequiredMixin, ListView):
    """ View of parking lots that customer is member of"""
    model = ParkingLot
    template_name = 'customers/parking_lot/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(customer__in=[self.request.user])


class CustomerParkingLotDetailView(DetailView):
    """ View for customer parking lot details"""
    model = ParkingLot
    template_name = 'customers/parking_lot/customer_parking_lot_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(customer__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get parking lot object
        parking_lot = self.get_object()
        context['parking_lot'] = parking_lot

        return context


def update_car_parking(request):
    form = UpdateParkingCarForm()

    if request.method == 'POST':

        if form.is_valid():
            parking = form.save(commit=False)
            parking.save()
            messages.success(request, 'Your have successfully updated where to park your car.')
            return redirect('home')
    else:
        form = UpdateParkingCarForm()
    return render(request, 'customers/car/management/update_form.html', {'form': form})
