import argparse
domains = ( 'algorithms', 'ai', 'databases', 'data-structures',
            'mathematics', 'c', 'cpp', 'java', 'python',
            'ruby', 'shell', 'fp', 'sql', 'regex',
            'tutorials/30-days-of-code',
            'tutorials/10-days-of-statistics',
            'tutorials/10-days-of-javascript' )

def category_name(string):
    category = string.lower()
    if (category not in domains):
        msg = f'https://www.hackerrank.com/domains/{category} is not a valid page.'
        raise argparse.ArgumentTypeError(msg)
    return category
