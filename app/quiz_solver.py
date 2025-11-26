import time
import json
from .llm_client import build_prompt, call_llm
from .executor import run_script
from .browser_fetcher import render_page
from .utils import strip_code_fences
from .settings import settings

def extract_script_from_llm(text: str) -> str:
    return strip_code_fences(text)

def try_parse_json(s: str):
    try:
        return json.loads(s.strip())
    except Exception:
        return None

def solve_single_task(task_url: str, start_time: float, max_total_seconds: int = 180):
    final_url, html = render_page(task_url, headless=settings.PLAYWRIGHT_HEADLESS)
    prompt = build_prompt(final_url, html)
    llm_text = call_llm(prompt)
    script = extract_script_from_llm(llm_text)
    elapsed = time.time() - start_time
    remaining = max_total_seconds - elapsed
    if remaining <= 2:
        return {"error": "timeout before execution", "llm_text": llm_text, "script": script}
    exec_result = run_script(script, timeout=int(max(1, remaining - 1)))
    stdout = exec_result.get("stdout", "")
    stderr = exec_result.get("stderr", "")
    parsed = try_parse_json(stdout)
    submit_response = parsed.get("submit_response") if isinstance(parsed, dict) else None
    next_url = None
    if isinstance(parsed, dict) and "url" in parsed:
        next_url = parsed["url"]
    else:
        for piece in (stdout + "\n" + stderr).split():
            if piece.startswith("http"):
                if "quiz" in piece or "submit" in piece:
                    next_url = piece
                    break
    return {"llm_text": llm_text, "script": script, "exec_result": exec_result, "parsed_stdout": parsed, "submit_response": submit_response, "next_url": next_url, "final_page_url": final_url}

def solve_chain(initial_url: str, max_total_seconds: int = 180):
    start = time.time()
    cur = initial_url
    history = []
    while True:
        elapsed = time.time() - start
        if elapsed > max_total_seconds:
            return {"error": "Overall time limit exceeded", "history": history}
        res = solve_single_task(cur, start, max_total_seconds)
        history.append({"url": cur, **res})
        if res.get("next_url") and settings.ALLOW_FOLLOW_CHAIN:
            cur = res["next_url"]
            if len(history) > 8:
                return {"error": "too many chain steps", "history": history}
            continue
        break
    return {"history": history}
