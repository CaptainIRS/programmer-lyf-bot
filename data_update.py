import re
import sys
import time

if __name__ == '__main__':
    log_file_path = sys.argv[1]
    errors = [
        'Stale publication',
        'Invalid feed entry',
        'Timestamps invalid',
        'Request to',
        'Cannot connect'
    ]
    data_files = [
        'data/blogs/company_blogs.opml',
        'data/blogs/infosec_blogs.opml',
        'data/blogs/podcasts.opml',
        'data/blogs/product_blogs.opml'
    ]
    error_urls = []
    with open(log_file_path) as log_file:
        for line in log_file:
            for error in errors:
                if error in line:
                    url = re.search('(?P<url>https?://[^\s]+)', line).group('url')[:-1]
                    error_urls.append(url)
    print(error_urls)
    for data_file in data_files:
        final_lines = []
        with open(data_file) as file:
            for line in file:
                if '<!--' in line:
                    continue
                for error_url in error_urls:
                    if error_url in line:
                        break
                else:
                    final_lines.append(line)
        time.sleep(1)
        with open(data_file, 'w') as file:
            file.writelines(final_lines)
