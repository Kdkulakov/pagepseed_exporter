class Response(object):
    """ Base Response Object

    Attributes:
        self.json (dict): JSON representation of response
        self._request (str): URL of
        self._response (`requests.models.Response` object): Response object from requests module
    """

    def __init__(self, response):
        response.raise_for_status()

        self._response = response
        self._request = response.url
        self.json = response.json()

    def __repr__(self):
        return '<Response>'


class PageSpeedResponse(Response):
    """ PageSpeed Response Object

    Attributes:
        self.url (str):
        self.title (str):
        self.responsecode (str):
        self.locale (str):
        self.version (str):
        self.speed (int):
        self.statistics (`Statistics` object): for_old_version_api
        self.loading_experience (`LoadingExperience` object):
        self.lighthouse_results_audits ('LighthouseResultsAudits' object): metrics from block
        self.lighthouse_results ('LighthouseResults' object): metrics from block
    """

    @property
    def url(self):
        return self.json.get('id')

    @property
    def title(self):
        return self.json.get('title')

    @property
    def responsecode(self):
        return self.json.get('responseCode')

    @property
    def locale(self):
        return self.json.get('formattedResults').get('locale')

    @property
    def version(self):
        major = self.json.get('version').get('major')
        minor = self.json.get('version').get('minor')
        return '{0}.{1}'.format(major, minor)

    @property
    def speed(self):
        return self.json.get('ruleGroups').get('SPEED').get('score')

    @property
    def statistics(self):
        page_stats = self.json.get('pageStats')
        return Statistics(page_stats)

    @property
    def loading_experience(self):
        metrics = self.json.get('loadingExperience').get('metrics')
        return LoadingExperience(metrics)

    @property
    def lighthouse_results_audits(self):
        metrics = self.json.get('lighthouseResult').get('audits')
        return LighthouseResultAudits(metrics)

    @property
    def lighthouse_results(self):
        metrics = self.json.get('lighthouseResult')
        return LighthouseResult(metrics)

    @property
    def categories(self):
        metrics = self.json.get('categories')
        return Categories(metrics)

    def to_csv(self, path):
        pass

    def pretty_print(self):
        pass

    def __repr__(self):
        return '<Response(url={0})>'.format(self.url)


class DesktopPageSpeed(PageSpeedResponse):

    def __repr__(self):
        return '<DesktopPageSpeed(url={0})>'.format(self.url)


class MobilePageSpeed(PageSpeedResponse):

    @property
    def usability(self):
        return self.json.get('ruleGroups').get('USABILITY').get('score')

    def __repr__(self):
        return '<MobilePageSpeed(url={0})>'.format(self.url)


class Statistics(object):
    def __init__(self, page_stats):
        self.page_stats = page_stats

    @property
    def css_response_bytes(self):
        return self.page_stats.get('cssResponseBytes')

    @property
    def html_response_bytes(self):
        return self.page_stats.get('htmlResponseBytes')

    @property
    def image_response_bytes(self):
        return self.page_stats.get('imageResponseBytes')

    @property
    def javascript_response_bytes(self):
        return self.page_stats.get('javascriptResponseBytes')

    @property
    def number_css_resources(self):
        return self.page_stats.get('numberCssResources')

    @property
    def number_hosts(self):
        return self.page_stats.get('numberHosts')

    @property
    def number_js_resources(self):
        return self.page_stats.get('numberJsResources')

    @property
    def number_resources(self):
        return self.page_stats.get('numberResources')

    @property
    def number_static_resources(self):
        return self.page_stats.get('numberStaticResources')

    @property
    def other_response_bytes(self):
        return self.page_stats.get('otherResponseBytes')

    @property
    def text_response_bytes(self):
        return self.page_stats.get('textResponseBytes')

    @property
    def total_request_bytes(self):
        return self.page_stats.get('totalRequestBytes')

    @property
    def over_the_wire_response_bytes(self):
        return self.page_stats.get('overTheWireResponseBytes')

    @property
    def num_total_round_trips(self):
        return self.page_stats.get('numTotalRoundTrips')

    @property
    def num_render_blocking_round_trips(self):
        return self.page_stats.get('numRenderBlockingRoundTrips')


class LoadingExperience(object):
    def __init__(self, metrics):
        self.metrics = metrics

    @property
    def first_input_delay(self):
        return self.metrics.get('FIRST_INPUT_DELAY_MS')


class Categories(object):
    def __init__(self, metrics):
        self.metrics = metrics

    @property
    def performance(self):
        return self.metrics.get('performance')


class LighthouseResult(object):
    def __init__(self, metrics):
        self.metrics = metrics

    @property
    def timing(self):
        return self.metrics.get('timing')


class LighthouseResultAudits(object):
    def __init__(self, metrics):
        self.metrics = metrics

    @property
    def interactive(self):
        return self.metrics.get('interactive')

    @property
    def third_party_summary(self):
        return self.metrics.get('third-party-summary')

    @property
    def speed_index(self):
        return self.metrics.get('speed-index')

    @property
    def first_cpu_idle(self):
        return self.metrics.get('first-cpu-idle')

    @property
    def total_byte_weight(self):
        return self.metrics.get('total-byte-weight')

    @property
    def mainthread_work_breakdown(self):
        return self.metrics.get('mainthread-work-breakdown')

    @property
    def first_contentful_paint(self):
        return self.metrics.get('first-contentful-paint')

    @property
    def uses_webp_images(self):
        return self.metrics.get('uses-webp-images')

    @ property
    def first_meaningful_paint(self):
        return self.metrics.get('first-meaningful-paint')

    @ property
    def render_blocking_resources(self):
        return self.metrics.get('render-blocking-resources')

    @ property
    def uses_text_compression(self):
        return self.metrics.get('uses-text-compression')

    @ property
    def uses_optimized_images(self):
        return self.metrics.get('uses-optimized-images')

    @ property
    def uses_long_cache_ttl(self):
        return self.metrics.get('uses-long-cache-ttl')

    @ property
    def max_potential_fid(self):
        return self.metrics.get('uses-long-cache-ttl')

    @ property
    def max_potential_fid(self):
        return self.metrics.get('uses-long-cache-ttl')

    @ property
    def total_blocking_time(self):
        return self.metrics.get('total-blocking-time')

    @ property
    def estimated_input_latency(self):
        return self.metrics.get('estimated-input-latency')

    @ property
    def uses_rel_preconnect(self):
        return self.metrics.get('uses-rel-preconnect')

    @ property
    def bootup_time(self):
        return self.metrics.get('bootup-time')

    @ property
    def unminified_css(self):
        return self.metrics.get('unminified-css')

    @ property
    def network_server_latency(self):
        return self.metrics.get('network-server-latency')

    @ property
    def offscreen_images(self):
        return self.metrics.get('offscreen-images')

    @ property
    def uses_responsive_images(self):
        return self.metrics.get('uses-responsive-images')

    @ property
    def unused_css_rules(self):
        return self.metrics.get('unused-css-rules')

    @ property
    def total_byte_weight(self):
        return self.metrics.get('total-byte-weight')

    @ property
    def uses_webp_images(self):
        return self.metrics.get('uses-webp-images')

    @ property
    def dom_size(self):
        return self.metrics.get('dom-size')

    @ property
    def uses_rel_preload(self):
        return self.metrics.get('uses-rel-preload')

    @ property
    def unminified_javascript(self):
        return self.metrics.get('unminified-javascript')

    @ property
    def redirects(self):
        return self.metrics.get('redirects')


