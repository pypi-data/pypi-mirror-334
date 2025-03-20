import re
import time

import contextvars
from functools import partial
from collections import defaultdict
from typing import Optional, Type, Union, List, Set, Tuple, Dict, DefaultDict, Callable

import asyncio
from asyncio import Future

from aioquic.buffer import Buffer, UINT_VAR_MAX, BufferReadError
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.connection import QuicConnection, QuicErrorCode, stream_is_unidirectional
from aioquic.quic.events import QuicEvent, StreamDataReceived, ProtocolNegotiated, DatagramFrameReceived
from aioquic.h3.connection import H3Connection, ErrorCode, H3_ALPN
from aioquic.h3.events import HeadersReceived

from .types import *
from .context import *
from .messages import *
from .utils.logger import *

from importlib.metadata import version
USER_AGENT = f"aiomoqt/{version('aiomoqt')}"


MOQT_IDLE_STREAM_TIMEOUT = 30

logger = get_logger(__name__)
    

class H3CustomConnection(H3Connection):
    """Custom H3Connection wrapper to support alternate SETTINGS"""
    
    def __init__(self, quic: QuicConnection, table_capacity: int = 0, **kwargs) -> None:
        # settings table capacity can be overridden - this should be generalized
        self._max_table_capacity = table_capacity
        self._max_table_capacity_cfg = table_capacity
        super().__init__(quic, **kwargs)
        # report sent settings
        settings = self.sent_settings
        if settings is not None:
            logger.debug("H3 SETTINGS sent:")
            for setting_id, value in settings.items():
                logger.debug(f"  Setting 0x{setting_id:x} = {value}")

    @property
    def _max_table_capacity(self):
        return self._max_table_capacity_cfg

    @_max_table_capacity.setter
    def _max_table_capacity(self, value):
        # Ignore the parent class attempt to set it
        pass
    
    
# base class for client and server session objects
class MOQTSession:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()


class MOQTSessionProtocol(QuicConnectionProtocol):
    """MOQT session protocol implementation."""

    def __init__(self, *args, session: 'MOQTSession', **kwargs):
        super().__init__(*args, **kwargs)
        self._session: MOQTSession = session  # backref to session object with config
        self._h3: Optional[H3Connection] = None
        self._session_id: Optional[int] = None
        self._control_stream_id: Optional[int] = None
        self._loop = asyncio.get_running_loop()
        self._wt_session_setup: Future[bool] = self._loop.create_future()
        self._moqt_version: int = MOQT_CUR_VERSION
        self._moqt_session_setup: Future[bool] = self._loop.create_future()
        self._moqt_session_closed: Future[Tuple[int,str]] = self._loop.create_future()
        self._next_subscribe_id = 1  # prime subscribe id generator
        self._next_track_alias = 1  # prime track alias generator
        self._stream_queues: DefaultDict[int, asyncio.Queue[Buffer]] = defaultdict(asyncio.Queue)
        self._stream_tasks: Dict[int, asyncio.Task] = {}
        self._tasks: Set[asyncio.Task] = set()
        self._close_err = None  # tuple holding latest (error_code, Reason_phrase)
        
        self._data_streams: Dict[int, int] = {}  # keep track of active data streams
        self._track_aliases: Dict[int, int] = {}  # map alias to subscription_id
        self._subscriptions: Dict[int, List] = {}  # map subscription_id to request
        self._announce_responses: Dict[int, Future[MOQTMessage]] = {}
        self._subscribe_announces_responses: Dict[int, Future[MOQTMessage]] = {}
        self._subscribe_responses: Dict[int, Future[MOQTMessage]] = {}
        self._unsubscribe_responses: Dict[int, Future[MOQTMessage]] = {}
        self._fetch_responses: Dict[int, Future[MOQTMessage]] = {}
        
        self._control_msg_registry = dict(MOQTSessionProtocol.MOQT_CONTROL_MESSAGE_REGISTRY)
        self._stream_data_registry = dict(MOQTSessionProtocol.MOQT_STREAM_DATA_REGISTRY)
        self._dgram_data_registry = dict(MOQTSessionProtocol.MOQT_DGRAM_DATA_REGISTRY)

    async def __aexit__(self, exc_type, exc, tb):
        # Clean up the context when the session exits

        return await super().__aexit__(exc_type, exc, tb)

    @staticmethod
    def get_ts_objid(line: str):
        # Convert bytes to string if needed
        if isinstance(line, bytes):
            line = line.decode('utf-8', errors='replace')
        # Pattern to match the timestamp and object ID
        pattern = r'^\|\s+(\d+)\s+\|\S\|\s+(\d+\.\d+(?:\.\d+)*)'
        match = re.search(pattern, line)
        if match:
            timestamp = match.group(1)
            object_id = match.group(2)
            timestamp = int(timestamp) if timestamp is not None else 0
            object_id = object_id if object_id is not None else "<no-match>"
            return timestamp, object_id
        return 0, "<no-match>"

    @staticmethod
    def _make_namespace_tuple(namespace: Union[str, Tuple[str, ...]]) -> Tuple[bytes, ...]:
        """Convert string or tuple into bytes tuple."""
        if isinstance(namespace, str):
            return tuple(part.encode() for part in namespace.split('/'))
        elif isinstance(namespace, tuple):
            if all(isinstance(x, bytes) for x in namespace):
                return namespace
            return tuple(part.encode() if isinstance(part, str) else part for part in namespace)
        raise ValueError("namespace must be string with '/' delimiters or tuple")

    def _allocate_subscribe_id(self) -> int:
        """Get next available subscribe ID."""
        subscribe_id = self._next_subscribe_id
        self._next_subscribe_id += 1
        return subscribe_id

    def _allocate_track_alias(self, subscribe_id: int = 1) -> int:
        """Get next available track alias."""
        track_alias = self._next_track_alias
        self._next_track_alias += 1
        self._track_aliases[track_alias] = subscribe_id
        return track_alias
    
    def _control_task_done(self, task: asyncio.Task) -> None:
        """Remove control task from set."""
        self._tasks.discard(task)
        if task.cancelled():
            logger.warning("MOQT warn: control task cancelled")
        else:
            e = task.exception()
            if e: logger.error(f"MOQT error: control task failed with exception: {e}")

    def _endpoint_match(self, path: Union[bytes,str]):
        endpoint = getattr(self._session, 'endpoint')
        if endpoint is None:
            return False
        # Convert bytes to str if needed
        if isinstance(endpoint, bytes):
            endpoint = endpoint.decode('utf-8')
        if isinstance(path, bytes):
            path = path.decode('utf-8')
            
        # Strip trailing slashes
        endpoint = endpoint.rstrip('/')
        path = path.rstrip('/')
        
        return endpoint == path
            
    def _moqt_handle_control_message(self, buf: Buffer) -> Optional[MOQTMessage]:
        """Process an incoming message."""
        buf_len = buf.capacity
        if buf_len == 0:
            logger.warning("MOQT event: handle control message: no data")
            return None
        pos = buf.tell()
        logger.debug(f"MOQT event: handle control message: ({buf_len} bytes) 0x{buf.data_slice(0, buf_len).hex()}")
        try:
            start_pos = buf.tell()
            msg_type = buf.pull_uint_var()
            msg_len = buf.pull_uint_var()
            hdr_len = buf.tell() - start_pos
            end_pos = start_pos + hdr_len + msg_len
            assert buf.tell() + msg_len <= buf_len
            # Check that msg_type exists
            try:
                msg_type = MOQTMessageType(msg_type)
            except ValueError:
                logger.error(f"MOQT error: unknown control message: type: {hex(msg_type)} start: {start_pos} len: {msg_len}")
                # Skip the rest of this message if possible
                buf.seek(end_pos)
                return
            # Look up message class
            message_class, handler = self._control_msg_registry[msg_type]
            logger.debug(f"MOQT event: control message: {message_class.__name__} ({msg_len} bytes)")
            # Deserialize message
            msg = message_class.deserialize(buf)
            msg_len += hdr_len
            if end_pos > buf.tell():
                logger.debug(f"MOQT event: control message: seeking msg end: {end_pos}")
                buf.seek(end_pos)
            #assert start_pos + msg_len == (buf.tell())
            logger.info(f"MOQT event: control message parsed: {msg})")

            # Schedule handler if one exists
            if handler is not None:
                logger.debug(f"MOQT event: creating handler task: {handler.__name__}")
                task = asyncio.create_task(handler(self, msg))
                task.add_done_callback(self._control_task_done)
                self._tasks.add(task)
                
            return msg

        except Exception as e:
            logger.error(f"handle_control_message: error handling control message: {e}")
            raise
 
    def _stream_task_done(self, stream_id: int, task: asyncio.Task) -> None:
        """Remove stream task from dict."""
        if stream_id in self._stream_tasks:
            del self._stream_tasks[stream_id]
        else:
            logger.error(f"MOQT error: _stream_task_done: stream does not exist: {stream_id}")
        if task.cancelled():
            logger.warning("MOQT warn: stream task cancelled")
        else:
            e = task.exception()
            if e: logger.error(f"MOQT error: stream task failed with exception: {e}")
 
    # task for processing data streams
    async def _process_data_stream(self, stream_id: int) -> None:
        ''' Subgroup stream data processing task '''
        re_buf = Buffer(capacity=(1024*1024*2))  # pre-allocate large buffer accumulator
        cur_pos: int = 0
        consumed: int = 0
        needed: int = 0
        group_id = None
        subgroup_id = None
        object_id = None
        while True:
            try:
                while True:
                    async with asyncio.timeout(MOQT_IDLE_STREAM_TIMEOUT):
                        msg_buf = await self._stream_queues[stream_id].get()
                        
                    if msg_buf is None:  # Sentinel done value - return
                        logger.debug(f"MOQT stream({stream_id}): queue closed: task shutdown")
                        return
                    
                    cur_pos = msg_buf.tell()
                    msg_len = msg_buf.capacity

                    if msg_len < needed:
                        needed -= msg_len
                        re_buf.push_bytes(msg_buf.data_slice(cur_pos,msg_len))
                        have = re_buf.tell()
                        logger.debug(f"MOQT stream({stream_id}): data added: len: {msg_len} have: {have} still need: {needed}")
                    elif cur_pos == msg_len:
                        continue  # special case where the stream id is all we got - next
                    else:
                        logger.debug(f"MOQT stream({stream_id}): data received: pos: {cur_pos} len: {msg_len} needed: {needed}")
                        break
                        
            except asyncio.TimeoutError:
                logger.warning(f"MOQT stream({stream_id}): idle timeout: {group_id}.{subgroup_id}.{object_id}")
                return
            
            # if more data was needed, add it to re_buf accumulator and reprocess
            if needed > 0:
                re_buf.push_bytes(msg_buf.data_slice(cur_pos,msg_buf.capacity))
                msg_len = re_buf.tell()
                msg_buf = re_buf  # process accumulator, GC msg_buf
                msg_buf.seek(0)
                cur_pos = 0
                needed = 0
                

            while cur_pos < msg_len:
                logger.debug(f"MOQT stream({stream_id}): process message: pos: {cur_pos} len: {msg_len}")
                msg_obj = None
                try:
                    msg_obj = self._moqt_handle_data_stream(stream_id, msg_buf, msg_len)
                except MOQTUnderflow as e:
                    logger.debug(f"MOQT MOQTUnderflow({stream_id}): at pos: {e.pos} need: {e.needed}")
                    needed = e.needed
                    break
                except BufferReadError as e:
                    logger.debug(f"MOQT BufferReadError({stream_id}): cur_pos: {cur_pos} tell: {msg_buf.tell()}")
                    needed = 1  # just get the next msg_buf - we dont know amount needed
                    break
                    
                if msg_obj is None:
                    error = f"MOQT error: data stream({stream_id}):: parsing failed at position: "
                    logger.error(error + f"{msg_buf.tell()} of {msg_len} bytes")
                    self._close_session(SessionCloseCode.PROTOCOL_VIOLATION, error)
                    raise asyncio.CancelledError(SessionCloseCode.PROTOCOL_VIOLATION, error)
                
                consumed = msg_buf.tell() - cur_pos
                cur_pos = msg_buf.tell()
                if isinstance(msg_obj, ObjectHeader):
                    assert object_id is None or msg_obj.object_id > object_id
                    object_id = msg_obj.object_id
                    status = ObjectStatus(msg_obj.status).name
                    if status != ObjectStatus.NORMAL:
                        if msg_obj.status in (ObjectStatus.END_OF_GROUP, ObjectStatus.END_OF_TRACK):
                                logger.info(f"MOQT stream({stream_id}): {group_id}.{subgroup_id}.{object_id} status: {status} size: {consumed} bytes")
                                self._stream_queues[stream_id].closed = True
                                return
                    logger.info(f"MOQT stream({stream_id}): {group_id}.{subgroup_id}.{object_id} {msg_obj} size: {consumed} bytes")
                elif isinstance(msg_obj, SubgroupHeader):
                    logger.info(f"MOQT stream({stream_id}): SubgroupHeader: {msg_obj.group_id}.{msg_obj.subgroup_id} {msg_obj} size: {consumed} bytes")
                    assert group_id is None or msg_obj.group_id > group_id
                    group_id = msg_obj.group_id
                    subgroup_id = msg_obj.subgroup_id
                else:
                    # raise RuntimeError
                    logger.info(f"MOQT stream({stream_id}): {class_name(msg_obj)} size: {consumed} bytes")

            if needed > 0:
                have = msg_len - cur_pos
                # yuck - python memove - custom stream reader in progress
                saved_bytes = msg_buf.data_slice(cur_pos, msg_len)
                if have < needed:  # we might not know how much we need
                    needed -= have
                re_buf.seek(0)
                re_buf.push_bytes(saved_bytes)
                logger.debug(f"MOQT stream({stream_id}): saved {have} bytes tell: {re_buf.tell()} still need: {needed}")
                cur_pos = 0

    def _moqt_handle_data_stream(self, stream_id: int, buf: Buffer, len: int) -> MOQTMessage:
        """Process incoming data messages (not control messages)."""
        if buf.capacity == 0 or buf.tell() >= buf.capacity:
            logger.error(f"MOQT stream({stream_id}): no data at position: {buf.tell()}")
            return
        
        try:
            pos = buf.tell()
            msg_header = None
            # new data streams will not yet have an entry
            if self._data_streams.get(stream_id) is None:
                # Get stream type from first byte
                stream_type = buf.pull_uint_var()
                if stream_type == DataStreamType.SUBGROUP_HEADER:
                    # logger.debug(f"MOQT stream({stream_id}): SubgroupHeader parse: data: 0x{buf.data_slice(pos,pos+8).hex()}...")
                    msg_header = SubgroupHeader.deserialize(buf)
                    data_type = DataStreamType(stream_type).name
                elif stream_type == DataStreamType.FETCH_HEADER:
                    msg_header = FetchHeader.deserialize(buf)
                    data_type = DataStreamType(stream_type).name
                else:
                    data_type = f"0x{hex(stream_type)}"
                    logger.error(f"MOQT stream({stream_id}): unexpected data stream type: {stream_type}")

                if msg_header is None:
                    error = f"data stream {stream_id}: {data_type} parse failed at: {buf.tell()}"
                    logger.error(f"MOQT error: " + error)
                    self._close_session(SessionCloseCode.PROTOCOL_VIOLATION, error)
                    return None
                
                # record that the data stream header has been processed
                consumed = buf.tell() - pos            
                logger.debug(f"MOQT stream({stream_id}): {msg_header} consumed: {consumed} bytes")
                self._data_streams[stream_id] = msg_header
            else:
                if isinstance(self._data_streams[stream_id], SubgroupHeader):
                    msg_header = ObjectHeader.deserialize(buf, len)

                elif isinstance(self._data_streams[stream_id], FetchHeader):
                    msg_header = FetchObject.deserialize(buf)

                if msg_header is None:
                    error = f"MOQT stream({stream_id}): ObjectHeader parse failed at: {buf.tell()}"
                    logger.error(f"MOQT error: " + error)
                    self._close_session(SessionCloseCode.PROTOCOL_VIOLATION, error)
                    return None
                consumed = buf.tell() - pos        
                logger.debug(f"MOQT stream({stream_id}): {class_name(msg_header)} consumed: {consumed} bytes")

                    
            return msg_header
        except Exception:
            raise

    def _moqt_handle_data_dgram(self, buf: Buffer) -> MOQTMessageType:
        """Process incoming data messages (not control messages)."""
        if buf.capacity == 0 or buf.tell() >= buf.capacity:
            logger.error(f"MOQT datagram: no data {buf.tell()}")
            return
        
        logger.debug(f"MOQT handle datagram: 0x{buf.data_slice(0,min(buf.capacity,12))}")

        # Get stream type from first byte
        dgram_type = buf.pull_uint_var()
        if dgram_type == DatagramType.OBJECT_DATAGRAM:
            msg = ObjectDatagram.deserialize(buf,buf.capacity)
            if msg is None:
                error = f"datagram parsing failed at: {buf.tell()}"
                logger.error(f"MOQT error: " + error)
                self._close_session(SessionCloseCode.PROTOCOL_VIOLATION, error)
                return msg
            (sts, id) = MOQTSessionProtocol.get_ts_objid(msg.payload)
            rts = int(time.time()*1000)
            logger.info(f"MOQT event: ObjectDatagram: {id} alias: {msg.track_alias} len: {buf.capacity} bytes delay: {rts-sts} ms")
            return msg            
        elif dgram_type == DatagramType.OBJECT_DATAGRAM_STATUS:
            msg = ObjectDatagramStatus.deserialize(buf)
            if msg is None:
                error = f"datagram parsing failed at: {buf.tell()}"
                logger.error(f"MOQT error: " + error)
                self._close_session(SessionCloseCode.PROTOCOL_VIOLATION, error)
                return msg
            logger.info(f"MOQT event: ObjectDatagramStatus: {msg.group_id}.{msg.object_id} status: {msg.status} len: {buf.capacity} bytes")               
        else:
            error = f"datagram type unknown: {dgram_type}"
            logger.error(f"MOQT error: " + error)
            self._close_session(SessionCloseCode.PROTOCOL_VIOLATION, error)
            return
    
    # def transmit(self) -> None:
    #     """Transmit pending data."""
    #     logger.debug("Transmitting data")
    #     super().transmit()

    def connection_made(self, transport):
        """Called when QUIC connection is established."""
        super().connection_made(transport)
        self._h3 = H3CustomConnection(self._quic, enable_webtransport=True)
        logger.info("H3 connection initialized")

    # primary event handling for all QUIC messaging
    def quic_event_received(self, event: QuicEvent) -> None:
        """Handle incoming QUIC events."""
        
        event_class = class_name(event)

        # QUIC errors terminate the session
        if hasattr(event, 'error_code'):  # Log any errors
            error = getattr(event, 'error_code', QuicErrorCode.INTERNAL_ERROR)
            reason = getattr(event, 'reason_phrase', event_class)
            logger.error(f"QUIC error: code: {error} reason: {reason}")
            self._close_session(error, reason)
            return
        
        # data_len = len(event.data) if hasattr(event, 'data') else 0
        # logger.debug(f"QUIC event: {event_class}: len: {data_len} bytes")
        
        if isinstance(event, ProtocolNegotiated):
            # Enforce supported ALPN
            if event.alpn_protocol in H3_ALPN:
                logger.debug(f"QUIC event: ALPN ProtocolNegotiated: {event.alpn_protocol}")
            elif event.alpn_protocol == "moq-00":
                # XXX - handle QUIC connection
                logger.debug(f"QUIC event: ALPN ProtocolNegotiated alpn: {event.alpn_protocol}")
            else:
                logger.error(f"QUIC error: unknown ALPN: {event.alpn_protocol}")
                self._close_session(
                    SessionCloseCode.UNAUTHORIZED, 
                    f"unsupported ALPN: {event.alpn_protocol}"
                )
            return
        elif isinstance(event, StreamDataReceived) and self._wt_session_setup.done():
            if self._closed.is_set() or self._close_err is not None:
                close_condition = f"MOQT: {self._close_err} QUIC: {self._closed.is_set()}"
                logger.warning(f"QUIC event: stream data after close: " + close_condition)
                return
            
            # Detect abrupt closure of critical streams
            stream_id = event.stream_id
            if (event.end_stream and len(event.data) == 0 and
                stream_id in [self._control_stream_id, self._session_id]):
                self._close_session(
                    SessionCloseCode.INTERNAL_ERROR, 
                    f"critical stream closed by remote peer: {stream_id}"
                )
                return
            
            msg_buf = Buffer(data=event.data)
            msg_len = msg_buf.capacity
            # logger.debug(f"MOQT event: StreamDataReceived: stream: {stream_id} (0x{msg_buf.data_slice(0, min(msg_len,16)).hex()}...)")
            
            # Handle possible MoQT control stream 
            if not stream_is_unidirectional(stream_id):
                # Assume first bidi stream is MoQT control stream
                if self._control_stream_id is None:
                    self._control_stream_id = stream_id
                    # strip of initial WT stream identifier
                    msg_buf.pull_uint_var()
                    msg_buf.pull_uint_var()
                elif stream_id != self._control_stream_id:
                    # XXX ignore additional bidi stream for now - for now
                    logger.warning(f"MOQT event: unrecognized bidirectional stream({stream_id}):")
                    return                      
                        
            # Handle MoQT control messages
            if stream_id == self._control_stream_id:
                # XXX handle underflow in control stream as well
                while msg_buf.tell() < msg_len:
                    msg = self._moqt_handle_control_message(msg_buf)
                    if msg is None:
                        error = f"control stream: parsing failed at position: {msg_buf.tell()} of {msg_len} bytes"
                        logger.error(f"MOQT error: " + error)
                        self._close_session(SessionCloseCode.PROTOCOL_VIOLATION, error)
                        break
                return

            # Handle MoQT data messages
            if stream_is_unidirectional(stream_id):
                if stream_id not in self._data_streams:
                    # strip of initial H3/WT stream identifier
                    msg_buf.pull_uint_var()
                    msg_buf.pull_uint_var()
                    # record the stream exists and stream id stripped
                    self._data_streams[stream_id] = None
                    # create a handler task for this stream
                    assert stream_id not in self._stream_tasks
                    task = asyncio.create_task(self._process_data_stream(stream_id))
                    self._stream_tasks[stream_id] = task
                    task.add_done_callback(partial(self._stream_task_done, stream_id))
                    logger.debug(f"MOQT event: creating _process_data_stream task: {stream_id}")
                    
                # Queue the event data buffer for processing
                if msg_buf.tell() < msg_len:
                    logger.debug(f"MOQT event: pushing data on stream: {stream_id} pos: {msg_buf.tell()} len: {msg_len}")
                    self._stream_queues[stream_id].put_nowait(msg_buf)
                else:
                    logger.debug(f"MOQT event: skipping empty data: {stream_id} pos: {msg_buf.tell()} len: {msg_len}")
                    
                return

        elif isinstance(event, DatagramFrameReceived) and self._wt_session_setup.done():
            msg_buf = Buffer(data=event.data)
            msg_len = msg_buf.capacity
            logger.debug(f"MOQT event: DatagramFrameReceived: 0x{msg_buf.data_slice(0,min(msg_len,16)).hex()}")
            # strip off some QUIC quarter identifier
            msg_buf.pull_uint_var()
            self._moqt_handle_data_dgram(msg_buf)
            return
                      
        # Pass remaining events to H3
        if self._h3 is not None:
            settings = self._h3.received_settings
            try:
                for h3_event in self._h3.handle_event(event):
                    self._h3_handle_event(h3_event)
                # Check if settings just received
                if self._h3.received_settings != settings:
                    settings = self._h3.received_settings
                    logger.debug(f"H3 event: SETTINGS received:")
                    if settings is not None:
                        for setting_id, value in settings.items():
                            logger.debug(f"  Setting 0x{setting_id:x} = {value}")
            except Exception as e:
                logger.error(f"H3 error: error handling event: {e}")
                raise
        else:
            logger.error(f"QUIC event: event not handled({event_class})")
  
    def _h3_handle_event(self, event: QuicEvent) -> None:
        """Handle H3-specific events."""
        logger.debug(f"H3 event: {event}")
        if isinstance(event, HeadersReceived):
            return self._h3_handle_headers_received(event)
        msg_class = class_name(event)
        data = getattr(event, 'data', None)
        hex_data = f"0x{data.hex()}" if data is not None else "<no data>"
        logger.debug(f"H3 event: stream {event.stream_id}: {msg_class}: {hex_data}")
        # pass to parent H3 to handle - XX not required?
        # self._h3.handle_event(event)

    def _h3_handle_headers_received(self, event: HeadersReceived) -> None:
        """Process incoming H3 headers."""
        method = None
        protocol = None
        path = None
        authority = None
        status = None
        is_client = self._quic.configuration.is_client
        stream_id = event.stream_id
        logger.info(f"H3 event: HeadersReceived: session id: {stream_id} is_client: {is_client} ")
        for name, value in event.headers:
            logger.debug(f"  {name.decode()}: {value.decode()}")
            if name == b":method":
                method = value
            elif name == b":protocol":
                protocol = value
            elif name == b":path":
                path = value
            elif name == b":authority":
                authority = value
            elif name == b':status':
                status = value
                
        if is_client:
            if status == b"200":
                logger.debug(f"H3 event: WebTransport client session setup: session id: {stream_id}")
                self._wt_session_setup.set_result(True)
            else:
                error = f"WebTransport session setup failed ({status})"
                logger.error(f"H3 error: stream {stream_id}: " + error)
                self._close_session(ErrorCode.H3_CONNECT_ERROR, error)
        else:
            # Server: Handle incoming WebTransport CONNECT request
            if method == b"CONNECT" and protocol == b"webtransport":
                if self._endpoint_match(path):
                    self._session_id = stream_id
                    # Send 200 response with WebTransport headers
                    response_headers = [
                        (b":status", b"200"),
                        (b"server", USER_AGENT.encode()),
                        (b"sec-webtransport-http3-draft", b"draft02"),
                    ]
                    self._h3.send_headers(
                        stream_id=stream_id,
                        headers=response_headers,
                        end_stream=False
                    )
                    self.transmit()
                    logger.debug(f"H3 event: WebTransport server session setup: session id: {stream_id}")
                    self._wt_session_setup.set_result(True)
                else:
                    # Endpoint doesn't match, return 404
                    logger.warning(f"H3 event: path not found: {path}")
                    error_headers = [
                        (b":status", b"404"),
                        (b"server", USER_AGENT.encode()),
                    ]
                    self._h3.send_headers(
                        stream_id=stream_id,
                        headers=error_headers,
                        end_stream=True
                    )
                    self.transmit()
            else:
                # Unsupported HTTP transaction
                logger.warning(f"H3 event: path not found: {path}")
                error_headers = [
                    (b":status", b"500"),
                    (b"server", USER_AGENT.encode()),
                ]
                self._h3.send_headers(
                    stream_id=stream_id,
                    headers=error_headers,
                    end_stream=True
                )
                self.transmit()
            
    def _close_session(self, 
              error_code: SessionCloseCode = SessionCloseCode.NO_ERROR, 
              reason_phrase: str = "no error") -> None:
        """Close the MoQT session."""
        logger.error(f"MOQT error: closing: {reason_phrase} ({error_code})")
        self._close_err = (error_code, reason_phrase)

        # Signal all stream tasks to shut down gracefully with sentinel value
        for stream_id in list(self._stream_tasks.keys()):
            if stream_id in self._stream_queues:
                self._stream_queues[stream_id].put_nowait(None)
                
        if not self._wt_session_setup.done():
            self._wt_session_setup.set_result(False)
        if not self._moqt_session_setup.done():
            self._moqt_session_setup.set_result(False)
        if not self._moqt_session_closed.done():
            self._moqt_session_closed.set_result((error_code, reason_phrase))
        
    def close(self, 
              error_code: SessionCloseCode = SessionCloseCode.NO_ERROR, 
              reason_phrase: str = "no error"
        ) -> None:
        """Session Protocol Close"""
        if self._close_err is not None:
            error_code, reason_phrase =  self._close_err
        logger.info(f"MOQT session: closing: {reason_phrase} ({error_code})")
        if self._session_id is not None:
            self._h3._quic.close(QuicErrorCode.NO_ERROR)
            logger.debug(f"H3 session: closing: {class_name(self._h3)} ({self._session_id})  QUIC: {self._h3._is_done}")
            if not self._h3._is_done:
                self._h3.send_data(self._session_id, b"", end_stream=True)
            self._session_id = None
        # drop H3 session
        self._h3 = None
        # set the async exit condition for session
        if not self._moqt_session_closed.done():
            self._moqt_session_closed.set_result((error_code, reason_phrase))
        # call parent close and transmit all
        super().close(error_code=error_code, reason_phrase=reason_phrase)
        self.transmit()
        
    async def async_closed(self) -> bool:
        if not self._moqt_session_closed.done():
            self._close_err = await self._moqt_session_closed
        return True


    async def client_session_init(self, timeout: int = 10) -> bool:
        """Initialize WebTransport and MoQT client session."""
        # Create WebTransport session
        self._session_id = self._h3._quic.get_next_available_stream_id(is_unidirectional=False)

        headers = [
            (b":method", b"CONNECT"),
            (b":protocol", b"webtransport"),
            (b":scheme", b"https"),
            (b":authority",
             f"{self._session.host}:{self._session.port}".encode()),
            (b":path", f"/{self._session.endpoint}".encode()),
            (b"sec-webtransport-http3-draft", b"draft02"),
            (b"user-agent", USER_AGENT.encode()),
        ]

        logger.info(f"H3 send: WebTransport CONNECT: session id: {self._session_id}")
        for name, value in headers:
            logger.debug(f"  {name.decode()}: {value.decode()}")
            
        self._h3.send_headers(stream_id=self._session_id, headers=headers, end_stream=False)
        self.transmit()
        
        # Wait for WebTransport session establishment
        try:
            async with asyncio.timeout(timeout):
                result = await self._wt_session_setup
            result = "SUCCESS" if result else "FAILED"
            logger.info(f"H3 event: WebTransport setup: {result}")
        except asyncio.TimeoutError:
            error = f"WebTransport session establishment timeout: {timeout} sec"
            logger.error("H3 error: " + error)
            self._close_session(SessionCloseCode.CONTROL_MESSAGE_TIMEOUT, error)
            raise MOQTException(*self._close_err)

        # Check for H3 connection close
        if self._close_err is not None:
            raise MOQTException(*self._close_err)
        
        # Create MoQT control stream
        self._control_stream_id = self._h3.create_webtransport_stream(session_id=self._session_id)
        logger.info(f"MOQT: control stream created stream id: {self._control_stream_id}")

        # Send CLIENT_SETUP
        client_setup = self.client_setup(
            versions=MOQT_VERSIONS,
            parameters={SetupParamType.MAX_SUBSCRIBER_ID: MOQTMessage._varint_encode(1000)}
        )

        # Wait for SERVER_SETUP
        session_setup = False
        try: 
            async with asyncio.timeout(timeout):
                session_setup = await self._moqt_session_setup
        except asyncio.TimeoutError:
            error = "timeout waiting for SERVER_SETUP"
            logger.error("MOQT error: " + error)
            self._close_session(SessionCloseCode.CONTROL_MESSAGE_TIMEOUT, error)
            pass
        
        if not session_setup or self._close_err is not None:
            logger.error(f"MOQT error: session setup failed: {session_setup}")
            raise MOQTException(*self._close_err)
        
        logger.info(f"MOQT session: setup complete: {result}")



    def send_control_message(self, buf: Buffer) -> None:
        """Send a MoQT message on the control stream."""
        if self._quic is None or self._control_stream_id is None:
            raise MOQTException(SessionCloseCode.INTERNAL_ERROR, "control stream not intialized")
        
        logger.debug(f"QUIC send: control message: {buf.capacity} bytes")

        self._quic.send_stream_data(
            stream_id=self._control_stream_id,
            data=buf.data,
            end_stream=False
        )
        self.transmit()

    def send_dgram_message(self, buf: Buffer) -> None:
        """Send a MoQT message on the control stream."""
        if self._quic is None:
            raise MOQTException(SessionCloseCode.INTERNAL_ERROR, "QUIC not intialized")
                
        logger.debug(f"QUIC send: datagram message: {buf.capacity} bytes")

        self._quic.send_datagram_frame(
            data=buf.data
        )
        self.transmit()

    ################################################################################################
    #  Outbound control message API - note: awaitable messages support 'wait_response' param       #
    ################################################################################################
    
    def client_setup(
        self,
        versions: List[int] = MOQT_VERSIONS,
        parameters: Optional[Dict[int, bytes]] = None,
    ) -> None:
        """Send CLIENT_SETUP message and optionally wait for SERVER_SETUP response."""
        if parameters is None:
            parameters = {}
        
        message = ClientSetup(
            versions=versions,
            parameters=parameters
        )
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        
        return message

    def server_setup(
        self,
        selected_version: int = MOQT_CUR_VERSION,
        parameters: Optional[Dict[int, bytes]] = None
    ) -> ServerSetup:
        """Send SERVER_SETUP message in response to CLIENT_SETUP."""
        if parameters is None:
            parameters = {}
        
        message = ServerSetup(
            selected_version=selected_version,
            parameters=parameters
        )
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        return message
  
    def subscribe(
        self,
        namespace: str,
        track_name: str,
        priority: int = 128,
        group_order: GroupOrder = GroupOrder.ASCENDING,
        filter_type: FilterType = FilterType.LATEST_OBJECT,
        start_group: Optional[int] = 0,
        start_object: Optional[int] = 0,
        end_group: Optional[int] = 0,
        parameters: Optional[Dict[int, bytes]] = None,
        wait_response: Optional[bool] = False,
    ) -> Optional[MOQTMessage]:
        """Subscribe to a track with configurable options."""
        if parameters is None:
            parameters = {}
        subscribe_id = self._allocate_subscribe_id()
        track_alias = self._allocate_track_alias(subscribe_id)
        namespace_tuple = self._make_namespace_tuple(namespace)
        track_name = track_name.encode() if isinstance(track_name, str) else track_name

        message = Subscribe(
            subscribe_id=subscribe_id,
            track_alias=track_alias,
            namespace=namespace_tuple,
            track_name=track_name,
            priority=priority,
            group_order=group_order,
            filter_type=filter_type,
            start_group=start_group,
            start_object=start_object,
            end_group=end_group,
            parameters=parameters
        )
        self._subscriptions[subscribe_id] = [message]
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())

        if not wait_response:
            return message

        # Create future for response
        subscribe_fut = self._loop.create_future()
        self._subscribe_responses[subscribe_id] = subscribe_fut

        async def wait_for_response():
            try:
                async with asyncio.timeout(10):
                    response = await subscribe_fut
            except asyncio.TimeoutError:
                # Create synthetic error response
                response = SubscribeError(
                    subscribe_id=subscribe_id,
                    error_code=0x5,  # TIMEOUT error code
                    reason="Subscribe Response Timeout",
                    track_alias=0
                )
                logger.error(f"Timeout waiting for subscribe response")
            finally:
                logger.debug(f"MOQT: removing subscribe response future: {subscribe_id}")
                self._subscribe_responses.pop(subscribe_id, None)    
            return response

        return wait_for_response()

    def subscribe_ok(
        self,
        subscribe_id: int,
        expires: int = 0,  # 0 means no expiry
        group_order: int = GroupOrder.ASCENDING,
        content_exists: int = 0,
        largest_group_id: Optional[int] = None,
        largest_object_id: Optional[int] = None,
        parameters: Optional[Dict[int, bytes]] = None
    ) -> Optional[MOQTMessage]:
        """Create and send a SUBSCRIBE_OK response."""
        message = SubscribeOk(
            subscribe_id=subscribe_id,
            expires=expires,
            group_order=group_order,
            content_exists=content_exists,
            largest_group_id=largest_group_id,
            largest_object_id=largest_object_id,
            parameters=parameters or {}
        )
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        return message

    def subscribe_error(
        self,
        subscribe_id: int,
        error_code: int = SubscribeErrorCode.INTERNAL_ERROR,
        reason: str = "Internal error",
        track_alias: Optional[int] = None
    ) -> Optional[MOQTMessage]:
        """Create and send a SUBSCRIBE_ERROR response."""
        message = SubscribeError(
            subscribe_id=subscribe_id,
            error_code=error_code,
            reason=reason,
            track_alias=track_alias
        )
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        return message
    
    def unsubscribe(
        self,
        subscribe_id: int,
    ) -> Optional[MOQTMessage]:
        """Unsubscribe from a track."""
        message = Unsubscribe(subscribe_id=subscribe_id)
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
 
        return message       

    def join(
        self,
        namespace: Union[Tuple[bytes,...]|List[Union[bytes,str]]|str],
        track_name: Union[bytes|str],
        subscriber_priority: int = 128,
        group_order: GroupOrder = GroupOrder.DESCENDING,
        pre_group_offset: Optional[int] = 0,
        parameters: Optional[Dict[int, bytes]] = None,
        wait_response: Optional[bool] = False,
    ) -> Optional[Tuple[MOQTMessage, MOQTMessage]]:
        """Subscribe and Joining Fetch."""
        parameters = {} if parameters is None else parameters
        subscribe_id = self._allocate_subscribe_id()
        track_alias = self._allocate_track_alias(subscribe_id)
        namespace = self._make_namespace_tuple(namespace)
        track_name = track_name.encode() if isinstance(track_name, str) else track_name

        message = Subscribe(
            subscribe_id=subscribe_id,
            track_alias=track_alias,
            namespace=namespace,
            track_name=track_name,
            priority=subscriber_priority,
            group_order=group_order,
            filter_type=FilterType.LATEST_OBJECT,
            parameters=parameters
        )
        self._subscriptions[subscribe_id] = [message]
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())

        fetch_subscribe_id = self._allocate_subscribe_id()
        message = Fetch(
            subscribe_id=fetch_subscribe_id,
            subscriber_priority=subscriber_priority,
            group_order=group_order,
            joining_sub_id=subscribe_id,
            fetch_type=FetchType.JOINING_FETCH,
            pre_group_offset=pre_group_offset,
            parameters=parameters
        )
        
        self._subscriptions[subscribe_id] = [message]
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())

        if not wait_response:
            return message

        # Create future for response
        subscribe_fut = self._loop.create_future()
        self._subscribe_responses[subscribe_id] = subscribe_fut        

        fetch_fut = self._loop.create_future()
        self._fetch_responses[fetch_subscribe_id] = fetch_fut

        async def wait_for_response():
            try:
                async with asyncio.timeout(10):
                    sub_response = await subscribe_fut
                    
                async with asyncio.timeout(10):
                    fetch_response = await fetch_fut

            except asyncio.TimeoutError:
                # Create synthetic error response
                response = SubscribeError(
                    subscribe_id=subscribe_id,
                    error_code=0x5,  # TIMEOUT error code
                    reason="Subscribe Response Timeout",
                    track_alias=0
                )
                logger.error(f"Timeout waiting for subscribe response")
                sub_response = response if sub_response is None else sub_response
                fetch_response = response if fetch_response is None else fetch_response
            finally:
                logger.debug(f"MOQT: removing subscribe response future: {subscribe_id}")
                self._subscribe_responses.pop(subscribe_id, None)    
                self._fetch_responses.pop(fetch_subscribe_id, None)
                
            return sub_response, fetch_response

        return wait_for_response()

    def fetch(
        self,
        namespace: Union[Tuple[bytes,...]|List[Union[bytes,str]]|str],
        track_name: Union[bytes|str],
        subscriber_priority: int = 128,
        group_order: GroupOrder = GroupOrder.ASCENDING,
        start_group: Optional[int] = 0,
        start_object: Optional[int] = 0,
        end_group: Optional[int] = 0,
        end_object: Optional[int] = 0,
        parameters: Optional[Dict[int, bytes]] = None,
        wait_response: Optional[bool] = False,
    ) -> Optional[MOQTMessage]:
        """Fetch data from a track with configurable options."""
        parameters = {} if parameters is None else parameters
        subscribe_id = self._allocate_subscribe_id()
        track_alias = self._allocate_track_alias(subscribe_id)
        namespace = self._make_namespace_tuple(namespace)

        if isinstance(track_name, str):
            track_name = track_name.encode()

        message = Fetch(
            subscribe_id=subscribe_id,
            track_alias=track_alias,
            namespace=namespace,
            track_name=track_name,
            priority=subscriber_priority,
            fetch_type=FetchType.FETCH,
            group_order=group_order,
            start_group=start_group,
            start_object=start_object,
            end_group=end_group,
            end_object=end_object,
            parameters=parameters
        )
        
        self._subscriptions[subscribe_id] = [message]
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())

        if not wait_response:
            return message

        # Create future for response
        subscribe_fut = self._loop.create_future()
        self._subscribe_responses[subscribe_id] = subscribe_fut

        async def wait_for_response():
            try:
                async with asyncio.timeout(10):
                    response = await subscribe_fut
            except asyncio.TimeoutError:
                # Create synthetic error response
                response = SubscribeError(
                    subscribe_id=subscribe_id,
                    error_code=0x5,  # TIMEOUT error code
                    reason="Subscribe Response Timeout",
                    track_alias=0
                )
                logger.error(f"Timeout waiting for subscribe response")
            finally:
                logger.debug(f"MOQT: removing subscribe response future: {subscribe_id}")
                self._subscribe_responses.pop(subscribe_id, None)    
            return response

        return wait_for_response()

    def fetch_ok(
        self,
        subscribe_id: int,
        expires: int = 0,  # 0 means no expiry
        group_order: int = GroupOrder.ASCENDING,
        content_exists: int = 0,
        largest_group_id: Optional[int] = None,
        largest_object_id: Optional[int] = None,
        parameters: Optional[Dict[int, bytes]] = None
    ) -> Optional[MOQTMessage]:
        """Create and send a SUBSCRIBE_OK response."""
        message = SubscribeOk(
            subscribe_id=subscribe_id,
            expires=expires,
            group_order=group_order,
            content_exists=content_exists,
            largest_group_id=largest_group_id,
            largest_object_id=largest_object_id,
            parameters=parameters or {}
        )
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        return message

    def fetch_error(
        self,
        subscribe_id: int,
        error_code: int = SubscribeErrorCode.INTERNAL_ERROR,
        reason: str = "Internal error",
        track_alias: Optional[int] = None
    ) -> Optional[MOQTMessage]:
        """Create and send a SUBSCRIBE_ERROR response."""
        message = SubscribeError(
            subscribe_id=subscribe_id,
            error_code=error_code,
            reason=reason,
            track_alias=track_alias
        )
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        return message

    def announce(
        self,
        namespace: Union[str, Tuple[str, ...]],
        parameters: Optional[Dict[int, bytes]] = None,
        wait_response: Optional[bool] = False
    ) -> Optional[MOQTMessage]:
        """Announce track namespace availability."""
        namespace_tuple = self._make_namespace_tuple(namespace)
        message = Announce(
            namespace=namespace_tuple,
            parameters=parameters or {}
        )
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())

        if not wait_response:
            return message

        # Create future for response
        announce_fut = self._loop.create_future()
        self._announce_responses[namespace_tuple] = announce_fut

        async def wait_for_response():
            try:
                async with asyncio.timeout(10):
                    response = await announce_fut
            except asyncio.TimeoutError:
                # Create synthetic error response
                response = AnnounceError(
                    namespace=namespace,
                    error_code=0x5,  # TIMEOUT error code
                    reason="Response timeout"
                )
                logger.error(f"Timeout waiting for announce response")
            finally:
                self._announce_responses.pop(namespace, None)
            return response

        return wait_for_response()

    def announce_ok(
        self,
        namespace: Union[str, Tuple[str, ...]],
    ) -> Optional[MOQTMessage]:
        """Create and send a ANNOUNCE_OK response."""
        namespace_tuple = self._make_namespace_tuple(namespace)
        message = AnnounceOk(
            namespace=namespace_tuple,
        )
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        return message

    def unannounce(
        self,
        namespace: Tuple[bytes, ...]
    ) -> Optional[MOQTMessage]:
        """Withdraw track namespace announcement. (no reply expected)"""        
        message =  Unannounce(namespace=namespace)
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        return message

    def subscribe_announces(
        self,
        namespace_prefix: str,
        parameters: Optional[Dict[int, bytes]] = None,
        wait_response: Optional[bool] = False
    ) -> Optional[MOQTMessage]:
        """Subscribe to announcements for a namespace prefix."""
        if parameters is None:
            parameters = {}

        prefix = self._make_namespace_tuple(namespace_prefix)
        message = SubscribeAnnounces(
            namespace_prefix=prefix,
            parameters=parameters
        )
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())

        if not wait_response:
            return message

        # Create future for response
        sub_announces_fut = self._loop.create_future()
        self._subscribe_announces_responses[prefix] = sub_announces_fut

        async def wait_for_response():
            try:
                async with asyncio.timeout(10):
                    response = await sub_announces_fut
            except asyncio.TimeoutError:
                # Create synthetic error response
                response = SubscribeAnnouncesError(
                    namespace_prefix=prefix,
                    error_code=0x5,  # TIMEOUT error code
                    reason="Response timeout"
                )
                logger.error(f"Timeout waiting for announce subscribe response")
            finally:
                self._subscribe_announces_responses.pop(prefix, None)
            
            return response

        return wait_for_response()

    def subscribe_announces_ok(
        self,
        namespace_prefix: Union[str, Tuple[str, ...]],
    ) -> Optional[MOQTMessage]:
        """Create and send a SUBSCRIBE_ANNOUNCES_OK response."""
        namespace_tuple = self._make_namespace_tuple(namespace_prefix)
        message = SubscribeAnnouncesOk(namespace_prefix=namespace_tuple)
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        return message

    def unsubscribe_announces(
        self,
        namespace_prefix: str
    ) -> Optional[MOQTMessage]:
        """Unsubscribe from announcements for a namespace prefix."""        
        prefix = self._make_namespace_tuple(namespace_prefix)
        message = UnsubscribeAnnounces(namespace_prefix=prefix)
        logger.info(f"MOQT send: {message}")
        self.send_control_message(message.serialize())
        return message


    ###############################################################################################
    #  Inbound MoQT message handlers                                                              #
    ###############################################################################################
    
    def default_message_handler(self, type: int,  msg: MOQTMessage) -> None:
        """Call the standard message handler"""
        _, handler = self.MOQT_CONTROL_MESSAGE_REGISTRY[type]
        # Schedule handler if one exists
        logger.info(f"MOQT event: calling default handler: {handler.__qualname__}")
        if handler is not None:
            task = asyncio.create_task(handler(self, msg))
            task.add_done_callback(lambda t: self._tasks.discard(t))
            self._tasks.add(task)       

    def register_handler(self, msg_type: int, handler: Callable) -> None:
        """Register a custom message handler."""
        (msg_class, _) = self._control_msg_registry[msg_type]
        self._control_msg_registry[msg_type] = (msg_class, handler)
    
    async def _handle_server_setup(self, msg: ServerSetup) -> None:
        logger.info(f"MOQT event: handle {msg}")

        if not self._quic.configuration.is_client:
            error = "MOQT event: received SERVER_SETUP message as server"
            logger.debug(error)
            self._close_session(
                error_code=SessionCloseCode.PROTOCOL_VIOLATION,
                reason_phrase=error
            )
        elif self._moqt_session_setup.done():
            error = "MOQT event: received multiple SERVER_SETUP messages"
            logger.debug(error)
            self._close_session(
                error_code=SessionCloseCode.PROTOCOL_VIOLATION,
                reason_phrase=error
            )
        else:
            selected_version = msg.selected_version
            if selected_version not in MOQT_VERSIONS:
                error = f"MOQT event: unsupported version in ServerSetup {hex(selected_version)}"
                logger.debug(error)
                self._close_session(
                    error_code=SessionCloseCode.PROTOCOL_VIOLATION,
                    reason_phrase=error
                )
            else:
                self._moqt_version = selected_version
                # set version context scoped to the session and save prev state token
                set_moqt_ctx_version(self._moqt_version)

            # indicate moqt session setup is complete
            self._moqt_session_setup.set_result(True)

    async def _handle_client_setup(self, msg: ClientSetup) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Send SERVER_SETUP in response
        if self._quic.configuration.is_client:
            error = "MOQT event: received CLIENT_SETUP message as client"
            logger.error(error)
            self._close_session(
                error_code=SessionCloseCode.PROTOCOL_VIOLATION,
                reason_phrase=error
            )
        elif self._moqt_session_setup.done():
            error = "MOQT event: received multiple CLIENT_SETUP messages"
            logger.error(error)
            self.close(
                error_code=SessionCloseCode.PROTOCOL_VIOLATION,
                reason_phrase=error
            )
        else:
            # indicate moqt session setup is complete
            if MOQT_CUR_VERSION in msg.versions:
                self.server_setup()
                self._moqt_session_setup.set_result(True)
        
    async def _handle_subscribe(self, msg: Subscribe) -> None:
        logger.info(f"MOQT receive: {msg}")
        self._track_aliases[msg.track_alias] = msg.subscribe_id
        self.subscribe_ok(
            subscribe_id=msg.subscribe_id,
            expires=0,
            group_order=GroupOrder.ASCENDING,
            content_exists=ContentExistsCode.NO_CONTENT,
        )

    async def _handle_announce(self, msg: Announce) -> None:
        logger.info(f"MOQT receive: {msg}")
        self.announce_ok(msg.namespace)

    async def _handle_subscribe_update(self, msg: SubscribeUpdate) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Handle subscription update

    async def _handle_subscribe_ok(self, msg: SubscribeOk) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Set future result for subscriber waiting for response
        future = self._subscribe_responses.get(msg.subscribe_id)
        if future and not future.done():
            future.set_result(msg)
        if msg.subscribe_id in self._subscriptions:
            self._subscriptions[msg.subscribe_id].append(msg)
        else:
            logger.warning(f"MOQT messages: unsolicited SubscribeOk(msg.subscribe_id)")

    async def _handle_subscribe_error(self, msg: SubscribeError) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Set future result for subscriber waiting for response
        future = self._subscribe_responses.get(msg.subscribe_id)
        if future and not future.done():
            future.set_result(msg)
        if msg.subscribe_id in self._subscriptions:
            self._subscriptions[msg.subscribe_id].append(msg)
        else:
            logger.warning(f"MOQT messages: unsolicited SubscribeError(msg.subscribe_id)")
            
    async def _handle_announce_ok(self, msg: AnnounceOk) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Set future result for announcer waiting for response
        future = self._announce_responses.get(msg.namespace)
        if future and not future.done():
            future.set_result(msg)

    async def _handle_announce_error(self, msg: AnnounceError) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Set future result for announcer waiting for response
        future = self._announce_responses.get(msg.namespace)
        if future and not future.done():
            future.set_result(msg)

    async def _handle_unannounce(self, msg: Unannounce) -> None:
        logger.info(f"MOQT event: handle {msg}")
        self.announce_ok(msg.namespace)

    async def _handle_announce_cancel(self, msg: AnnounceCancel) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Handle announcement cancellation

    async def _handle_unsubscribe(self, msg: Unsubscribe) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Handle unsubscribe request

    async def _handle_subscribe_done(self, msg: SubscribeDone) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Set future result for subscriber waiting for completion
        future = self._subscribe_responses.get(msg.subscribe_id)
        if future and not future.done():
            future.set_result(msg)

    async def _handle_max_subscribe_id(self, msg: MaxSubscribeId) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Update maximum subscribe ID

    async def _handle_subscribes_blocked(self, msg: SubscribesBlocked) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Handle subscribes blocked notification

    async def _handle_track_status_request(self, msg: TrackStatusRequest) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Send track status in response

    async def _handle_track_status(self, msg: TrackStatus) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Handle track status update

    async def _handle_goaway(self, msg: GoAway) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Handle session migration request

    async def _handle_subscribe_announces(self, msg: SubscribeAnnounces) -> None:
        logger.info(f"MOQT event: handle {msg}")
        self.subscribe_announces_ok(msg.namespace_prefix)
           
    async def _handle_subscribe_announces_ok(self, msg: SubscribeAnnouncesOk) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Set future result for subscriber waiting for response
        future = self._subscribe_announces_responses.get(msg.namespace_prefix)
        if future and not future.done():
            future.set_result(msg)
        logger.debug(f"_handle_subscribe_announces_ok: {future} {future.done()}")

    async def _handle_subscribe_announces_error(self, msg: SubscribeAnnouncesError) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Set future result for subscriber waiting for response
        future = self._subscribe_announces_responses.get(msg.namespace_prefix)
        if future and not future.done():
            future.set_result(msg)

    async def _handle_unsubscribe_announces(self, msg: UnsubscribeAnnounces) -> None:
        logger.info(f"MOQT event: handle {msg}")
        self.subscribe_announces_ok(msg.namespace_prefix)

    async def _handle_fetch(self, msg: Fetch) -> None:
        logger.info(f"MOQT event: handle {msg}")
        self.fetch_ok(msg.subscribe_id)

    async def _handle_fetch_cancel(self, msg: FetchCancel) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Handle fetch cancellation

    async def _handle_fetch_ok(self, msg: FetchOk) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Set future result for fetcher waiting for response
        future = self._fetch_responses.get(msg.subscribe_id)
        if future and not future.done():
            future.set_result(msg)

    async def _handle_fetch_error(self, msg: FetchError) -> None:
        logger.info(f"MOQT event: handle {msg}")
        # Set future result for fetcher waiting for response
        future = self._fetch_responses.get(msg.subscribe_id)
        if future and not future.done():
            future.set_result(msg)


    # Data handlers need full update - stream reader in progress
    async def _handle_subgroup_header(self, msg: SubgroupHeader, buf: Buffer) -> None:
        """Handle subgroup header message."""
        logger.info(f"MOQT event: handle {msg}")
        # Process subgroup header - 
        sub_id = self._track_aliases.get(msg.track_alias)
        if sub_id is not None:
            sub_state = self._subscriptions[sub_id]
        else:
            logger.error(f"MOQT error: unrecognized track alias: {msg.track_alias}")

    async def _handle_fetch_header(self, msg: FetchHeader) -> None:
        """Handle fetch header message."""
        logger.info(f"MOQT event: handle {msg}")
        # Process fetch header
        # Validate subscribe_id exists
        if msg.subscribe_id not in self._subscriptions:
            logger.error(f"MOQT error: fetch for unknown subscription: {msg.subscribe_id}")
            self.close(
                error_code=SessionCloseCode.PROTOCOL_VIOLATION,
                reason_phrase="Invalid subscription ID in fetch"
            )
        return

    async def _handle_object_datagram(self, msg: ObjectDatagram) -> None:
        """Handle object datagram message."""
        logger.info(f"MOQT event: handle {msg}")
        # Process object datagram
        # Validate track alias exists
        subscribe_id = self._track_aliases.get(msg.track_alias)
        if subscribe_id is None:
            logger.error(f"MOQT error: datagram for unknown track: {msg.track_alias}")
            self._close_session(
                error_code=SessionCloseCode.PROTOCOL_VIOLATION,
                reason_phrase="Invalid track alias in datagram"
            )
            return
        logger.debug(f"MOQT event: datagram object: {msg.group_id}.{msg.s}")
        # Process object data
        # Could add to local storage or forward to subscribers

    async def _handle_object_datagram_status(self, msg: ObjectDatagramStatus) -> None:
        """Handle object datagram status message."""
        logger.info(f"MOQT event: handle {msg}")
        # Process object status
        # Update status in local tracking
        subscibe_id = self._track_aliases.get(msg.track_alias)
        if subscibe_id is None:
            logger.error(f"MOQT error: datagram status for unknown track: {msg.track_alias}")
            self._close_session(
                error_code=SessionCloseCode.PROTOCOL_VIOLATION,
                reason_phrase="Invalid track alias in status"
            )
            return
        # Update object status in local storage or notify subscribers            


    # MoQT message classes for serialize/deserialize, message handler methods (unbound)       
    MOQT_CONTROL_MESSAGE_REGISTRY: Dict[MOQTMessageType, Tuple[Type[MOQTMessage], Callable]] = {
       # Setup messages
       MOQTMessageType.CLIENT_SETUP: (ClientSetup, _handle_client_setup),
       MOQTMessageType.SERVER_SETUP: (ServerSetup, _handle_server_setup),

       # Subscribe messages
       MOQTMessageType.SUBSCRIBE_UPDATE: (SubscribeUpdate, _handle_subscribe_update),
       MOQTMessageType.SUBSCRIBE: (Subscribe, _handle_subscribe),
       MOQTMessageType.SUBSCRIBE_OK: (SubscribeOk, _handle_subscribe_ok), 
       MOQTMessageType.SUBSCRIBE_ERROR: (SubscribeError, _handle_subscribe_error),

       # Announce messages
       MOQTMessageType.ANNOUNCE: (Announce, _handle_announce),
       MOQTMessageType.ANNOUNCE_OK: (AnnounceOk, _handle_announce_ok),
       MOQTMessageType.ANNOUNCE_ERROR: (AnnounceError, _handle_announce_error),
       MOQTMessageType.UNANNOUNCE: (Unannounce, _handle_unannounce),
       MOQTMessageType.ANNOUNCE_CANCEL: (AnnounceCancel, _handle_announce_cancel),

       # Subscribe control messages
       MOQTMessageType.UNSUBSCRIBE: (Unsubscribe, _handle_unsubscribe),
       MOQTMessageType.SUBSCRIBE_DONE: (SubscribeDone, _handle_subscribe_done),
       MOQTMessageType.MAX_SUBSCRIBE_ID: (MaxSubscribeId, _handle_max_subscribe_id),
       MOQTMessageType.SUBSCRIBES_BLOCKED: (SubscribesBlocked, _handle_subscribes_blocked),

       # Status messages
       MOQTMessageType.TRACK_STATUS_REQUEST: (TrackStatusRequest, _handle_track_status_request),
       MOQTMessageType.TRACK_STATUS: (TrackStatus, _handle_track_status),

       # Session control messages
       MOQTMessageType.GOAWAY: (GoAway, _handle_goaway),

       # Subscribe announces messages
       MOQTMessageType.SUBSCRIBE_ANNOUNCES: (SubscribeAnnounces, _handle_subscribe_announces),
       MOQTMessageType.SUBSCRIBE_ANNOUNCES_OK: (SubscribeAnnouncesOk, _handle_subscribe_announces_ok),
       MOQTMessageType.SUBSCRIBE_ANNOUNCES_ERROR: (SubscribeAnnouncesError, _handle_subscribe_announces_error),
       MOQTMessageType.UNSUBSCRIBE_ANNOUNCES: (UnsubscribeAnnounces, _handle_unsubscribe_announces),

       # Fetch messages
       MOQTMessageType.FETCH: (Fetch, _handle_fetch),
       MOQTMessageType.FETCH_CANCEL: (FetchCancel, _handle_fetch_cancel),
       MOQTMessageType.FETCH_OK: (FetchOk, _handle_fetch_ok),
       MOQTMessageType.FETCH_ERROR: (FetchError, _handle_fetch_error),
   }

    # Stream data message types    
    MOQT_STREAM_DATA_REGISTRY: Dict[DataStreamType, Tuple[Type[MOQTMessage], Callable]] = {
        DataStreamType.SUBGROUP_HEADER: (SubgroupHeader, _handle_subgroup_header),
        DataStreamType.FETCH_HEADER: (FetchHeader, _handle_fetch_header),
    }
    
    # Datagram data message types
    MOQT_DGRAM_DATA_REGISTRY: Dict[DataStreamType, Tuple[Type[MOQTMessage], Callable]] = {
        DatagramType.OBJECT_DATAGRAM: (ObjectDatagram, _handle_object_datagram),
        DatagramType.OBJECT_DATAGRAM_STATUS: (ObjectDatagramStatus, _handle_object_datagram_status),
    }