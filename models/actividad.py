from odoo import models, fields

class actividad(models.Model):
    _name = 'gestor.actividad'
    _description = 'gestor.actividad'

    nombre = fields.Char(string='Nombre de la Actividad', required=True)
    detalle_tarea = fields.Text(string='Detalle de la Tarea')
    trabajo_id = fields.Many2one('gestor.trabajo', string='Trabajo al que pertenece', required=True)
    persona_id = fields.Many2one('res.partner', string='Persona que la realiza')
    inicio_planificado = fields.Date(string='Inicio Planificado')
    fin_planificado = fields.Date(string='Fin Planificado')
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En curso'),
        ('en_revision', 'En revisión'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    ], string='Estado de la Actividad', default='pendiente')
    avance_individual = fields.Float(string='Avance Individual (%)', default=0.0, required=True)