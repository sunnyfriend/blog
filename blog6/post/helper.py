from django.core.cache import cache

#function : @page_cache, for view.home and view.article
#           to cache the html-page
#           add one case with timeout reload cache
def page_cache(timeout):
	def wrap1(func):
		def wrap2(request):
			key = 'Pages-%s'%request.get_full_path()
			require =  cache.get(key)
			if require:
				response = require
			else:
				cache.set(key,func(request),timeout)
				response = func(request)
			return response
		return wrap2
	return wrap1
