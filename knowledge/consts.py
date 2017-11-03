# -*- coding: utf-8 -*-

class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

consts = _const()

# 知识
consts.RENTI_TYPE = 1
consts.SHENGHUO_TYPE = 2
consts.CHANGSHI_TYPE = 3
consts.DONGWU_TYPE = 4
consts.ZHIWU_TYPE = 5
consts.DIQIU_TYPE = 6
consts.YUZHOU_TYPE = 7
consts.KEJI_TYPE = 8
consts.JUNSHI_TYPE = 9
consts.SHULIHUA_TYPE = 10
consts.LISHI_TYPE = 11
consts.WENHUA_TYPE = 12

# 故事
consts.YOUER_TYPE = 50
consts.ERTONG_TYPE = 51
consts.SHUIQIAN_TYPE = 52
consts.YIZHI_TYPE = 53
consts.YUYAN_TYPE = 54
consts.MINJIAN_TYPE = 55

# 知识
consts.RENTI_DESC = '人体小知识'
consts.SHENGHUO_DESC = '健康生活小常识'
consts.CHANGSHI_DESC = '身边的常识大全'
consts.DONGWU_DESC = '动物小知识'
consts.ZHIWU_DESC = '植物的小知识'
consts.DIQIU_DESC = '地球科普小知识'
consts.YUZHOU_DESC = '宇宙科普知识'
consts.KEJI_DESC = '科技小知识'
consts.JUNSHI_DESC = '军事'
consts.SHULIHUA_DESC = '数理化之谜'
consts.LISHI_DESC = '中外历史'
consts.WENHUA_DESC = '文化艺术'

# 故事
consts.YOUER_DESC = '幼儿故事'
consts.ERTONG_DESC = '儿童小故事'
consts.SHUIQIAN_DESC = '睡前故事'
consts.YIZHI_DESC = '益智故事'
consts.YUYAN_DESC = '寓言故事'
consts.MINJIAN_DESC = '民间故事'
