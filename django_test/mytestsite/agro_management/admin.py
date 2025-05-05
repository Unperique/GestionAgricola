from django.contrib import admin
from .models import *

# Cultivo
@admin.register(Parcela)
class ParcelaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'superficie', 'ubicacion', 'fecha_ultima_utilizacion')
    search_fields = ('codigo', 'nombre', 'ubicacion')

@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
    list_display = ('variedad', 'parcela', 'fecha_siembra', 'fecha_cosecha_estimada')
    search_fields = ('parcela__nombre', 'variedad__nombre')
    list_filter = ('fecha_siembra',)

@admin.register(TipoCultivo)
class TipoCultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')
    search_fields = ('nombre',)
    list_filter = ('categoria',)

@admin.register(Variedad)
class VariedadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_cultivo', 'tiempo_maduracion', 'rendimiento_esperado')
    search_fields = ('nombre', 'tipo_cultivo__nombre')

# Venta y Distribución
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'ruc_dni', 'telefono', 'email')
    search_fields = ('nombre', 'ruc_dni')
    list_filter = ('tipo',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'cliente', 'fecha_pedido', 'fecha_entrega_solicitada', 'estado')
    search_fields = ('codigo', 'cliente__nombre')
    list_filter = ('estado', 'fecha_pedido')

@admin.register(ProductoTerminado)
class ProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'cultivo', 'categoria_calidad', 'cantidad', 'precio_unitario')
    search_fields = ('codigo', 'cultivo__variedad__nombre')
    list_filter = ('categoria_calidad',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'pedido', 'fecha_emision', 'total', 'estado')
    search_fields = ('numero', 'pedido__codigo')
    list_filter = ('estado', 'fecha_emision')

# Gestión de Recursos
@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre_completo', 'cargo', 'telefono', 'estado')
    search_fields = ('codigo', 'nombre_completo', 'documento_identidad')
    list_filter = ('estado', 'cargo')

@admin.register(Maquinaria)
class MaquinariaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'categoria', 'marca', 'modelo', 'estado')
    search_fields = ('codigo', 'marca', 'modelo')
    list_filter = ('estado', 'categoria')

@admin.register(CostoOperativo)
class CostoOperativoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'tipo', 'fecha', 'monto', 'cultivo')
    search_fields = ('codigo', 'descripcion')
    list_filter = ('tipo', 'fecha')

# Registrar el resto de modelos con configuración básica
admin.site.register(AnalisisSuelo)
admin.site.register(SistemaRiego)
admin.site.register(FuenteAgua)
admin.site.register(PlanRiego)
admin.site.register(PlanFertilizacion)
admin.site.register(AplicacionFertilizante)
admin.site.register(Plaga)
admin.site.register(Enfermedad)
admin.site.register(ControlPlagasEnfermedades)
admin.site.register(AccionCorrectiva)
admin.site.register(EtapaFenologica)
admin.site.register(TipoLabor)
admin.site.register(LaborAgricola)
admin.site.register(CategoriaInsumo)
admin.site.register(InsumoAgricola)
admin.site.register(LoteInsumo)
admin.site.register(UsoInsumo)
admin.site.register(ContactoCliente)
admin.site.register(PreferenciaProducto)
admin.site.register(CanalDistribucion)
admin.site.register(PreferenciaCanal)
admin.site.register(CategoriaCalidad)
admin.site.register(Presentacion)
admin.site.register(InventarioProducto)
admin.site.register(DetallePedido)
admin.site.register(Vehiculo)
admin.site.register(RutaEntrega)
admin.site.register(PuntoIntermedio)
admin.site.register(Envio)
admin.site.register(DocumentoEnvio)
admin.site.register(Pago)
admin.site.register(Devolucion)
admin.site.register(DetalleDevolucion)
admin.site.register(Cargo)
admin.site.register(Habilidad)
admin.site.register(HabilidadTrabajador)
admin.site.register(Capacitacion)
admin.site.register(CapacitacionTrabajador)
admin.site.register(Contrato)
admin.site.register(AsignacionLabor)
admin.site.register(CategoriaMaquinaria)
admin.site.register(MantenimientoMaquinaria)
admin.site.register(UsoMaquinaria)
admin.site.register(TipoCosto)
admin.site.register(Presupuesto)
admin.site.register(LineaPresupuesto)
admin.site.register(InformeFinanciero)
admin.site.register(AnalisisRentabilidad)
admin.site.register(Proveedor)
admin.site.register(ContactoProveedor)
admin.site.register(Contrato_Proveedor)
admin.site.register(EvaluacionProveedor)