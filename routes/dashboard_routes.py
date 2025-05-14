from flask import Blueprint, render_template, g
from models import AnnualLeave
from decorators import login_required

# Define the 'dashboard' blueprint
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def dashboard_view():
    # Fetch all approved leave records, ordered by updated_at descending
    leaves = AnnualLeave.query.where(AnnualLeave.status == 'Approved').order_by(AnnualLeave.updated_at.desc()).all()

    # Render the dashboard template with user role and leave data
    return render_template(
        'pages/dashboard.html',
        is_admin=g.user.is_admin,
        leaves=leaves
    )


@dashboard.route('/your-leaves')
@login_required
def your_leave_view():

    # Fetch all leave records for the current user, ordered by updated_at descending. If rejected do not display on the dashboard
    leaves = AnnualLeave.query.filter_by(user_id=g.user.id).order_by(AnnualLeave.updated_at.desc()).all()

    # Render the dashboard template with user role and leave data
    return render_template('pages/your_leaves.html', user=g.user, leaves=leaves)
    
