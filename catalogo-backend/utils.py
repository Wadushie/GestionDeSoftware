import sys
from flask_restful.reqparse import Namespace
from flask import request

# Utility function to only execute and assigment to an object if the value from a reqparse.Namespace dict is not None
def _assign_if_something(obj: object, newdata: Namespace, key: str):
    value = newdata.get(key)
    if value is not None:
        obj.__setattr__(key, value)

def paginated_results(query):
    pagination = request.args.get('pagination', 'true', str)
    jsondepth = request.args.get('jsondepth', 1, int)
    if pagination == 'true':
        per_page = request.args.get('rowsPerPage', None, int)
        per_page = sys.maxsize if per_page == 0 else per_page  # Cero is evaluated to None, Max items take 1000 items
        page=request.args.get('page', 1, int)
        paginated = query.paginate(page=page, per_page=per_page)
        return {
            'page': paginated.page,
            'pages': paginated.pages,
            'per_page': paginated.per_page,
            'total': query.count(),
            'items': [x.json(jsondepth) if jsondepth else x.json() for x in paginated.items]
        }
    else:
        return [x.json(jsondepth) if jsondepth else x.json() for x in query.all()]
 
 # Apply filter restrictions
def restrict(query, filters, name, condition, null_condition=None):
    f = filters.get(name)
    if f is not None:
        if isinstance(f, str):
            if f != '':
                query = query.filter(condition(f))
        else:
            query = query.filter(condition(f))
    elif name is not None and null_condition is not None:
        query = query.filter(null_condition(name))
    return query