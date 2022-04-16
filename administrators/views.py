import geocoder
import folium
import haversine as hs
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
from django.views import generic
from customers.models import ParkingHistory
from .forms import RegisterParkingForm
# from parking.local_settings import MAPS_KEY
from django.conf.settings import MAPS_KEY


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


class ParkingLotsMapsView(TemplateResponseMixin, View):
    """View for the list of parking lots on a map"""
    model = ParkingLot
    template_name = 'parking_lots/maps.html'

    def get(self, request):
        parking_lots = ParkingLot.objects.annotate(total_parking_lots=Count('parking_name'))
        parking_lots = parking_lots.all()
        # Temporary coordinates
        coordinates = [41.66123962402344, -91.5301284790039]
        map = folium.Map(location=coordinates, zoom_start=13)

        for parking_lot in parking_lots:
            data = geocoder.bing(parking_lot.parking_full_address, key=MAPS_KEY).json
            parking_coordinates = [data['lat'], data['lng']]
            distance = hs.haversine((coordinates[0], coordinates[1]), (parking_coordinates[0], parking_coordinates[1]), unit=hs.Unit.MILES)
            infos = parking_lot.parking_name + "<br>" + parking_lot.parking_full_address + "<br>" \
                    + str(parking_lot.free_spots) + " " + "available spots" + "<br>" + "{:.2f}".format(distance) + " " \
                    + "miles from the University of Iowa" + "<br> "
            line = folium.IFrame(infos, width=320, height=90)
            show_infos = folium.Popup(line, max_width=400)
            folium.Marker(location=parking_coordinates, tooltip='More infos', popup=show_infos).add_to(map)

        folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
        folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
        folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)
        folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(map)
        folium.LayerControl().add_to(map)
        map = map._repr_html_()

        return self.render_to_response({'maps': map})


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
    form_class = RegisterParkingForm
    fields = ['parking_name', 'overview', 'street_address', 'city', 'state', 'zip_code', 'phone', 'business_email',
              'capacities', 'fee_per_hour', 'free_spots', 'max_overdue']
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


class ParkingLotCustomersView(generic.TemplateView, LoginRequiredMixin):
    """View for the parking lot customers"""
    template_name = "administrators/parking/customers/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = ParkingHistory.objects.filter(paid=False).select_related('car', 'parking') \
            .filter(parking__administrator=self.request.user)
        context["customers"] = customers

        return context
