from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Proyecto(models.Model):
    _name = 'gestor.proyecto'
    _inherit=['mail.thread','mail.activity.mixin']
    _description = 'Proyecto'

    name = fields.Char(string='Nombre del proyecto', required=True)
    descripcion = fields.Text(string='Descripción general')
    fecha_inicio = fields.Date(string='Fecha de inicio')
    fecha_fin = fields.Date(string='Fecha de fin')
    responsable_id = fields.Many2one('res.users', string='Responsable del proyecto')
    
    # Relación con trabajos [cite: 10]
    trabajo_ids = fields.One2many('gestor.trabajo', 'proyecto_id', string='Trabajos')
    
    # Campo calculado para el avance del proyecto [cite: 10]
    porcentaje_avance = fields.Float(
        string='Porcentaje de avance (%)', 
        compute='_compute_avance_proyecto', 
        store=True
    )
    
    avance_individual = fields.Float(string='Avance manual (%)', default=0.0)

    # Estados del proyecto [cite: 12-17]
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('planificacion', 'En planificación'),
        ('ejecucion', 'En ejecución'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado')
    ], string='Estado', default='borrador')

    porcentaje_avance = fields.Float(
        string='Porcentaje de avance (%)', 
        compute='_compute_avance_proyecto', 
        store=True
    )
    
    # IMPORTANTE: Este campo debe ser editable para que el usuario ponga el % manual
    avance_individual = fields.Float(string='Avance manual (%)', default=0.0)

    # CORRECCIÓN 1: Añadimos 'avance_individual' a los depends para que recalcule al cambiarlo
    @api.depends('trabajo_ids.promedio_avance', 'avance_individual')
    def _compute_avance_proyecto(self):
        for record in self:
            if record.trabajo_ids:
                # Si hay trabajos, mandan los trabajos (calculo automático)
                total_avance = sum(record.trabajo_ids.mapped('promedio_avance'))
                # Evitamos división por cero por seguridad
                record.porcentaje_avance = total_avance / len(record.trabajo_ids) if len(record.trabajo_ids) > 0 else 0.0
            else:
                # Si NO hay trabajos, usamos el valor manual
                record.porcentaje_avance = record.avance_individual

    # Regla de negocio 2: Si todos los trabajos finalizan, el proyecto finaliza [cite: 41]
    def verificar_estado_finalizado(self):
        for record in self:
            # Si tiene trabajos y todos están finalizados
            if record.trabajo_ids and all(t.estado == 'finalizado' for t in record.trabajo_ids):
                record.estado = 'finalizado'

    # Regla de negocio 3: Restricción de borrado [cite: 43]
    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_draft(self):
        for record in self:
            if record.trabajo_ids and record.estado != 'borrador':
                raise ValidationError("No se puede eliminar un proyecto con trabajos asociados salvo que esté en estado Borrador.")

    # Regla de negocio 3: No cerrar si hay trabajos en curso [cite: 44]
    @api.constrains('estado')
    def _check_cierre_proyecto(self):
        for record in self:
            if record.estado == 'finalizado':
                trabajos_pendientes = record.trabajo_ids.filtered(lambda t: t.estado not in ['finalizado', 'cancelado'])
                if trabajos_pendientes:
                    raise ValidationError("No se puede cerrar el proyecto si hay trabajos en curso o pendientes.")