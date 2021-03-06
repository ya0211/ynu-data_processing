import time


class Progress:
    """
    Examples
    --------
    ::

        pro = Progress(100, bar_length=60)
        for index in range(0, 100):
            '''
            do something
            '''
            pro.progress_default()
    """
    def __init__(self, total: int, bar_length=100):
        """
        progress bar package

        Parameters
        ----------
        total:
            total, Integer required
        bar_length:
            Specify the length of the progress bar you want, the default is 100
        """
        self._total = total
        self._start_time_total = time.time()
        self._start_time_last = self._start_time_total
        self._bar_length = bar_length
        self._progress = 0

    def progress_default(self):
        """
        Style:
            100%|####| 100/100 [0:59, 10s/it]
        """
        self._progress += 1

        percentage = int((self._progress / self._total) * 100)
        show_finished = "#" * int(self._progress * self._bar_length / self._total)
        show_needed = " " * (self._bar_length - int(self._progress * self._bar_length / self._total))
        proportion = "{0}/{1}".format(self._progress, self._total)

        total_time_minute = int((time.time() - self._start_time_total) / 60)
        total_time_second = int((time.time() - self._start_time_total) % 60)
        total_time = "{0}:{1}".format(str(total_time_minute).rjust(2, '0'), str(total_time_second).rjust(2, '0'))

        speed = round(time.time() - self._start_time_last, 3)

        self._start_time_last = time.time()

        print("\r{0}%|{1}{2}| {3} [{4}, {5}s/it]".format(
            str(percentage).rjust(3),
            show_finished, show_needed,
            proportion,
            total_time, str(speed).ljust(5, '0')
        ), end="")
