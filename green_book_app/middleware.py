# myapp/middleware.py

from django.utils.deprecation import MiddlewareMixin


class TrackPageVisitsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        session = request.session
        visited_pages = session.get('visited_pages', {})

        # Get the current path
        path = request.path

        print(path)
        ignore_paths = ["/ajax", "/search", "/display-search-tags/", "admin"]
        # Count the number of slashes in the path
        if path.count('/') > 2 and not any(ignore in path for ignore in ignore_paths):
            # Update the visit count
            if path in visited_pages:
                visited_pages[path] += 1
            else:
                visited_pages[path] = 1

        session['visited_pages'] = visited_pages
        return None
