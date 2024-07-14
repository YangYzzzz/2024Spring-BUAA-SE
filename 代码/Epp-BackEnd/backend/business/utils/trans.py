def url_to_pdf(url: str) -> str:
    return url.replace('abs/', 'pdf/') + '.pdf'
