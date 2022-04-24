import geocoder
import folium
import requests
import ipinfo
import haversine as hs
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from administrators.models import ParkingLot
from customers.forms import ParkingLotMembership
from users.models import User
from django.views import generic
from customers.models import ParkingHistory
from .forms import RegisterParkingForm, SearchParking
# from parking.local_settings import MAPS_KEY, IPINFO_TOKEN
from ipware import get_client_ip
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
class ParkingLotListView(ListView):
    """View for the list of parking lots"""
    model = ParkingLot
    template_name = 'parking_lots/parking_lots.html'
    paginate_by = 3
    context_object_name = 'parking_lots'
    form_class = SearchParking

    def get_queryset(self):
        return super().get_queryset().annotate(total_parking_lots=Count('parking_name'))


def search_parking_lots(request):
    parking_lots = []

    if request.method == 'GET':
        data = request.GET.get('q')
        if data == '':
            return HttpResponseRedirect(reverse_lazy('parking_lots_list'))
        else:
            parking_lots = ParkingLot.objects.filter(Q(parking_name__icontains=data) | Q(city__icontains=data) |
                                                     Q(zip_code__icontains=data))
        parking_lots = parking_lots

        # paginator = Paginator(parking_lots, 3)
        # page= request.GET.get('page')

        # try:
        #   parking_lots = paginator.page(page)
        # except PageNotAnInteger:
        # Deliver the first page
        # parking_lots = paginator.page(1)
        # except EmptyPage:
        # Deliver last page
        # parking_lots = paginator.page(paginator.num_pages)

    return render(request, 'parking_lots/search.html', {'data': data, 'parking_lots': parking_lots})


def manage_search_parking_lots(request):
    object_list = []

    if request.method == 'GET':
        data = request.GET.get('q')
        if data == '':
            return HttpResponseRedirect(reverse_lazy('manage_parking_lots_list'))
        else:
            object_list = ParkingLot.objects.filter(Q(parking_name__icontains=data) | Q(city__icontains=data) |
                                                     Q(zip_code__icontains=data))
        object_list = object_list

    return render(request, 'administrators/parking/management/search.html', {'data': data, 'object_list': object_list})


def get_ip_address():
    return requests.get('https://api64.ipify.org?format=json').json()["ip"]


def get_coordinates(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()

    if response is not None:
        coordinates = {
            "latitude": response.get("latitude"),
            "longitude": response.get("longitude"),
            "region": response.get("region"),
        }
    else:
        coordinates = {
            "latitude": 41.66123962402344,
            "longitude": -91.5301284790039,
            "region": "The University of Iowa",
        }

    return coordinates


class ParkingLotsMapsView(TemplateResponseMixin, View):
    """View for the list of parking lots on a map"""
    model = ParkingLot
    template_name = 'parking_lots/maps.html'

    def get(self, request):
        parking_lots = ParkingLot.objects.annotate(total_parking_lots=Count('parking_name'))
        parking_lots = parking_lots.all()

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            address = x_forwarded_for.split(',')[-1].strip()
        elif request.META.get('HTTP_X_REAL_IP'):
            address = request.META.get('HTTP_X_REAL_IP')
        else:
            address = request.META.get('REMOTE_ADDR')

        response = address

        coordinates = [get_coordinates(response)["latitude"], get_coordinates(response)["longitude"]]
        map = folium.Map(location=coordinates, zoom_start=14)

        for parking_lot in parking_lots:
            data = geocoder.bing(parking_lot.parking_full_address, key=settings.MAPS_KEY).json
            parking_coordinates = [data['lat'], data['lng']]
            distance = hs.haversine((coordinates[0], coordinates[1]), (parking_coordinates[0], parking_coordinates[1]),
                                    unit=hs.Unit.MILES)
            infos = parking_lot.parking_name + "<br>" + parking_lot.parking_full_address + "<br>" \
                    + str(parking_lot.free_spots) + " " + "available spots" + "<br>" + "{:.2f}".format(distance) + " " \
                    + "miles" + "<br> " + "$ " + str(parking_lot.fee_per_hour) + " per hour" + "<br>"
            line = folium.IFrame(infos, width=320, height=100)
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


class ManageParkingLotDetailView(DetailView, LoginRequiredMixin):
    """ View for managing parking lot details"""

    model = ParkingLot
    template_name = 'administrators/parking/management/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parking_lots = ParkingLot.objects.filter(administrator=self.request.user)
        context["parking_lots"] = parking_lots

        return context


class CreatorMixin(object):
    model = ParkingLot
    form_class = RegisterParkingForm

    def get_queryset(self):
        """Allows to only display or update the parking lots created"""
        queryset = super().get_queryset()
        return queryset.filter(administrator=self.request.user)


class EditableCreatorMixin(object):
    def form_valid(self, form):
        form.instance.administrator = self.request.user
        return super().form_valid(form)


class CreatorParkingLotMixin(CreatorMixin, LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin):
    # model = ParkingLot
    # fields = ['parking_name', 'overview', 'street_address', 'city', 'state', 'zip_code', 'phone', 'business_email',
    # 'capacities', 'fee_per_hour', 'free_spots', 'max_overdue']
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
