import ctypes

import vpex
import vpex._C

__all__ = ["Stream", "Event"]


class Stream(vpex._C._VtalStreamBase):
    r"""Wrapper around a VSI stream.

    A VSI stream is a linear sequence of execution that belongs to a specific
    device, independent from other streams.

    Arguments:
        device(torch.device or int, optional): a device on which to allocate
            the stream. If :attr:`device` is ``None`` (default) or a negative
            integer, this will use the current device.
        priority(int, optional): priority of the stream. Lower numbers
                                 represent higher priorities.
    """

    def __new__(cls, device=None, priority=0, **kwargs):
        with vpex.vtal.device(device):
            return super(Stream, cls).__new__(cls, priority=priority, **kwargs)

    def wait_event(self, event):
        r"""Makes all future work submitted to the stream wait for an event.

        Arguments:
            event (Event): an event to wait for.

           This function returns without waiting for :attr:`event`: only future
           operations are affected.

        """
        event.wait(self)

    def wait_stream(self, stream):
        r"""Synchronizes with another stream.

        All future work submitted to this stream will wait until all kernels
        submitted to a given stream at the time of call complete.

        Arguments:
            stream (Stream): a stream to synchronize.

        .. note:: This function returns without waiting for currently enqueued
           kernels in :attr:`stream`: only future operations are affected.
        """
        self.wait_event(stream.record_event())

    def record_event(self, event=None):
        r"""Records an event.

        Arguments:
            event (Event, optional): event to record. If not given, a new one
                will be allocated.

        Returns:
            Recorded event.
        """
        if event is None:
            event = Event()
        event.record(self)
        return event

    def synchronize(self):
        r"""Wait for all the kernels in this stream to complete.
        """
        super(Stream, self).synchronize()


    @property
    def _as_parameter_(self):
        return ctypes.c_void_p(self.vtal_stream)

    def __eq__(self, other):
        if isinstance(other, Stream):
            return super(Stream, self).__eq__(other)
        return False

    def __hash__(self):
        return hash((self.vtal_stream, self.device))

    def __repr__(self):
        return ('<vpex.vtal.Stream device={0} vtal_stream={1:#x}>'
                .format(self.device, self.vtal_stream))


class Event(vpex._C._VtalEventBase):
    r"""Wrapper around a VSI event.

    VSI events are synchronization markers that can be used to monitor the
    device's progress, to accurately measure timing, and to synchronize VSI
    streams.

    The underlying VSI events are lazily initialized when the event is first
    recorded or exported to another process. After creation, only streams on the
    same device may record the event. However, streams on any device can wait on
    the event.

    Arguments:
        enable_timing (bool, optional): indicates if the event should measure time
            (default: ``False``)
        blocking (bool, optional): if ``True``, :meth:`wait` will be blocking (default: ``False``)
        interprocess (bool): if ``True``, the event can be shared between processes
            (default: ``False``)

    """

    def __new__(cls, enable_timing=False, blocking=False, interprocess=False):
        return super(Event, cls).__new__(cls, enable_timing=enable_timing, blocking=blocking, interprocess=interprocess)

    def record(self, stream=None):
        r"""Records the event in a given stream.

        Uses ``vpex.vtal.current_stream()`` if no stream is specified. The
        stream's device must match the event's device.
        """
        if stream is None:
            stream = vpex.vtal.current_stream()
        super(Event, self).record(stream)

    def wait(self, stream=None):
        r"""Makes all future work submitted to the given stream wait for this
        event.

        Use ``vpex.vtal.current_stream()`` if no stream is specified.
        """
        if stream is None:
            stream = vpex.vtal.current_stream()
        super(Event, self).wait(stream)

    def query(self):
        r"""Checks if all work currently captured by event has completed.

        Returns:
            A boolean indicating if all work currently captured by event has
            completed.
        """
        return super(Event, self).query()

    def elapsed_time(self, end_event):
        r"""Returns the time elapsed in milliseconds after the event was
        recorded and before the end_event was recorded.
        """
        return super(Event, self).elapsed_time(end_event)

    def synchronize(self):
        r"""Waits for the event to complete.

        Waits until the completion of all work currently captured in this event.
        This prevents the CPU thread from proceeding until the event completes.
        """
        super(Event, self).synchronize()

    @property
    def _as_parameter_(self):
        return ctypes.c_void_p(self.vtal_event)

    def __repr__(self):
        if self.vtal_event:
            return '<vpex.vtal.Event {0:#x}>'.format(self._as_parameter_.value)
        else:
            return '<vpex.vtal.Event uninitialized>'

