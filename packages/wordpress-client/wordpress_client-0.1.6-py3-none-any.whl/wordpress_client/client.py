import requests
from urllib.parse import urlparse, urlunparse
import random

class WordPressPost:
    def __init__(self, post_data):
        self.id = post_data.get('id')
        self.post_title = post_data.get('title', {}).get('rendered', '')
        self.post_content = post_data.get('content', {}).get('rendered', '')
        self.post_date = post_data.get('date')
        self.post_url = post_data.get('link')
        self.status = post_data.get('status')
        self.author_id = post_data.get('author')
        self.categories = post_data.get('categories', [])
        self.tags = post_data.get('tags', [])
        self.comment_count = post_data.get('comment_count')
        self.excerpt = post_data.get('excerpt', {}).get('rendered', '')
        self.featured_media = post_data.get('featured_media')
        self.metadata = post_data.get('meta', {})

class WordPressCategory:
    def __init__(self, category_data):
        self.id = category_data.get('id')
        self.name = category_data.get('name', '')
        self.slug = category_data.get('slug', '')
        self.description = category_data.get('description', '')
        self.count = category_data.get('count')
        self.parent = category_data.get('parent')

class WordPressTag:
    def __init__(self, tag_data):
        self.id = tag_data.get('id')
        self.name = tag_data.get('name', '')
        self.slug = tag_data.get('slug', '')
        self.description = tag_data.get('description', '')
        self.count = tag_data.get('count')

class WordPressComment:
    def __init__(self, comment_data):
        self.id = comment_data.get('id')
        self.post = comment_data.get('post')
        self.author_name = comment_data.get('author_name', '')
        self.author_email = comment_data.get('author_email', '')
        self.content = comment_data.get('content', {}).get('rendered', '')
        self.date = comment_data.get('date')
        self.status = comment_data.get('status')

class WordPressClient:
    def __init__(self, site_url, proxy=None):
        parsed_url = urlparse(site_url)
        if not parsed_url.scheme:
            parsed_url = parsed_url._replace(scheme='https')
        elif parsed_url.scheme not in ['http', 'https']:
            raise ValueError("URL scheme must be either 'http' or 'https'")
        
        self.site_url = urlunparse(parsed_url).rstrip('/')
        self.session = requests.Session()
        
        # Proxy ayarı varsa session’a ekleniyor
        if proxy:
            self.session.proxies.update(proxy)

    def _json_to_wordpress_posts(self, json_posts):
        """Convert JSON data to WordPressPost instances."""
        return [WordPressPost(post_data) for post_data in json_posts]

    def _json_to_wordpress_categories(self, json_categories):
        """Convert JSON data to WordPressCategory instances."""
        return [WordPressCategory(category_data) for category_data in json_categories]

    def _json_to_wordpress_tags(self, json_tags):
        """Convert JSON data to WordPressTag instances."""
        return [WordPressTag(tag_data) for tag_data in json_tags]

    def _json_to_wordpress_comments(self, json_comments):
        """Convert JSON data to WordPressComment instances."""
        return [WordPressComment(comment_data) for comment_data in json_comments]

    def _make_request_with_retry(self, method, url, **kwargs):
        """
        Proxy kullanılıyorsa 3 kez deneme (retry) yapan yardımcı metod.
        Başarısız olursa None döndürür. 
        Proxy yoksa tek seferlik istek yapar.
        """
        # Eğer proxy tanımlı ise en az 3 kez dene
        if self.session.proxies:
            attempts = 3
            last_exception = None

            for attempt in range(attempts):
                try:
                    response = self.session.request(method, url, **kwargs)
                    response.raise_for_status()
                    return response
                except requests.RequestException as e:
                    last_exception = e
                    # Deneme başarısız oldu, yeniden dene
                    if attempt < attempts - 1:
                        continue
            # Tüm denemeler başarısız
            print(f"Failed after {attempts} attempts. Last error: {last_exception}")
            return None
        else:
            # Proxy yoksa tek seferde istek yap
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Request failed. Error: {e}")
                return None

    def get_recent_posts(self, post_count=5):
        url = f'{self.site_url}/wp-json/wp/v2/posts?per_page={post_count}'
        response = self._make_request_with_retry('GET', url)
        if response:
            return self._json_to_wordpress_posts(response.json())
        return []

    def get_categories(self):
        url = f'{self.site_url}/wp-json/wp/v2/categories'
        response = self._make_request_with_retry('GET', url)
        if response:
            return self._json_to_wordpress_categories(response.json())
        return []

    def get_tags(self):
        url = f'{self.site_url}/wp-json/wp/v2/tags'
        response = self._make_request_with_retry('GET', url)
        if response:
            return self._json_to_wordpress_tags(response.json())
        return []

    def get_posts_by_category(self, category_id, post_count=5, post_order='desc'):
        url = f'{self.site_url}/wp-json/wp/v2/posts?categories={category_id}&per_page={post_count}&orderby=date&order={post_order}'
        response = self._make_request_with_retry('GET', url)
        if response:
            return self._json_to_wordpress_posts(response.json())
        return []

    def get_posts_by_date_range(self, start_date, end_date, category_id=None, post_count=5):
        try:
            url = f'{self.site_url}/wp-json/wp/v2/posts?after={start_date}T00:00:00&before={end_date}T23:59:59&per_page={post_count}'
            if category_id:
                url += f'&categories={category_id}'
            response = self._make_request_with_retry('GET', url)
            if response:
                return self._json_to_wordpress_posts(response.json())
            return []
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return []
        
    def get_image_url_by_media_id(self, media_id):
        """
        Retrieve the URL of the image for a given featured_media ID.
        
        :param media_id: The ID of the media to retrieve.
        :return: The URL of the image, or None if not found.
        """
        url = f'{self.site_url}/wp-json/wp/v2/media/{media_id}'
        response = self._make_request_with_retry('GET', url)
        if response:
            media_data = response.json()
            if 'source_url' in media_data:
                return media_data['source_url']
            else:
                print(f"No 'source_url' found for media ID {media_id}")
                return None
        return None

    def get_comments_by_post(self, post_id):
        url = f'{self.site_url}/wp-json/wp/v2/comments?post={post_id}'
        response = self._make_request_with_retry('GET', url)
        if response:
            return self._json_to_wordpress_comments(response.json())
        return []

    def get_posts_by_author(self, author_id, post_count=5):
        url = f'{self.site_url}/wp-json/wp/v2/posts?author={author_id}&per_page={post_count}'
        response = self._make_request_with_retry('GET', url)
        if response:
            return self._json_to_wordpress_posts(response.json())
        return []

    def get_posts_from_wordpress(self, website_categories="", post_count=1, post_order='desc'):
        # Split categories into a list if provided
        categories = website_categories.split(',') if website_categories else []
        
        all_posts = []

        def fetch_posts(category=None):
            params = {
                'per_page': post_count,
                'orderby': 'date',
                'order': 'desc' if post_order == 'desc' else 'asc',
            }
            if category:
                params['categories'] = category

            # Tek seferde proxy varsa 3 kez denemeli istek yap
            response = self._make_request_with_retry('GET', f'{self.site_url}/wp-json/wp/v2/posts', params=params)
            if response:
                return response.json()
            return []

        # Fetch posts for each category if provided
        if categories:
            for category in categories:
                posts = fetch_posts(category)
                all_posts.extend(self._json_to_wordpress_posts(posts))
        else:
            # No categories provided, fetch latest posts
            posts = fetch_posts()
            all_posts.extend(self._json_to_wordpress_posts(posts))

        # Handle post_order (sort posts based on post_order)
        if post_order == 'random':
            random.shuffle(all_posts)
        elif post_order == 'asc':
            all_posts.sort(key=lambda x: x.post_date)
        else:
            # Default to 'desc' (latest first)
            all_posts.sort(key=lambda x: x.post_date, reverse=True)

        return all_posts
