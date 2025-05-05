from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Avg, Count
import datetime

from .models import (
    # Cultivo
    Parcela, AnalisisSuelo, TipoCultivo, Variedad, Cultivo, SistemaRiego, 
    FuenteAgua, PlanRiego, PlanFertilizacion, AplicacionFertilizante,
    Plaga, Enfermedad, ControlPlagasEnfermedades, AccionCorrectiva, 
    EtapaFenologica, TipoLabor, LaborAgricola, CategoriaInsumo, 
    InsumoAgricola, LoteInsumo, UsoInsumo,
    
    # Venta y Distribución
    Cliente, ContactoCliente, PreferenciaProducto, CanalDistribucion,
    PreferenciaCanal, CategoriaCalidad, Presentacion, ProductoTerminado,
    InventarioProducto, Pedido, DetallePedido, Vehiculo, RutaEntrega,
    PuntoIntermedio, Envio, DocumentoEnvio, Factura, Pago, Devolucion,
    DetalleDevolucion,
    
    # Gestión de Recursos
    Cargo, Trabajador, Habilidad, HabilidadTrabajador, Capacitacion,
    CapacitacionTrabajador, Contrato, AsignacionLabor, CategoriaMaquinaria,
    Maquinaria, MantenimientoMaquinaria, UsoMaquinaria, TipoCosto,
    CostoOperativo, Presupuesto, LineaPresupuesto, InformeFinanciero,
    AnalisisRentabilidad, Proveedor, ContactoProveedor, Contrato_Proveedor,
    EvaluacionProveedor
)

# Dashboard
@login_required
def dashboard(request):
    cultivos_activos = Cultivo.objects.filter(fecha_cosecha_real__isnull=True).count()
    parcelas_total = Parcela.objects.count()
    productos_inventario = InventarioProducto.objects.aggregate(total=Sum('cantidad_disponible'))['total'] or 0
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente').count()
    
    context = {
        'cultivos_activos': cultivos_activos,
        'parcelas_total': parcelas_total,
        'productos_inventario': productos_inventario,
        'pedidos_pendientes': pedidos_pendientes,
    }
    return render(request, 'agro_management/dashboard.html', context)

# ---- Vistas para Cultivo ----

# Parcelas
class ParcelaListView(LoginRequiredMixin, ListView):
    model = Parcela
    template_name = 'agro_management/parcela_list.html'
    context_object_name = 'parcelas'

class ParcelaDetailView(LoginRequiredMixin, DetailView):
    model = Parcela
    template_name = 'agro_management/parcela_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parcela = self.get_object()
        context['analisis_suelo'] = AnalisisSuelo.objects.filter(parcela=parcela).order_by('-fecha_analisis')
        context['cultivos'] = Cultivo.objects.filter(parcela=parcela).order_by('-fecha_siembra')
        return context

class ParcelaCreateView(LoginRequiredMixin, CreateView):
    model = Parcela
    template_name = 'agro_management/parcela_form.html'
    fields = ['codigo', 'nombre', 'superficie', 'ubicacion', 'potencial_productivo']
    success_url = reverse_lazy('parcela_list')

class ParcelaUpdateView(LoginRequiredMixin, UpdateView):
    model = Parcela
    template_name = 'agro_management/parcela_form.html'
    fields = ['nombre', 'superficie', 'ubicacion', 'potencial_productivo', 'fecha_ultima_utilizacion']
    
    def get_success_url(self):
        return reverse_lazy('parcela_detail', kwargs={'pk': self.object.pk})

class ParcelaDeleteView(LoginRequiredMixin, DeleteView):
    model = Parcela
    template_name = 'agro_management/parcela_confirm_delete.html'
    success_url = reverse_lazy('parcela_list')

# Cultivos
class CultivoListView(LoginRequiredMixin, ListView):
    model = Cultivo
    template_name = 'agro_management/cultivo_list.html'
    context_object_name = 'cultivos'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        fecha_siembra = self.request.GET.get('fecha_siembra')
        parcela = self.request.GET.get('parcela')
        tipo_cultivo = self.request.GET.get('tipo_cultivo')
        
        if fecha_siembra:
            queryset = queryset.filter(fecha_siembra__year=fecha_siembra)
        if parcela:
            queryset = queryset.filter(parcela_id=parcela)
        if tipo_cultivo:
            queryset = queryset.filter(variedad__tipo_cultivo_id=tipo_cultivo)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parcelas'] = Parcela.objects.all()
        context['tipos_cultivo'] = TipoCultivo.objects.all()
        return context

class CultivoDetailView(LoginRequiredMixin, DetailView):
    model = Cultivo
    template_name = 'agro_management/cultivo_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cultivo = self.get_object()
        context['etapas'] = EtapaFenologica.objects.filter(cultivo=cultivo).order_by('fecha_inicio')
        context['planes_riego'] = PlanRiego.objects.filter(cultivo=cultivo)
        context['planes_fertilizacion'] = PlanFertilizacion.objects.filter(cultivo=cultivo)
        context['controles'] = ControlPlagasEnfermedades.objects.filter(cultivo=cultivo).order_by('-fecha_deteccion')
        context['labores'] = LaborAgricola.objects.filter(cultivo=cultivo).order_by('-fecha_realizacion')
        return context

class CultivoCreateView(LoginRequiredMixin, CreateView):
    model = Cultivo
    template_name = 'agro_management/cultivo_form.html'
    fields = ['parcela', 'variedad', 'fecha_siembra', 'fecha_cosecha_estimada', 'area_sembrada', 'observaciones']
    success_url = reverse_lazy('cultivo_list')

class CultivoUpdateView(LoginRequiredMixin, UpdateView):
    model = Cultivo
    template_name = 'agro_management/cultivo_form.html'
    fields = ['fecha_cosecha_estimada', 'fecha_cosecha_real', 'rendimiento_obtenido', 'observaciones']
    
    def get_success_url(self):
        return reverse_lazy('cultivo_detail', kwargs={'pk': self.object.pk})

# Análisis de Suelo
class AnalisisSueloCreateView(LoginRequiredMixin, CreateView):
    model = AnalisisSuelo
    template_name = 'agro_management/analisis_suelo_form.html'
    fields = ['parcela', 'fecha_analisis', 'ph', 'materia_organica', 'nitratos', 'fosfatos', 'potasio', 'calcio', 'magnesio', 'sodio', 'sulfatos']
    success_url = reverse_lazy('parcela_list')