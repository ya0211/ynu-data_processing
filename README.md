# ynu-data_processing
 1. Read an Excel file and filter data
 2. OCR(depends on [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)) and text match
 3. I have no idea
## Examples
- ExcelProcessing
    ```
    excel_p = ExcelProcessing("excel.xlsx", sheet_name='Sheet1')
    excel_p.get_index_tag_header('header1', 'header2', 'header3', 'header4')
    all = excel_p.filter_data()

    for one in all
        header1, header2, header3, header4 = one
        '''
        do something
        '''
    ```
- ImageProcessing
    ```
    image_p = ImageProcessing(image_dir='image', log_dir='log', show_log=False)
    text_all = image_p.scan_text(data_input=[1.png, 2.png, 3.png], image_info=[info1, info2])
    for text in text_all:
        '''
        do something
        '''
    ```
- TextProcessing
    ```
    text_p = TextProcessing(precision=0.7, show_log=False)
    update_time, place = text_p.info_match(text=text)
    '''
    do something
    '''
    ```

## License
This project is released under [Apache 2.0 license](LICENSE)