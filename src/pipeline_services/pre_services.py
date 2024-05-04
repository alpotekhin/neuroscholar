"""
Pre Services
---
This module defines services that process user requests before script transition.
"""
from dff.script import Context

from qa.rag import retrieve

def question_processor(ctx: Context):
        last_request = ctx.last_request
        if last_request is None:
            return
        else:
            if last_request.annotations is None:
                last_request.annotations = {}
            else:
                if last_request.annotations.get("retrieved_docs") is not None:
                    return
            if last_request.text is None:
                last_request.annotations["retrieved_docs"] = None
            else:
                last_request.annotations["retrieved_docs"] = retrieve(last_request.text)

        ctx.set_last_request(last_request)


services = [question_processor]  # pre-services run before bot sends a response
