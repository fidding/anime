if __name__ == '__main__':
    """
    图片解析脚本
    """
    import json
    import os
    import hashlib
    import pymysql.cursors
    import uuid

    print('图片解析开始')
    # 连接数据库
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='',
        db='anime',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        # 读取文件
        with open('sogou20180711.jl', 'r') as f:
            for line in f.readlines():
                line = json.loads(line.strip())  # 把末尾的'\n'删掉
                # 判断图片是否存在
                img_name = hashlib.sha1(
                    line['picUrl'].encode("utf-8")
                ).hexdigest()
                file = 'download/images/full/'+img_name+'.jpg'
                if os.path.exists(file):
                    image_id = str(uuid.uuid4())
                    title = line['title']
                    name = img_name
                    ext = '.jpg'
                    width = line['width']
                    height = line['height']
                    tag = line['tag']
                    catalog = line['catalog']
                    # 图片存在, 将图片信息写入数据库
                    with connection.cursor() as cursor:
                        # 判断数据是否已存在数据库中
                        sql = "SELECT count(`id`) as count FROM `images` \
                        WHERE `name`=%s"
                        cursor.execute(sql, (name,))
                        result = cursor.fetchone()
                        if not result['count']:
                            # 写入数据库
                            sql = "INSERT INTO images  \
                            (`image_id`, `title`, `name`, `ext`, `width`, \
                            `height`, `tag`, `type`, `catalog`) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(
                                sql,
                                (image_id, title, name, ext, width,
                                 height, tag, '', catalog)
                            )
                        else:
                            print('已存在相同数据')
                    connection.commit()
                else:
                    print('图片源缺失')
            print('图片解析结束')
    finally:
        connection.close()
