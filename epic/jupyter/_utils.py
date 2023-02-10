import io
import base64
import urllib.parse


def fig2html(fig) -> str:
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    img = urllib.parse.quote_from_bytes(base64.encodebytes(buffer.getvalue()))
    return f'<img src="data:image/png;base64,{img}">'
