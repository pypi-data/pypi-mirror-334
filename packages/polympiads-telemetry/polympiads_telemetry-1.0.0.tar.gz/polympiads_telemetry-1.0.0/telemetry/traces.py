
from typing import Any, Dict, List, Tuple
from opentelemetry import trace
from opentelemetry.trace import get_tracer
from opentelemetry.propagate import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as HTTPExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as GRPCExporter
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
from opentelemetry.sdk.trace import ReadableSpan

from telemetry.config import TestConfig, HttpConfig

#################
# CONFIGURATION #
#################

_TEST_EXPORTER = InMemorySpanExporter()

def configure_http (config: HttpConfig):
    provider = TracerProvider(resource=config.resource)
    provider.add_span_processor(BatchSpanProcessor(HTTPExporter( config.traces_endpoint )))

    trace.set_tracer_provider(provider)

def get_test_exporter ():
    return _TEST_EXPORTER
def configure_test (config: TestConfig):
    provider = TracerProvider(resource=config.resource)
    provider.add_span_processor(SimpleSpanProcessor(_TEST_EXPORTER))

    trace.set_tracer_provider(provider)

#################
#### TESTING ####
#################

class TraceTestVerbosity:
    NONE = 0
    FULL = 1

class BaseInterval:
    start_time: int
    end_time: int

def group_intervals (l: List[BaseInterval]) -> List[List[BaseInterval]]:
    # Given a set of increasing intervals
    # Group them into equivalence classes

    groups = []
    id_by_key: Dict[str, int] = {}
    keys = []

    for itv in l:
        key = f"{itv.start_time}:{itv.end_time}"

        if key not in id_by_key:
            keys.append( (itv.start_time, itv.end_time, key) )
            id_by_key[key] = len(groups)
            groups.append([])
        
        groups[id_by_key[key]].append(itv)
    
    res = []
    keys.sort()
    
    for st, et, key in keys:
        res.append(groups[id_by_key[key]])
    
    return res

class VirtualEvent:
    name  : str
    attrs : Dict[str, Any]

    time : int

    @property
    def start_time (self): return self.time
    @property
    def end_time (self): return self.time

    def match_with (self, other: "VirtualEvent"):
        if self.name != other.name:
            return False
        
        if set( self.attrs.keys() ) != set( other.attrs.keys() ):
            return False
        
        for key in self.attrs.keys():
            if str(self.attrs[key]) != str(other.attrs[key]):
                return False
        
        return True

class VirtualSpan:
    parent : "VirtualSpan | None"
    name   : str
    attrs  : Dict[str, Any]
    events : List[VirtualEvent]
    childs : "List[VirtualSpan]"

    start_time : int
    end_time   : int

    def __lt__ (self, other: "VirtualSpan"):
        if self.start_time == other.start_time:
            return self.end_time < other.end_time
        return self.start_time < other.start_time

    @property
    def __equiv_itvs__ (self) -> "List[List[VirtualSpan | VirtualEvent]]":
        itvs = self.events + self.childs

        return group_intervals(itvs)
    def match_with (self, other: "VirtualSpan"):
        if self.name != other.name:
            return False
        if set( self.attrs.keys() ) != set( other.attrs.keys() ):
            return False
        for key in self.attrs.keys():
            if str( self.attrs[key] ) != str( other.attrs[key] ):
                return False
        
        if len(self.events) != len(other.events):
            return False
        if len(self.childs) != len(other.childs):
            return False
        
        sgroups = list(reversed(self .__equiv_itvs__))
        ogroups = list(reversed(other.__equiv_itvs__))

        while len(sgroups) != 0 and len(ogroups) != 0:
            g1 = sgroups[-1]
            if len(g1) == 0:
                sgroups.pop()
                continue
            g2 = ogroups[-1]
            if len(g2) == 0:
                ogroups.pop()
                continue
            found = None
            for m1 in g1:
                for other in g2:
                    if type(m1) != type(other):
                        continue
                    if m1.match_with(other):
                        found = m1, other
                        break
                if found is not None:
                    break
            if found is None:
                return False
            g1.remove(found[0])
            g2.remove(found[1])

        return True

class VirtualContext:
    roots : List[VirtualSpan]

    def __init__(self):
        self.roots = []

    def as_span (self):
        span = VirtualSpan()
        span.parent = None
        span.childs = self.roots
        span.attrs = {}
        span.events = []
        span.name = "<root>"
        span.start_time = 0
        span.end_time = 0
        return span
    def match_with (self, other: "VirtualContext"):
        return self.as_span().match_with(other.as_span())
        
    def as_scheme (self):
        lines: List[Tuple[str, str]] = []

        def args_to_string (args: Dict[str, Any]):
            l = []
            for key in args.keys():
                l.append((key, args[key]))
            l.sort()

            def arg_to_string (arg: Tuple[str, Any]):
                return f"[{arg[0]}:{arg[1]}]"

            if len(args) == 0: return ""
            return " " + ("".join(
                map(
                    arg_to_string,
                    l
                )
            ))
        def dfs (node: VirtualSpan, depth=0):
            pref = "| " * depth
            lines.append((pref + "+", f"Span  \"{node.name}\"{args_to_string(node.attrs)}"))

            events = list(reversed(node.events))
            childs = list(reversed(node.childs))

            while len(events) + len(childs) != 0:
                use_child = len(childs) > 0
                if len(events) > 0 and len(childs) > 0:
                    use_child = childs[-1].start_time < events[-1].time
                
                if use_child:
                    dfs(childs[-1], depth + 1)
                    childs.pop()
                else:
                    event = events[-1]
                    lines.append((pref + "|", f"Event \"{event.name}\"{args_to_string(event.attrs)}"))
                    events.pop()

            lines.append((pref + "+", ""))
        
        for node in self.roots:
            dfs(node)
        
        max_sze = 0
        for pref, suff in lines:
            max_sze = max(len(pref), max_sze)
        
        true_lines = []
        for pref, suff in lines:
            pref = pref.ljust(max_sze + 2)

            true_lines.append(pref + suff)
        return "\n".join(true_lines)

    @staticmethod
    def from_scheme (scheme: str):
        def parse_name_and_args (param: str):
            param = param.strip()
            assert param[0] == '"'

            offset = param.find('"', 1)
            assert offset != -1

            name  = param[1:offset]
            param = param[offset:]
            words = "".join(param.split("]")).split("[")[1:]
            
            attrs = {}
            for word in words:
                word = word.strip()
                key, value = word.split(":", 1)

                attrs[key] = value
                if value.isdigit():
                    attrs[key] = int(value)
            return name, attrs

        def parse_params (param: str):
            param  = param.strip()
            offset = param.find(' ')
            if offset == -1: return None

            ptyp = param[:offset]
            return ptyp, parse_name_and_args(param[offset:])

        lines = scheme.splitlines()
        params = []
        for i in range(len(lines)):
            lines[i] = lines[i].strip()

            offset = 0
            while offset < len(lines[i]) and lines[i][offset] in " +|":
                offset += 1

            params.append( parse_params(lines[i][offset:]) )

        def dfs (line: int, offset = 0) -> VirtualSpan:
            span = VirtualSpan()
            span.childs = []
            span.parent = None
            span.start_time = line
            span.events = []
            span.name = "<unknown>"
            span.attrs = {}
            
            if params[line] is not None:
                _ptyp, (name, attrs) = params[line]
                span.name = name
                span.attrs = attrs

            line += 1

            cnt_plus = 0
            while lines[line][offset] == '|':
                nxt_plus = lines[line].find('+', offset + 1)
                nxt_bar  = lines[line].find('|', offset + 1)

                if params[line] is not None and nxt_bar == -1 and nxt_plus == -1:
                    vevent = VirtualEvent()
                    _ptyp, (name, attrs) = params[line]
                    vevent.name = name
                    vevent.attrs = attrs
                    vevent.time = line
                    span.events.append(vevent)

                if nxt_plus != -1 and nxt_bar == -1:
                    cnt_plus += 1
                    if (cnt_plus % 2) == 1:
                        subspan = dfs(line, nxt_plus)

                        span.childs.append(subspan)
                        subspan.parent = span

                line += 1
            
            span.end_time = line
            return span
        
        roots = []

        cnt_plus = 0
        for i in range(len(lines)):
            if len(lines[i]) == 0: continue
            if lines[i][0] == '+':
                cnt_plus += 1
                if (cnt_plus % 2) == 1:
                    roots.append( dfs(i) )
        
        ctx = VirtualContext()
        ctx.roots = roots
        return ctx

    @staticmethod
    def from_spans (spans: Tuple[ReadableSpan]):
        span_by_id: Dict[int, VirtualSpan] = {}
        for span in spans:
            vspan = VirtualSpan()
            vspan.name = span.name
            vspan.attrs = span.attributes
            vspan.events = []
            vspan.childs = []
            vspan.parent = None
            vspan.start_time = span.start_time
            vspan.end_time = span.end_time
            for event in span.events:
                vevent = VirtualEvent()
                vevent.name = event.name
                vevent.attrs = event.attributes
                vevent.time = event.timestamp
                vspan.events.append(vevent)
            span_by_id[span.context.span_id] = vspan
        
        ctx = VirtualContext()
        for span in spans:
            vspan = span_by_id[span.context.span_id]
            if span.parent is None:
                ctx.roots.append(vspan)
                continue

            vspan.parent = span_by_id[span.parent.span_id]
            vspan.parent.childs.append(vspan)
        ctx.roots.sort()
        for span in spans:    
            vspan = span_by_id[span.context.span_id]
            vspan.childs.sort()

        return ctx

    @staticmethod
    def from_exporter (clear: bool = True, exporter: InMemorySpanExporter = None):
        if exporter is None:
            exporter = _TEST_EXPORTER
        
        spans = exporter.get_finished_spans()

        if clear:
            exporter.clear()
        
        return VirtualContext.from_spans( spans )

    @staticmethod
    def verify_scheme (
            scheme: str, verbosity: TraceTestVerbosity = TraceTestVerbosity.NONE, 
            clear: bool = True, exporter: InMemorySpanExporter = None):
        ctx_scheme = VirtualContext.from_scheme   ( scheme )
        ctx_export = VirtualContext.from_exporter ( clear, exporter )

        if ctx_scheme.match_with(ctx_export):
            return True
        
        if verbosity == TraceTestVerbosity.FULL:
            print("===== EXPECTED =====")
            print(ctx_scheme.as_scheme())
            print()
            print("===== FOUND =====")
            print(ctx_export.as_scheme())
            print()
            print("Warning, in case of short time spans, the scheme might look different")
            print("But they might be equivalent in the match.")

        return False
