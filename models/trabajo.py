from odoo import models, fields, api

class trabajo(models.Model):
    _name = 'gestor.trabajo'
    _description = 'gestor.trabajo'

    name = fields.Char(string='Descripción del trabajo', required=True)
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
    promedio_avance = fields.Float(string='Promedio de avance de actividades', compute='_compute_promedio_avance', store=True)
    importancia = fields.Selection([
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente')
    ], string='Importancia', default='media')
    avance_individual = fields.Float(string='Avance individual (%)', default=0.0)

    @api.depends('actividad_ids.avance')
    def _compute_promedio_avance(self):
        for record in self:
            avances = record.actividad_ids.mapped('avance')
            record.promedio_avance = sum(avances) / len(avances) if avances else 0.0