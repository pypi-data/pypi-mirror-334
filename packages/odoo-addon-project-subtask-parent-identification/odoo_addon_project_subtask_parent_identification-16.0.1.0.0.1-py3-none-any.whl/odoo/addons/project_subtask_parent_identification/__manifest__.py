# Copyright 2025 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Project Subtask Parent Identification",
    "summary": "Project Subtask Parent Identification",
    "version": "16.0.1.0.0",
    "category": "Project",
    "website": "https://github.com/sygel-technology/sy-project",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "project",
        "project_task_identification",
    ],
    "data": [
        "views/project_task_views.xml",
    ],
}
