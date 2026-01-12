from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Trabajo(models.Model):
    _name = 'gestor.trabajo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Trabajo'

    name = fields.Char(string='Descripción del trabajo', required=True)
    # Relación con el padre (Proyecto)
    proyecto_id = fields.Many2one('gestor.proyecto', string='Proyecto', required=True)
    responsable_id = fields.Many2one('res.users', string='Responsable/Técnico asignado')
    fecha_inicio = fields.Date(string='Fecha de inicio')
    fecha_fin = fields.Date(string='Fecha de finalización')
    
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('en_revision', 'En revisión'),
        ('finalizado', 'Finalizado')
    ], string='Estado actual', default='pendiente')

    actividad_ids = fields.One2many('gestor.actividad', 'trabajo_id', string='Actividades')
    
    # Campo calculado para el avance
    promedio_avance = fields.Float(
        string='Promedio de avance de actividades', 
        compute='_compute_promedio_avance', 
        store=True
    )
    
    importancia = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente')
    ], string='Importancia', default='media')
    
   # Campo para escribir manualmente el dato
    avance_individual = fields.Float(string='Avance manual (%)', default=0.0)

    # Campo que muestra el resultado final (La barra)
    promedio_avance = fields.Float(
        string='Promedio de avance', 
        compute='_compute_promedio_avance', 
        store=True
    )

    # CORRECCIÓN 1: Añadir 'avance_individual' a los depends
    @api.depends('actividad_ids.avance_individual', 'avance_individual')
    def _compute_promedio_avance(self):
        for record in self:
            if record.actividad_ids:
                # CASO A: Si tiene actividades, calculamos la media de ellas
                avances = record.actividad_ids.mapped('avance_individual')
                record.promedio_avance = sum(avances) / len(avances) if avances else 0.0
            else:
                # CASO B: Si NO tiene actividades, usamos el valor manual que escribiste
                record.promedio_avance = record.avance_individual

    # Regla de negocio 2: Si todas las actividades finalizan, el trabajo finaliza
    def verificar_estado_finalizado(self):
        for record in self:
            if record.actividad_ids and all(a.estado == 'finalizada' for a in record.actividad_ids):
                record.estado = 'finalizado'
                # Avisar al proyecto padre para ver si también debe finalizarse
                record.proyecto_id.verificar_estado_finalizado()

    # Regla de negocio 4: Control de fechas
    # IMPORTANTE: Fíjate que esto está metido hacia la derecha, alineado con 'def' de arriba
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas_proyecto(self):
        for record in self:
            if record.proyecto_id.fecha_inicio and record.fecha_inicio:
                if record.fecha_inicio < record.proyecto_id.fecha_inicio:
                    raise ValidationError("La fecha de inicio del trabajo no puede ser anterior a la del proyecto.")
            if record.proyecto_id.fecha_fin and record.fecha_fin:
                if record.fecha_fin > record.proyecto_id.fecha_fin:
                    raise ValidationError("La fecha fin del trabajo no puede ser posterior a la del proyecto.")