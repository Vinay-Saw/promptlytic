\
        import re
        import json
        from typing import Optional
        from urllib.parse import urljoin, urlparse

        def strip_code_fences(text: str) -> str:
            m = re.search(r"```(?:python)?\n(.*)```", text, flags=re.S)
            if m:
                return m.group(1)
            return text

        def find_submit_url(html: str) -> Optional[str]:
            m = re.search(r"https?://[^\s'\"<>]*(?:submit|answer|api)[^\s'\"<>]*", html, flags=re.I)
            if m:
                return m.group(0)
            m2 = re.search(r"(['\"])(/[^'\"<>]*?(?:submit|answer|api)[^'\"<>]*?)\1", html, flags=re.I)
            if m2:
                return m2.group(2)
            return None

        def join_url(base: str, maybe_rel: str) -> str:
            if not maybe_rel:
                return maybe_rel
            p = urlparse(maybe_rel)
            if p.scheme:
                return maybe_rel
            return urljoin(base, maybe_rel)
