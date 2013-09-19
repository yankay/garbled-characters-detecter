garbled-characters-detecter
===========================

Detect garbled characters, and find the reason.

When user input the garbled characters, the detecter can tell him way. And it will show the original characters.

For Example:


    # python setup install
    # garbled-characters-detecter
    garbled-characters-detecter [Filename or Garbled chars]
    # garbled-characters-detecter çˆ±æ— ç ï¼Œæ¨ä¹±ç 
    ===========0============
    from code: utf-8:
    to   code: iso8859-1:
    org  text: 码恨乱码:
    ===========1============
    from code: gbk:
    to   code: utf-8:
    org  text: 莽藛卤忙鈥斅犆犅伱寂捗β伮ぢ孤泵犅:
    ===========2============
    from code: gbk:
    to   code: iso8859-1:
    org  text: 绫鏍鐮侊兼仺涔辩爜:


For the infomation has been lost in garbled characters, it may only return parts of correctly data.

----------------------------

乱码发现器
===========================

可以发现乱码的原因


当用户输入乱码的时候，乱码发现器可以找到其是如何产生的。并且还能够给出未乱前的原文。


    # python setup install
    # garbled-characters-detecter
    garbled-characters-detecter [Filename or Garbled chars]
    # garbled-characters-detecter çˆ±æ— ç ï¼Œæ¨ä¹±ç 
    ===========0============
    from code: utf-8:
    to   code: iso8859-1:
    org  text: 码恨乱码:
    ===========1============
    from code: gbk:
    to   code: utf-8:
    org  text: 莽藛卤忙鈥斅犆犅伱寂捗β伮ぢ孤泵犅:
    ===========2============
    from code: gbk:
    to   code: iso8859-1:
    org  text: 绫鏍鐮侊兼仺涔辩爜:


可能性越高的结果越靠前，由于信息可能已经或多或少的丢失，可能只能返回部分正确数据。






