{
    'name': "To-Do Application",
    'description': "Manage your personal Tasks with this module.",
    'author': "Mohamed Alkobrosli",
    'depends': ['mail'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/todo_view.xml'
        ],
}
