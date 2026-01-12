from odoo import models, fields, api

class Actividad(models.Model): # Convención: PascalCase
    _name = 'gestor.actividad'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Actividad / Sub-tarea'

    # CORRECCIÓN 1: Usamos 'name' para que Odoo lo reconozca automáticamente como título
    name = fields.Char(string='Nombre de la Actividad', required=True)
    
    detalle_tarea = fields.Text(string='Detalle de la Tarea')
    trabajo_id = fields.Many2one('gestor.trabajo', string='Trabajo padre', required=True, ondelete='cascade')
    
    # Nota: res.partner es para contactos/clientes. Si quieres usuarios internos usa 'res.users'
    persona_id = fields.Many2one('res.partner', string='Persona asignada') 
    
    inicio_planificado = fields.Date(string='Inicio Planificado')
    fin_planificado = fields.Date(string='Fin Planificado')
    
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En curso'),
        ('en_revision', 'En revisión'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    ], string='Estado', default='pendiente', tracking=True)
    
    # Este campo es el que suma el padre. Es required para evitar nulls en la suma.
    avance_individual = fields.Float(string='Avance (%)', default=0.0, required=True)

    # --- TRIGGERS PARA EL PADRE ---

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.trabajo_id:
                # Actualiza estado del padre si es necesario
                record.trabajo_id.verificar_estado_finalizado()
        return records

    def write(self, vals):
        res = super().write(vals)
        # Si cambiamos estado o avance, avisamos al padre
        if 'estado' in vals or 'avance_individual' in vals:
            for record in self:
                if record.trabajo_id:
                    # Esto revisa si el trabajo debe finalizarse
                    record.trabajo_id.verificar_estado_finalizado()
                    
                    # El recalculo del % del padre se hace solo gracias al @api.depends
                    # que pusimos en gestor.trabajo, no hace falta forzarlo aquí.
        return res