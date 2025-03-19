from asyncinotify import Inotify, Mask
import asyncio
import os
from pathlib import Path
import traceback
from typing import Optional


__all__ = ("watch_file_creation",)


class ReadinessWatcher:
    def __init__(self):
        self.inotify = Inotify()
        self.info_by_path = {}


    async def loop(self):
        try:
            async for ievent in self.inotify:
                if (ievent.mask & Mask.CREATE) and ievent.path in self.info_by_path:
                    event, watch = self.info_by_path[ievent.path]
                    self.inotify.rm_watch(watch)
                    event.set()
                    del self.info_by_path[ievent.path]
        except Exception:
            traceback.print_exc()
            raise


    async def wait_for_path(self, path: str):
        # Using `os.path.realpath` here is horribly wrong and has caused issues in the past. Our
        # paths often refer to files in other mount namespaces via `/proc/<pid>/root/...`. `root`
        # has mismatching `get_link` vs `readlink` implementations, which causes userland `realpath`
        # to resolve the path equivalently to `/...`.
        path = Path(path)

        if path.exists():
            return

        if path in self.info_by_path:
            event, _ = self.info_by_path[path]
        else:
            event = asyncio.Event()
            watch = self.inotify.add_watch(path.parent, Mask.CREATE)
            self.info_by_path[path] = event, watch
            if path.exists():  # race
                if not event.is_set():
                    self.inotify.rm_watch(watch)
                    event.set()
                    del self.info_by_path[path]

        await event.wait()


readiness_watcher: Optional[ReadinessWatcher] = None
readiness_watcher_task = None  # keep a strong reference to prevent the task from dying


async def watch_file_creation(path: str):
    global readiness_watcher, readiness_watcher_task

    if readiness_watcher is None:
        readiness_watcher = ReadinessWatcher()
        readiness_watcher_task = asyncio.create_task(readiness_watcher.loop())

    await readiness_watcher.wait_for_path(path)
