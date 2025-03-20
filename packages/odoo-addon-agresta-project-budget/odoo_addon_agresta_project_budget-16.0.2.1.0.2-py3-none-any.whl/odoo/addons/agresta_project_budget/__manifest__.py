{
    "name": "Odoo customizations for Agresta",
    "version": "16.0.2.1.0.2",
    "depends": [
        "project",
        "sale_timesheet",
    ],
    "author": "Coopdevs Treball SCCL",
    "website": "https://coopdevs.org",
    "category": "Project",
    "summary": """
    Odoo customizations for Agresta
    """,
    "license": "AGPL-3",
    "data": [
        "data/security_groups.xml",
        "data/scheduled_action.xml",
        "security/ir.model.access.csv",
        "views/project_task.xml",
        "views/project.xml",
        "views/project_update.xml",
        "views/menus.xml",
    ],
}
