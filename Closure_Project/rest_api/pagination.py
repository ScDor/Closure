from django.core.exceptions import BadRequest
from rest_framework.pagination import LimitOffsetPagination


def _validate_limit(integer_string, max_value):
    num = int(integer_string)
    if num <= 0 or num > max_value:
        raise BadRequest(f'limit must be between 1 and {max_value}')
    return num


class ResultSetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                return _validate_limit(
                    request.query_params[self.limit_query_param],
                    self.max_limit
                )
            except KeyError:
                self.default_limit
