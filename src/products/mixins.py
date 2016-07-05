import hashlib

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response 
from rest_framework import status

class ETAGMixin(object):
	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.response_with_etag_or_304(request, serializer, self.get_paginated_response(serializer.data))

		serializer = self.get_serializer(queryset, many=True)
		return self.response_with_etag_or_304(request, serializer, Response(serializer.data))

	def response_with_etag_or_304 (self, request, serializer, response):
		etag = hashlib.md5(JSONRenderer().render(serializer.data)).hexdigest()
		none_match_header = None
		if 'HTTP_IF_NONE_MATCH' in request.META:
			none_match_header = request.META['HTTP_IF_NONE_MATCH']
		elif 'If-None-Match' in request.META:
			none_match_header = request.META['If-None-Match']

		if none_match_header:
			if etag == none_match_header:
				response_304 = Response (data= '{}', status = status.HTTP_304_NOT_MODIFIED)
				return response_304
		response['ETAG'] = etag
		return response
