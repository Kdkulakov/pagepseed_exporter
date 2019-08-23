from prometheus_client import start_http_server, Summary, Counter, Info, Gauge
import time
from pagespeed import PageSpeed
import csv

psd = PageSpeed()

# иницализация метрик
speed_index = Gauge('pagespeed_speedindex', '', ['url'])
speed_index_displayvalue = Gauge('pagespeed_speedindex_displayvalue', '', ['url'])
speed_index_info = Info('pagespeed_speedindex', '')

time_to_interactive = Gauge('pagespeed_timetointeractive', '', ['url'])
time_to_interactive_displayvalue = Gauge('pagespeed_timetointeractive_displayvalue', '', ['url'])
time_to_interactive_info = Info('pagespeed_timetointeractive', '')

first_contentful_paint = Gauge('pagespeed_first_contentful_paint', '', ['url'])
first_contentful_paint_displayvalue = Gauge('pagespeed_first_contentful_paint_displayvalue', '', ['url'])
first_contentful_paint_info = Info('pagespeed_first_contentful_paint', '')

first_cpu_idle_score = Gauge('pagespeed_first_cpu_idle_score', '', ['url'])
first_cpu_idle_score_displayvalue = Gauge('pagespeed_first_cpu_idle_score_displayvalue', '', ['url'])
first_cpu_idle_score_info = Info('pagespeed_first_cpu_idle_score', '')

mainthread_work_breakdown = Gauge('pagespeed_mainthread_work_breakdown', '', ['url'])
mainthread_work_breakdown_displayvalue = Gauge('pagespeed_mainthread_work_breakdown_displayvalue', '', ['url'])
mainthread_work_breakdown_info = Info('pagespeed_mainthread_work_breakdown', '')

first_meaningful_paint = Gauge('pagespeed_first_meaningful_paint', '', ['url'])
first_meaningful_paint_displayvalue = Gauge('pagespeed_first_meaningful_paint_displayvalue', '', ['url'])
first_meaningful_paint_info = Info('pagespeed_first_meaningful_paint', '')

render_blocking_resources = Gauge('pagespeed_render_blocking_resources', '', ['url'])
render_blocking_resources_displayvalue = Gauge('pagespeed_render_blocking_resources_displayvalue', '', ['url', 'displayValue'])
render_blocking_resources_info = Info('pagespeed_render_blocking_resources', '')

total_time_page_load = Gauge('pagespeed_total_time_page_load', '  время загрузки всей страницы в ms', ['url'])


def process_request():
    """Основаня функция забора данных."""

    with open('inlist.csv', 'r') as csvfile:
        file_read_lines = csv.reader(csvfile, delimiter=',')
        for row in file_read_lines:
            page = ', '.join(row[:1])  # берем первый столбик со списком страниц
            print(page)
            try:
                response_desktop = psd.analyse(page, strategy='desktop')
                url = response_desktop.url
            except Exception as err:
                print('EXEPTIONS: ' + str(err))
                pass


            # Total time page of load
            lighthouse_total_time_page_load = response_desktop.lighthouse_results.timing['total']
            total_time_page_load.labels(url).set(lighthouse_total_time_page_load)

            # speed index metric
            lighthouse_speed_index_score = response_desktop.lighthouse_results_audits.speed_index['score']
            speed_index.labels(url).set(lighthouse_speed_index_score)

            lighthouse_speed_index_display = response_desktop.lighthouse_results_audits.speed_index['displayValue']
            display_value = float(lighthouse_speed_index_display[:3])
            speed_index_displayvalue.labels(url).set(display_value)

            lighthouse_speed_index_title = response_desktop.lighthouse_results_audits.speed_index['title']
            lighthouse_speed_index_description = response_desktop.lighthouse_results_audits.speed_index['description']

            speed_index_info.info({
                'title': lighthouse_speed_index_title,
                'description': lighthouse_speed_index_description,
                'url': url
            })

            # Time to interactive metric
            lighthouse_time_to_interactive_score = response_desktop.lighthouse_results_audits.interactive['score']
            time_to_interactive.labels(url).set(lighthouse_time_to_interactive_score)

            lighthouse_time_to_interactive_display = response_desktop.lighthouse_results_audits. \
            interactive['displayValue']
            display_value = float(lighthouse_time_to_interactive_display[:3])
            time_to_interactive_displayvalue.labels(url).set(display_value)

            lighthouse_time_to_interactive_title = response_desktop.lighthouse_results_audits.interactive['title']
            lighthouse_time_to_interactive_description = response_desktop.lighthouse_results_audits. \
            interactive['description']

            time_to_interactive_info.info({
                'title': lighthouse_time_to_interactive_title,
                'description': lighthouse_time_to_interactive_description,
                'url': url
            })

            # first contentful paint metric
            lighthouse_first_contentful_paint_score = response_desktop.lighthouse_results_audits. \
                first_contentful_paint['score']
            first_contentful_paint.labels(url).set(lighthouse_first_contentful_paint_score)

            lighthouse_first_contentful_paint_display = response_desktop.lighthouse_results_audits. \
                first_contentful_paint['displayValue']
            display_value = float(lighthouse_first_contentful_paint_display[:3])
            first_contentful_paint_displayvalue.labels(url).set(display_value)

            lighthouse_first_contentful_paint_title = response_desktop.lighthouse_results_audits. \
                first_contentful_paint['title']
            lighthouse_first_contentful_paint_description = response_desktop.lighthouse_results_audits. \
                first_contentful_paint['description']

            first_contentful_paint_info.info({
                'title': lighthouse_first_contentful_paint_title,
                'description': lighthouse_first_contentful_paint_description,
                'url': url
            })

            # first cpu idle metric
            lighthouse_first_cpu_idle_score = response_desktop.lighthouse_results_audits.first_cpu_idle['score']
            first_cpu_idle_score.labels(url).set(lighthouse_first_cpu_idle_score)

            lighthouse_first_cpu_idle_display = response_desktop.lighthouse_results_audits.first_cpu_idle['displayValue']
            display_value = float(lighthouse_first_cpu_idle_display[:3])
            first_cpu_idle_score_displayvalue.labels(url).set(display_value)

            lighthouse_first_cpu_idle_title = response_desktop.lighthouse_results_audits.first_cpu_idle['title']
            lighthouse_first_cpu_idle_description = response_desktop.lighthouse_results_audits.first_cpu_idle['description']

            first_cpu_idle_score_info.info({
                'title': lighthouse_first_cpu_idle_title,
                'description': lighthouse_first_cpu_idle_description,
                'url': url
            })

            # mainthread work breakdown metric
            lighthouse_mainthread_work_breakdown_score = response_desktop.lighthouse_results_audits.\
                mainthread_work_breakdown['score']
            mainthread_work_breakdown.labels(url).set(lighthouse_mainthread_work_breakdown_score)

            lighthouse_mainthread_work_breakdown_display = response_desktop.lighthouse_results_audits. \
                mainthread_work_breakdown['displayValue']
            display_value = float(lighthouse_mainthread_work_breakdown_display[:3])
            mainthread_work_breakdown_displayvalue.labels(url).set(display_value)

            lighthouse_mainthread_work_breakdown_title = response_desktop.lighthouse_results_audits. \
                mainthread_work_breakdown['title']
            lighthouse_mainthread_work_breakdown_description = response_desktop.lighthouse_results_audits. \
                mainthread_work_breakdown['description']

            mainthread_work_breakdown_info.info({
                'title': lighthouse_mainthread_work_breakdown_title,
                'description': lighthouse_mainthread_work_breakdown_description,
                'url': url
            })


            # first_meaningful_paint metric
            lighthouse_first_meaningful_paint_score = response_desktop.lighthouse_results_audits.\
                first_meaningful_paint['score']
            first_meaningful_paint.labels(url).set(lighthouse_first_meaningful_paint_score)

            lighthouse_first_meaningful_paint_display = response_desktop.lighthouse_results_audits. \
                first_meaningful_paint['displayValue']
            display_value = float(lighthouse_first_meaningful_paint_display[:3])
            first_meaningful_paint_displayvalue.labels(url).set(display_value)

            lighthouse_first_meaningful_paint_title = response_desktop.lighthouse_results_audits. \
                first_meaningful_paint['title']
            lighthouse_first_meaningful_paint_description = response_desktop.lighthouse_results_audits. \
                first_meaningful_paint['description']

            first_meaningful_paint_info.info({
                'title': lighthouse_first_meaningful_paint_title,
                'description': lighthouse_first_meaningful_paint_description,
                'url': url
            })

            # render_blocking_resources metric
            lighthouse_render_blocking_resources_score = response_desktop.lighthouse_results_audits.\
                render_blocking_resources['score']
            render_blocking_resources.labels(url).set(lighthouse_render_blocking_resources_score)

            lighthouse_render_blocking_resources_display = response_desktop.lighthouse_results_audits. \
                render_blocking_resources['displayValue']
            display_value = lighthouse_render_blocking_resources_display
            render_blocking_resources_displayvalue.labels(url, display_value)

            lighthouse_render_blocking_resources_title = response_desktop.lighthouse_results_audits. \
                render_blocking_resources['title']
            lighthouse_render_blocking_resources_description = response_desktop.lighthouse_results_audits. \
                render_blocking_resources['description']

            render_blocking_resources_info.info({
                'title': lighthouse_render_blocking_resources_title,
                'description': lighthouse_render_blocking_resources_description,
                'url': url
            })

            print('collect')


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        try:
            process_request()
        except Exception as err:
            print('EXPETION: ' + str(err))
            pass

        print('start sleep')
        time.sleep(120)
        print('end slip')