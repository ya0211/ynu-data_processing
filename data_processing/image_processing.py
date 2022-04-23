import os.path
import subprocess
from paddleocr import PaddleOCR
from data_processing.utils.logging import get_logger


class ImageProcessing:
    """
    Examples
    --------
    ::

        image_p = ImageProcessing(image_dir='image', log_dir='log', show_log=False)
        text_all = image_p.scan_text(data_input=[1.png, 2.png, 3.png], image_info=[info1, info2])
        for text in text_all:
            '''
            do something
            '''
    """
    def __init__(self,
                 image_dir='image',
                 log_dir='log',
                 show_log=True,
                 **kwargs):
        """
        image processing package

        Parameters
        ----------
        image_dir:
            Specify the directory or folder to store images, the default is 'image'.
        log_dir:
            Specify the directory or folder to store log file, the default is 'log'.
        show_log:
            Show log, default is True.
        """
        self._kwargs = kwargs
        self._image_dir = image_dir
        self._log_dir = log_dir
        self._show_log = show_log

        self._logger = get_logger("ImageProcessing", "{0}/ImageProcessing.log".format(self._log_dir))
        self._ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=self._show_log)

        if not os.path.exists(self._image_dir):
            os.makedirs(self._image_dir)

        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)

    def _parse_args(self, tag, default):
        if tag in self._kwargs.keys():
            return self._kwargs.get(tag)
        else:
            return default

    def download(self, url: str, rename: str):
        """
        Download the file from the URL, make sure you have the `curl` command in your system

        Parameters
        ----------
        url:
            Specify download URL of the file
        rename:
            Rename the file to the specified name
        """
        if self._show_log is True:
            self._logger.debug("url={0}".format(url))
        file_dir = "{0}/{1}".format(self._image_dir, rename)
        subprocess.run([
            "curl", "-LSs", "-o",
            file_dir,
            url], check=True)

    def scan_text(self, data_input: list, image_info=None) -> list:
        """
        Image scanning with PaddleOCR(https://github.com/PaddlePaddle/PaddleOCR)

        Parameters
        ----------
        data_input:
            list of image data, supports URL and file directory
        image_info:
            a list of length 2 or None, information about the image, only useful for online image,
            the picture will be downloaded and named with image_info

        """
        text_all = list()

        for index in range(0, len(data_input)):
            text = None
            if 'http' in data_input[index]:
                url = data_input[index]
                image_name = "{0}_{1}_{2}.png".format(image_info[0], image_info[1], index)
                image_dir = "{0}/{1}".format(self._image_dir, image_name)

                if not os.path.exists(image_dir):
                    self.download(url=url, rename=image_name)

            else:
                image_dir = data_input[index]
                image_name = image_dir.split('/')[-1]
                if not os.path.exists(image_dir):
                    image_dir = None

            if image_dir is not None:
                result = self._ocr.ocr(image_dir, cls=True)
                text = [line[1][0] for line in result]

            if self._show_log is True:
                self._logger.debug("{0}: {1}".format(image_name, text))
            text_all.append(text)
        return text_all
