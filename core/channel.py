
class Channel():
    #TODO 使用sqlalchemy 为Channel添加数据库类型, 并添加主键id字段
    #TODO 实现跟Project的一对多关系, 一个通道包含多个项目
    def __init__(self, index):
        self._index = index;
        self._projects = []
