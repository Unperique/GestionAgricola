from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Contexto Delimitado: Cultivo
class Parcela(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    superficie = models.DecimalField(max_digits=10, decimal_places=2)  # en hectáreas
    ubicacion = models.CharField(max_length=255)
    fecha_ultima_utilizacion = models.DateField(null=True, blank=True)
    potencial_productivo = models.CharField(max_length=50)
    coordenadas_gps = models.CharField(max_length=100, blank=True)  # Nuevo campo
    tipo_suelo = models.CharField(max_length=50, blank=True)  # Nuevo campo
    
    class Meta:
        verbose_name = 'Parcela'
        verbose_name_plural = 'Parcelas'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class AnalisisSuelo(models.Model):
    parcela = models.ForeignKey(Parcela, on_delete=models.CASCADE, related_name='analisis')
    fecha_analisis = models.DateField()
    ph = models.DecimalField(max_digits=4, decimal_places=2)
    materia_organica = models.DecimalField(max_digits=5, decimal_places=2)  # en porcentaje
    nitrogeno = models.DecimalField(max_digits=6, decimal_places=2)  # en ppm
    fosforo = models.DecimalField(max_digits=6, decimal_places=2)  # en ppm
    potasio = models.DecimalField(max_digits=6, decimal_places=2)  # en ppm
    otros_minerales = models.JSONField(null=True, blank=True)  # Otros minerales en formato JSON
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Análisis de {self.parcela} del {self.fecha_analisis}"

class TipoCultivo(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)  # Granos, Frutas, Vegetales
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Variedad(models.Model):
    tipo_cultivo = models.ForeignKey(TipoCultivo, on_delete=models.CASCADE, related_name='variedades')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tiempo_maduracion = models.IntegerField()  # en días
    resistencia_enfermedades = models.CharField(max_length=50)
    rendimiento_esperado = models.DecimalField(max_digits=8, decimal_places=2)  # por hectárea
    
    def __str__(self):
        return f"{self.tipo_cultivo} - {self.nombre}"

class Cultivo(models.Model):
    ESTADO_CHOICES = [
        ('planificado', 'Planificado'),
        ('en_siembra', 'En Siembra'),
        ('en_crecimiento', 'En Crecimiento'),
        ('en_cosecha', 'En Cosecha'),
        ('finalizado', 'Finalizado'),
    ]

    parcela = models.ForeignKey(Parcela, on_delete=models.CASCADE, related_name='cultivos')
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE)
    fecha_siembra = models.DateField()
    fecha_cosecha_estimada = models.DateField()
    fecha_cosecha_real = models.DateField(null=True, blank=True)
    area_sembrada = models.DecimalField(max_digits=8, decimal_places=2)  # en hectáreas
    rendimiento_obtenido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificado')  # Nuevo campo
    densidad_siembra = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Nuevo campo
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Cultivo'
        verbose_name_plural = 'Cultivos'
        ordering = ['-fecha_siembra']

    def __str__(self):
        return f"{self.variedad} en {self.parcela} ({self.fecha_siembra})"

class SistemaRiego(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # Aspersión, Goteo, Gravedad, etc.
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class FuenteAgua(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # Pozo, Río, Reservorio, etc.
    ubicacion = models.CharField(max_length=255)
    capacidad = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # en m³
    
    def __str__(self):
        return self.nombre

class PlanRiego(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='planes_riego')
    sistema_riego = models.ForeignKey(SistemaRiego, on_delete=models.CASCADE)
    fuente_agua = models.ForeignKey(FuenteAgua, on_delete=models.CASCADE)
    frecuencia_dias = models.IntegerField()  # cada cuántos días
    cantidad_agua = models.DecimalField(max_digits=8, decimal_places=2)  # en m³ por hectárea
    duracion = models.IntegerField()  # en minutos
    hora_preferida = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Plan de riego para {self.cultivo}"

class PlanFertilizacion(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='planes_fertilizacion')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return f"Plan de fertilización: {self.nombre} para {self.cultivo}"

class AplicacionFertilizante(models.Model):
    plan = models.ForeignKey(PlanFertilizacion, on_delete=models.CASCADE, related_name='aplicaciones')
    fecha_programada = models.DateField()
    fecha_aplicacion = models.DateField(null=True, blank=True)
    tipo_fertilizante = models.CharField(max_length=100)
    dosis_por_hectarea = models.DecimalField(max_digits=8, decimal_places=2)
    metodo_aplicacion = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Aplicación de {self.tipo_fertilizante} el {self.fecha_programada}"

class Plaga(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_cientifico = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    sintomas = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Enfermedad(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_cientifico = models.CharField(max_length=100, blank=True)
    agente_causal = models.CharField(max_length=100)  # Bacteria, Hongo, Virus, etc.
    descripcion = models.TextField(blank=True)
    sintomas = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class ControlPlagasEnfermedades(models.Model):
    TIPO_INCIDENCIA = [
        ('plaga', 'Plaga'),
        ('enfermedad', 'Enfermedad'),
    ]
    
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='controles')
    tipo_incidencia = models.CharField(max_length=20, choices=TIPO_INCIDENCIA)
    plaga = models.ForeignKey(Plaga, on_delete=models.CASCADE, null=True, blank=True)
    enfermedad = models.ForeignKey(Enfermedad, on_delete=models.CASCADE, null=True, blank=True)
    fecha_deteccion = models.DateField()
    nivel_infestacion = models.CharField(max_length=50)  # Bajo, Medio, Alto
    area_afectada = models.DecimalField(max_digits=8, decimal_places=2)  # en hectáreas
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        if self.tipo_incidencia == 'plaga':
            return f"Control de {self.plaga} en {self.cultivo}"
        else:
            return f"Control de {self.enfermedad} en {self.cultivo}"

class AccionCorrectiva(models.Model):
    control = models.ForeignKey(ControlPlagasEnfermedades, on_delete=models.CASCADE, related_name='acciones')
    fecha_accion = models.DateField()
    producto_aplicado = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)
    metodo_aplicacion = models.CharField(max_length=100)
    efectividad = models.CharField(max_length=50, null=True, blank=True)  # Baja, Media, Alta
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Acción del {self.fecha_accion} para {self.control}"

class EtapaFenologica(models.Model):
    ETAPA_CHOICES = [
        ('germinacion', 'Germinación'),
        ('desarrollo_vegetativo', 'Desarrollo Vegetativo'),
        ('floracion', 'Floración'),
        ('fructificacion', 'Fructificación'),
        ('maduracion', 'Maduración'),
    ]

    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='etapas')
    nombre = models.CharField(max_length=100, choices=ETAPA_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    grados_dia = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Nuevo campo
    descripcion = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Etapa Fenológica'
        verbose_name_plural = 'Etapas Fenológicas'
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"{self.nombre} de {self.cultivo}"

class TipoLabor(models.Model):
    nombre = models.CharField(max_length=100)  # Arado, Siembra, Cosecha, etc.
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class LaborAgricola(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='labores')
    tipo_labor = models.ForeignKey(TipoLabor, on_delete=models.CASCADE)
    fecha_realizacion = models.DateField()
    horas_empleadas = models.DecimalField(max_digits=5, decimal_places=2)
    personal_asignado = models.IntegerField()  # Número de trabajadores
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.tipo_labor} en {self.cultivo} el {self.fecha_realizacion}"

class CategoriaInsumo(models.Model):
    nombre = models.CharField(max_length=100)  # Semillas, Fertilizantes, Pesticidas, etc.
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class InsumoAgricola(models.Model):
    categoria = models.ForeignKey(CategoriaInsumo, on_delete=models.CASCADE, related_name='insumos')
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, blank=True)
    unidad_medida = models.CharField(max_length=50)  # kg, l, unidades, etc.
    descripcion = models.TextField(blank=True)
    instrucciones_uso = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

class LoteInsumo(models.Model):
    insumo = models.ForeignKey(InsumoAgricola, on_delete=models.CASCADE, related_name='lotes')
    codigo_lote = models.CharField(max_length=50)
    fecha_adquisicion = models.DateField()
    fecha_caducidad = models.DateField(null=True, blank=True)
    cantidad_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_actual = models.DecimalField(max_digits=10, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.CharField(max_length=100)  # Simplificado, podría ser una relación
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Lote {self.codigo_lote} de {self.insumo}"

class UsoInsumo(models.Model):
    labor = models.ForeignKey(LaborAgricola, on_delete=models.CASCADE, related_name='insumos_utilizados')
    lote_insumo = models.ForeignKey(LoteInsumo, on_delete=models.CASCADE, related_name='usos')
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_uso = models.DateField()
    
    def __str__(self):
        return f"Uso de {self.lote_insumo} en {self.labor}"

# Contexto Delimitado: Venta y Distribución
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # Mayorista, Minorista, Exportador, etc.
    ruc_dni = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    fecha_registro = models.DateField(auto_now_add=True)
    notas = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class ContactoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contactos')
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.nombre} de {self.cliente}"

class PreferenciaProducto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='preferencias')
    tipo_cultivo = models.ForeignKey(TipoCultivo, on_delete=models.CASCADE)
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE, null=True, blank=True)
    calidad_preferida = models.CharField(max_length=50)
    presentacion_preferida = models.CharField(max_length=100)
    volumen_habitual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    frecuencia_compra = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"Preferencia de {self.cliente}: {self.tipo_cultivo}"

class CanalDistribucion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class PreferenciaCanal(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='canales_preferidos')
    canal = models.ForeignKey(CanalDistribucion, on_delete=models.CASCADE)
    prioridad = models.IntegerField()  # 1 para el canal preferido, 2 para el segundo, etc.
    
    def __str__(self):
        return f"{self.cliente} prefiere {self.canal} (prioridad {self.prioridad})"

class CategoriaCalidad(models.Model):
    nombre = models.CharField(max_length=50)  # Premium, Estándar, Económico, etc.
    descripcion = models.TextField()
    criterios = models.JSONField()  # Criterios específicos en formato JSON
    
    def __str__(self):
        return self.nombre

class Presentacion(models.Model):
    nombre = models.CharField(max_length=100)  # Caja 10kg, Bolsa 1kg, etc.
    descripcion = models.TextField(blank=True)
    tipo_empaque = models.CharField(max_length=100)
    capacidad = models.DecimalField(max_digits=8, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)  # kg, unidades, etc.
    
    def __str__(self):
        return self.nombre

class ProductoTerminado(models.Model):
    ESTADO_CHOICES = [
        ('en_proceso', 'En Proceso'),
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('vendido', 'Vendido'),
    ]

    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='productos')
    codigo = models.CharField(max_length=50, unique=True)
    lote_produccion = models.CharField(max_length=50)
    fecha_procesamiento = models.DateField()
    categoria_calidad = models.ForeignKey(CategoriaCalidad, on_delete=models.CASCADE)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_caducidad = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_proceso')  # Nuevo campo
    trazabilidad_qr = models.CharField(max_length=255, blank=True)  # Nuevo campo
    
    class Meta:
        verbose_name = 'Producto Terminado'
        verbose_name_plural = 'Productos Terminados'
        ordering = ['-fecha_procesamiento']

    def __str__(self):
        return f"{self.codigo} - {self.cultivo.variedad} ({self.categoria_calidad})"

class InventarioProducto(models.Model):
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE, related_name='inventario')
    ubicacion_almacen = models.CharField(max_length=100)
    cantidad_disponible = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_reservada = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_ultima_actualizacion = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"Inventario de {self.producto}"

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    codigo = models.CharField(max_length=50, unique=True)
    fecha_pedido = models.DateField()
    fecha_entrega_solicitada = models.DateField()
    direccion_entrega = models.CharField(max_length=255)
    canal_distribucion = models.ForeignKey(CanalDistribucion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True)
    
    def __str__(self):
        return f"Pedido {self.codigo} de {self.cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Detalle: {self.producto} en {self.pedido}"

class Vehiculo(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=50)  # Camión, Furgoneta, etc.
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=20, unique=True)
    capacidad_carga = models.DecimalField(max_digits=10, decimal_places=2)  # en kg
    tipo_propiedad = models.CharField(max_length=50)  # Propio, Contratado
    estado = models.CharField(max_length=50)  # Disponible, En mantenimiento, En ruta
    
    def __str__(self):
        return f"{self.codigo} - {self.marca} {self.modelo} ({self.placa})"

class RutaEntrega(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    punto_partida = models.CharField(max_length=255)
    punto_llegada = models.CharField(max_length=255)
    distancia_total = models.DecimalField(max_digits=8, decimal_places=2)  # en km
    tiempo_estimado = models.IntegerField()  # en minutos
    
    def __str__(self):
        return self.nombre

class PuntoIntermedio(models.Model):
    ruta = models.ForeignKey(RutaEntrega, on_delete=models.CASCADE, related_name='puntos')
    nombre = models.CharField(max_length=100)
    orden = models.IntegerField()
    ubicacion = models.CharField(max_length=255)
    tiempo_estimado_llegada = models.IntegerField()  # en minutos desde el inicio
    
    def __str__(self):
        return f"{self.nombre} en {self.ruta}"

class Envio(models.Model):
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('en_transito', 'En Tránsito'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    pedidos = models.ManyToManyField(Pedido, related_name='envios')
    codigo = models.CharField(max_length=50, unique=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    ruta = models.ForeignKey(RutaEntrega, on_delete=models.CASCADE)
    fecha_programada = models.DateField()
    hora_salida = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programado')
    conductor = models.CharField(max_length=100)  # Simplificado, podría ser una relación
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Envío {self.codigo} del {self.fecha_programada}"

class DocumentoEnvio(models.Model):
    TIPO_CHOICES = [
        ('guia_remision', 'Guía de Remisión'),
        ('manifiesto_carga', 'Manifiesto de Carga'),
        ('otro', 'Otro'),
    ]
    
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    numero = models.CharField(max_length=50)
    fecha_emision = models.DateField()
    archivo = models.CharField(max_length=255, blank=True)  # Ruta al archivo
    
    def __str__(self):
        return f"{self.get_tipo_display()} {self.numero}"

class Factura(models.Model):
    ESTADO_CHOICES = [
        ('emitida', 'Emitida'),
        ('pagada', 'Pagada'),
        ('anulada', 'Anulada'),
    ]
    
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='factura')
    numero = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='emitida')
    
    def __str__(self):
        return f"Factura {self.numero} ({self.estado})"

class Pago(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='pagos')
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)  # Transferencia, Efectivo, Cheque, etc.
    referencia = models.CharField(max_length=100, blank=True)  # Nº de transferencia, cheque, etc.
    notas = models.TextField(blank=True)
    
    def __str__(self):
        return f"Pago de {self.monto} a {self.factura}"

class Devolucion(models.Model):
    MOTIVO_CHOICES = [
        ('calidad', 'Problemas de Calidad'),
        ('cantidad', 'Cantidad Incorrecta'),
        ('producto', 'Producto Incorrecto'),
        ('daño', 'Producto Dañado'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('solicitada', 'Solicitada'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('procesada', 'Procesada'),
    ]
    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='devoluciones')
    fecha_solicitud = models.DateField()
    motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='solicitada')
    fecha_resolucion = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Devolución de {self.pedido} ({self.estado})"

class DetalleDevolucion(models.Model):
    devolucion = models.ForeignKey(Devolucion, on_delete=models.CASCADE, related_name='detalles')
    detalle_pedido = models.ForeignKey(DetallePedido, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo_especifico = models.TextField(blank=True)
    accion = models.CharField(max_length=50)  # Reembolso, Reemplazo, Nota de crédito
    
    def __str__(self):
        return f"Detalle devolución: {self.cantidad} de {self.detalle_pedido.producto}"

# Contexto Delimitado: Gestión de Recursos
class Cargo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre

class Trabajador(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('vacaciones', 'En Vacaciones'),
        ('licencia', 'En Licencia'),
        ('suspendido', 'Suspendido'),
        ('inactivo', 'Inactivo'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=100)
    documento_identidad = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    fecha_contratacion = models.DateField()
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='activo')
    foto = models.CharField(max_length=255, blank=True)  # Nuevo campo
    contacto_emergencia = models.CharField(max_length=255, blank=True)  # Nuevo campo
    
    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'
        ordering = ['nombre_completo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre_completo}"

class Habilidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=50)  # Técnica, Administrativa, Operativa, etc.
    
    def __str__(self):
        return self.nombre

class HabilidadTrabajador(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    ]
    
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, related_name='habilidades')
    habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    fecha_adquisicion = models.DateField()
    certificado = models.CharField(max_length=255, blank=True)  # Ruta al certificado
    
    def __str__(self):
        return f"{self.trabajador} - {self.habilidad} ({self.nivel})"

class Capacitacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    institucion = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    horas_duracion = models.IntegerField()
    
    def __str__(self):
        return self.nombre

class CapacitacionTrabajador(models.Model):
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, related_name='capacitaciones')
    capacitacion = models.ForeignKey(Capacitacion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.trabajador} - {self.capacitacion}"

class Contrato(models.Model):
    TIPO_CHOICES = [
        ('indefinido', 'Indefinido'),
        ('temporal', 'Temporal'),
        ('obra', 'Por Obra'),
        ('parcial', 'Tiempo Parcial'),
    ]
    
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, related_name='contratos')
    codigo = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    horario = models.CharField(max_length=255)
    beneficios = models.TextField(blank=True)
    archivo = models.CharField(max_length=255, blank=True)  # Ruta al archivo
    
    def __str__(self):
        return f"Contrato {self.codigo} de {self.trabajador}"

class AsignacionLabor(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, related_name='asignaciones')
    labor = models.ForeignKey(LaborAgricola, on_delete=models.CASCADE, related_name='asignaciones')
    horas_asignadas = models.DecimalField(max_digits=5, decimal_places=2)
    rol = models.CharField(max_length=50)  # Supervisor, Operario, Auxiliar, etc.
    
    def __str__(self):
        return f"{self.trabajador} asignado a {self.labor}"

class CategoriaMaquinaria(models.Model):
    nombre = models.CharField(max_length=100)  # Tractor, Cosechadora, Sistema de Riego, etc.
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Maquinaria(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    categoria = models.ForeignKey(CategoriaMaquinaria, on_delete=models.CASCADE)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serie = models.CharField(max_length=100)
    año_fabricacion = models.IntegerField()
    capacidad = models.CharField(max_length=100)
    potencia = models.CharField(max_length=50, blank=True)
    horas_uso = models.IntegerField(default=0)
    estado = models.CharField(max_length=50)  # Operativa, Mantenimiento, Fuera de servicio
    ubicacion_actual = models.CharField(max_length=255)
    valor_adquisicion = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_adquisicion = models.DateField()
    
    def __str__(self):
        return f"{self.codigo} - {self.marca} {self.modelo}"

class MantenimientoMaquinaria(models.Model):
    TIPO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
    ]
    
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.CASCADE, related_name='mantenimientos')
    codigo = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha_programada = models.DateField()
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    horas_trabajo = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    costo_repuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    responsable = models.ForeignKey(Trabajador, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programado')
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.tipo} {self.codigo} para {self.maquinaria}"

class UsoMaquinaria(models.Model):
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.CASCADE, related_name='usos')
    labor = models.ForeignKey(LaborAgricola, on_delete=models.CASCADE, related_name='maquinarias_utilizadas')
    fecha_uso = models.DateField()
    horas_uso = models.DecimalField(max_digits=5, decimal_places=2)
    operador = models.ForeignKey(Trabajador, on_delete=models.SET_NULL, null=True, blank=True)
    combustible_consumido = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # en litros
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.maquinaria} en {self.labor}"

class TipoCosto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)  # Insumo, Mano de Obra, Maquinaria, Otros
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

class CostoOperativo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    tipo = models.ForeignKey(TipoCosto, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    cultivo = models.ForeignKey(Cultivo, on_delete=models.SET_NULL, null=True, blank=True, related_name='costos')
    labor = models.ForeignKey(LaborAgricola, on_delete=models.SET_NULL, null=True, blank=True)
    factura_referencia = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.tipo} ({self.monto})"

class Presupuesto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class LineaPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='lineas')
    tipo_costo = models.ForeignKey(TipoCosto, on_delete=models.CASCADE)
    descripcion = models.TextField()
    monto_presupuestado = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.tipo_costo} en {self.presupuesto}"

class InformeFinanciero(models.Model):
    TIPO_CHOICES = [
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('anual', 'Anual'),
        ('especial', 'Especial'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_generacion = models.DateField()
    autor = models.CharField(max_length=100)
    archivo = models.CharField(max_length=255, blank=True)  # Ruta al archivo
    
    def __str__(self):
        return f"{self.codigo} - {self.titulo}"

class AnalisisRentabilidad(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name='analisis_rentabilidad')
    fecha_analisis = models.DateField()
    ingresos_totales = models.DecimalField(max_digits=12, decimal_places=2)
    costos_directos = models.DecimalField(max_digits=12, decimal_places=2)
    costos_indirectos = models.DecimalField(max_digits=12, decimal_places=2)
    margen_bruto = models.DecimalField(max_digits=12, decimal_places=2)
    margen_neto = models.DecimalField(max_digits=12, decimal_places=2)
    roi = models.DecimalField(max_digits=8, decimal_places=2)  # Retorno sobre inversión en porcentaje
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Análisis de rentabilidad para {self.cultivo}"

class Proveedor(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    pagina_web = models.URLField(blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=50)  # Insumos, Maquinaria, Servicios, etc.
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class ContactoProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='contactos')
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.nombre} de {self.proveedor}"

class Contrato_Proveedor(models.Model):
    ESTADO_CHOICES = [
        ('vigente', 'Vigente'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='contratos')
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    condiciones_pago = models.CharField(max_length=255)
    monto_contrato = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='vigente')
    archivo = models.CharField(max_length=255, blank=True)  # Ruta al archivo
    
    def __str__(self):
        return f"Contrato {self.codigo} con {self.proveedor}"

class EvaluacionProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='evaluaciones')
    fecha = models.DateField()
    calidad_productos = models.IntegerField()  # De 1 a 10
    puntualidad_entregas = models.IntegerField()  # De 1 a 10
    precio_competitividad = models.IntegerField()  # De 1 a 10
    servicio_atencion = models.IntegerField()  # De 1 a 10
    puntuacion_total = models.IntegerField()
    comentarios = models.TextField(blank=True)
    evaluador = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Evaluación de {self.proveedor} el {self.fecha}"