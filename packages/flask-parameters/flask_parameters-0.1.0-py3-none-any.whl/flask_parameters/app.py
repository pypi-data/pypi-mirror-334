import flask

from flask_parameters.exceptions import register_error_handlers
from flask_parameters.flask_helpers import inject_and_validate_query_params


class Flask(flask.Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        register_error_handlers(self)

    def route(self, rule, ignore_args=[], **options):
        def decorator(f):
            endpoint = options.pop("endpoint", f.__name__)
            self.add_url_rule(
                rule,
                endpoint,
                inject_and_validate_query_params(ignore_args=ignore_args)(f),
                **options,
            )
            return f

        return decorator
