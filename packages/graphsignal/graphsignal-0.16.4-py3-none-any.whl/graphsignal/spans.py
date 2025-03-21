from typing import Union, Any, Optional, Dict
import logging
import sys
import time
import traceback
import json
import base64

import graphsignal
from graphsignal import client
from graphsignal.utils import uuid_sha1, sanitize_str

logger = logging.getLogger('graphsignal')

def _tracer():
    return graphsignal._tracer

class Usage:
    __slots__ = [
        'name',
        'value'
    ]

    def __init__(self, name, value):
        self.name = name
        self.value = value

class Payload:
    __slots__ = [
        'name',
        'content']

    def __init__(self, name, content):
        self.name = name
        self.content = content

class Profile:
    __slots__ = [
        'name',
        'format',
        'content']

    def __init__(self, name, format, content):
        self.name = name
        self.format = format
        self.content = content

class Span:
    MAX_SPAN_TAGS = 25
    MAX_PARAMS = 100
    MAX_USAGES_COUNTERS = 25
    MAX_PAYLOADS = 10
    MAX_PAYLOAD_BYTES = 256 * 1024
    MAX_PROFILES = 10
    MAX_PROFILE_SIZE = 256 * 1024

    __slots__ = [
        '_operation',
        '_tags',
        '_with_profile',
        '_context_tags',
        '_span_id',
        '_root_span_id',
        '_parent_span_id',
        '_is_root',
        '_recorder_context',
        '_model',
        '_is_started',
        '_is_stopped',
        '_start_counter',
        '_stop_counter',
        '_first_token_counter',
        '_output_tokens',
        '_exc_infos',
        '_params',
        '_usage',
        '_payloads',
        '_profiles'
    ]

    def __init__(self, operation, tags=None, with_profile=False, root_span_id=None, parent_span_id=None):
        self._is_started = False

        if not operation:
            logger.error('Span: operation is required')
            return
        if tags is not None:
            if not isinstance(tags, dict):
                logger.error('Span: tags must be dict')
                return
            if len(tags) > Span.MAX_SPAN_TAGS:
                logger.error('Span: too many tags (>{0})'.format(Span.MAX_SPAN_TAGS))
                return

        self._operation = sanitize_str(operation)
        self._tags = dict(operation=self._operation)
        if tags is not None:
            self._tags.update(tags)
        self._with_profile = with_profile
        self._context_tags = None
        self._is_stopped = False
        self._span_id = None
        self._root_span_id = root_span_id
        self._parent_span_id = parent_span_id
        self._is_root = False
        self._start_counter = None
        self._stop_counter = None
        self._first_token_counter = None
        self._output_tokens = None
        self._recorder_context = False
        self._model = None
        self._exc_infos = None
        self._usage = None
        self._params = None
        self._payloads = None
        self._profiles = None

        try:
            self._start()
        except Exception:
            logger.error('Error starting span', exc_info=True)
            self._is_stopped = True

    def __enter__(self):
        return self

    async def __aenter__(self):
        return self

    def __exit__(self, *exc_info):
        if exc_info and exc_info[1] and isinstance(exc_info[1], Exception):
            if not self._exc_infos:
                self._exc_infos = []
            self._exc_infos.append(exc_info)
        self.stop()
        return False

    async def __aexit__(self, *exc_info):
        if exc_info and exc_info[1] and isinstance(exc_info[1], Exception):
            if not self._exc_infos:
                self._exc_infos = []
            self._exc_infos.append(exc_info)
        self.stop()
        return False

    def _start(self):
        if self._is_started:
            return
        if self._is_stopped:
            return

        if _tracer().debug_mode:
            logger.debug(f'Starting span {self._operation}')

        self._span_id = uuid_sha1(size=12)
        if self._root_span_id is None:
            self._root_span_id = self._span_id
            self._is_root = True

        self._context_tags = _tracer().context_tags.get().copy()

        self._model = client.Span(
            span_id=self._span_id,
            start_us=0,
            end_us=0,
            tags=[],
            exceptions=[],
            params=[],
            usage=[],
            payloads=[],
            profiles=[]
        )

        self._recorder_context = {}

        # emit start event
        try:
            _tracer().emit_span_start(self, self._recorder_context)
        except Exception as exc:
            logger.error('Error in span start event handlers', exc_info=True)

        self._start_counter = time.perf_counter_ns()
        self._is_started = True

    def _measure(self) -> None:
        self._stop_counter = time.perf_counter_ns()

    def _stop(self) -> None:
        if not self._is_started:
            return
        if self._is_stopped:
            return
        self._is_stopped = True

        if _tracer().debug_mode:
            logger.debug(f'Stopping span {self._operation}')

        if self._stop_counter is None:
            self._measure()
        latency_ns = self._stop_counter - self._start_counter
        ttft_ns = None
        if self._first_token_counter:
            ttft_ns = self._first_token_counter - self._start_counter

        now = time.time()
        end_us = int(now * 1e6)
        start_us = int(end_us - latency_ns / 1e3)
        now = int(now)

        # emit stop event
        try:
            _tracer().emit_span_stop(self, self._recorder_context)
        except Exception as exc:
            logger.error('Error in span stop event handlers', exc_info=True)

        # emit read event
        try:
            _tracer().emit_span_read(self, self._recorder_context)
        except Exception as exc:
            logger.error('Error in span read event handlers', exc_info=True)

        span_tags = self._merged_span_tags()

        # update RED metrics
        _tracer().metric_store().update_histogram(
            scope='performance', name='latency', tags=span_tags, value=latency_ns, update_ts=now, is_time=True)
        if ttft_ns:
            _tracer().metric_store().update_histogram(
                scope='performance', name='first_token', tags=span_tags, value=ttft_ns, update_ts=now, is_time=True)
        _tracer().metric_store().inc_counter(
            scope='performance', name='call_count', tags=span_tags, value=1, update_ts=now)
        if self._exc_infos and len(self._exc_infos) > 0:
            for exc_info in self._exc_infos:
                if exc_info[0] is not None:
                    _tracer().metric_store().inc_counter(
                        scope='performance', name='exception_count', tags=span_tags, value=1, update_ts=now)
                    self.set_tag('exception', exc_info[0].__name__)
        if latency_ns > 0 and self._output_tokens and self._output_tokens > 0:
            _tracer().metric_store().update_rate(
                scope='performance', name='output_tps', tags=span_tags, count=self._output_tokens, interval=latency_ns/1e9, update_ts=now)

        # update usage metrics
        if self._usage is not None:
            for usage in self._usage.values():
                usage_tags = span_tags.copy()
                _tracer().metric_store().inc_counter(
                    scope='usage', name=usage.name, tags=usage_tags, value=usage.value, update_ts=now)

        # update recorder metrics
        if _tracer().check_metric_read_interval(now):
            _tracer().set_metric_read(now)
            try:
                _tracer().emit_metric_update()
            except Exception as exc:
                logger.error('Error in span read event handlers', exc_info=True)

        # fill and upload span
        # copy data to span model
        self._model.start_us = start_us
        self._model.end_us = end_us
        if self._root_span_id:
            self._model.root_span_id = self._root_span_id
        if self._parent_span_id:
            self._model.parent_span_id = self._parent_span_id

        self._model.latency_ns = latency_ns
        if ttft_ns:
            self._model.ttft_ns = ttft_ns
        if self._output_tokens:
            self._model.output_tokens = self._output_tokens

        # copy tags
        for key, value in span_tags.items():
            self._model.tags.append(client.Tag(
                key=sanitize_str(key, max_len=50),
                value=sanitize_str(value, max_len=250)
            ))

        # copy exception
        if self._exc_infos:
            for exc_info in self._exc_infos:
                exc_type = None
                message = None
                stack_trace = None
                if exc_info[0] and hasattr(exc_info[0], '__name__'):
                    exc_type = str(exc_info[0].__name__)
                if exc_info[1]:
                    message = str(exc_info[1])
                if exc_info[2]:
                    frames = traceback.format_tb(exc_info[2])
                    if len(frames) > 0:
                        stack_trace = ''.join(frames)

                if exc_type and message:
                    exception_model = client.Exception(
                        exc_type=exc_type,
                        message=message,
                    )
                    if stack_trace:
                        exception_model.stack_trace = stack_trace
                    self._model.exceptions.append(exception_model)

        # copy params
        if self._params is not None:
            for key, value in self._merged_params().items():
                self._model.params.append(client.Param(
                    name=sanitize_str(key, max_len=50),
                    value=sanitize_str(value, max_len=250)
                ))

        # copy usage counters
        if self._usage is not None:
            for usage in self._usage.values():
                self._model.usage.append(client.UsageCounter(
                    name=usage.name,
                    value=usage.value
                ))

        # copy payloads
        if self._payloads is not None:
            for payload in self._payloads.values():
                if _tracer().record_payloads:
                    try:
                        content_type, content_bytes = encode_payload(payload.content)
                        if len(content_bytes) <= Span.MAX_PAYLOAD_BYTES:
                            self._model.payloads.append(client.Payload(
                                name=payload.name,
                                content_type=content_type,
                                content_base64=base64.b64encode(content_bytes).decode('utf-8')
                            ))
                    except Exception as exc:
                        logger.debug('Error encoding {0} payload for operation {1}'.format(payload.name, self._operation))

        # copy profiles
        if self._profiles is not None:
            for profile in self._profiles.values():
                if len(profile.content) <= Span.MAX_PROFILE_SIZE:
                    self._model.profiles.append(client.Profile(
                        name=profile.name,
                        format=profile.format,
                        content=profile.content
                    ))

        # queue span model for upload
        _tracer().uploader().upload_span(self._model)

        # trigger upload
        if self._is_root:
            _tracer().tick(now)

    def measure(self) -> None:
        if not self._is_stopped:
            self._measure()

    def first_token(self) -> None:
        if not self._first_token_counter:
            self._first_token_counter = time.perf_counter_ns()

    def set_output_tokens(self, tokens: int) -> None:
        self._output_tokens = tokens

    def inc_output_tokens(self, tokens: int) -> None:
        if self._output_tokens is None:
            self._output_tokens = 1
        else:
            self._output_tokens += tokens

    def stop(self) -> None:
        try:
            self._stop()
        except Exception:
            logger.error('Error stopping span', exc_info=True)
        finally:
            self._is_stopped = True
    
    def set_tag(self, key: str, value: str) -> None:
        if not key:
            logger.error('set_tag: key must be provided')
            return

        if self._tags is None:
            self._tags = {}

        if value is None:
            self._tags.pop(key, None)
            return

        if len(self._tags) > Span.MAX_SPAN_TAGS:
            logger.error('set_tag: too many tags (>{0})'.format(Span.MAX_SPAN_TAGS))
            return

        self._tags[key] = value

    def get_tag(self, key):
        if self._tags is None:
            return None
        return self._tags.get(key)

    def add_exception(self, exc: Optional[Exception] = None, exc_info: Optional[bool] = None) -> None:
        if exc is not None and not isinstance(exc, Exception):
            logger.error('add_exception: exc must be instance of Exception')
            return

        if exc_info is not None and not isinstance(exc_info, bool):
            logger.error('add_exception: exc_info must be bool')
            return

        if self._exc_infos is None:
            self._exc_infos = []

        if exc:
            self._exc_infos.append((exc.__class__, str(exc), exc.__traceback__))
        elif exc_info == True:
            self._exc_infos.append(sys.exc_info())

    def set_param(self, name: str, value: str) -> None:
        if self._params is None:
            self._params = {}

        if not name:
            logger.error('set_param: name must be provided')
            return

        if not value:
            logger.error('set_param: value must be provided')
            return

        if len(self._params) > Span.MAX_PARAMS:
            logger.error('set_param: too many params (>{0})'.format(Span.MAX_PARAMS))
            return

        self._params[name] = value

    def set_usage(self, name: str, value: int) -> None:
        if self._usage is None:
            self._usage = {}

        if name and not isinstance(name, str):
            logger.error('set_usage: name must be string')
            return

        if value and not isinstance(value, (int, float)):
            logger.error('set_usage: value must be number')
            return

        if len(self._usage) > Span.MAX_USAGES_COUNTERS:
            logger.error('set_usage: too many usage counters (>{0})'.format(Span.MAX_USAGES_COUNTERS))
            return

        self._usage[name] = Usage(name=name, value=value)

    def inc_usage(self, name: str, value: int) -> None:
        if self._usage is None or name not in self._usage:
            self.set_usage(name, value)
        else:
            self._usage[name].value += value

    def set_payload(
            self, 
            name: str, 
            content: Any) -> None:
        if self._payloads is None:
            self._payloads = {}

        if not name or not isinstance(name, str):
            logger.error('set_payload: name must be string')
            return

        if len(self._payloads) > Span.MAX_PAYLOADS:
            logger.error('set_payload: too many payloads (>{0})'.format(Span.MAX_PAYLOADS))
            return

        self._payloads[name] = Payload(
            name=name,
            content=content)

    def append_payload(
            self, 
            name: str, 
            content: Any) -> None:
        if self._payloads is None:
            self._payloads = {}
 
        if not name or not isinstance(name, str):
            logger.error('append_payload: name must be string')
            return

        if len(self._payloads) > Span.MAX_PAYLOADS:
            logger.error('append_payload: too many payloads (>{0})'.format(Span.MAX_PAYLOADS))
            return

        if name in self._payloads:
            payload = self._payloads[name]
            payload.content += content
        else:
            self._payloads[name] = Payload(
                name=name,
                content=content)

    def set_profile(
            self, 
            name: str, 
            format: str,
            content: str) -> None:
        if self._profiles is None:
            self._profiles = {}

        if not name or not isinstance(name, str):
            logger.error('set_profile: name must be string')
            return

        if len(self._profiles) > Span.MAX_PROFILES:
            logger.error('set_profile: too many profiles (>{0})'.format(Span.MAX_PROFILES))
            return

        self._profiles[name] = Profile(
            name=name,
            format=format,
            content=content)

    def score(
            self,
            name: str, 
            score: Union[int, float], 
            unit: Optional[str] = None,
            severity: Optional[int] = None,
            comment: Optional[str] = None) -> None:
        now = int(time.time())

        if not name:
            logger.error('Span.score: name is required')
            return

        if not name:
            logger.error('Span.score: score is required')
            return

        score_obj = client.Score(
            score_id=uuid_sha1(size=12),
            tags=[],
            span_id=self._model.span_id,
            name=name,
            score=score,
            create_ts=now
        )

        for tag_key, tag_value in self._merged_span_tags().items():
            score_obj.tags.append(client.Tag(
                key=sanitize_str(tag_key, max_len=50),
                value=sanitize_str(tag_value, max_len=250)
            ))

        if unit is not None:
            score_obj.unit = unit

        if severity and severity >= 1 and severity <= 5:
            score_obj.severity = severity

        if comment:
            score_obj.comment = comment
        
        _tracer().uploader().upload_score(score_obj)
        _tracer().tick(now)

    def trace(
            self, 
            operation: str,
            tags: Optional[Dict[str, str]] = None) -> 'Span':
        return Span(
            operation=operation, 
            tags=tags,
            root_span_id=self._root_span_id,
            parent_span_id=self._span_id)

    def _merged_span_tags(self, extra_tags=None):
        span_tags = {}
        if _tracer().tags is not None:
            span_tags.update(_tracer().tags)
        if self._context_tags:
            span_tags.update(self._context_tags)
        if self._tags is not None:
            span_tags.update(self._tags)
        if extra_tags is not None:
            span_tags.update(extra_tags)
        return span_tags

    def _merged_params(self):
        params = {}
        if _tracer().params is not None:
            params.update(_tracer().params)
        if self._params is not None:
            params.update(self._params)
        return params

    def repr(self):
        return 'Span({0})'.format(self._operation)


def encode_payload(content):
    content_dict = _obj_to_dict(content)
    return ('application/json', json.dumps(content_dict).encode('utf-8'))


def _obj_to_dict(obj, level=0):
    if level >= 50:
        return
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    elif isinstance(obj, dict):
        return {k: _obj_to_dict(v, level=level+1) for k, v in obj.items()}
    elif isinstance(obj, (list, set, tuple)):
        return [_obj_to_dict(e, level=level+1) for e in obj]
    elif hasattr(obj, '__dict__'):
        return _obj_to_dict(vars(obj), level=level+1)
    else:
        return str(obj)