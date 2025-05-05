from django import forms
from django.forms import inlineformset_factory
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
import datetime

# Formularios para Cultivo
class ParcelaForm(forms.ModelForm):
    class Meta:
        model = Parcela
        fields = ['codigo', 'nombre', 'superficie', 'ubicacion', 'fecha_ultima_utilizacion', 'potencial_productivo']
        widgets = {
            'fecha_ultima_utilizacion': forms.DateInput(attrs={'type': 'date'}),
        }

class AnalisisSueloForm(forms.ModelForm):
    class Meta:
        model = AnalisisSuelo
        fields = ['parcela', 'fecha_analisis', 'ph', 'materia_organica', 'nitrogeno', 'fosforo', 'potasio', 'otros_minerales', 'observaciones']
        widgets = {
            'fecha_analisis': forms.DateInput(attrs={'type': 'date'}),
            'otros_minerales': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class TipoCultivoForm(forms.ModelForm):
    class Meta:
        model = TipoCultivo
        fields = ['nombre', 'categoria', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class VariedadForm(forms.ModelForm):
    class Meta:
        model = Variedad
        fields = ['tipo_cultivo', 'nombre', 'descripcion', 'tiempo_maduracion', 'resistencia_enfermedades', 'rendimiento_esperado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class CultivoForm(forms.ModelForm):
    class Meta:
        model = Cultivo
        fields = ['parcela', 'variedad', 'fecha_siembra', 'fecha_cosecha_estimada', 'fecha_cosecha_real', 'area_sembrada', 'rendimiento_obtenido', 'observaciones']
        widgets = {
            'fecha_siembra': forms.DateInput(attrs={'type': 'date'}),
            'fecha_cosecha_estimada': forms.DateInput(attrs={'type': 'date'}),
            'fecha_cosecha_real': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class CultivoBusquedaForm(forms.Form):
    parcela = forms.ModelChoiceField(queryset=Parcela.objects.all(), required=False, empty_label="Todas las parcelas")
    tipo_cultivo = forms.ModelChoiceField(queryset=TipoCultivo.objects.all(), required=False, empty_label="Todos los tipos")
    año_siembra = forms.ChoiceField(choices=[], required=False)
    estado = forms.ChoiceField(choices=[('', 'Todos'), ('activo', 'Activos'), ('cosechado', 'Cosechados')], required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generar opciones de años desde 5 años atrás hasta el próximo año
        año_actual = datetime.datetime.now().year
        años = [(str(año), str(año)) for año in range(año_actual - 5, año_actual + 2)]
        años.insert(0, ('', 'Todos los años'))
        self.fields['año_siembra'].choices = años

class PlanRiegoForm(forms.ModelForm):
    class Meta:
        model = PlanRiego
        fields = ['cultivo', 'sistema_riego', 'fuente_agua', 'frecuencia_dias', 'cantidad_agua', 'duracion', 'hora_preferida']
        widgets = {
            'hora_preferida': forms.TimeInput(attrs={'type': 'time'}),
        }

class PlanFertilizacionForm(forms.ModelForm):
    class Meta:
        model = PlanFertilizacion
        fields = ['cultivo', 'nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class AplicacionFertilizanteForm(forms.ModelForm):
    class Meta:
        model = AplicacionFertilizante
        fields = ['plan', 'fecha_programada', 'fecha_aplicacion', 'tipo_fertilizante', 'dosis_por_hectarea', 'metodo_aplicacion', 'observaciones']
        widgets = {
            'fecha_programada': forms.DateInput(attrs={'type': 'date'}),
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class ControlPlagasEnfermedadesForm(forms.ModelForm):
    class Meta:
        model = ControlPlagasEnfermedades
        fields = ['cultivo', 'tipo_incidencia', 'plaga', 'enfermedad', 'fecha_deteccion', 'nivel_infestacion', 'area_afectada', 'observaciones']
        widgets = {
            'fecha_deteccion': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plaga'].required = False
        self.fields['enfermedad'].required = False
        
        # Agregar JavaScript para mostrar/ocultar campos según el tipo de incidencia
        self.fields['tipo_incidencia'].widget.attrs.update({'onchange': 'toggleFields()'})

class AccionCorrectivaForm(forms.ModelForm):
    class Meta:
        model = AccionCorrectiva
        fields = ['control', 'fecha_accion', 'producto_aplicado', 'dosis', 'metodo_aplicacion', 'efectividad', 'observaciones']
        widgets = {
            'fecha_accion': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class EtapaFenologicaForm(forms.ModelForm):
    class Meta:
        model = EtapaFenologica
        fields = ['cultivo', 'nombre', 'fecha_inicio', 'fecha_fin', 'descripcion', 'observaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

class LaborAgricolaForm(forms.ModelForm):
    class Meta:
        model = LaborAgricola
        fields = ['cultivo', 'tipo_labor', 'fecha_realizacion', 'horas_empleadas', 'personal_asignado', 'observaciones']
        widgets = {
            'fecha_realizacion': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }