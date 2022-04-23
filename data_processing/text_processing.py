from data_processing.utils.logging import get_logger


class TextProcessing:
    """
    Examples
    --------
    ::

        text_p = TextProcessing(precision=0.7, show_log=False)
        update_time, place = text_p.info_match(text=text)
        '''
        do something
        '''
    """
    def __init__(self,
                 precision=0.9,
                 show_log=True,
                 **kwargs):
        """
        text processing package

        Parameters
        ----------
        precision:
            Specify precision for `text_match`, default is 0.9 (90%)
        show_log:
            Show log, default is True.
        """
        self._kwargs = kwargs
        self._precision = precision
        self._show_log = show_log
        self._credibility = list()

        self._logger = get_logger("TextProcessing")

    def _parse_args(self, tag, default):
        if tag in self._kwargs.keys():
            return self._kwargs.get(tag)
        else:
            return default

    def text_match(self, tag: str, txt: str) -> bool:
        """
        Compares if two texts are the same

        Parameters
        ----------
        tag:
            target text
        txt:
            text to compare
        """
        condition = list()
        for char_index in range(0, len(tag)):
            condition.append(tag[char_index])

        credibility = 0
        for con in condition:
            if con in txt:
                credibility += 1 / len(condition)
            if credibility >= self._precision:
                break

        self._credibility.append(credibility)

        if credibility >= self._precision:
            return True
        else:
            return False

    def info_match(self, text: list) -> list:
        """
        健康码将被排除, 只匹配行程码信息, 待优化

        Parameters
        ----------
        text:
             text to match
        """
        time, place = None, None
        for index_1 in range(0, len(text)):
            if self.text_match('云南健康码', text[index_1]):
                break

            if self.text_match('更新于', text[index_1]):
                time = text[index_1].replace('更新于：', '').replace('：', ':')

            if self.text_match('您于前14天内到达或途经', text[index_1]):
                place = text[index_1].split('：')[-1]
                for index_2 in range(index_1 + 1, len(text)):
                    if self.text_match('结果包含您在前14天内到访的国家', text[index_2]) or \
                            self.text_match('色卡仅对到访地作提醒', text[index_2]):
                        break
                    else:
                        place += text[index_2].replace('，', ',')

            if self._show_log is True:
                self._logger.debug("{0}: credibility={1}".format(text[index_1], self._credibility))
            self._credibility.clear()
        return [time, place]
