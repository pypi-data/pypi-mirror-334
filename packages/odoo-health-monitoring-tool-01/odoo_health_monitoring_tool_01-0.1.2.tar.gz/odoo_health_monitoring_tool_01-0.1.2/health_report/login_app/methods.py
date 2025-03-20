
import xmlrpc
from login_app.models import OdooSetup


def xmlrpc_connection(model_name,function_name):
    """Fetch Odoo's file health from PostgreSQL"""
    try:
        odoo_setup = OdooSetup.objects.filter().first()
        url = odoo_setup.url
        database=odoo_setup.database_name
        user = odoo_setup.username
        password = odoo_setup.api_token

        # Authenticate using the common endpoint
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')

        uid = common.authenticate(database, user, password, {})
        if uid:
            # Now connect to the object endpoint
            model = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            # Call the custom method
            result = model.execute_kw(database, uid, password,model_name,function_name, [])
            return result
        else:
            print("Authentication failed")
    except Exception as e:
        return {'error': f"{e}"}