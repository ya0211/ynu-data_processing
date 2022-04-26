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

    def info_journey(self, text: list):
        """
        to do
        """
        time, place = [None, None]
        for txt in text:
            if self.text_match('抱歉，没有找到您的行程数据', txt):
                time = '未知'
                break

            elif self.text_match('更新于', txt):
                time = txt.replace('更新于：', '').replace('：', ':')

            elif self.text_match('您于前14天内到达或途经', txt):
                place = txt.split('：')[-1]
                for index in range(text.index(txt) + 1, len(text)):
                    if self.text_match('结果包含您在前14天内到访的国家', text[index]):
                        break
                    else:
                        place += text[index].replace('，', ',')
        return time, place

    def info_healthy(self, text: list):
        """
        to do
        """
        time, color = [None, None]
        return time, color

    def info_match(self, text: list) -> list:
        """
        健康码将被排除, 只匹配行程码信息, 待优化

        Parameters
        ----------
        text:
             text to match
        """
        time_info_journey, place_info_journey = [None, None]
        time_info_healthy, color_info_healthy = [None, None]
        for txt in text:
            if self.text_match('云南健康码', txt):
                time_info_healthy,  color_info_healthy = self.info_healthy(text)
                break

            elif self.text_match('通信大数据行程卡', txt):
                time_info_journey, place_info_journey = self.info_journey(text)
                break

            elif self.text_match('CXMYD', txt):
                time_info_journey, place_info_journey = '短信查询', None
                break

            if self._show_log is True:
                self._logger.debug("text_match: {0}: credibility={1}".format(txt, self._credibility))
            self._credibility.clear()
        return [[time_info_journey, place_info_journey], [time_info_healthy, color_info_healthy]]
