from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, send_from_directory, render_template
from flask_appbuilder import BaseView, expose
import os

# Get Plugin Directory
PLUGIN_DIR = os.path.dirname(__file__)

# Define Blueprint
react_bp = Blueprint(
    "react_plugin",
    __name__,
    static_folder=os.path.join(PLUGIN_DIR, "static"),
    template_folder=os.path.join(PLUGIN_DIR, "templates")
)

# Serve static assets (JS, CSS, images)
@react_bp.route("/react/static/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(os.path.join(PLUGIN_DIR, "static/assets"), filename)

@react_bp.route("/react/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(os.path.join(PLUGIN_DIR, "static"), filename)

# Serve React Index Page
@react_bp.route("/react")
def serve_react():
    return render_template("index.html")

# Flask AppBuilder View for Airflow UI
class ReactView(BaseView):
    default_view = "react"

    @expose("/")
    def react(self):
        return self.render_template("index.html")

# Register Plugin
class MyReactPlugin(AirflowPlugin):
    name = "drag_drop"
    flask_blueprints = [react_bp]  # Enable /react in Flask
    appbuilder_views = [
        {
            "name": "Drag & Drop",
            "category": "Plugins",
            "view": ReactView()
        }
    ]

