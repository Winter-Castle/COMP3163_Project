# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .student import student_views
from .staff import staff_views
from .commandHistory import command_history_views


views = [user_views, index_views, auth_views, student_views,staff_views, command_history_views]

# blueprints must be added to this list
