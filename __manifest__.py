{
    'name': "Gestor De Proyectos",
    'summary': "Gestor donde se lleva el seguimiento de proyectos",
    'description': """
        Gestor de proyectos para controlar el desarrollo de apps en 2ºDAM.
        Permite gestionar Proyectos, Trabajos y Actividades.
    """,
    'author': "Luis Alfonso Pérez Rojo", # [cite: 76] El PDF pide el autor.
    'website': "https://www.yourcompany.com",
    'category': 'Project Management',
    'version': '0.1',

    # Dependencias: 'mail' es OBLIGATORIO para las notificaciones y el chatter
    'depends': ['base', 'mail'], 

    # Archivos de datos: El orden es IMPORTANTE
    'data': [
        # 1. Seguridad (Primero los grupos, luego el CSV)
        'security/security.xml',
        'security/ir.model.access.csv',
        
        # 2. Vistas de los modelos (Tal como pide el PDF )
        'views/proyecto_view.xml',
        'views/trabajo_view.xml',
        'views/actividad_view.xml',
        
        # 3. Menús (Se cargan al final para que encuentren las acciones)
        'views/menus.xml',
    ],
    
    # Archivos de demostración [cite: 81]
    'demo': [
        'data/demo_data.xml', # Asegúrate de crear este archivo o comenta la línea si no lo tienes aún
    ],
    
    # Icono del módulo 
    'icon': '/gestor/static/description/icon.png', 
    
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}