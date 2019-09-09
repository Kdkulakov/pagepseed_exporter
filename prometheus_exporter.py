from prometheus_client import start_http_server, Summary, Counter, Info, Gauge
import time
import os
from pagespeed import PageSpeed
import csv
import logging
from importlib import reload  # need to reload logging module
import re
reload(logging)


"""Simple is better than complex."""

SLEEP_TIMER = 120
HTTP_SERVER_PORT = 8000

psd = PageSpeed()

# inicializing metrics names to prometheus

time_to_interactive = Gauge('pagespeed_timetointeractive', '', ['url'])
time_to_interactive_displayvalue = Gauge('pagespeed_timetointeractive_displayvalue', '', ['url'])
time_to_interactive_info = Info('pagespeed_timetointeractive', '')

speed_index = Gauge('pagespeed_speedindex', '', ['url'])
speed_index_displayvalue = Gauge('pagespeed_speedindex_displayvalue', '', ['url'])
speed_index_info = Info('pagespeed_speedindex', '')

first_cpu_idle_score = Gauge('pagespeed_first_cpu_idle_score', '', ['url'])
first_cpu_idle_score_displayvalue = Gauge('pagespeed_first_cpu_idle_score_displayvalue', '', ['url'])
first_cpu_idle_score_info = Info('pagespeed_first_cpu_idle_score', '')

mainthread_work_breakdown = Gauge('pagespeed_mainthread_work_breakdown', '', ['url'])
mainthread_work_breakdown_displayvalue = Gauge('pagespeed_mainthread_work_breakdown_displayvalue', '', ['url'])
mainthread_work_breakdown_info = Info('pagespeed_mainthread_work_breakdown', '')

first_contentful_paint = Gauge('pagespeed_first_contentful_paint', '', ['url'])
first_contentful_paint_displayvalue = Gauge('pagespeed_first_contentful_paint_displayvalue', '', ['url'])
first_contentful_paint_info = Info('pagespeed_first_contentful_paint', '')

first_meaningful_paint = Gauge('pagespeed_first_meaningful_paint', '', ['url'])
first_meaningful_paint_displayvalue = Gauge('pagespeed_first_meaningful_paint_displayvalue', '', ['url'])
first_meaningful_paint_info = Info('pagespeed_first_meaningful_paint', '')

render_blocking_resources = Gauge('pagespeed_render_blocking_resources', '', ['url'])
render_blocking_resources_overall = Gauge('pagespeed_render_blocking_resources_overall', '', ['url', 'type', 'id'])
render_blocking_resources_displayvalue = Gauge('pagespeed_render_blocking_resources_displayvalue', '', ['url'])
render_blocking_resources_info = Info('pagespeed_render_blocking_resources', '')

uses_text_compression = Gauge('pagespeed_uses_text_compression', '', ['url'])
uses_text_compression_overall = Gauge('pagespeed_uses_text_compression_overall', '', ['url', 'type', 'id'])
# uses_text_compression_displayvalue = Gauge('pagespeed_uses_text_compression_displayvalue', '', ['url', 'displayValue']) # no metric
uses_text_compression_info = Info('pagespeed_uses_text_compression', '')

uses_optimized_images = Gauge('pagespeed_uses_optimized_images', '', ['url'])
uses_optimized_images_overall = Gauge('pagespeed_uses_optimized_images_overall', '', ['url', 'type', 'id'])
# uses_text_compression_displayvalue = Gauge('pagespeed_uses_text_compression_displayvalue', '', ['url', 'displayValue'])
uses_optimized_images_info = Info('pagespeed_uses_optimized_images', '')

uses_long_cache_ttl = Gauge('pagespeed_uses_long_cache_ttl', '', ['url'])
uses_long_cache_ttl_displayvalue = Gauge('pagespeed_uses_long_cache_ttl_displayvalue', '', ['url'])
uses_long_cache_ttl_info = Info('pagespeed_uses_long_cache_ttl', '')

max_potential_fid = Gauge('pagespeed_max_potential_fid', '', ['url'])
max_potential_fid_displayvalue = Gauge('pagespeed_max_potential_fid_displayvalue', '', ['url'])
max_potential_fid_info = Info('pagespeed_max_potential_fid', '')

total_blocking_time = Gauge('pagespeed_total_blocking_time', '', ['url'])
total_blocking_time_displayvalue = Gauge('pagespeed_total_blocking_time_displayvalue', '', ['url'])
total_blocking_time_info = Info('pagespeed_total_blocking_time', '')

estimated_input_latency = Gauge('pagespeed_estimated_input_latency_time', '', ['url'])
estimated_input_latency_displayvalue = Gauge('pagespeed_estimated_input_latency_displayvalue', '', ['url'])
estimated_input_latency_info = Info('pagespeed_estimated_input_latency', '')

uses_rel_preconnect = Gauge('pagespeed_uses_rel_preconnect', '', ['url'])
uses_rel_preconnect_overall = Gauge('pagespeed_uses_rel_preconnect_overall', '', ['url', 'type', 'id'])
# uses_rel_preconnect_displayvalue = Gauge('pagespeed_uses_rel_preconnect_displayvalue', '', ['url']) # no metric
uses_rel_preconnect_info = Info('pagespeed_uses_rel_preconnect', '')

bootup_time = Gauge('pagespeed_bootup_time', '', ['url'])
bootup_time_wastedms = Gauge('pagespeed_bootup_time_wastedms', '', ['url', 'id'])
bootup_time_displayvalue = Gauge('pagespeed_bootup_time_displayvalue', '', ['url'])
bootup_time_info = Info('pagespeed_bootup_time', '')

unminified_css = Gauge('pagespeed_unminified_css', '', ['url'])
unminified_css_overall = Gauge('pagespeed_unminified_css_overall', '', ['url', 'type', 'id'])
unminified_css_displayvalue = Gauge('pagespeed_unminified_css_displayvalue', '', ['url'])
unminified_css_info = Info('pagespeed_unminified_css', '')

# network_server_latency = Gauge('pagespeed_network_server_latency', '', ['url'])  # null type - not to get
network_server_latency_displayvalue = Gauge('pagespeed_network_server_latency_displayvalue', '', ['url'])
network_server_latency_info = Info('pagespeed_network_server_latency', '')

offscreen_images = Gauge('pagespeed_offscreen_images', '', ['url'])
offscreen_images_overall = Gauge('pagespeed_offscreen_images_overall', '', ['url', 'type', 'id'])
offscreen_images_displayvalue = Gauge('pagespeed_offscreen_images_displayvalue', '', ['url', 'displayValue'])
offscreen_images_info = Info('pagespeed_offscreen_images', '')

uses_responsive_images = Gauge('pagespeed_uses_responsive_images', '', ['url'])
uses_responsive_images_overall = Gauge('pagespeed_uses_responsive_images_overall', '', ['url', 'type', 'id'])
# uses_responsive_images_displayvalue = Gauge('pagespeed_uses_responsive_images_displayvalue', '', ['url', 'displayValue'])  #no metric
uses_responsive_images_info = Info('pagespeed_uses_responsive_images', '')

unused_css_rules = Gauge('pagespeed_unused_css_rules', '', ['url'])
unused_css_rules_overall = Gauge('pagespeed_unused_css_rules_overall', '', ['url', 'type', 'id'])
unused_css_rules_displayvalue = Gauge('pagespeed_unused_css_rules_displayvalue', '', ['url', 'displayValue'])
unused_css_rules_info = Info('pagespeed_unused_css_rules', '')

total_byte_weight_score = Gauge('pagespeed_total_byte_weight_score', '', ['url'])
total_byte_weight_displayvalue = Gauge('pagespeed_total_byte_weight_displayvalue', '', ['url', 'display_value'])
total_byte_weight_info = Info('pagespeed_total_byte_weight', '')

uses_webp_images = Gauge('pagespeed_uses_webp_images', '', ['url'])
uses_webp_images_overall = Gauge('pagespeed_uses_webp_images_overall', '', ['url', 'type', 'id'])
uses_webp_images_displayvalue = Gauge('pagespeed_uses_webp_images_displayvalue', '', ['url'])
uses_webp_images_info = Info('pagespeed_uses_webp_images', '')

dom_size = Gauge('pagespeed_dom_size', '', ['url'])
dom_size_displayvalue = Gauge('pagespeed_dom_size_displayvalue', '', ['url'])
dom_size_info = Info('pagespeed_dom_size', '')

uses_rel_preload = Gauge('pagespeed_uses_rel_preload', '', ['url'])
uses_rel_preload_overall = Gauge('pagespeed_uses_rel_preload_overall', '', ['url', 'type', 'id'])
# uses_rel_preload_displayvalue = Gauge('pagespeed_uses_rel_preload_displayvalue', '', ['url'])
uses_rel_preload_info = Info('pagespeed_uses_rel_preload', '')

unminified_javascript = Gauge('pagespeed_unminified_javascript', '', ['url'])
unminified_javascript_overall = Gauge('pagespeed_unminified_javascript_overall_seconds', '', ['url', 'type', 'id'])
unminified_javascript_displayvalue = Gauge('pagespeed_unminified_javascript_displayvalue', '', ['url'])
unminified_javascript_info = Info('pagespeed_unminified_javascript', '')

redirects = Gauge('pagespeed_redirects', '', ['url'])
redirects_overall = Gauge('pagespeed_redirects_overall', '', ['url', 'type', 'id'])
redirects_displayvalue = Gauge('pagespeed_redirects_displayvalue', '', ['url'])
redirects_info = Info('pagespeed_redirects', '')

total_time_page_load = Gauge('pagespeed_total_time_page_load', '  время загрузки всей страницы в ms', ['url'])
performance_page_score = Gauge('pagespeed_total_performance_score', 'основная собирательная метрика производительности'
                                                                    'страницы', ['url'])

# make logger errors and save in to file
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/info.log', encoding='UTF-8'),
            logging.StreamHandler()
        ]
    )

except FileNotFoundError:
    print('Not found logs dir. Add...')
    os.makedirs('logs')


def process_request():
    """
    Main function to get list urls in csv file, collect metrics form PageSpeed
    and pulling metrics to the prometheus
    """

    with open('inlist.csv', 'r') as csvfile:
        file_read_lines = csv.reader(csvfile, delimiter=',')
        for row in file_read_lines:
            page = ', '.join(row[:1])  # getting first row from file
            logging.info(f'Take URL: {page}')

            try:
                response_desktop = psd.analyse(page, strategy='desktop')
                url = response_desktop.url
            except Exception as err:
                logging.info('Error to get response form google: ' + str(err))
                pass
            
            results = response_desktop.lighthouse_results
            audits_results = response_desktop.lighthouse_results_audits
            categories = response_desktop.categories

            # Total time page of load
            lighthouse_total_time_page_load = results.timing['total']
            total_time_page_load.labels(url).set(lighthouse_total_time_page_load)

            # Main Performance page score
            lighthouse_total_performance_score = categories.performance['score']
            performance_page_score.labels(url).set(lighthouse_total_performance_score)

            # Time to interactive metric
            lighthouse_time_to_interactive_score = audits_results.interactive['score']
            time_to_interactive.labels(url).set(lighthouse_time_to_interactive_score)

            try:
                lighthouse_time_to_interactive_display = audits_results.interactive['displayValue']
                display_value = re.match(r"[0-9]+\.*\,*[0-9]*", lighthouse_time_to_interactive_display)
                time_to_interactive_displayvalue.labels(url).set(float(display_value.group(0)))
            except Exception as err:
                logging.error(f'Time to interactive error: {str(err)}')
                time_to_interactive_displayvalue.labels(url).set(0)
                pass

            lighthouse_time_to_interactive_title = audits_results.interactive['title']
            lighthouse_time_to_interactive_description = audits_results.interactive['description']

            time_to_interactive_info.info({
                'title': lighthouse_time_to_interactive_title,
                'description': lighthouse_time_to_interactive_description,
                'url': url
            })

            # speed index metric
            lighthouse_speed_index_score = audits_results.speed_index['score']
            speed_index.labels(url).set(lighthouse_speed_index_score)

            try:
                lighthouse_speed_index_display = audits_results.speed_index['displayValue']
                display_value = float(lighthouse_speed_index_display[:3])
                speed_index_displayvalue.labels(url).set(display_value)
            except Exception as err:
                logging.error(f'speed index error: {str(err)}')
                speed_index_displayvalue.labels(url).set(0)
                pass

            lighthouse_speed_index_title = audits_results.speed_index['title']
            lighthouse_speed_index_description = audits_results.speed_index['description']

            speed_index_info.info({
                'title': lighthouse_speed_index_title,
                'description': lighthouse_speed_index_description,
                'url': url
            })

            # first cpu idle metric
            lighthouse_first_cpu_idle_score = audits_results.first_cpu_idle['score']
            first_cpu_idle_score.labels(url).set(lighthouse_first_cpu_idle_score)
            try:
                lighthouse_first_cpu_idle_display = audits_results.first_cpu_idle['displayValue']
                display_value = float(lighthouse_first_cpu_idle_display[:3])
                first_cpu_idle_score_displayvalue.labels(url).set(display_value)
            except Exception as err:
                logging.error(f'first_cpu_idle error: {str(err)}')
                first_cpu_idle_score_displayvalue.labels(url).set(0)
                pass

            lighthouse_first_cpu_idle_title = audits_results.first_cpu_idle['title']
            lighthouse_first_cpu_idle_description = audits_results.first_cpu_idle['description']

            first_cpu_idle_score_info.info({
                'title': lighthouse_first_cpu_idle_title,
                'description': lighthouse_first_cpu_idle_description,
                'url': url
            })

            # mainthread work breakdown metric
            lighthouse_mainthread_work_breakdown_score = audits_results.mainthread_work_breakdown['score']
            mainthread_work_breakdown.labels(url).set(lighthouse_mainthread_work_breakdown_score)

            try:
                lighthouse_mainthread_work_breakdown_display = audits_results.mainthread_work_breakdown['displayValue']
                display_value = float(lighthouse_mainthread_work_breakdown_display[:3])
                mainthread_work_breakdown_displayvalue.labels(url).set(display_value)
            except Exception as err:
                logging.error(f'mainthread_work_breakdown error: {str(err)}')
                mainthread_work_breakdown_displayvalue.labels(url).set(0)
                pass

            lighthouse_mainthread_work_breakdown_title = audits_results.mainthread_work_breakdown['title']
            lighthouse_mainthread_work_breakdown_description = audits_results.mainthread_work_breakdown['description']

            mainthread_work_breakdown_info.info({
                'title': lighthouse_mainthread_work_breakdown_title,
                'description': lighthouse_mainthread_work_breakdown_description,
                'url': url
            })

            # first contentful paint metric
            lighthouse_first_contentful_paint_score = audits_results.first_contentful_paint['score']
            first_contentful_paint.labels(url).set(lighthouse_first_contentful_paint_score)

            try:
                lighthouse_first_contentful_paint_display = audits_results.first_contentful_paint['displayValue']
                display_value = float(lighthouse_first_contentful_paint_display[:3])
                first_contentful_paint_displayvalue.labels(url).set(display_value)
            except Exception as err:
                logging.error(f'first_contentful_paint error: {str(err)}')
                first_contentful_paint_displayvalue.labels(url).set(0)
                pass

            lighthouse_first_contentful_paint_title = audits_results.first_contentful_paint['title']
            lighthouse_first_contentful_paint_description = audits_results.first_contentful_paint['description']

            first_contentful_paint_info.info({
                'title': lighthouse_first_contentful_paint_title,
                'description': lighthouse_first_contentful_paint_description,
                'url': url
            })

            # first_meaningful_paint metric
            lighthouse_first_meaningful_paint_score = audits_results.first_meaningful_paint['score']
            first_meaningful_paint.labels(url).set(lighthouse_first_meaningful_paint_score)
            try:
                lighthouse_first_meaningful_paint_display = audits_results.first_meaningful_paint['displayValue']
                display_value = float(lighthouse_first_meaningful_paint_display[:3])
                first_meaningful_paint_displayvalue.labels(url).set(display_value)
            except Exception as err:
                logging.error(f'first_meaningful_paint error: {str(err)}')
                first_meaningful_paint_displayvalue.labels(url).set(0)
                pass

            lighthouse_first_meaningful_paint_title = audits_results.first_meaningful_paint['title']
            lighthouse_first_meaningful_paint_description = audits_results.first_meaningful_paint['description']

            first_meaningful_paint_info.info({
                'title': lighthouse_first_meaningful_paint_title,
                'description': lighthouse_first_meaningful_paint_description,
                'url': url
            })

            # render_blocking_resources metric
            lighthouse_render_blocking_resources_score = audits_results.render_blocking_resources['score']
            render_blocking_resources.labels(url).set(lighthouse_render_blocking_resources_score)

            try:
                lighthouse_render_blocking_resources_display = audits_results.render_blocking_resources['displayValue']
                display_value = re.search(r"[0-9]+\.*\,*[0-9]*", lighthouse_render_blocking_resources_display)
                render_blocking_resources_displayvalue.labels(url).set(float(display_value.group(0)))
            except Exception as err:
                logging.error(f'network_server_latency error: {str(err)}')
                render_blocking_resources_displayvalue.labels(url).set(0)
                pass

            lighthouse_render_blocking_resources_overall = audits_results.render_blocking_resources['details']['overallSavingsMs']
            render_blocking_resources_overall.labels(url, 'overall', 'render_blocking_resources').set(lighthouse_render_blocking_resources_overall)

            lighthouse_render_blocking_resources_title = audits_results.render_blocking_resources['title']
            lighthouse_render_blocking_resources_description = audits_results.render_blocking_resources['description']

            render_blocking_resources_info.info({
                'title': lighthouse_render_blocking_resources_title,
                'description': lighthouse_render_blocking_resources_description,
                'url': url
            })

            # uses_text_compression metric
            lighthouse_uses_text_compression_score = audits_results.uses_text_compression['score']
            uses_text_compression.labels(url).set(lighthouse_uses_text_compression_score)

            # lighthouse_uses_text_compression_display = audits_results.uses_text_compression['displayValue']
            # display_value = lighthouse_uses_text_compression_display
            # uses_text_compression_displayvalue.labels(url, display_value)  # no metric

            lighthouse_uses_text_compression_overall = audits_results.uses_text_compression['details']['overallSavingsMs']
            uses_text_compression_overall.labels(url, 'overall', 'uses_text_compression').set(lighthouse_uses_text_compression_overall)

            lighthouse_uses_text_compression_title = audits_results.uses_text_compression['title']
            lighthouse_uses_text_compression_description = audits_results.uses_text_compression['description']

            uses_text_compression_info.info({
                'title': lighthouse_uses_text_compression_title,
                'description': lighthouse_uses_text_compression_description,
                'url': url
            })

            # uses_optimized_images metric
            lighthouse_uses_optimized_images_score = audits_results.uses_optimized_images['score']
            uses_optimized_images.labels(url).set(lighthouse_uses_optimized_images_score)

            # lighthouse_uses_text_compression_display = audits_results.uses_text_compression['displayValue']
            # display_value = lighthouse_uses_text_compression_display
            # uses_text_compression_displayvalue.labels(url, display_value)  #no metric

            lighthouse_uses_optimized_images_overall = audits_results.uses_optimized_images['details']['overallSavingsMs']
            uses_optimized_images_overall.labels(url, 'overall', 'uses_optimized_images').set(lighthouse_uses_optimized_images_overall)

            lighthouse_uses_optimized_images_title = audits_results.uses_optimized_images['title']
            lighthouse_uses_optimized_images_description = audits_results.uses_optimized_images['description']

            uses_optimized_images_info.info({
                'title': lighthouse_uses_optimized_images_title,
                'description': lighthouse_uses_optimized_images_description,
                'url': url
            })

            # uses_long_cache_ttl metric
            lighthouse_uses_long_cache_ttl_score = audits_results.uses_long_cache_ttl['score']
            uses_long_cache_ttl.labels(url).set(lighthouse_uses_long_cache_ttl_score)

            try:
                lighthouse_uses_long_cache_ttl_display = audits_results.uses_long_cache_ttl['displayValue']
                display_value = re.match(r"[0-9]+\.*\,*[0-9]*", lighthouse_uses_long_cache_ttl_display)
                uses_long_cache_ttl_displayvalue.labels(url).set(float(display_value.group(0)))
            except Exception as err:
                logging.error(f'network_server_latency error: {str(err)}')
                uses_long_cache_ttl_displayvalue.labels(url).set(0)
                pass

            lighthouse_uses_long_cache_ttl_title = audits_results.uses_long_cache_ttl['title']
            lighthouse_uses_long_cache_ttl_description = audits_results.uses_long_cache_ttl['description']

            uses_long_cache_ttl_info.info({
                'title': lighthouse_uses_long_cache_ttl_title,
                'description': lighthouse_uses_long_cache_ttl_description,
                'url': url
            })

            # max_potential_fid metric
            lighthouse_max_potential_fid_score = audits_results.max_potential_fid['score']
            max_potential_fid.labels(url).set(lighthouse_max_potential_fid_score)
            try:
                lighthouse_max_potential_fid_display = audits_results.max_potential_fid['displayValue']
                display_value = float(lighthouse_max_potential_fid_display[:3].replace(',','.'))
                max_potential_fid_displayvalue.labels(url).set(display_value)
            except Exception as err:
                logging.error(f'max_potential_fid err: {str(err)}')
                pass

            lighthouse_max_potential_fid_title = audits_results.max_potential_fid['title']
            lighthouse_max_potential_fid_description = audits_results.max_potential_fid['description']

            max_potential_fid_info.info({
                'title': lighthouse_max_potential_fid_title,
                'description': lighthouse_max_potential_fid_description,
                'url': url
            })

            # total_blocking_time metric
            lighthouse_total_blocking_time_score = audits_results.total_blocking_time['score']
            total_blocking_time.labels(url).set(lighthouse_total_blocking_time_score)

            try:
                lighthouse_total_blocking_time_display = audits_results.total_blocking_time['displayValue']
                display_value = float(lighthouse_total_blocking_time_display[:3].replace(',','.'))
                total_blocking_time_displayvalue.labels(url).set(display_value)
            except Exception as err:
                logging.error(f'total_blocking_time error: {str(err)}')
                total_blocking_time_displayvalue.labels(url).set(0)
                pass

            lighthouse_total_blocking_time_title = audits_results.total_blocking_time['title']
            lighthouse_total_blocking_time_description = audits_results.total_blocking_time['description']

            total_blocking_time_info.info({
                'title': lighthouse_total_blocking_time_title,
                'description': lighthouse_total_blocking_time_description,
                'url': url
            })

            # estimated_input_latency metric
            lighthouse_estimated_input_latency_score = audits_results.estimated_input_latency['score']
            estimated_input_latency.labels(url).set(lighthouse_estimated_input_latency_score)
            try:
                lighthouse_estimated_input_latency_display = audits_results.estimated_input_latency['displayValue']
                display_value = float(lighthouse_estimated_input_latency_display[:3].replace(',','.'))
                estimated_input_latency_displayvalue.labels(url).set(display_value)
            except Exception as err:
                logging.error(f'estimated_input_latency error: {str(err)}')
                estimated_input_latency_displayvalue.labels(url).set(0)
                pass

            lighthouse_estimated_input_latency_title = audits_results.estimated_input_latency['title']
            lighthouse_estimated_input_latency_description = audits_results.estimated_input_latency['description']

            estimated_input_latency_info.info({
                'title': lighthouse_estimated_input_latency_title,
                'description': lighthouse_estimated_input_latency_description,
                'url': url
            })

            # uses_rel_preconnect metric
            lighthouse_uses_rel_preconnect_score = audits_results.uses_rel_preconnect['score']
            uses_rel_preconnect.labels(url).set(lighthouse_uses_rel_preconnect_score)

            # lighthouse_uses_rel_preconnect_display = audits_results.uses_rel_preconnect['displayValue']
            # display_value = lighthouse_uses_rel_preconnect_display
            # uses_rel_preconnect_displayvalue.labels(url, display_value)  # no metric

            lighthouse_uses_rel_preconnect_overall = audits_results.uses_rel_preconnect['details']['overallSavingsMs']
            uses_rel_preconnect_overall.labels(url, 'overall', 'uses_rel_preconnect').set(lighthouse_uses_rel_preconnect_overall)

            lighthouse_uses_rel_preconnect_title = audits_results.uses_rel_preconnect['title']
            lighthouse_uses_rel_preconnect_description = audits_results.uses_rel_preconnect['description']

            uses_rel_preconnect_info.info({
                'title': lighthouse_uses_rel_preconnect_title,
                'description': lighthouse_uses_rel_preconnect_description,
                'url': url
            })

            # bootup_time metric
            lighthouse_bootup_time_score = audits_results.bootup_time['score']
            bootup_time.labels(url).set(lighthouse_bootup_time_score)


            try:
                lighthouse_bootup_time_display = audits_results.bootup_time['displayValue']
                display_value = float(lighthouse_bootup_time_display[:3])
                bootup_time_displayvalue.labels(url).set(display_value)
            except Exception as err:
                logging.error(f'bootup_time error: {str(err)}')
                bootup_time_displayvalue.labels(url).set(0)
                pass

            lighthouse_bootup_time_wastedms = audits_results.bootup_time['details']['summary']['wastedMs']
            bootup_time_wastedms.labels(url, 'bootup_time').set(lighthouse_bootup_time_wastedms)

            lighthouse_bootup_time_title = audits_results.bootup_time['title']
            lighthouse_bootup_time_description = audits_results.bootup_time['description']

            bootup_time_info.info({
                'title': lighthouse_bootup_time_title,
                'description': lighthouse_bootup_time_description,
                'url': url
            })

            # unminified_css metric
            lighthouse_unminified_css_score = audits_results.unminified_css['score']
            unminified_css.labels(url).set(lighthouse_unminified_css_score)

            # lighthouse_unminified_css_display = audits_results.unminified_css['displayValue']
            # display_value = lighthouse_unminified_css_display
            # unminified_css_displayvalue.labels(url, display_value) # no this metric

            lighthouse_unminified_css_overall = audits_results.unminified_css['details']['overallSavingsMs']
            unminified_css_overall.labels(url, 'overall', 'unminified_css').set(lighthouse_unminified_css_overall)

            lighthouse_unminified_css_title = audits_results.unminified_css['title']
            lighthouse_unminified_css_description = audits_results.unminified_css['description']

            unminified_css_info.info({
                'title': lighthouse_unminified_css_title,
                'description': lighthouse_unminified_css_description,
                'url': url
            })

            # network_server_latency metric
            # lighthouse_network_server_latency_score = audits_results.network_server_latency['score']
            # network_server_latency.labels(url).set(lighthouse_network_server_latency_score)
            try:
                lighthouse_network_server_latency_display = audits_results.network_server_latency['displayValue']
                display_value = re.match(r"[0-9]+\.*\,*[0-9]*", lighthouse_network_server_latency_display)
                network_server_latency_displayvalue.labels(url).set(float(display_value.group(0)))
            except Exception as err:
                logging.error(f'network_server_latency error: {str(err)}')
                network_server_latency_displayvalue.labels(url).set(0)
                pass

            lighthouse_network_server_latency_title = audits_results.network_server_latency['title']
            lighthouse_network_server_latency_description = audits_results.network_server_latency['description']

            network_server_latency_info.info({
                'title': lighthouse_network_server_latency_title,
                'description': lighthouse_network_server_latency_description,
                'url': url
            })

            # offscreen_images metric
            lighthouse_offscreen_images_score = audits_results.offscreen_images['score']
            offscreen_images.labels(url).set(lighthouse_offscreen_images_score)

            lighthouse_offscreen_images_overall = audits_results.offscreen_images['details']['overallSavingsMs']
            offscreen_images_overall.labels(url, 'overall', 'offscreen_images').set(lighthouse_offscreen_images_overall)

            try:
                lighthouse_offscreen_images_display = audits_results.offscreen_images['displayValue']
                display_value = lighthouse_offscreen_images_display
                offscreen_images_displayvalue.labels(url, display_value)
            except Exception as err:
                logging.error(f'Offscreen_images error: {str(err)}')
                offscreen_images_displayvalue.labels(url, '0')
                pass

            lighthouse_offscreen_images_title = audits_results.offscreen_images['title']
            lighthouse_offscreen_images_description = audits_results.offscreen_images['description']

            offscreen_images_info.info({
                'title': lighthouse_offscreen_images_title,
                'description': lighthouse_offscreen_images_description,
                'url': url
            })

            # uses_responsive_images metric
            lighthouse_uses_responsive_images_score = audits_results.uses_responsive_images['score']
            uses_responsive_images.labels(url).set(lighthouse_uses_responsive_images_score)

            lighthouse_uses_responsive_images_overall = audits_results.uses_responsive_images['details']['overallSavingsMs']
            uses_responsive_images_overall.labels(url, 'overall', 'uses_responsive_images').set(lighthouse_uses_responsive_images_overall)

            # lighthouse_offscreen_images_display = audits_results.offscreen_images['displayValue']
            # display_value = lighthouse_offscreen_images_display
            # offscreen_images_displayvalue.labels(url, display_value)  # no metric

            lighthouse_uses_responsive_images_title = audits_results.uses_responsive_images['title']
            lighthouse_uses_responsive_images_description = audits_results.uses_responsive_images['description']

            uses_responsive_images_info.info({
                'title': lighthouse_uses_responsive_images_title,
                'description': lighthouse_uses_responsive_images_description,
                'url': url
            })

            # unused_css_rules metric
            lighthouse_unused_css_rules_score = audits_results.unused_css_rules['score']
            unused_css_rules.labels(url).set(lighthouse_unused_css_rules_score)

            lighthouse_unused_css_rules_display = audits_results.unused_css_rules['displayValue']
            display_value = lighthouse_unused_css_rules_display
            unused_css_rules_displayvalue.labels(url, display_value)

            lighthouse_unused_css_rules_overall = audits_results.unused_css_rules['details']['overallSavingsMs']
            unused_css_rules_overall.labels(url, 'overall', 'unused_css_rules').set(lighthouse_unused_css_rules_overall)

            lighthouse_unused_css_rules_title = audits_results.unused_css_rules['title']
            lighthouse_unused_css_rules_description = audits_results.unused_css_rules['description']

            unused_css_rules_info.info({
                'title': lighthouse_unused_css_rules_title,
                'description': lighthouse_unused_css_rules_description,
                'url': url
            })

            # Total byte weight metric
            lighthouse_total_byte_weight_score = audits_results.total_byte_weight['score']
            total_byte_weight_score.labels(url).set(lighthouse_total_byte_weight_score)

            lighthouse_total_byte_weight_display = audits_results.total_byte_weight['displayValue']
            display_value = lighthouse_total_byte_weight_display
            total_byte_weight_displayvalue.labels(url, display_value)

            lighthouse_total_byte_weight_title = audits_results.total_byte_weight['title']
            lighthouse_total_byte_weight_description = audits_results.total_byte_weight['description']

            total_byte_weight_info.info({
                'title': lighthouse_total_byte_weight_title,
                'description': lighthouse_total_byte_weight_description,
                'url': url
            })

            # Uses webp images metric
            lighthouse_uses_webp_images_score = audits_results.uses_webp_images['score']
            uses_webp_images.labels(url).set(lighthouse_uses_webp_images_score)

            # lighthouse_uses_webp_images_display = audits_results.uses_webp_images['displayValue']
            # display_value = float(lighthouse_uses_webp_images_display[:3])
            # uses_webp_images_displayvalue.labels(url).set(display_value)

            lighthouse_uses_webp_images_overall = audits_results.uses_webp_images['details']['overallSavingsMs']
            uses_webp_images_overall.labels(url, 'overall', 'uses_webp_images').set(lighthouse_uses_webp_images_overall)

            lighthouse_uses_webp_images_title = audits_results.uses_webp_images['title']
            lighthouse_uses_webp_images_description = audits_results.uses_webp_images['description']

            uses_webp_images_info.info({
                'title': lighthouse_uses_webp_images_title,
                'description': lighthouse_uses_webp_images_description,
                'url': url
            })

            # dom_size metric
            lighthouse_dom_size_score = audits_results.dom_size['score']
            dom_size.labels(url).set(lighthouse_dom_size_score)

            try:
                lighthouse_dom_size_display = audits_results.dom_size['displayValue']
                display_value = re.match(r"[0-9]+\.*\,*[0-9]*", lighthouse_dom_size_display)
                dom_size_displayvalue.labels(url).set(float(display_value.group(0).replace(',','.')))
            except Exception as err:
                logging.error(f'dom_siz error: {str(err)}')
                offscreen_images_displayvalue.labels(url, '0')
                pass

            lighthouse_dom_size_title = audits_results.dom_size['title']
            lighthouse_dom_size_description = audits_results.dom_size['description']

            dom_size_info.info({
                'title': lighthouse_dom_size_title,
                'description': lighthouse_dom_size_description,
                'url': url
            })

            # uses_rel_preload metric
            lighthouse_uses_rel_preload_score = audits_results.uses_rel_preload['score']
            uses_rel_preload.labels(url).set(lighthouse_uses_rel_preload_score)

            # lighthouse_uses_rel_preload_display = audits_results.uses_rel_preload['displayValue']
            # display_value = float(lighthouse_uses_rel_preload_display[:3].replace(',', '.'))
            # uses_rel_preload_displayvalue.labels(url).set(display_value)

            lighthouse_uses_rel_preload_overall = audits_results.uses_rel_preload['details']['overallSavingsMs']
            uses_rel_preload_overall.labels(url, 'overall', 'uses_rel_preload').set(lighthouse_uses_rel_preload_overall)

            lighthouse_uses_rel_preload_title = audits_results.uses_rel_preload['title']
            lighthouse_uses_rel_preload_description = audits_results.uses_rel_preload['description']

            uses_rel_preload_info.info({
                'title': lighthouse_uses_rel_preload_title,
                'description': lighthouse_uses_rel_preload_description,
                'url': url
            })

            # unminified_javascript metric
            lighthouse_unminified_javascript_score = audits_results.unminified_javascript['score']
            unminified_javascript.labels(url).set(lighthouse_unminified_javascript_score)


            lighthouse_unminified_javascript_overall = audits_results.unminified_javascript['details']['overallSavingsMs']
            unminified_javascript_overall.labels(url, 'overall', 'unminified_javascript').set(lighthouse_unminified_javascript_overall)

            # lighthouse_unminified_javascript_display = audits_results.unminified_javascript['displayValue']
            # display_value = float(lighthouse_unminified_javascript_display[:3].replace(',', '.'))
            # unminified_javascript_displayvalue.labels(url).set(display_value)   # no metric

            lighthouse_unminified_javascript_title = audits_results.unminified_javascript['title']
            lighthouse_unminified_javascript_description = audits_results.unminified_javascript['description']

            unminified_javascript_info.info({
                'title': lighthouse_unminified_javascript_title,
                'description': lighthouse_unminified_javascript_description,
                'url': url
            })

            # redirects metric
            lighthouse_redirects_score = audits_results.redirects['score']
            redirects.labels(url).set(lighthouse_redirects_score)

            lighthouse_redirects_overall = audits_results.redirects['details']['overallSavingsMs']
            redirects_overall.labels(url, 'overall', 'redirects').set(lighthouse_redirects_overall)

            # lighthouse_unminified_javascript_display = audits_results.unminified_javascript['displayValue']
            # display_value = float(lighthouse_unminified_javascript_display[:3].replace(',', '.'))
            # unminified_javascript_displayvalue.labels(url).set(display_value)   # no metric

            lighthouse_redirects_title = audits_results.redirects['title']
            lighthouse_redirects_description = audits_results.redirects['description']

            redirects_info.info({
                'title': lighthouse_redirects_title,
                'description': lighthouse_redirects_description,
                'url': url
            })

            logging.info('Done.')


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    try:
        start_http_server(HTTP_SERVER_PORT)
        logging.info(f'HTTP Server Start on port: {str(HTTP_SERVER_PORT)}')
    except Exception as err:
        logging.error('HTTP Server ERROR: ' + str(err))

    # The main cycle of polling metrics
    while True:
        try:
            process_request()
        except Exception as err:
            logging.error(f'Error in process_request function with message: {err}')
            pass

        logging.info('Main cycle end. Lets sleep...' + str(SLEEP_TIMER) + ' sec')
        time.sleep(SLEEP_TIMER)
